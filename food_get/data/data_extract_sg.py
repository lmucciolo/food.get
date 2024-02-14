"""
Project: Analyzing food access and security in Chicago
Team: food.get
File Name: data_extract.py
Authors: Danielle Rosenthal and Stacy George
Note: 
    * Danielle created import_atlas_data
    * Stacy created import_business_liscense_data and import_snap_retailers_data

Description:
    This file imports all the raw data from their source
"""
import pandas as pd
import requests
import json
import time
from urllib.parse import urlencode

def make_api_request(url, params = None):
    """
    Make an API request and parse the JSON response.

    Args:
        url (str): The URL for the API endpoint.
        params (dict): Optional parameters for the API request (default is None).

    Returns:
        dict: Parsed JSON response.
    """
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    response.raise_for_status()
    return json.loads(response.text)


def import_business_license_data(base_url, limit = 1000, offset = 0):
    """
    Retrieve business license data from the Chicago data portal.

    Args:
        base_url (str): The base URL of the API endpoint.
        limit (int): The number of results to return in each batch (default is 1000).
        offset (int): The index of the result array to start the returned list of results (default is 0).

    Returns:
        list: A list containing raw data components of businesses from the portal.
    """
    base_url = "https://data.cityofchicago.org/resource/r5kz-chrr.json"
    params = {'$limit': limit,
             '$offset': offset
             }

    business_license_data = make_api_request(base_url, params = params)

    # check if there are more results to fetch
    while business_license_data:
        # process the current batch of results
        # increment offset for the next batch
        offset += limit
        # update parameters for the next API call
        params = {'$limit': limit, '$offset': offset}

        # make the next API request
        batch_data = make_api_request(base_url, params = params)

        # extend the list with the new batch
        business_license_data.extend(batch_data)

        # check if there are more results to fetch
        if not batch_data:
            break

        time.sleep(0.1)

    return business_license_data


def import_snap_retailers_data():
    """
    This function loads the data from the USDA Food and Nutrition Service portal on the 
    location for currently authorized SNAP retailers.

    Returns:
        A list of the retailer's features and associated raw data components from the portal
    """
    base_url = "https://services1.arcgis.com/RLQu0rK7h4kbsBq5/arcgis/rest/services/snap_retailer_location_data/FeatureServer/0/query?"

    # parameters for ObjectID retrieval
    params_object_ids = {
        'where': "City = 'CHICAGO'",
        'outFields': '*',
        'returnIdsOnly': True,
        'outSR': 4326,
        'f': 'json'
        }

    # Parameters for detailed information retrieval
    params_features = {
        'outFields': '*',
        'outSR': 4326,
        'f': 'json'
        }
    
    # retrieve ObjectIDs for Chicago SNAP groceries
    url_object_ids = base_url + urlencode(params_object_ids)
    response_object_ids = make_api_request(url_object_ids)
    object_id_lst = response_object_ids.get('objectIds', []) if response_object_ids else []

    snap_retailer_data_lst = []
    batch_size = 10

    # iterate over Chicago SNAP ObjectIDs in batches
    for i in range(0, len(object_id_lst), batch_size):
        batch_object_ids = object_id_lst[i:i + batch_size]
        # construct URL for batch request
        url_detail_batch = base_url + urlencode(params_features) + "&where=ObjectId IN (" + ",".join(map(str, batch_object_ids)) + ")"
        # get snap retailer data for the batch
        response_detail_batch = make_api_request(url_detail_batch)
        # append snap retailer data to the list
        snap_retailer_data_lst.extend(response_detail_batch['features'])
        # time delay between batches
        time.sleep(0.1)

    return snap_retailer_data_lst
