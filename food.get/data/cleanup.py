from data_extract.data_extract import import_business_license_data

# Stacy changes on 2/4/24
def clean_business_liscense():
    """
    This function cleans the list of the businesses and all their raw data components from the portal

    * Consolidate the data to 'city','license_id','legal_name','doing_business_as_name',
        'application_type', 'license_description','location' 
    * Only keep rows where 'license_description' = "Retail Food Establishment"


    Returns:
        A list of the businesses and all their cleaned data components from the portal
    """
    # may need to think through not calling this function each time?
    liscense_raw_data = import_business_license_data()

    business_liscense_columns = ['city','license_id','legal_name','doing_business_as_name',
                                 'application_type', 'license_description','location' ]
    
    cleaned_business_liscense_data = []

    for business in liscense_raw_data:
        # check if 'license_description' is "Retail Food Establishment"
        if business.get('license_description') == "Retail Food Establishment":
            # Create a dictionary with only the desired columns
            cleaned_business = {column: business.get(column) for column in business_liscense_columns}
            cleaned_business_liscense_data.append(cleaned_business)

    return cleaned_business_liscense_data

def clean_snap_retailer_data():
    """
    This function cleans the dictionary of the snap retailers and all their raw data components from the portal

    * Consolidate the data to be only a list or relevant dictionary elements
    * Only keep rows where 'City' = "Chicago" and 'State' = "IL"


    Returns:
        A list of the businesses and all their cleaned data components from the portal
    """
    # may need to think through not calling this function each time?
    snap_raw_data = import_business_license_data()
    # extracting the 'features' key and converting it to a list
    snap_retailer_list = snap_raw_data.get('features', [])

    # extracting attributes from each entry in snap_retailer_list
    cleaned_snap_retailer_data = []

    for retailer_entry in snap_retailer_list:
        # access the 'attributes' key within each entry
        attributes = retailer_entry.get('attributes', {})

        # check if lowercase 'City' is 'chicago' and 'State' is 'IL'
        if attributes.get('City', '').lower() == 'chicago' and attributes.get('State', '').upper() == 'IL':
        # append the attributes dictionary to the result list
            cleaned_snap_retailer_data.append(attributes)
    
    return cleaned_snap_retailer_data