# use the trained model to predict on the testing data and save the results to prediction_rf.csv

import pandas as pd
import pickle
from pathlib import Path
from time import sleep
import glob, os
from sklearn.metrics import r2_score, mean_squared_error
from cmaq_ai_utils import *
import math



def calculate_distance(airnow_station, grid_location):

    dist = math.sqrt( (grid_location[0] - airnow_station[0])**2 + (grid_location[1] - airnow_station[1])**2 )
    return dist
  
  
def match_closest_airnow_with_gridCell(station_distance=0.2):
  """
  Match all airnow stations to closest grid cell.
  """
  print("Starting!")
  testing_path = f'{cmaq_folder}/testing_input_hourly'
  all_hourly_files = sorted(glob.glob(os.path.join(testing_path, "test_data_*.csv")))

  stations = pd.read_csv('/groups/ESS/share/projects/SWUS3km/data/OBS/AirNow/AQF5X/AQF5X_Hourly_2022091304.dat', delimiter=r"\s+", engine='python', skiprows=1, names=['AQSID', 'Latitude', 'Longitude', 'OZONE(ppb)', 'NO2(ppb)', 'CO(ppm)',
       'PM25(ug/m3)', 'SO2(ppb)', 'PM10(ug/m3)'])
  
  stations = stations.replace(',','', regex=True)
  station_locations = stations[['Latitude', 'Longitude']]
  print("reading testing data csv")

  testing_df = pd.read_csv(all_hourly_files[0])
  print(testing_df['YYYYMMDDHH'].values[0])
  
  final_mapping_array = []
  
  for j, cmaq in testing_df.iterrows():
    if j % 1000 == 0:
      print("Looping through: ", j)
      print("Length of final_mapping_array: ", len(final_mapping_array) )
      
    nearest_distance = 9999
    closest_station = []
    
    grid_location = [cmaq['Latitude'], cmaq['Longitude']]

    for i, station in station_locations.iterrows():
      airnow_station = [float(station['Latitude']), float(station['Longitude'])]

      current_dist = calculate_distance(airnow_station, grid_location)

      if nearest_distance > current_dist:
        closest_station = airnow_station
        nearest_distance = current_dist

    print(closest_station, grid_location)
    final_mapping_array.append([closest_station[0], closest_station[1], grid_location[0], grid_location[1]])
  
  closest = pd.DataFrame(final_mapping_array, columns=["Lat_airnow", "Lon_airnow", "Lat_cmaq", "Lon_cmaq"])
  
  
  
  
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
