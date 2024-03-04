"""
Project: Analyzing food access and security in Chicago
Team: food.get
File Name: extract_census.py
Author: Danielle Rosenthal

Notes:
    * In the current implementation we only support searching for Illinois counties

Description:
    This file scrapes the US Census 2022 5-Year Estimate Data Profiles tables.
"""
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)

import requests
import pandas as pd
import pathlib
import json

illinois_counties = pd.read_csv(
    pathlib.Path(__file__).parent / "../data/import_data/illinois_counties_guide.csv"
)
with open(
    pathlib.Path(__file__).parent / "../data/import_data/state_fips.json"
) as json_file:
    state_name_fips_dict = json.load(json_file)


def json_to_df(response):
    """
    Formats json response object from API pull into a pandas dataframe.

    Args:
        response (json response object): the response object from the API pull

    Returns:
        df (pandas DataFrame): pandas DataFrame version of the json response object.
    """
    return pd.DataFrame(response.json()[1:], columns=response.json()[0])


def tract_level_extract(
    table=None, variables=None, state_fips_code=None, county_code=None
):
    """ "
    Extracts data for either an entire table or a set of variables from the ACS 2022
        5-Year Data Profiles at the census tract level. Can filter data by state and county,
        however the current implementation does not support filtering by county
        without specifying a state first.


    All available variables for the 2022 ACS Data Profiles can be found here
        https://api.census.gov/data/2022/acs/acs5/profile/variables.html

    Args:
        table (str): name of the Data Profiles table
        variables (list of strings): the name of the state
        state_fips_code (str): FIPS code for the state
        county_code (str): FIPS code for the county

    Returns:
        response (response object): the response object from the API pull.
    """
    if not table and not variables:
        raise KeyError(
            "No table or variable was provided. Please enter either the name of a table or a list of variables"
        )
    if county_code and not state_fips_code:
        raise KeyError(
            "The current implementation does not support filtering by county without specifying a state."
        )

    # If an entire table is requested, pull the entire table
    if table:
        if table.startswith("DP"):
            # If a county is not specified, we will look at all tracts within the given state
            if not county_code:
                link = "https://api.census.gov/data/2022/acs/acs5/profile?get=group({})&for=tract:*&in=state:{}".format(
                    table, state_fips_code
                )
            # If no state is specified, pull the table for every census tract in the entire country
            elif not state_fips_code:
                link = "https://api.census.gov/data/2022/acs/acs5/profile?get=group({})&for=tract:*".format(
                    table
                )
            else:
                link = "https://api.census.gov/data/2022/acs/acs5/profile?get=group({})&for=tract:*&in=state:{}&in=county:{}".format(
                    table, state_fips_code, county_code
                )
        else:
            raise KeyError(
                "You seem to have specified a table outside of the ACS data profiles database!"
            )

    # If a list of specific variables is requested, pull just those
    elif variables:
        if type(variables) != list:
            raise TypeError("Variables must be entered in list format")
        formatted_variables = ",".join(variables)

        # If no county is provided, return the variables for all tracts within a given state
        if not county_code:
            link = "https://api.census.gov/data/2022/acs/acs5/profile?get={}&for=tract:*&in=state:{}".format(
                formatted_variables, state_fips_code
            )
        # If no state is provided, return the variables for every census tract within the entire country
        elif not state_fips_code:
            link = "https://api.census.gov/data/2022/acs/acs5/profile?get={}&for=tract:*".format(
                formatted_variables
            )
        else:
            link = "https://api.census.gov/data/2022/acs/acs5/profile?get={}&for=tract:*&in=state:{}&in=county:{}".format(
                formatted_variables, state_fips_code, county_code
            )

    response = requests.request("GET", link)
    return response


def census_tract_metrics(export=False, state="Illinois", county="Cook County"):
    """ "
    Returns dataframe with tract level information required for building the
        low access metric for 2022.

    Args:
        export (bool): of True, the function will create a csv of the resulting dataframe
        state (str): the name of the state
        county (str): the name of the county

    Returns:
        df_response (pandas DataFrame): a dataframe with tract level metrics
    """

    # Getting state and county FIPS codes
    if state:
        state_fips_code = get_fips_code(state)
    else:
        state_fips_code = None

    if county:
        county_code = get_county_code(county)
    else:
        county_code = None

    col_name_mapping = {
        "DP05_0001E": "total_population",
        "DP02_0001E": "total_households",
        "DP03_0062E": "median_household_income",
        "DP03_0063E": "mean_household_income",
        "DP03_0119PE": "poverty_rate",
    }

    # Calling the Census API and transforming the result into a dataframe
    api_response = tract_level_extract(
        variables=list(col_name_mapping.keys()),
        state_fips_code=state_fips_code,
        county_code=county_code,
    )
    df_response = json_to_df(api_response)

    # Renaming columns for legibility
    df_response.rename(columns=col_name_mapping, inplace=True)

    if export:
        df_response.to_csv("census_2022.csv")

    return df_response


def get_fips_code(state):
    """ "
    Returns the FIPS code for a state.

    Args:
        state (str): the name of the state

    Returns:
        state_code (str): the FIPS code for the given state
    """
    if state not in state_name_fips_dict.keys():
        raise KeyError("Please enter a valid US state name")
    return state_name_fips_dict[state]


def get_county_code(county):
    """ "
    Returns the FIPS code for a county.

    Args:
        county (str): the name of the county

    Returns:
        county_code (str): the FIPS code for the given county
    """
    if not county.endswith(" County"):
        county = county + " County"

    if county in illinois_counties["COUNTYNAME"].values:
        county_info = illinois_counties[
            illinois_counties["COUNTYNAME"] == county
        ].reset_index()
        county_code = county_info["COUNTYFP"][0]
        county_code = str(county_code)
        if len(county_code) == 1:
            county_code = "00" + county_code
        elif len(county_code) == 2:
            county_code = "0" + county_code
    else:
        raise KeyError("You have not entered a correct Illinois county name")

    return county_code


def state_income(export=False, state="Illinois"):
    """ "
    Creates a one line dataframe with the state level median and mean household
        incomes according to the 2022 ACS 5 Year Estimates.

    Args:
        export (bool): If True, the function will generate a csv of the resulting dataframe
        state (str): the name of the state

    Returns:
        df_response (pandas DataFrame): if export is False, the function will
            return the resulting dataframe.
    """
    state_fips_code = get_fips_code(state)
    link = "https://api.census.gov/data/2022/acs/acs5/profile?get=DP03_0062E,DP03_0063E&for=state:{}".format(
        state_fips_code
    )
    response = requests.request("GET", link)
    df_response = json_to_df(response)
    column_renaming = {
        "DP03_0062E": "median_household_income",
        "DP03_0063E": "mean_household_income",
    }
    df_response.rename(columns=column_renaming, inplace=True)
    df_response["state"] = state

    if export:
        df_response.to_csv("{}_2022.csv".format(state))
    else:
        return df_response


def county_income(export=False, state="Illinois", county="Cook County"):
    """ "
    Creates a one line dataframe with the county level median and mean household
        incomes according to the 2022 ACS 5 Year Estimates. This function currently
        only supports counties within the State of Illinois.

    Args:
        export (bool): If True, the function will generate a csv of the resulting dataframe
        state (str): the name of the state
        county (str): the name of the county

    Returns:
        df_response (pandas DataFrame): if export is False, the function will
            return the resulting dataframe.
    """
    state_fips_code = get_fips_code(state)
    county_code = get_county_code(county)

    link = "https://api.census.gov/data/2022/acs/acs5/profile?get=DP03_0062E,DP03_0063E&for=county:{}&in=state:{}".format(
        county_code, state_fips_code
    )
    response = requests.request("GET", link)
    df_response = json_to_df(response)
    column_renaming = {
        "DP03_0062E": "median_household_income",
        "DP03_0063E": "mean_household_income",
    }
    df_response.rename(columns=column_renaming, inplace=True)

    if export:
        df_response.to_csv("cook_county_2022.csv")
    else:
        return df_response
