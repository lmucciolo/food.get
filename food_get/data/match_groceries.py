"""
Project: Analyzing food access and security in Chicago
Team: food.get
File Name: match_groceries.py
Authors: Austin Steinhart

Description:
    This matches the Chicago grocery stores to the SNAP database
"""

import pandas as pd
from math import asin, sqrt, cos, sin, radians
import numpy as np

EARTH_R_MI = 3963


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on a sphere (like Earth) in miles.
    Used code from CAPP 122 PA3

    :param lat1: latitude of first point
    :param lon1: longitude of first point
    :param lat2: latitude of second point
    :param lon2: longitude of second point

    :return: distance in miles
    """

    rlat1, rlon1, rlat2, rlon2 = (
        radians(lat1),
        radians(lon1),
        radians(lat2),
        radians(lon2),
    )

    d = (
        2
        * EARTH_R_MI
        * asin(
            sqrt(
                sin((rlat2 - rlat1) / 2) ** 2
                + cos(rlat1) * cos(rlat2) * sin((rlon2 - rlon1) / 2) ** 2
            )
        )
    )

    return d


def match_grocery_stores(stores1_df, stores2_df, max_dist=1000):
    """
    Matches grocery stores from two data sets with address and lat/long given a
    max_dist. Matches on dist and the numbers of an address. Only uses the first match
    even if there are multiple. Default value for max_distance = 1000 feet.
    """

    stores1_df["match_id"] = None
    stores2_df["match_id"] = None
    stores1_df["address_num"] = stores1_df["address"].str.split(" ").str[0]
    stores2_df["address_num"] = stores2_df["address"].str.split(" ").str[0]
    match_id = 1

    for index1, store1 in stores1_df.iterrows():
        for index2, store2 in stores2_df.iterrows():
            # check that not already matched matched and numbers match
            if (
                stores1_df.loc[index1, "match_id"] is None
                and store1["address_num"] == store2["address_num"]
            ):
                dist = haversine_distance(
                    float(store1["latitude"]),
                    float(store1["longitude"]),
                    float(store2["latitude"]),
                    float(store2["longitude"]),
                )
                # dist is how many feet away
                if dist * 5280 <= max_dist:
                    stores1_df.loc[index1, "match_id"] = match_id
                    stores2_df.loc[index2, "match_id"] = match_id
                    match_id += 1

    # change non matches so they dont get matched
    mask = stores2_df["match_id"].isnull()
    stores2_df["match_id"] = np.where(mask, "missing", stores2_df["match_id"])
    stores2_df[stores2_df["match_id"].isnull()]["match_id"] = "missing"
    merged_df = pd.merge(stores1_df, stores2_df, how="left", on="match_id")
    mask = merged_df["match_id"].notna()
    merged_df["is_snap"] = np.where(mask, True, False)

    merge_drop_cols = [
        "store_name_y",
        "address_num_x",
        "address_num_y",
        "latitude_y",
        "longitude_y",
        "address_y",
        "match_id",
    ]

    merged_df = merged_df.drop(merge_drop_cols, axis=1)
    merged_df.rename(
        {
            "store_name_x": "store_name",
            "address_x": "address",
            "latitude_x": "latitude",
            "longitude_x": "longitude",
        },
        axis=1,
        inplace=True,
    )
    merged_df["address"] = merged_df["address"].str.title()

    return merged_df
