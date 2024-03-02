"""
Project: Analyzing food access and security in Chicago
Team: food.get
File Name: extract_grocery.py
Authors: Danielle Rosenthal and Stacy George
Note: 
    * Stacy created import_business_liscense_data and import_snap_retailers_data

Description:
    This file imports all the raw data from their source
"""

import pandas as pd
import requests
import json
import time
from urllib.parse import urlencode


def make_api_request(url, params=None):
    """
    Make an API request and parse the JSON response.

    Args:
        url (str): The URL for the API endpoint.
        params (dict): Optional parameters for the API request (default is None).

    Returns:
        dict: Parsed JSON response.
    """
    response = requests.get(url)
    response.raise_for_status()
    return json.loads(response.text)


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
        "where": "City = 'CHICAGO'",
        "outFields": "*",
        "returnIdsOnly": True,
        "outSR": 4326,
        "f": "json",
    }

    # Parameters for detailed information retrieval
    params_features = {"outFields": "*", "outSR": 4326, "f": "json"}

    # retrieve ObjectIDs for Chicago SNAP groceries
    url_object_ids = base_url + urlencode(params_object_ids)
    response_object_ids = make_api_request(url_object_ids)
    object_id_lst = (
        response_object_ids.get("objectIds", []) if response_object_ids else []
    )

    snap_retailer_data_lst = []
    batch_size = 10

    # iterate over Chicago SNAP ObjectIDs in batches
    for i in range(0, len(object_id_lst), batch_size):
        batch_object_ids = object_id_lst[i : i + batch_size]
        # construct URL for batch request
        url_detail_batch = (
            base_url
            + urlencode(params_features)
            + "&where=ObjectId IN ("
            + ",".join(map(str, batch_object_ids))
            + ")"
        )
        # get snap retailer data for the batch
        response_detail_batch = make_api_request(url_detail_batch)
        # append snap retailer data to the list
        snap_retailer_data_lst.extend(response_detail_batch["features"])
        # time delay between batches
        time.sleep(0.1)

        # Initialize an empty list to store dictionaries
        stored_snap_retailer_data = []

        for retailer_entry in snap_retailer_data_lst:
            # Access the 'attributes' key within each entry
            attributes = retailer_entry.get("attributes", {})

            # Append the attributes dictionary to the result list
            stored_snap_retailer_data.append(attributes)

        # Convert the list of dictionaries to a Pandas DataFrame
        stored_snap_retailer_df = pd.DataFrame(stored_snap_retailer_data)

        stored_snap_retailer_df.to_csv(
            "data/import_data/snap_retailers_data.csv", index=False
        )


def import_grocery_store_data():
    """
    This function loads the data from a Chicago data portal csv of Grocery stores from 2020.

    Returns:
        A pandas dataframe of Chicago grocery detail's features.
    """
    grocery_store_df = pd.read_csv("data/import_data/Grocery_Store_Status_20240219.csv")

    return grocery_store_df
