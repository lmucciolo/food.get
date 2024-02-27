import requests
import io
import pandas as pd
import numpy as np
import geopandas as gpd
import pathlib


# Step 1: Get 2010 chi census tracks into a pandas dataFrame \
# Step 2: Get 2020 chi census tracks into a pandas dataFrame \
# Step 3: Determine relationship between 2010 and 2020. \
# Step 4: Limit to just census tracks in 2020 and 2010 that have a one to one relationship


# step 1
def extract_chi_census_tracts_2010():
    """
    Takes in census track data (geojson) and returns shorted pandas df
    to filter by census track for chicago. Includes geometries.

    """
    filename = (
        pathlib.Path(__file__).parent / "../data/raw_data/census_tracts_2010.geojson"
    )
    # filename = 'raw_data/census_tracts_2010.geojson'
    census = gpd.read_file(filename)
    columns = ["tractce10", "geoid10", "name10", "namelsad10", "geometry"]
    final_df = pd.DataFrame(census[columns])

    return final_df


# step 2
def extract_chi_census_tracts_2020():
    """
    Takes in census track data and returns shorted table to filter by
    census track for chicago
    """
    # for now until we get 2020 data
    # filename = "/Users/austinsteinhart/Desktop/CAPP122/food.get/food_get/data/raw_data/chi_ct_2020.csv"
    filename = pathlib.Path(__file__).parent / "../data/raw_data/chi_ct_2020.csv"
    # filename = "raw_data/chi_ct_2020.csv"

    census = pd.read_csv(filename, dtype=str)
    final_df = census[["ct_chicago", "community_name"]].rename(
        columns={"ct_chicago": "geoid20"}
    )

    return final_df


# all census tracts for chicago from 2010
# chi_census_tracts_2010 = extract_chi_census_tracts_2010()

# all census tracts for chicago from 2020
# chi_census_tracts_2020 = extract_chi_census_tracts_2020()


# step 3 / 4
# https://www.census.gov/geographies/reference-files/time-series/geo/relationship-files.2020.html#tract


def census_tracts_2020_2010_relationships():
    """
    returns a mapping of only 1:1 census tracts from 2020 and 2010 with GEOID_TRACT
    """
    url = "https://www2.census.gov/geo/docs/maps-data/data/rel2020/tract/tab20_tract20_tract10_natl.txt"
    data = requests.get(url).content
    relationships = pd.read_csv(io.StringIO(data.decode("utf-8")), sep="|", dtype=str)

    chi_census_tracts_2020 = extract_chi_census_tracts_2020()

    # filter to just tracts in chicago, will need to be 2020
    chi_geoid20 = list(chi_census_tracts_2020["geoid20"].astype(str))
    filter = relationships["GEOID_TRACT_20"].isin(chi_geoid20)
    chi_relationships = relationships[filter]

    dupe_count = chi_relationships["GEOID_TRACT_20"].value_counts().reset_index()

    chi_relationships_flag = chi_relationships.merge(
        dupe_count, how="left", left_on="GEOID_TRACT_20", right_on="GEOID_TRACT_20"
    )

    filter = chi_relationships_flag["count"] == 1
    chi_relationships_flag["relation"] = np.where(filter, "one", "many")

    # limit columns
    columns = ["GEOID_TRACT_20", "GEOID_TRACT_10", "relation"]

    return chi_relationships_flag[columns].reset_index(drop=True)


def full_chi_10_20_tracts_one_mapping():
    """
    Returns a pandas df of all chicago census tracks that have a 1:1 mapping
    (didnt change) from 2010 to 2020. Includes 2020 id (geoid20), 2010 id
    (geoid10) and the boundaries for the tract (geometry).
    Note: includes full census track. should then apply restrict_tract_to_shore()
    for metric calculation.
    """

    tracts_2010 = extract_chi_census_tracts_2010()
    tracts_2010 = tracts_2010[["geoid10", "geometry"]]
    tracts_2020 = extract_chi_census_tracts_2020()

    tract_relationships = census_tracts_2020_2010_relationships()
    # only 1:1 tracts in 2020
    tract_relationships_1_1 = tract_relationships[
        tract_relationships["relation"] == "one"
    ]

    # add on geometries to file, preference 2020 geo (2010 for now)
    final_df = tract_relationships_1_1.merge(
        tracts_2010, how="left", left_on="GEOID_TRACT_10", right_on="geoid10"
    )

    final_df = final_df.drop(columns=["geoid10", "relation"])

    return final_df


def restrict_tract_to_shore():
    """
    Returns a pandas df with the census tracks bounded by shore for metric
    calculation
    """

    census_tracks = full_chi_10_20_tracts_one_mapping()
    census_tracks_geo = gpd.GeoDataFrame(census_tracks)

    lake = gpd.read_file(
        pathlib.Path(__file__).parent
        / "../data/raw_data/Lake_Michigan_Shoreline.geojson"
        # "/Users/austinsteinhart/Desktop/CAPP122/food.get/food_get/data/raw_data/Lake_Michigan_Shoreline.geojson"
    )

    final_geo = census_tracks_geo.overlay(lake, how="difference")

    final_df = pd.DataFrame(final_geo)

    return final_df


def tracts_2010_key():
    """
    df marking which tracts we excluded due to not mapping 1:1 in 2010 to 2020
    to visualize and understand implications.
    """

    tracts_2010 = extract_chi_census_tracts_2010()
    chi_ct_relationships = census_tracts_2020_2010_relationships()

    collapse = (
        chi_ct_relationships.groupby("GEOID_TRACT_10")
        .agg({"relation": lambda x: max(x)})
        .reset_index()
    )
    final_df = collapse.merge(
        tracts_2010,
        how="left",
        left_on="GEOID_TRACT_10",
        right_on="geoid10",
    )

    final_df = final_df[["geoid10", "relation", "namelsad10", "geometry"]]

    # take out NaN
    final_df = final_df.dropna()

    return final_df
