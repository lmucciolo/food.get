"""
Project: Analyzing food access and security in Chicago
Team: food.get
File Name: data_extract.py
Authors: Danielle Rosenthal and Stacy George
Note: 
    * Danielle created import_atlas_data
    * Stacy created import_business_liscense_data and import_snap_retailers_data

Description:
    This file imports all the raw data from their source
"""
import pandas as pd

relevant_columns = ['CensusTract', 'State', 'County', 'Urban', 'Pop2010', 'OHU2010', 'lapop1',
'lapop1share', 'lalowi1', 'lalowi1share', 'lasnap1', 'lasnap1share', 'lapop10',
'lapop10share', 'lalowi10', 'lalowi10share', 'lapop20', 'lapop20share', 'lalowi20',
'lalowi20share']

#Atlas_2019 = pd.read_csv('/Users/daniellerosenthal/Downloads/2019Atlas.csv')
#Atlas_2015 = pd.read_csv('/Users/daniellerosenthal/Downloads/2015Atlas.csv')
#Atlas_2010 = pd.read_csv('Users/daniellerosenthal/Downloads/2010Atlas.csv')
Atlas_Sets = pd.DataFrame()

def import_atlas_data(year):
    Atlas_Raw = pd.read_csv('/Users/daniellerosenthal/Downloads/{}Atlas.csv'.format(year))
    Atlas_Filtered = Atlas_Raw[relevant_columns]
    Atlas_Filtered['YearLabel'] = year

    Atlas_Sets = pd.concat([Atlas_Sets, Atlas_Filtered])

# Stacy additions 2/4/24
import requests
import json

def import_business_liscense_data():
    """
    This function loads the data from the Chicago data portal on business liscenses
    and returns a list of all the raw data.

    Returns:
        A list of the businesses and all their raw data components from the portal
    """
    # API Call of Business Liscense for Grocery Stores using Turk's Take 1 from notes
    url = "https://data.cityofchicago.org/resource/r5kz-chrr.json"
    response = requests.get(url)
    business_liscense_data = json.loads(response.text)

    return business_liscense_data

def import_snap_retailers_data():
    """
    This function loads the data from the USDA Food and Nutrition Service portal on the 
    location for currently authorized SNAP retailers.

    Returns:
        A list of the retailers and all their raw data components from the portal
    """
    # API Call of SNAP retailers using Turk's Take 1 from notes
    url = "https://services1.arcgis.com/RLQu0rK7h4kbsBq5/arcgis/rest/services/snap_retailer_location_data/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json"
    response = requests.get(url)
    snap_retailer_data = json.loads(response.text)

    return snap_retailer_data

import requests
import time

census_base_call = 'http://api.census.gov/data/2022/acs/acs5'
CENSUS_API_KEY = '33d3a1aa6c54c6ef7e892aba406cc5fbb1c743fa'
params = {'key': CENSUS_API_KEY}
cbc = 'https://api.census.gov/data/2022/acs/acs5?get=NAME,B01001_001E&for=tract:*&in=state:17&key=33d3a1aa6c54c6ef7e892aba406cc5fbb1c743fa'

# Columns related to features of the census tract itself at a high level
tract_identifying_columns = ['CensusTract', 'State', 'County', 'Urban', 
                    'Pop2010', 'OHU2010', 'GroupQuartersFlag', 'NUMGQTRS', 'PCTGQTRS',
 'LowIncomeTracts', 'PovertyRate', 'MedianFamily Income', 'LATracts_half', 'LATracts1', 'LATracts10', 'LATracts20', 'TractSNAP', 'TractLOWI']

tract_half_mile = ['lapophalf','lapophalfshare','lalowihalf','lalowihalfshare','lakidshalf','lakidshalfshare','laseniorshalf','laseniorshalfshare','lawhitehalf','lawhitehalfshare','lablackhalf','lablackhalfshare','laasianhalf','laasianhalfshare','lanhopihalf','lanhopihalfshare','laaianhalf','laaianhalfshare','laomultirhalf','laomultirhalfshare','lahisphalf','lahisphalfshare','lahunvhalf','lahunvhalfshare','lasnaphalf','lasnaphalfshare']

tract_one_mile = ['lapop1','lapop1share','lalowi1','lalowi1share','lakids1','lakids1share','laseniors1','laseniors1share','lawhite1','lawhite1share','lablack1','lablack1share','laasian1','laasian1share','lanhopi1','lanhopi1share','laaian1','laaian1share','laomultir1','laomultir1share','lahisp1','lahisp1share','lahunv1','lahunv1share','lasnap1','lasnap1share']

relevant_columns = ['CensusTract', 'State', 'County', 'Urban', 
                    'POP2010', 'OHU2010', 'lapop1',
                    'lapop1share', 'lalowi1', 'lalowi1share', 'lasnap1', 'lasnap1share', 
                    'lapop10',
                    'lapop10share', 'lalowi10', 'lalowi10share', 
                    'lapop20', 'lapop20share', 'lalowi20',
'lalowi20share']

rel_col_2010 = ['CensusTract', 'State', 'County', 'Urban', 
                    'POP2010', 'OHU2010', 'lapop1',
                    'lapop1share', 'lalowi1', 'lalowi1share', 
                    'lapop10',
                    'lapop10share', 'lalowi10', 'lalowi10share', 
                    'lapop20', 'lapop20share', 'lalowi20',
'lalowi20share']


# get rid of long distance; 

#Atlas_2019 = pd.read_csv('/Users/daniellerosenthal/Downloads/2019Atlas.csv')
#Atlas_2015 = pd.read_csv('/Users/daniellerosenthal/Downloads/2015Atlas.csv')

Atlas_Sets = pd.DataFrame()

def import_atlas_data():
    years = ['2010', '2015', '2019']
    atlas_sets = pd.DataFrame()
    
    for year in years:
        Atlas_Raw = pd.read_csv('/Users/daniellerosenthal/Downloads/AtlasData/Atlas{}.csv'.format(year))
       
        if year == '2010':
            Atlas_Filtered = Atlas_Raw[rel_col_2010]
        else:
            Atlas_Filtered = Atlas_Raw[relevant_columns]
        
        Atlas_Filtered = Atlas_Raw.add_suffix('_{}'.format(year))
        Atlas_Filtered.rename(columns={'CensusTract_{}'.format(year): 'CensusTract'}, inplace=True)
        
        if len(atlas_sets) == 0:
            atlas_sets = Atlas_Filtered
        else:
            atlas_sets.merge(Atlas_Filtered, on='CensusTract', how='left')
    
    atlas_sets.to_csv('atlas_historical.csv')

    return atlas_sets
    

def make_request():
    time.sleep(0.1)
    resp = requests.get(census_base_call, params=params)
    return resp

def import_census():
    response = requests.get(cbc)
    body = response.headers
    return response
    #print(response)
