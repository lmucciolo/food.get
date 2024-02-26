"""
Project: Analyzing food access and security in Chicago
Team: food.get
File Name: generate_metric.py
Authors: Livia Mucciolo
Note: 
    * Livia created all functions below.

Description:
    This file generates the low-access and low-income metrics by Census tract.
"""
from data.cleanup_sg import clean_grocery_stores
from data.data_extract_census import restrict_tract_to_shore
import geopandas as gpd
import pandas as pd

M_TO_MILES = 1609.34


def create_buffers():
    """
    This function takes in a dataframe of grocery store locations and produces
    ½ mile buffers around each location. 

    Returns:
        GeoDataFrame of grocery store locations and the geometry of their buffers
    """
    # pull in cleaned grocery store data with merged SNAP data
    cleaned_grocery = clean_grocery_stores()
    cleaned_grocery['store_id'] = range(1, len(cleaned_grocery.index)+1)

    # read in grocery store data as points
    stores_gdf = gpd.GeoDataFrame(
        cleaned_grocery,
        geometry=gpd.points_from_xy(cleaned_grocery.longitude, cleaned_grocery.latitude),
        crs="epsg:4326")
    
    stores_gdf = stores_gdf.to_crs({'init': 'epsg:3174'})

    # create ½ mile buffers around each grocery store
    # geometry is now a column of buffer polygons
    stores_gdf["geometry"] = stores_gdf["geometry"].buffer(0.5*M_TO_MILES)

    return stores_gdf


def find_intersections(stores_gdf):
    """
    This function first finds the grocery store buffers contained in each 2020
    Census tract. For each tract it then finds the ratio of a tract's area to 
    grocery store buffers inside of the tract. This is done by first creating a 
    series of polygons where a grocery store buffer intersects with a tract. The
    series is then passed to find_ratio to calculate the ratio. Last, it flags 
    whether a tract is low-income and/or low-access

    Inputs:
        stores_gdf (GeoDataFrame): grocery stores with buffers around their
            locations

    Returns:
        A GeoDataFrame of 2020 Census tracts, their boundary polygons, their
        ratio of a tract's area to grocery store buffers inside of the tract, 
        and flags for whether a tract is low-access or low-income.  
    """
    # pull in census tract data frame for 2020 as a geo dataframe
    tracts_2020 = gpd.GeoDataFrame(restrict_tract_to_shore())
    tracts_2020 = tracts_2020.to_crs(crs=3174)

    # find difference of census tracts and buffers by tract
    difference = tracts_2020.overlay(stores_gdf, how="difference")

    # find area of tracts with difference
    difference["difference_area"] = difference.area

    # find total area of all tracts
    tracts_2020["tract_area"] = tracts_2020.area

    # find ratio of grocery store buffers to tract area
    tracts_with_ratios = find_ratio(difference, tracts_2020)
    print(tracts_with_ratios)

    # for id in tracts_2020["GEOID_TRACT_20"]:
    #     print(id)
    #     intersection_series = gpd.GeoDataFrame()
    #     # pull tract information
    #     current_tract = tracts_with_buffers[tracts_with_buffers["GEOID_TRACT_20"] == id]
    #     print("current tract", current_tract)
    #     num_tract += 1

    #     for store in current_tract["store_id"]:
    #         print("store")
    #         current_store = gpd.GeoDataFrame(stores_gdf[stores_gdf["store_id"] == store]["geometry"])
    #         # find intersection of current store with current tract
    #         intersection = current_tract.overlay(current_store, how="intersection", keep_geom_type = True)
    #         # add intersection to series
    #         intersection_series = pd.concat([intersection_series, intersection])

    tracts_with_access_label = identify_low_access(tracts_with_ratios)
    tracts_with_all_labels = identify_low_income(tracts_with_access_label)

    # return tracts_with_all_labels
    return tracts_with_all_labels


def find_ratio(difference, tracts):
    """
    This function calculates the ratio of a tract's area to grocery store 
    buffers inside of the tract. It first finds the tract area and total buffer
    area. It also calculates the area of overlapping buffers to avoid 
    double-counting. The ratio is then added to the tract GeoDataFrame for the
    particular tract.

    Inputs:
        tracts_gdf (GeoDataFrame): contains all tract information and boundaries

    Returns:
        A GeoDataFrame of 2020 Census tracts with a new column of the ratio of
        grocery stores to total area

    """
    for tract in tracts["GEOID_TRACT_20"]:
        # BETTER WAY TO WRITE THIS WAY?
        if tract in list(difference["GEOID_TRACT_20"]):
            tracts[tracts["GEOID_TRACT_20" == tract]]["ratio"] = (1 - 
            (difference["difference_area"][difference["GEOID_TRACT_20" == tract]]/
                tracts["tract_area"][tracts["GEOID_TRACT_20" == tract]]))
        else:
            tracts[tracts["GEOID_TRACT_20" == tract]]["ratio"] = 1

    # since some census tracts are completely covered by buffers need to merge
    # back with all tracts
    #tracts_2020 = tracts_2020.merge(difference, on=["GEOID_TRACT_20", "GEOID_TRACT_10"],
                                    #how="left", indicator=False)
    # calculate area of intersecting buffers and tracts
    
    # total_buffer_area = intersection_series["geometry"].area.sum()

    # repeating_areas = 0

    # # find areas of intersecting buffers to subtract from total area
    # for i, polygon1 in enumerate(intersection_series[:-1]):
    #     for polygon2 in intersection_series[i+1:]:
    #         repeating_areas += polygon1.overlay(polygon2, how="intersection").area()

    # # find ratio of grocery stores within 1/2 mile radius to tract area and
    # # remove intersections between buffers
    # store_tract_ratio = (total_buffer_area - repeating_areas)/tract_area

    # tracts_gdf[tracts_gdf["GEOID_TRACT_20"] == id]["ratio"] = store_tract_ratio

    return tracts


def identify_low_access(tracts_with_ratios):
    """
    This function identifies 2020 Census tracts as low-access. If less than ⅔ of
    the census tract is within a ½ mile of a grocery store then the tract is 
    considered low-access.

    Inputs:
        tracts_with_ratios (GeoDataFrame): contains all tract information and
            boundaries, as well as access ratios
            
    Returns:
        A GeoDataFrame of 2020 Census tracts with a low_access indiciator column

    """
    if tracts_with_ratios["ratio"] < (1/3):
        tracts_with_ratios["low_access"] = 1
    else:
        tracts_with_ratios["low_access"] = 0

    return tracts_with_ratios


def identify_low_income(tracts_with_access_label):
    """
    This function identifies 2020 Census tracts as low-income. If the Census
    tract pverty rate is greater than 20 percent, then the tract is considered
    low-access.

    Inputs:
        tracts_with_access_label (GeoDataFrame): contains all tract information 
            and boundaries and access label

    Returns:
        A GeoDataFrame of 2020 Census tracts with a low_income indiciator column

    """
    # merge tracts dataframe with income data frame

    # if census tract poverty rate >20% then low-income

    return tracts_with_access_label