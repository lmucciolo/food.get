"""
Project: Analyzing food access and security in Chicago
Team: food.get
File Name: generate_metric.py
Authors: Livia Mucciolo
Note: 
    * Livia created ...

Description:
    This file generates the low-access and low-income metrics by census tract
"""
from ..data.data_cleanup_sg import clean_business_liscense
from ..data.data_extract_census import final_10_20_tracts
import geopandas as gpd
import itertools

M_TO_MILES = 1609.34

# pull in cleaned grocery store data with merged SNAP data
cleaned_grocery = clean_business_liscense()

# pull in census tract data frame for 2020 as a geo dataframe
tracts_2020 = final_10_20_tracts()

def create_buffers():
    """
    """
    # read in grocery store data as points
    stores_gdf = gpd.GeoDataFrame(
        cleaned_grocery,
        geometry=gpd.points_from_xy(cleaned_grocery.long, cleaned_grocery.lat),
        crs="EPSG:4326") # IS 4326 THE CORRECT CRS?

    # create 1/2 mile buffers around each grocery store
    # geometry is now a column of polygons
    stores_gdf["geometry"] = stores_gdf.buffer(0.5*M_TO_MILES)

    return stores_gdf

def find_intersections(stores_gdf):
    """
    """
    tracts_with_buffers = gpd.sjoin_nearest(tracts_2020, stores_gdf, distance_col = "distances")

    for id in tracts_2020["tract_id"]:
        intersection_series = gpd.GeoSeries()
        current_tract = tracts_with_buffers[tracts_with_buffers["tract_id"] == id]

        for store in current_tract["store_id"]:
            current_store = stores_gdf[stores_gdf["gs_id"] == store]["geometry"]
            # find intersection of current store with current tract
            intersection = current_tract.overlay(current_store, how="intersection")
            # add intersection to dictionary
            intersection_series.append(intersection)
            # find ratio of grocery store buffers to tract area
            find_ratio(id, intersection_series)

    identify_low_access()
    identify_low_income()

    return tracts_2020

def find_ratio(id, intersection_series):
    """
    """
    # calculate area of intersecting buffers and tracts
    tract_area = tracts_2020[tracts_2020["tract_id"] == id]["geometry"].area()
    total_buffer_area = intersection_series.area().sum()

    repeating_areas = 0

    # find areas of intersecting buffers to subtract from total area
    for i, polygon1 in enumerate(intersection_series[:-1]):
        for polygon2 in intersection_series[i+1:]:
            repeating_areas += polygon1.overlay(polygon2, how="intersection").area()

    # find ratio of grocery stores within 1/2 mile radius to tract area and
    # remove intersections between buffers
    store_tract_ratio = (total_buffer_area - repeating_areas)/tract_area

    tracts_2020[tracts_2020["tract_id"] == id]["ratio"] = store_tract_ratio

    return None


def identify_low_access():
    """
    If less than ⅔ of the census tract is within a ½ mile of a grocery store 
    then tract is considered low-access.
    """
    if tracts_2020["ratio"] < (2/3):
        tracts_2020["low_access"] = 1
    else:
        tracts_2020["low_access"] = 0

    return None


def identify_low_income():
    """
    """
    # merge tracts dataframe with income data frame

    # if census tract poverty rate >20% then low-income

    return None



