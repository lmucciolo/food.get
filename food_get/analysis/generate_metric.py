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
import geopandas as gpd
M_TO_MILES = 1609.34

# pull in cleaned grocery store data with merged SNAP data
cleaned_grocery = clean_business_license()

# pull in census tract data for 2020 as a geo dataframe
#tracts_2020 = 

def create_buffers():
    """
    """
    # read in grocery store data as points
    stores_gdf = gpd.GeoDataFrame(
        cleaned_grocery,
        geometry=gpd.points_from_xy(cleaned_grocery.long, cleaned_grocery.lat),
        crs="EPSG:4326") # IS 4326 THE CORRECT CRS?
    
    # this will drop any stores that are not within the Chicago tracts
    #stores_with_tracts = stores_gdf.sjoin(census_tracts_2020, how="inner")

    # create 1/2 mile buffers around each grocery store
    # geometry is now a column of polygons
    stores_gdf["geometry"] = stores_gdf.buffer(0.5*M_TO_MILES)

    return stores_gdf

def find_intersections(stores_gdf):
    """
    """
    tracts_with_buffers = gpd.sjoin_nearest(tracts_2020, stores_gdf, distance_col = "distances")

    for id in tracts_2020["tract_id"]:
        intersection_dict = {}
        current_tract = tracts_with_buffers[tracts_with_buffers["tract_id"] == id]

        for store in current_tract["store_id"]:
            current_store = stores_gdf["gs_id" == store]["buffer"]
            # find intersection of current store with current tract
            intersection = current_tract.overlay(current_store, how="intersection")
            # add intersection to dictionary
            intersection_dict[store] = intersection



def find_areas():
    """
    """
    stores_with_tracts = merge_stores_with_tracts()

    # calculate area of buffers and tracts
    stores_with_tracts["buffer_area"] = stores_with_tracts["buffer"].area()
    stores_with_tracts["tract_area"] = stores_with_tracts["tract"].area()

    for _, row in stores_with_tracts.iterrows():
        row["store_intersection"] = 

    return stores_with_tracts



def create_low_income_metric():
    """
    """

    return None



