# use the trained model to predict on the testing data and save the results to prediction_rf.csv

import pandas as pd
import pickle
from pathlib import Path
from time import sleep
import glob, os
from sklearn.metrics import r2_score, mean_squared_error
from cmaq_ai_utils import *

# from geopy import distance
from math import radians, cos, sin, asin, sqrt
import time


def prepare_update_grid_cells(station_distance=0.2):
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
  
prepare_update_grid_cells(0.2)
