"""
Project: Analyzing food access and security in Chicago
Team: food.get
File Name: agg_metrics.py
Authors: Austin Steinhart

Description:
    This file generates DataFrames of the combined metrics and grocery stores 
    for use in the map.
"""

import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)

import geopandas as gpd
import numpy as np
import pathlib
from food_get.data.extract_tracts import (
    full_chi_10_20_tracts_one_mapping,
    tracts_2010_key,
)
from food_get.analysis.generate_metric import create_buffers, find_intersections
from food_get.data.cleanup_grocery import clean_grocery_stores, clean_snap_retailer_data
from food_get.data.extract_atlas import filtered_atlas
from food_get.data.match_groceries import match_grocery_stores


def tracts_metrics_df():
    """
    Create the complete data frames used for the maps with metrics and boundaries

    Args: None

    Returns:
        tracts_metrics (GeoDataFrame): GeoDataFrame including census tract boundaries,
            historical Atlas data, and computed 2022 metric
    """
    # Pulling in tract boundaries dataframe
    all_tracts = full_chi_10_20_tracts_one_mapping()
    all_tracts["GEOID_TRACT_20"] = all_tracts["GEOID_TRACT_20"].astype(int)
    all_tracts["GEOID_TRACT_10"] = all_tracts["GEOID_TRACT_10"].astype(int)
    # Importing historical Atlas dataset
    atlas_hist = filtered_atlas()
    atlas_hist["CensusTract"] = atlas_hist["CensusTract"].astype(int)

    # Importing 2022 metric
    stores = create_buffers()
    metric_2022 = find_intersections(stores)

    # Renaming 2022 metric columns to align wit historical data
    metric_2022 = metric_2022.rename(
        columns={
            "ratio": "lapophalfshare_2022",
            "low_access": "LATracts_half_2022",
            "low_income": "LowIncomeTracts_2022",
        }
    )
    metric_2022["tract_id"] = metric_2022["tract_id"].astype(int)

    # Merging 2022 metric with bounds
    metrics_2022_bounds = all_tracts.merge(
        metric_2022, how="left", left_on="GEOID_TRACT_20", right_on="tract_id"
    )

    metrics_2022_bounds.drop(["tract_id"], axis=1, inplace=True)

    # Merge 2022 with historic
    tracts_metrics = metrics_2022_bounds.merge(
        atlas_hist, how="left", left_on="GEOID_TRACT_10", right_on="CensusTract"
    )

    tracts_metrics.drop(["CensusTract"], axis=1, inplace=True)

    # Creating column with label for whether 2010 to 2022 metric improved
    tracts_metrics["10_22_diff"] = np.where(
        tracts_metrics["lapophalfshare_2022"] < tracts_metrics["lapophalfshare_2019"],
        "Worse",
        np.where(
            tracts_metrics["lapophalfshare_2022"]
            > tracts_metrics["lapophalfshare_2019"],
            "Better",
            "Same",
        ),
    )
    tracts_metrics["GEOID_TRACT_20"] = tracts_metrics["GEOID_TRACT_20"].astype(str)

    # Transforming dataset into a GeoDataFrame
    tracts_metrics = gpd.GeoDataFrame(tracts_metrics)

    return tracts_metrics


def track_comparison_df():
    """
    Create the data frames used for track comparison maps

    Args: None

    Returns:
        tracts_keep (GeoDataFrame): census tracts with one-to-one mappings
            we are using to compare 2010 to 2020
        tracts_drop (GeoDataFrame): tracts which do not map one-to-one for 2010
            to 2020
        tracts_keep_shoreline (GeoDataFrame): tracts whose are is restricted
            by the presence of waterways
        lake (GeoDataFrame): boundaries of all waterways

    """
    # Import and prepare census tract geographic information
    geojson_data = gpd.GeoDataFrame(tracts_2010_key())
    lake = gpd.read_file(
        pathlib.Path(__file__).parent
        / "../data/import_data/Lake_Michigan_Shoreline.geojson"
    )

    tracts_keep = geojson_data[geojson_data["relation"] == "one"]
    tracts_drop = geojson_data[geojson_data["relation"] == "many"]
    tracts_keep_shore = tracts_keep.overlay(lake, how="difference")

    return tracts_keep, tracts_drop, tracts_keep_shore, lake


def grocery_stores_df():
    """
    Create the data frames used for grocery store mapping

    Args: None

    Returns:
        groc_gdf (GeoDataFrame): locations of grocery stores across the given area

    """
    clean_groc = clean_grocery_stores()
    clean_snap = clean_snap_retailer_data()
    groc_merge = match_grocery_stores(clean_groc, clean_snap)
    groc_merge["is_snap_map"] = np.where(groc_merge["is_snap"], "Yes", "No")

    groc_gdf = gpd.GeoDataFrame(
        groc_merge,
        geometry=gpd.points_from_xy(clean_groc.longitude, clean_groc.latitude),
        crs="EPSG:4326",
    )
    groc_gdf = groc_gdf[groc_gdf["longitude"].notna()]

    return groc_gdf
