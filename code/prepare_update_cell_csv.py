# use the trained model to predict on the testing data and save the results to prediction_rf.csv

import pandas as pd
import pickle
from pathlib import Path
from time import sleep
import glob, os
from sklearn.metrics import r2_score, mean_squared_error
from cmaq_ai_utils import *
from scipy import spatial

# from geopy import distance
from math import radians, cos, sin, asin, sqrt
import time


def match_closest_airnow_with_gridCell():
  """
  Match all airnow stations to closest grid cell.
  """
  print("Starting!")
  remove_file(f'{cmaq_folder}/updated_station_to_cell.csv')
  testing_path = f'{cmaq_folder}/testing_input_hourly'
  all_hourly_files = sorted(glob.glob(os.path.join(testing_path, "test_data_*.csv")))
  print("reading stations csv")
  stations = pd.read_csv(f'{cmaq_folder}/AQF5X_Hourly_2022091304.dat', sep=', ', skiprows=1, names=['AQSID', 'Latitude', 'Longitude', 'OZONE(ppb)', 'NO2(ppb)', 'CO(ppm)', 'PM25(ug/m3)', 'SO2(ppb)', 'PM10(ug/m3)'])

  # stations = stations.replace(',','', regex=True)
  print(stations.columns)
  print(stations[['Latitude', 'Longitude']])
  station_locations = stations[['Latitude', 'Longitude']].astype(float).values
  print("station_locations - ", station_locations)
  print("station_locations.shape: ", station_locations.shape)
  print("reading testing data csv")

  testing_df = pd.read_csv(all_hourly_files[0]) # just pick the first one to generate the mapping
  print(testing_df['YYYYMMDDHH'].values[0])

  closest_stations = []
  cmaq_cell_array = []
  final_mapping_array = []
  for j, cmaq in testing_df.iterrows():
    cmaq_location = [cmaq['Latitude'], cmaq['Longitude']]
    cmaq_cell_array.append(cmaq_location)
  
  print("cmaq_cell_array.shape: ", len(cmaq_cell_array))
  
  for station_loc in station_locations:
    distance,index = spatial.KDTree(cmaq_cell_array).query(station_loc)
    if distance > 0.2:
      continue
    closest_cell = cmaq_cell_array[index]
    new_row = [station_loc[0], station_loc[1], closest_cell[0], closest_cell[1]]
    final_mapping_array.append(new_row)

  print("final_mapping_array length: ", len(final_mapping_array))
  closest = pd.DataFrame(final_mapping_array, columns=["Lat_airnow", "Lon_airnow", "Lat_cmaq", "Lon_cmaq"])
  #closest.drop_duplicates().reset_index(drop=True)
  print("Saving fixed_station_cmaq_location.csv...")
  closest.to_csv(f'{cmaq_folder}/updated_station_to_cell.csv',index=False)

  

def prepare_update_grid_cells_with_distance(station_distance=0.2):
  """
  Get all grid cells within the specified distance around airnow stations
  args: station_distance, default: 50km (0.2 degrees)
  """
  print("Starting!")
  testing_path = f'{cmaq_folder}/testing_input_hourly'
  all_hourly_files = sorted(glob.glob(os.path.join(testing_path, "test_data_*.csv")))
  print("reading stations csv")
  airnow_obs_path = '/groups/ESS/share/projects/SWUS3km/data/OBS/AirNow/AQF5X'
  stations = pd.read_csv(f'{cmaq_folder}/station_cmaq_location.csv')
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
    for i, station in stations.iterrows():
      #print("inner-Looping through: ", i)
      airnow_stations = (station['Latitude_y'], station['Longitude_y'])
      prediction_location = (cmaq['Latitude'], cmaq['Longitude'])
        
      if (station['Latitude_y'] < cmaq['Latitude'] + station_distance) and (station['Latitude_y'] > cmaq['Latitude'] - station_distance) and (station['Longitude_y'] < cmaq['Longitude'] + station_distance) and (station['Longitude_y'] > cmaq['Longitude'] - station_distance):
        new_df.loc[j] = cmaq
        break
  new_df.to_csv(f'{cmaq_folder}/prediction_files/update_cell.csv',index=False)

def prepare_update_grid_cells_with_distance(station_distance=0.2):
  """
  Get all grid cells within the specified distance around airnow stations
  args: station_distance, default: 50km (0.2 degrees)
  """
  print("Starting!")
  testing_path = f'{cmaq_folder}/testing_input_hourly'
  all_hourly_files = sorted(glob.glob(os.path.join(testing_path, "test_data_*.csv")))
  print("reading stations csv")
  stations = pd.read_csv(f'{cmaq_folder}/station_cmaq_location.csv')
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
    for i, station in stations.iterrows():
      #print("inner-Looping through: ", i)
      airnow_stations = (station['Latitude_y'], station['Longitude_y'])
      prediction_location = (cmaq['Latitude'], cmaq['Longitude'])
        
      if (station['Latitude_y'] < cmaq['Latitude'] + station_distance) and (station['Latitude_y'] > cmaq['Latitude'] - station_distance) and (station['Longitude_y'] < cmaq['Longitude'] + station_distance) and (station['Longitude_y'] > cmaq['Longitude'] - station_distance):
        new_df.loc[j] = cmaq
        break
  new_df.to_csv(f'{cmaq_folder}/prediction_files/update_cell.csv',index=False)
  
#prepare_update_grid_cells(0.2)
match_closest_airnow_with_gridCell()
