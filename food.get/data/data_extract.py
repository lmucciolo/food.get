import pandas as pd

relevant_columns = ['CensusTract', 'State', 'County', 'Urban', 'Pop2010', 'OHU2010', 'lapop1',
'lapop1share', 'lalowi1', 'lalowi1share', 'lasnap1', 'lasnap1share', 'lapop10',
'lapop10share', 'lalowi10', 'lalowi10share', 'lapop20', 'lapop20share', 'lalowi20',
'lalowi20share']

#Atlas_2019 = pd.read_csv('/Users/daniellerosenthal/Downloads/2019Atlas.csv')
#Atlas_2015 = pd.read_csv('/Users/daniellerosenthal/Downloads/2015Atlas.csv')
#
Atlas_Sets = pd.DataFrame()

def import_atlas_data(year):
    Atlas_Raw = pd.read_csv('/Users/daniellerosenthal/Downloads/{}Atlas.csv'.format(year))
    Atlas_Filtered = Atlas_Raw[relevant_columns]
    Atlas_Filtered['YearLabel'] = year

    Atlas_Sets = pd.concat([Atlas_Sets, Atlas_Filtered])