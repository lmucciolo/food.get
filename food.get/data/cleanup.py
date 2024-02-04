from data_extract import import_business_license_data

# Stacy changes on 2/4/24
def clean_business_liscense():
    """
    This function should clean the list of the businesses and all their raw data components from the portal

    * Consolidate the data to 'city','license_id','legal_name','doing_business_as_name',
        'application_type', 'license_description','location' 
    * Only keep rows where 'license_description' = "Retail Food Establishment"


    Returns:
        A list of the businesses and all their cleaned data components from the portal
    """
    # may need to think through not calling this function each time?
    raw_data = import_business_license_data()

    business_liscense_columns = ['city','license_id','legal_name','doing_business_as_name',
                                 'application_type', 'license_description','location' ]
    
    cleaned_business_liscense_data = []

    for business in raw_data:
        # check if 'license_description' is "Retail Food Establishment"
        if business.get('license_description') == "Retail Food Establishment":
            # Create a dictionary with only the desired columns
            cleaned_business = {column: business.get(column) for column in business_liscense_columns}
            cleaned_business_liscense_data.append(cleaned_business)

    return cleaned_business_liscense_data