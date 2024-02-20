import requests
import time
import pandas as pd
from lxml import html


"""
All available variables for the 2022 ACS Data Profiles can be found here
https://api.census.gov/data/2022/acs/acs5/profile/variables.html

"""

def json_to_df(response):
    return pd.DataFrame(response.json()[1:], columns=response.json()[0])

def extract(table=None, variable=None):

    if not table and not variable:
        print("No table or variable was provided. Please enter either the name of the table or variable you want to pull")
        raise KeyError()

    # If an entire table is requested, pull the entire table
    if table:
        if table.startswith("DP"):
            link = "https://api.census.gov/data/2022/acs/acs5/profile?get=group({})&for=tract:*&in=state:17&in=county:031".format(table)
        else:
            print("You seem to have specified a table outside of the ACS data profiles database!")
            raise KeyError()

    # If just one variable is requested, pull just that one variable
    elif variable:
        link = "https://api.census.gov/data/2022/acs/acs5/profile?get={}&for=tract:*&in=state:17&in=county:031".format(variable)

    response = requests.request("GET", link)
    return response

def format_extract():
    final_dataframe = pd.DataFrame()

    # DP05_0001E = total population
    # DP02_0001E = Total Households
    # DP03_0062E Median household income
    # DP03_0063E = Mean household income 
    # DP03_0119E = Percentage of families and people whose income in the
        # past 12 months is below the poverty level

    for variable in ['DP05_0001E', 'DP02_0001E',
                      'DP03_0062E', 'DP03_0063E',
                      'DP03_0119E']:
        api_response = extract(variable=variable)
        df_response = json_to_df(api_response)
        if final_dataframe.empty:
            final_dataframe = df_response
        else:
            final_dataframe = final_dataframe.merge(df_response[['tract', variable]], on='tract', how='left')

    final_dataframe.to_csv('census_2022.csv')

    return final_dataframe