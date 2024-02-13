import pandas as pd

# import geopandas as gpd


def extract_chi_census_tracts(filename, year):
    """
    Takes in census track data and returns shorted table to filter by
    census track for chicago

    """
    census = pd.read_csv(filename, dtype=str)

    if year == 2000:
        columns = ["CENSUS_TRA", "CENSUS_T_1"]
    elif year == 2010:
        columns = ["TRACTCE10", "GEOID10", "NAME10", "NAMELSAD10"]
    else:
        print("Year not compatible with function")

    census = pd.read_csv(filename, dtype=str)

    return census[columns]


census_tracts_2000 = extract_chi_census_tracts(
    "food.get/data/raw_data/census_tracts_2000.csv"
)
census_tracts_2010 = extract_chi_census_tracts(
    "food.get/data/raw_data/census_tracts_2010.csv"
)
