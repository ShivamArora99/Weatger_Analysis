import json
import streamlit as st
import pandas as pd
import air
import warnings

warnings.filterwarnings("ignore")

SITE_DETAILS_URL = "https://data.airquality.nsw.gov.au/api/Data/get_SiteDetails"
PARAMETER_DETAILS_URL = "https://data.airquality.nsw.gov.au/api/Data/get_ParameterDetails"
OBSERVATIONS_URL = "https://data.airquality.nsw.gov.au/api/Data/get_Observations"




def display_site_info(site_data: json):
    site_df = pd.DataFrame(site_data)
    selected_site_names = st.multiselect("Select Sites",site_df['SiteName'])

    selected_sites = site_df.loc[site_df["SiteName"].isin(selected_site_names), "Site_Id"].tolist()
    return selected_sites


def display_paramter_details(parameter_data: json):
    
    selected_parameter_codes = []
    selected_categories = []
    selected_subcategories = []
    selected_frequencies = []


    selected_parameter_codes = st.multiselect("Select Parameter Code", pd.unique([param["ParameterCode"] for param in parameter_data]))
    selected_categories = st.multiselect("Select Category", pd.unique([param["Category"] for param in parameter_data]))
    selected_subcategories = st.multiselect("Select SubCategory", pd.unique([param["SubCategory"] for param in parameter_data]))
    selected_frequencies = st.multiselect("Select Frequency", pd.unique([param["Frequency"] for param in parameter_data]))
    start_date = st.date_input("Select a start date:")
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = st.date_input("Select an end date:")
    end_date = end_date.strftime("%Y-%m-%d")



    print(selected_parameter_codes)
    print(selected_categories)
    return (selected_parameter_codes,
            selected_categories, selected_subcategories, selected_frequencies, start_date, end_date)


def fetch_observation_payload(selected_sites,selected_parameter_codes,
     selected_categories, selected_subcategories, selected_frequencies,start_date:str, end_date:str):
    
    payload = {
        "Parameters" : selected_parameter_codes,
        "Sites" : selected_sites,
        "StartDate": start_date,
        "EndDate": end_date,
        "Categories":selected_categories,
        "SubCategories": selected_subcategories,
        "Frequency": selected_frequencies
        }
    
    return payload



def main():
    st.title("NSW AIr Quality Dashboard")
    st.subheader("Site Details")

    site_details = air.fetch_details(SITE_DETAILS_URL)
    parameter_data = air.fetch_details(PARAMETER_DETAILS_URL)

    selected_sites =  display_site_info(site_data=site_details)

    (selected_parameter_codes, 
            selected_categories, selected_subcategories, selected_frequencies,start_date, end_date) = display_paramter_details(parameter_data=parameter_data)
    
    payload = fetch_observation_payload(selected_sites,selected_parameter_codes,
     selected_categories, selected_subcategories, selected_frequencies,start_date, end_date)
    print(payload)
    
    data = air.fetch_observations_details(api_url=OBSERVATIONS_URL , payload=payload)
    if st.button("Fetch Data"):
        if data:
            df = pd.json_normalize(data)
            st.write(df)
        else:
            st.write("No Data available for current selection")
    
    if st.button("Save to CSV"):
        if data:
            data_df = pd.json_normalize(data)
            data_df.to_csv("result.csv")
            st.write("Saved")
        else:
            st.warning("Can not save csv without data")

    
    

if __name__ == "__main__":
    main()