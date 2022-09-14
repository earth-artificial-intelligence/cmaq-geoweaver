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


# create_and_clean_folder(f"{cmaq_folder}/prediction_files/")
print("Starting!")
# importing data
# final=pd.read_csv(f"{cmaq_folder}/testing_input_hourly/testing.csv")
testing_path = f'{cmaq_folder}/testing_input_hourly'
all_hourly_files = sorted(glob.glob(os.path.join(testing_path, "test_data_*.csv")))
df_from_each_hourly_file = [pd.read_csv(f) for f in all_hourly_files]

print("reading stations csv")
stations = pd.read_csv(f'{cmaq_folder}/station_cmaq_location.csv')

# load the model from disk
# filename = f'{cmaq_folder}/models/rf_pycaret.sav'

# filename = f'{cmaq_folder}/models/rf_pycaret_o3_only.sav'
# loaded_model = pickle.load(open(filename, 'rb'))
print("reading testing data csv")
# testing_df = pd.read_csv(all_hourly_files[0])

for testing_df in df_from_each_hourly_file:
  print(testing_df['YYYYMMDDHH'].values[0])
  file_dateTime = testing_df['YYYYMMDDHH'].values[0]
  print("copying testing_df to new_df")
  new_df = testing_df.copy()
  new_df.drop(new_df.index, inplace=True)
  print(testing_df.shape, new_df.shape)

#   testing_df['time_of_day'] = (testing_df['hours'] % 24 + 4) // 4

  # Make coords even more coarse by rounding to closest multiple of 5 
  # (e.g., 40, 45, 85, 55)
#   testing_df['Latitude_ExtraCoarse'] = 0.1 * round(testing_df['Latitude']/0.1)
#   testing_df['Longitude_ExtraCoarse'] = 0.1 * round(testing_df['Longitude']/0.1)


  for j, cmaq in testing_df.iterrows():
  
  # To reduce output
    if j % 1000 == 0:
  	  print("Looping through: ", j)

#     start = time.time()
    for i, station in stations.iterrows():
        #print("inner-Looping through: ", i)
        airnow_stations = (station['Latitude_y'], station['Longitude_y'])
        prediction_location = (cmaq['Latitude'], cmaq['Longitude'])
        
        if (station['Latitude_y'] < cmaq['Latitude'] + 0.2) and (station['Latitude_y'] > cmaq['Latitude'] - 0.2) and (station['Longitude_y'] < cmaq['Longitude'] + 0.2) and (station['Longitude_y'] > cmaq['Longitude'] - 0.2):
          new_df.loc[j] = cmaq
          break
#     stop = time.time()
#     duration = stop-start
  #   print(duration)
  new_df.to_csv(f'{cmaq_folder}/prediction_files/update_cell_{file_dateTime}.csv',index=False)
#         dist = distance.distance(airnow_stations, prediction_location).km
#         #             print("Distance: {} KM".format(dist))

#         if dist <= radius:
#           print("{} point is inside the {} km radius from {} coordinate".format(prediction_location, radius, airnow_stations))
#           testing_df.at[j, 'distance'] = dist

#   print(testing_df[testing_df['distance'] <= radius])
#   testing_df = testing_df[testing_df['distance'] <= radius]

#   X = new_df.drop(['YYYYMMDDHH','Latitude','Longitude','CMAQ12KM_NO2(ppb)', 'CMAQ12KM_CO(ppm)', 'CMAQ_OC(ug/m3)', 'CO(moles/s)', 'PRSFC(Pa)', 'PBL(m)', 'TEMP2(K)','WSPD10(m/s)', 'WDIR10(degree)', 'RGRND(W/m2)', 'CFRAC', 'month', 'day', 'hours', 'distance'],axis=1)

# # # making prediction
#   pred = loaded_model.predict(X)

# # adding prediction values to test dataset
#   #testing_df['prediction'] = testing_df['CMAQ12KM_O3(ppb)'].tolist()
#   testing_df['prediction'] = pred

#   testing_df = testing_df[['Latitude', 'Longitude','YYYYMMDDHH','prediction']]
# # saving the dataset into local drive
#   print(f'Saving: {cmaq_folder}/prediction_files/prediction_rf_{file_dateTime}.csv')
#   testing_df.to_csv(f'{cmaq_folder}/prediction_files/prediction_rf_50km_{file_dateTime}.csv',index=False)
