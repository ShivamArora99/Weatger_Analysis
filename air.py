import requests
import json


def fetch_details(api_url: str):
    response = requests.get(api_url)
    site_data = response.json()
    return site_data


def fetch_observations_details(payload: json,api_url: str):
    response = requests.post(url=api_url, json=payload)
    if response.status_code ==200:
        data = response.json()
        return data
    else:
        return {"Error" : "Observation not found"}
    






    