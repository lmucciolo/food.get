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

from food_get.data.cleanup_grocery import clean_grocery_stores
from food_get.data.extract_tracts import restrict_tract_to_shore
import geopandas as gpd
import pandas as pd
import pathlib

M_TO_MILES = 1609.34
COUNTY_HH_INCOME = 78304


def create_buffers():
    """
    This function takes in a dataframe of grocery store locations and produces
    ½ mile buffers around each location.

    Returns:
        GeoDataFrame of grocery store locations and the geometry of their buffers
    """
    # pull in cleaned grocery store data with merged SNAP data
    cleaned_grocery = clean_grocery_stores()
    cleaned_grocery["store_id"] = range(1, len(cleaned_grocery.index) + 1)

    # read in grocery store data as points
    stores_gdf = gpd.GeoDataFrame(
        cleaned_grocery,
        geometry=gpd.points_from_xy(
            cleaned_grocery.longitude, cleaned_grocery.latitude
        ),
        crs="epsg:4326",
    )

    stores_gdf = stores_gdf.to_crs({"init": "epsg:3174"})

    # create ½ mile buffers around each grocery store
    # geometry is now a column of buffer polygons
    stores_gdf["geometry"] = stores_gdf["geometry"].buffer(0.5 * M_TO_MILES)

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

    tracts_with_access_label = identify_low_access(tracts_with_ratios)
    tracts_with_all_labels = identify_low_income(tracts_with_access_label)

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
    diff_tracts = list(difference["GEOID_TRACT_20"])
    ratios_dict = {}

    for _, tract in tracts.iterrows():
        if tract["GEOID_TRACT_20"] in diff_tracts:
            index_ = difference["GEOID_TRACT_20"]
            difference.index = index_
            diff_area = difference.loc[tract["GEOID_TRACT_20"], "difference_area"]
            ratios_dict[tract["GEOID_TRACT_20"]] = 1 - diff_area / tract["tract_area"]
        else:
            ratios_dict[tract["GEOID_TRACT_20"]] = 1

    ratios_df = pd.DataFrame(ratios_dict.items(), columns=["tract_id", "ratio"])

    return ratios_df


def identify_low_access(ratios_df):
    """
    This function identifies 2020 Census tracts as low-access. If less than ⅔ of
    the census tract is within a ½ mile of a grocery store then the tract is
    considered low-access.

    Inputs:
        tracts_with_ratios (GeoDataFrame): contains all tract information and
            boundaries, as well as access ratios

    Returns:
        A GeoDataFrame of 2020 Census tracts with a low_access indicator column

    """
    ratios_df["low_access"] = ratios_df.apply(
        lambda x: 1 if x["ratio"] < 1 / 3 else 0, axis=1
    )
    ratios_df["2022_prop_label"] = (ratios_df["ratio"] * 100).round(1)
    ratios_df["2022_prop_label"] = ratios_df["2022_prop_label"].astype(str) + "%"

    return ratios_df


def identify_low_income(tracts_with_access_label):
    """
    This function identifies 2020 Census tracts as low-income. If the Census
    tract's median household income is  less than or equal to 80 percent of the
    metropolitan area's (in this case County) median family income, then the
    tract is considered low-access.

    Inputs:
        tracts_with_access_label (GeoDataFrame): contains all tract information
            and boundaries and access label

    Returns:
        A GeoDataFrame of 2020 Census tracts with a low_income indiciator column

    """
    # pull in census 2022 income data for the tract level
    income_census = pd.read_csv(
        pathlib.Path(__file__).parent / "../data/census_2022.csv"
    )

    # create variable for tract id
    income_census.loc[income_census["tract"] < 100000, "tract_id"] = (
        income_census["state"].astype(str)
        + "0"
        + income_census["county"].astype(str)
        + "0"
        + income_census["tract"].astype(str)
    )
    income_census.loc[income_census["tract"] >= 100000, "tract_id"] = (
        income_census["state"].astype(str)
        + "0"
        + income_census["county"].astype(str)
        + income_census["tract"].astype(str)
    )

    # keep only necessary variables
    income_census = income_census.rename(columns={"DP03_0062E": "median_hh_income"})
    income_census = income_census[["median_hh_income", "tract_id"]]

    # merge census data with tract data
    tracts_with_access_label = tracts_with_access_label.merge(
        income_census, how="left", on="tract_id"
    )

    # if census tract median hh income <=80% county hh income then low-income
    tracts_with_access_label["low_income"] = tracts_with_access_label.apply(
        lambda x: 1 if x["median_hh_income"] <= 0.8 * COUNTY_HH_INCOME else 0, axis=1
    )

    return tracts_with_access_label
