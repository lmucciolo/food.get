import pytest

from food_get.data.census_data_pull import get_fips_code, get_county_code, state_income, county_income, tract_level_extract


@pytest.mark.parametrize("state,state_code", [
    ('Illinois', '17'),
    ('North Dakota', '38'),
    ('Alabama', '01')
])

def test_state_code_retreival(state, state_code):
    code = get_fips_code(state)
    assert code == state_code

def test_state_code_retreival_invalid_state():
    with pytest.raises(KeyError) as info:  
        get_fips_code("Narnia")  
    assert str(info.value) == "Please enter a valid US state name"

@pytest.mark.parametrize("county,county_code", [
    ('Cook', '031'),
    ('Cook County', '031'),
])

def test_county_code_retreival(county, county_code):
    code = get_county_code(county)
    assert code == county_code

def test_county_code_retreival_invalid():
    with pytest.raises(KeyError) as info:
        get_county_code("Antartica")
    assert str(info.value) == "You have not entered a correct Illinois county name"


@pytest.mark.parametrize("export,state,expected_len, expected_median, expeected_mean", [
    (False, 'Illinois', 1, '78433', '108873'),
    (False, "New Hampshire", 1, '90845', '118118')
])

# Tests for state income
def test_state_income(export, state, expected_len, expected_median, expeected_mean):
    income_df = state_income(export=export, state=state)
    assert len(income_df) == expected_len
    assert income_df['median_household_income'][0] == expected_median
    assert income_df['mean_household_income'][0] == expeected_mean


# Tests for county income
@pytest.mark.parametrize("export,county,expected_len, expected_median, expeected_mean", [
    (False, "Cook County", 1, 100, 100),
    (False, "Woodford", 1, 100, 100)
])

def test_county_income(export, county, expected_len, expected_median, expeected_mean):
    income_df = county_income(export=export, county=county)
    assert len(income_df) == expected_len
    assert income_df['median_household_income'][0] == expected_median
    assert income_df['mean_household_income'][0] == expeected_mean

# ALL THE TESTS FOR TRACT LEVEL EXTRACT
def test_invalid_table():
    with pytest.raises(KeyError) as info:
        tract_level_extract(table='B01001', state_fips_code='17', county_code='031')
    assert str(info.value) == "You seem to have specified a table outside of the ACS data profiles database!"

def test_no_table_no_variable():
    with pytest.raises(KeyError) as info:
        tract_level_extract(state_fips_code='17', county_code='031')
    assert str(info.value) == "No table or variable was provided. Please enter either the name of a table or a list of variables"


@pytest.mark.parametrize("state_code,county_code, expected_length, test_metric_label, test_metric_value", [
    (False, "Cook County", 1, 100, 100),
    (False, "Woodford", 1, 100, 100)
])



def test_one_variable():
    return None

def test_list_of_variables():


def 

