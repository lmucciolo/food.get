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
    """
    # tract boundaries dataframe 
    all_tracts = full_chi_10_20_tracts_one_mapping()
    all_tracts["GEOID_TRACT_20"] = all_tracts["GEOID_TRACT_20"].astype(int)

    # historic atlas data
    atlas_hist = pd.read_csv(
        pathlib.Path(__file__).parent / "../data/filtered_atlas_update.csv"
    )
    
    # atlas_hist = filtered_atlas()

    # 2022 created metric
    stores = create_buffers()
    metric_2022 = find_intersections(stores)

    metric_2022 = metric_2022.rename(
        columns={"ratio": "lapophalfshare_2022", "low_access": "LATracts_half_2022"}
    )
    metric_2022["tract_id"] = metric_2022["tract_id"].astype(int)

    # merge historic with 2022 metric
    all_metrics = metric_2022.merge(
        atlas_hist, how="left", left_on="tract_id", right_on="CensusTract"
    )

    drop = [
        "Unnamed: 0",
        "CensusTract",
    ]
    all_metrics.drop(drop, axis=1, inplace=True)

    # merge metrics with boundaries
    tracts_metrics = all_tracts.merge(
        all_metrics, how="left", left_on="GEOID_TRACT_20", right_on="tract_id"
    )

    tracts_metrics.drop(["tract_id"], axis=1, inplace=True)

    # add column that is diff from 2010 to 2022

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

    tracts_metrics = gpd.GeoDataFrame(tracts_metrics)

    return tracts_metrics


def track_comparison_df():
    """
    Create the data frames used for track comparison maps
    """
    # prep data
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


# create proportions (times by 100)
# fix zeros on 2019
