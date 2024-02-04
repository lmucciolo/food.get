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

relevant_columns = ['CensusTract', 'State', 'County', 'Urban', 'Pop2010', 'OHU2010', 'lapop1',
'lapop1share', 'lalowi1', 'lalowi1share', 'lasnap1', 'lasnap1share', 'lapop10',
'lapop10share', 'lalowi10', 'lalowi10share', 'lapop20', 'lapop20share', 'lalowi20',
'lalowi20share']

#Atlas_2019 = pd.read_csv('/Users/daniellerosenthal/Downloads/2019Atlas.csv')
#Atlas_2015 = pd.read_csv('/Users/daniellerosenthal/Downloads/2015Atlas.csv')
#
Atlas_Sets = pd.DataFrame()

def import_atlas_data(year):
    Atlas_Raw = pd.read_csv('/Users/daniellerosenthal/Downloads/{}Atlas.csv'.format(year))
    Atlas_Filtered = Atlas_Raw[relevant_columns]
    Atlas_Filtered['YearLabel'] = year

    Atlas_Sets = pd.concat([Atlas_Sets, Atlas_Filtered])

# Stacy additions 2/4/24
import requests
import json

def import_business_liscense_data():
    """
    This function loads the data from the Chicago data portal on business liscenses
    and returns a list of all the raw data.

    Returns:
        A list of the businesses and all their raw data components from the portal
    """
    # API Call of Business Liscense for Grocery Stores using Turk's Take 1 from notes
    url = "https://data.cityofchicago.org/resource/r5kz-chrr.json"
    response = requests.get(url)
    business_liscense_data = json.loads(response.text)

    return business_liscense_data

def import_snap_retailers_data():
    """
    This function loads the data from the USDA Food and Nutrition Service portal on the 
    location for currently authorized SNAP retailers.

    Returns:
        A list of the retailers and all their raw data components from the portal
    """
    # API Call of SNAP retailers using Turk's Take 1 from notes
    url = "https://services1.arcgis.com/RLQu0rK7h4kbsBq5/arcgis/rest/services/snap_retailer_location_data/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json"
    response = requests.get(url)
    snap_retailer_data = json.loads(response.text)

    return snap_retailer_data

