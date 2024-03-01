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
import numpy as np


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

import requests
import time

Atlas_Sets = pd.DataFrame()

def import_atlas_data(export=False):
    years = ['2010', '2015', '2019']
    atlas_sets = pd.DataFrame()

    for year in years:
        Atlas_Raw = pd.read_csv('/Users/daniellerosenthal/Downloads/AtlasData/Atlas{}.csv'.format(year))
        if year == '2010':
            Atlas_Raw = Atlas_Raw[Atlas_Raw['State']=="IL"]
        else:
            Atlas_Raw = Atlas_Raw[Atlas_Raw['State']=="Illinois"]
        
        Atlas_Filtered = Atlas_Raw[['CensusTract', 'LowIncomeTracts', 'LATracts_half', 'lapophalfshare', 'lapophalf']]
        Atlas_Filtered = Atlas_Filtered.add_suffix('_{}'.format(year))
        Atlas_Filtered.rename(columns={'CensusTract_{}'.format(year): 'CensusTract'}, inplace=True)

        if len(atlas_sets) == 0:
            atlas_sets = Atlas_Filtered
        else:
            atlas_sets = atlas_sets.merge(Atlas_Filtered, on='CensusTract', how='outer')
    
    if export:
        atlas_sets.to_csv('atlas_historical.csv')

    return atlas_sets

def one_year(year=None):
    Atlas_Raw = pd.read_csv('/Users/daniellerosenthal/Downloads/AtlasData/Atlas{}.csv'.format(year))
    Atlas_Raw = Atlas_Raw[Atlas_Raw['State'] == "Illinois"]
    return Atlas_Raw

def percentage_string_label(value):
    return f"{value * 100:.1f}%"

def filtered_atlas(export=False, years=['2010', '2015', '2019']):
    filtered_df = import_atlas_data()

    # Making some small adjustments to 2019 columns to account for changes to raw data structure
    filtered_df['LowIncomeTracts_2019'] = filtered_df['LowIncomeTracts_2019'].values.astype(np.int64)
    filtered_df['LATracts_half_2019'] = filtered_df['LATracts_half_2019'].values.astype(np.int64)
    filtered_df['lapophalfshare_2019'] = filtered_df['lapophalfshare_2019'] / 100

    for year in ['2010', '2015', '2019']:
        col_name = f"lapophalfshare_{year}"
        filtered_df[col_name] = 1 - filtered_atlas[col_name]
        label_column_name = f"{year}_prop_label"
        filtered_df[label_column_name] = filtered_df[col_name].apply(lambda x: percentage_string_label(x))

    if export:
        filtered_df.to_csv('filtered_atlas_update.csv')

    return filtered_df