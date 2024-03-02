"""
Project: Analyzing food access and security in Chicago
Team: food.get
File Name: cleanup_grocery
Authors: Stacy George
Note: 
    * Stacy created clean_business_license and clean_snap_retailer_data

Description:
    This file cleans all the raw data
"""

# cleanup_sg
# cleanup_grocery

import pandas as pd
import pathlib
from food_get.data.match_groceries import match_grocery_stores


GROCERY_RAW = pd.read_csv(
    pathlib.Path(__file__).parent / "../data/raw_data/Grocery_Store_Status_20240219.csv"
)
pathlib.Path(__file__).parent / "../data/raw_data/snap_retailers_data.csv"
SNAP_RAW = pd.read_csv(
    pathlib.Path(__file__).parent / "../data/raw_data/snap_retailers_data.csv"
)
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

    no_membership = GROCERY_RAW[~GROCERY_RAW["Store Name"].isin(MEMBERSHIP_STORES)]
    cleaned_stores_df = no_membership[no_membership["New status"] == "OPEN"]
    cleaned_stores_df[["Longitude", "Latitude"]] = cleaned_stores_df[
        "Location"
    ].str.extract(r"POINT \(([-+]?\d*\.\d+) ([-+]?\d*\.\d+)\)")
    cleaned_stores_df = cleaned_stores_df.loc[
        :, ["Store Name", "Latitude", "Longitude", "Address"]
    ]
    cleaned_stores_df = cleaned_stores_df.rename(
        columns=lambda x: x.lower().replace(" ", "_")
    )

    return cleaned_stores_df


def clean_snap_retailer_data():
    """
    This function cleans the dictionary of the snap retailers and all their raw data components from the portal

    * Consolidate the data to be only a list or relevant dictionary elements
    * Only keep rows where 'City' = "Chicago" and 'State' = "IL"
    * Lowercase column names

    Returns:
        A pandas dataframe of the businesses and all their cleaned data components from the portal
    """

    cleaned_snap_retailer_df = SNAP_RAW.loc[
        :, ["Store_Name", "Latitude", "Longitude", "Store_Street_Address"]
    ]
    cleaned_snap_retailer_df = cleaned_snap_retailer_df.rename(
        columns={"Store_Street_Address": "address"}
    )
    cleaned_snap_retailer_df = cleaned_snap_retailer_df.rename(
        columns=lambda x: x.lower()
    )

    return cleaned_snap_retailer_df


def merge_and_assign_ids():
    stores1_df = clean_grocery_stores()
    stores2_df = clean_snap_retailer_data()
    matched_stores_df = match_grocery_stores(stores1_df, stores2_df, max_dist=1000)
    matched_stores_df.insert(0, "store_id", range(1, len(matched_stores_df) + 1))

    return matched_stores_df
