import requests
from datetime import datetime

COVID_API_URL = "https://disease.sh/v3/covid-19/all"

def fetch_covid_data():
    response = requests.get(COVID_API_URL)
    data = response.json()
    return data
