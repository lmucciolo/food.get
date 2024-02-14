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
from food_get.data.data_extract_sg import import_business_license_data, import_snap_retailers_data

LISCENSE_RAW = import_business_license_data()
SNAP_RAW = import_snap_retailers_data()

def clean_business_liscense():
    """
    This function cleans the list of the businesses and all their raw data components from the portal

    * Consolidate the data to 'city','license_id','legal_name','doing_business_as_name',
        'application_type', 'license_description','location' 
    * Only keep rows where 'license_description' = "Retail Food Establishment"


    Returns:
        A pandas dataframe of the businesses and all their cleaned data components from the portal
    """    
    business_liscense_columns = ['city','license_id','legal_name','doing_business_as_name',
                                 'application_type', 'license_description','location' ]
    
    cleaned_business_liscense_data = []

    for business in LISCENSE_RAW:
        # check if 'license_description' is "Retail Food Establishment"
        if business.get('license_description') == "Retail Food Establishment":
            # create a dictionary with only the desired columns
            cleaned_business = {column: business.get(column) for column in business_liscense_columns}
            cleaned_business_liscense_data.append(cleaned_business)
    
    # Convert the list of dictionaries to a Pandas DataFrame
    cleaned_business_license_df = pd.DataFrame(cleaned_business_liscense_data)

    return cleaned_business_license_df

def clean_snap_retailer_data():
    """
    This function cleans the dictionary of the snap retailers and all their raw data components from the portal

    * Consolidate the data to be only a list or relevant dictionary elements
    * Only keep rows where 'City' = "Chicago" and 'State' = "IL"


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

    return cleaned_snap_retailer_df

