"""
Project: Analyzing food access and security in Chicago
Team: food.get
File Name: cleanup.py
Authors: Stacy George
Note: 
    * Stacy created clean_business_license and clean_snap_retailer_data

Description:
    This file cleans all the raw data
"""
import pandas as pd
from food_get.data.data_extract_sg import import_grocery_store_data, import_snap_retailers_data

GROCERY_RAW = import_grocery_store_data()
SNAP_RAW = import_snap_retailers_data()

MEMBERSHIP_STORES = ["Costco", "Sam's Club", "BJ's Wholesale Club"]

def clean_grocery_stores():
    """
    This function cleans the data frame of grocery stores

    * Only keep rows where groceries are not membership stores
    * Format to have a Lat and Long column
    * Lowercase column names and replace spaces with underscores

    Returns:
        A pandas dataframe of the businesses and all their cleaned data components from the portal
    """
        
    no_membership = GROCERY_RAW[~GROCERY_RAW['Store Name'].isin(MEMBERSHIP_STORES)]
    open_stores = no_membership[no_membership['New status'] == 'OPEN']
    open_stores[['Longitude', 'Latitude']] = open_stores['Location'].str.extract(r'POINT \(([-+]?\d*\.\d+) ([-+]?\d*\.\d+)\)')
    open_stores = open_stores.drop('Location', axis=1)
    open_stores = open_stores.rename(columns=lambda x: x.lower().replace(' ', '_'))

    return open_stores


def clean_snap_retailer_data():
    """
    This function cleans the dictionary of the snap retailers and all their raw data components from the portal

    * Consolidate the data to be only a list or relevant dictionary elements
    * Only keep rows where 'City' = "Chicago" and 'State' = "IL"
    * Lowercase column names

    Returns:
        A pandas dataframe of the businesses and all their cleaned data components from the portal
    """
    # Initialize an empty list to store dictionaries
    cleaned_snap_retailer_data = []

    for retailer_entry in SNAP_RAW:
        # Access the 'attributes' key within each entry
        attributes = retailer_entry.get('attributes', {})

        # Append the attributes dictionary to the result list
        cleaned_snap_retailer_data.append(attributes)

    # Convert the list of dictionaries to a Pandas DataFrame
    cleaned_snap_retailer_df = pd.DataFrame(cleaned_snap_retailer_data)
    cleaned_snap_retailer_df = cleaned_snap_retailer_df.rename(columns=lambda x: x.lower())

    return cleaned_snap_retailer_df

