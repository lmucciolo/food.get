import pandas as pd
import geopandas as gpd
import numpy as np
import pathlib
from food_get.data.data_extract_census import full_chi_10_20_tracts_one_mapping
from food_get.analysis.generate_metric import create_buffers, find_intersections
from food_get.data.data_extract_census import tracts_2010_key
from food_get.data.cleanup_sg import clean_grocery_stores, clean_snap_retailer_data
from food_get.data.data_extract import filtered_atlas
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

    # Importing historical Atlas dataset
    atlas_hist = filtered_atlas()

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

    # Merging historic Atlas data with 2022 metric
    all_metrics = metric_2022.merge(
        atlas_hist, how="left", left_on="tract_id", right_on="CensusTract"
    )

    drop = [
        "CensusTract",
    ]
    all_metrics.drop(drop, axis=1, inplace=True)

    # Merge metrics dataframe with census tracts information
    tracts_metrics = all_tracts.merge(
        all_metrics, how="left", left_on="GEOID_TRACT_20", right_on="tract_id"
    )

    tracts_metrics.drop(["tract_id"], axis=1, inplace=True)

    # Creating column with label for whether 2010 to 2022 metric improved
    tracts_metrics["10_22_diff"] = np.where(
        tracts_metrics["lapophalfshare_2022"] < tracts_metrics["lapophalfshare_2010"],
        "Worse",
        np.where(
            tracts_metrics["lapophalfshare_2022"]
            > tracts_metrics["lapophalfshare_2010"],
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
        / "../data/raw_data/Lake_Michigan_Shoreline.geojson"
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
