# use the trained model to predict on the testing data and save the results to prediction_rf.csv

import pandas as pd
import pickle
from pathlib import Path
from time import sleep
import glob, os
from sklearn.metrics import r2_score, mean_squared_error
from cmaq_ai_utils import cmaq_folder

# from geopy import distance
from math import radians, cos, sin, asin, sqrt
import time

print(pd.__version__)
print(np.__version__)
def match_closest_airnow_with_gridCell():
  """
  Match all airnow stations to closest grid cell.
  """
  print("Starting!")
  testing_path = f'{cmaq_folder}/testing_input_hourly'
  all_hourly_files = sorted(glob.glob(os.path.join(testing_path, "test_data_*.csv")))
  print("reading stations csv")
#   stations = pd.read_csv(f'{cmaq_folder}/station_cmaq_location.csv')
  stations = pd.read_csv('/groups/ESS/share/projects/SWUS3km/data/OBS/AirNow/AQF5X/AQF5X_Hourly_2022091304.dat', delimiter=r"\s+", engine='python', skiprows=1, names=['AQSID', 'Latitude', 'Longitude', 'OZONE(ppb)', 'NO2(ppb)', 'CO(ppm)',
       'PM25(ug/m3)', 'SO2(ppb)', 'PM10(ug/m3)'])
  
  stations = stations.replace(',','', regex=True)
  print(stations.columns)
  station_locations = stations[['Latitude', 'Longitude']].astype(float).values
  print("reading testing data csv")

  testing_df = pd.read_csv(all_hourly_files[0])
  print(testing_df['YYYYMMDDHH'].values[0])

  closest_stations = []
  
  cmaq_station_array = np.array([[testing_df['Latitude'][0],testing_df['Longitude'][0]]]*2920)
  
  for j, cmaq in testing_df.iterrows():
    if j % 1000 == 0:
  	  print("Looping through: ", j)
    if j >= 100:
      break
      
    cmaq_location = [cmaq['Latitude'], cmaq['Longitude']]
#     cmaq_station_array = np.array([[cmaq_location[0],cmaq_location[1]]]*2920)

    distances = np.linalg.norm(station_locations-cmaq_station_array, axis=1)
    min_index = np.argmin(distances)

    print(distances)
    closest_stations.append(station_locations[min_index])
       
  closest = pd.DataFrame(closest_stations, columns=['Latitude', 'Longitude'])
  closest.drop_duplicates().reset_index(drop=True)
  print("Saving fixed_station_cmaq_location.csv...")
#   closest.to_csv(f'{cmaq_folder}/fixed_station_cmaq_location.csv',index=False)

def prepare_update_grid_cells(station_distance=0.2):
  """
  Get all grid cells within the specified distance around airnow stations
  args: station_distance, default: 50km (0.2 degrees)
  """
  print("Starting!")
  testing_path = f'{cmaq_folder}/testing_input_hourly'
  all_hourly_files = sorted(glob.glob(os.path.join(testing_path, "test_data_*.csv")))
  print("reading stations csv")
#   stations = pd.read_csv(f'{cmaq_folder}/fixed_station_cmaq_location.csv')
  stations = pd.read_csv('/groups/ESS/share/projects/SWUS3km/data/OBS/AirNow/AQF5X/AQF5X_Hourly_2022091304.dat', delimiter=r"\s+", engine='python', skiprows=1, names=['AQSID', 'Latitude', 'Longitude', 'OZONE(ppb)', 'NO2(ppb)', 'CO(ppm)',
       'PM25(ug/m3)', 'SO2(ppb)', 'PM10(ug/m3)'])
  
  stations = stations.replace(',','', regex=True)
  station_locations = stations[['Latitude', 'Longitude']].astype(float)
  print("reading testing data csv")

  testing_df = pd.read_csv(all_hourly_files[0])
  print(testing_df['YYYYMMDDHH'].values[0])
  file_dateTime = testing_df['YYYYMMDDHH'].values[0]
  print("copying testing_df to new_df")
  new_df = testing_df.copy()
  new_df.drop(new_df.index, inplace=True)
  print(testing_df.shape, new_df.shape)

  for j, cmaq in testing_df.iterrows():
    if j % 1000 == 0:
  	  print("Looping through: ", j)
    for i, station in station_locations.iterrows():
      #print("inner-Looping through: ", i)
      airnow_stations = (station['Latitude'], station['Longitude'])
      prediction_location = (cmaq['Latitude'], cmaq['Longitude'])
        
      if (station['Latitude'] < cmaq['Latitude'] + station_distance) and (station['Latitude'] > cmaq['Latitude'] - station_distance) and (station['Longitude'] < cmaq['Longitude'] + station_distance) and (station['Longitude'] > cmaq['Longitude'] - station_distance):
        new_df.loc[j] = cmaq
        break
  new_df.to_csv(f'{cmaq_folder}/grid_cells/fixed_update_cell.csv',index=False)
  
# prepare_update_grid_cells(0.2)
match_closest_airnow_with_gridCell()
