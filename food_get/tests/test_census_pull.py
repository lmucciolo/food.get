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
import pytest

from food_get.data.extract_census import (
    get_fips_code,
    get_county_code,
    state_income,
    county_income,
    tract_level_extract,
    json_to_df,
)


@pytest.mark.parametrize(
    "state,state_code", [("Illinois", "17"), ("North Dakota", "38"), ("Alabama", "01")]
)
def test_state_code_retreival(state, state_code):
    code = get_fips_code(state)
    assert code == state_code


def test_state_code_retreival_invalid_state():
    with pytest.raises(KeyError) as info:
        get_fips_code("Narnia")
    assert "Please enter a valid US state name" in str(info.value)


@pytest.mark.parametrize(
    "county,county_code",
    [
        ("Cook", "031"),
        ("Cook County", "031"),
    ],
)
def test_county_code_retreival(county, county_code):
    code = get_county_code(county)
    assert code == county_code


def test_county_code_retreival_invalid():
    with pytest.raises(KeyError) as info:
        get_county_code("Antartica")
    assert "You have not entered a correct Illinois county name" in str(info.value)


# Tests for state income
@pytest.mark.parametrize(
    "export,state,expected_len, expected_median, expeected_mean",
    [
        (False, "Illinois", 1, "78433", "108873"),
        (False, "New Hampshire", 1, "90845", "118118"),
    ],
)
def test_state_income(export, state, expected_len, expected_median, expeected_mean):
    income_df = state_income(export=export, state=state)
    assert len(income_df) == expected_len
    assert income_df["median_household_income"][0] == expected_median
    assert income_df["mean_household_income"][0] == expeected_mean


# Tests for county income
@pytest.mark.parametrize(
    "export,county,expected_len, expected_median, expeected_mean",
    [
        (False, "Cook County", 1, "78304", "113411"),
        (False, "Woodford", 1, "80093", "103919"),
    ],
)
def test_county_income(export, county, expected_len, expected_median, expeected_mean):
    income_df = county_income(export=export, county=county)
    assert len(income_df) == expected_len
    assert income_df["median_household_income"][0] == expected_median
    assert income_df["mean_household_income"][0] == expeected_mean


# ALL THE TESTS FOR TRACT LEVEL EXTRACT
def test_invalid_table():
    with pytest.raises(KeyError) as info:
        tract_level_extract(table="B01001", state_fips_code="17", county_code="031")
    assert (
        "You seem to have specified a table outside of the ACS data profiles database!"
        in str(info.value)
    )


def test_no_table_no_variable():
    with pytest.raises(KeyError) as info:
        tract_level_extract(state_fips_code="17", county_code="031")
    assert (
        "No table or variable was provided. Please enter either the name of a table or a list of variables"
        in str(info.value)
    )


def test_one_variable():
    api_response = tract_level_extract(
        variables=["DP05_0001E"], state_fips_code="17", county_code="031"
    )
    api_response_df = json_to_df(api_response)
    assert len(api_response_df) == 1332
    one_tract = api_response_df[api_response_df["tract"] == "010100"]
    assert one_tract["DP05_0001E"].iloc[0] == "4284"
