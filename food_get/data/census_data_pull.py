import requests
import time
import pandas as pd
from lxml import html

illinois_counties = pd.read_csv('/Users/daniellerosenthal/Downloads/illinois_counties.txt', sep='|', dtype=str)
#illinois_counties['COUNTYNAME'] = illinois_counties['COUNTYNAME'].astype('str')

state_name_fips_dict = {
    'Alabama': '01',
    'Alaska': '02',
    'Arizona': '04',
    'Arkansas': '05',
    'California': '06',
    'Colorado': '08',
    'Connecticut': '09',
    'Delaware': '10',
    'Florida': '12',
    'Georgia': '13',
    'Hawaii': '15',
    'Idaho': '16',
    'Illinois': '17',
    'Indiana': '18',
    'Iowa': '19',
    'Kansas': '20',
    'Kentucky': '21',
    'Louisiana': '22',
    'Maine': '23',
    'Maryland': '24',
    'Massachusetts': '25',
    'Michigan': '26',
    'Minnesota': '27',
    'Mississippi': '28',
    'Missouri': '29',
    'Montana': '30',
    'Nebraska': '31',
    'Nevada': '32',
    'New Hampshire': '33',
    'New Jersey': '34',
    'New Mexico': '35',
    'New York': '36',
    'North Carolina': '37',
    'North Dakota': '38',
    'Ohio': '39',
    'Oklahoma': '40',
    'Oregon': '41',
    'Pennsylvania': '42',
    'Rhode Island': '44',
    'South Carolina': '45',
    'South Dakota': '46',
    'Tennessee': '47',
    'Texas': '48',
    'Utah': '49',
    'Vermont': '50',
    'Virginia': '51',
    'Washington': '53',
    'West Virginia': '54',
    'Wisconsin': '55',
    'Wyoming': '56',
    'American Samoa': '60',
    'Guam': '66',
    'Northern Mariana Islands': '69',
    'Puerto Rico': '72',
    'Virgin Islands': '78'}

"""
All available variables for the 2022 ACS Data Profiles can be found here
https://api.census.gov/data/2022/acs/acs5/profile/variables.html

"""

def json_to_df(response):
    return pd.DataFrame(response.json()[1:], columns=response.json()[0])

def tract_level_extract(table=None, variables=None, state='Illinois', county='Cook County'):
    state_fips_code = get_fips_code(state)
    county_code = get_county_code(county)

    if not table and not variables:
        print("No table or variable was provided. Please enter either the name of the table or variable you want to pull")
        raise KeyError()

    # If an entire table is requested, pull the entire table
    if table:
        if table.startswith("DP"):
            link = "https://api.census.gov/data/2022/acs/acs5/profile?get=group({})&for=tract:*&in=state:{}&in=county:{}".format(table, state_fips_code, county_code)
        else:
            print("You seem to have specified a table outside of the ACS data profiles database!")
            raise KeyError()

    # If just one variable is requested, pull just that one variable
    elif variables:
        formatted_variables = ",".join(variables)
        link = "https://api.census.gov/data/2022/acs/acs5/profile?get={}&for=tract:*&in=state:17&in=county:{}".format(formatted_variables, county_code)

    response = requests.request("GET", link)
    return response

def format_extract():
    #final_dataframe = pd.DataFrame()

    # DP05_0001E = total population
    # DP02_0001E = Total Households
    # DP03_0062E Median household income
    # DP03_0063E = Mean household income 
    # DP03_0119PE = Percentage of families and people whose income in the
        # past 12 months is below the poverty level

    col_name_mapping = {'DP05_0001E': 'total_population', 'DP02_0001E': 'total_households', 
     'DP03_0062E': 'median_household_income', 'DP03_0063E': 'mean_household_income',
     'DP03_0119PE': 'poverty_rate'}


    variables = ['DP05_0001E', 'DP02_0001E',
                      'DP03_0062E', 'DP03_0063E',
                      'DP03_0119PE']
    api_response = tract_level_extract(variables=variables)
    df_response = json_to_df(api_response)
    #if final_dataframe.empty:
        #final_dataframe = df_response
    
    df_response.rename(columns=col_name_mapping, inplace=True)
    df_response.to_csv('census_2022.csv')

    return df_response

def get_fips_code(state):
    if state not in state_name_fips_dict.keys():
        raise KeyError("Please enter a valid US state name")
    return state_name_fips_dict[state]

def get_county_code(county):
    if not county.endswith(' County'):
        county = county + ' County'
    
    if county in illinois_counties['COUNTYNAME'].values:
        county_info = illinois_counties[illinois_counties['COUNTYNAME']==county].reset_index()
        county_code = county_info['COUNTYFP'][0]

    else:
        raise KeyError("You have not entered a correct Illinois county name")
    
    return county_code

def state_income(export=False, state='Illinois'):
    state_fips_code = get_fips_code(state)
    link = "https://api.census.gov/data/2022/acs/acs5/profile?get=DP03_0062E,DP03_0063E&for=state:{}".format(state_fips_code)
    response = requests.request("GET", link)
    df_response = json_to_df(response)
    column_renaming = {'DP03_0062E': 'median_household_income', 'DP03_0063E': 'mean_household_income'}
    df_response.rename(columns=column_renaming, inplace=True)
    df_response['state'] = state

    if export:
        df_response.to_csv('{}_2022.csv'.format(state))
    else:
        return df_response

def county_income(export=False, state='Illinois', county='Cook County'):
    state_fips_code = get_fips_code(state)
    county_code = get_county_code(county)

    link = 'https://api.census.gov/data/2022/acs/acs5/profile?get=DP03_0062E,DP03_0063E&for=county:{}&in=state:{}'.format(county_code, state_fips_code)
    response = requests.request("GET", link)
    df_response = json_to_df(response)
    column_renaming = {'DP03_0062E': 'median_household_income', 'DP03_0063E': 'mean_household_income'}
    df_response.rename(columns=column_renaming, inplace=True)
    
    if export:
        df_response.to_csv('cook_county_2022.csv')
    else:
        return df_response