from pyairnow.conv import aqi_to_concentration
import pandas as pd
import requests
import json


lat = '32.047501'
lon = '-110.773903'
API_KEY = '9FF8FB8B-229C-424F-8882-3AF164DD8C17'

# distance is used when no reporting area is associated with the latitude/longitude, 
# looks for an observation from a nearby reporting area within this distance (in miles).
distance = '50' 

# Construct a list of date string, each timed at midnight.
date_range_str = [date.strftime('%Y-%m-%dT00-0000') for date in pd.date_range('2017-01-01','2017-02-28')]

# An empty list to save the O3 data returned.
O3_data = []
CO_data = []
NO2_data = []

# Loop through each date to intiate an API call for the duration specified above.
for dateStr in date_range_str:

    # Construct URL to contact airnowapi.org and get the AQI (Air Quality Index) for our desired location.
    url = f'https://www.airnowapi.org/aq/observation/latLong/historical/?format=application/json&latitude={lat}&longitude={lon}&date={dateStr}&distance={distance}&API_KEY={API_KEY}'

    # Initiate the request to the API.
    res = requests.get(url)
    # Extract the AQI level for our location.
    aqiData = json.loads(res.content)[0]['AQI']

    # This function can be passed the AQI observations 
    # and return the corresponding O3 level in that area for the day.
    O3_data.append(aqi_to_concentration(aqiData, 'O3'))
    CO_data.append(aqi_to_concentration(aqiData, 'CO'))
    NO2_data.append(aqi_to_concentration(aqiData, 'NO2'))

pd.DataFrame({"Date": date_range_str, "Lat": lat, "Lon": lon, "AirNow_O3": O3_data, "AirNow_CO": CO_data, "AirNow_NO2": NO2_data}).to_csv("/Users/uhhmed/Desktop/CMAQ_Ch15_bookCode/airnow_data.csv", index=False)

