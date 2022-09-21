# use the trained model to predict on the testing data and save the results to prediction_rf.csv

import pandas as pd
import pickle
from pathlib import Path
from time import sleep
import glob, os
from sklearn.metrics import r2_score, mean_squared_error
from cmaq_ai_utils import *

create_and_clean_folder(f"{cmaq_folder}/prediction_files/")

# importing data
# final=pd.read_csv(f"{cmaq_folder}/testing_input_hourly/testing.csv")
testing_path = f'{cmaq_folder}/testing_input_hourly'
all_hourly_files = glob.glob(os.path.join(testing_path, "test_data_*.csv"))
df_from_each_hourly_file = (pd.read_csv(f) for f in all_hourly_files)

# load the model from disk
# filename = f'{cmaq_folder}/models/rf_pycaret.sav'

filename = f'{cmaq_folder}/models/rf_pycaret_o3_new_matched.sav'
loaded_model = pickle.load(open(filename, 'rb'))

for testing_df in df_from_each_hourly_file:
  print(testing_df['YYYYMMDDHH'].values[0])
  file_dateTime = testing_df['YYYYMMDDHH'].values[0]
  #X = testing_df.drop(['YYYYMMDDHH','Latitude','Longitude'],axis=1)
  testing_df['time_of_day'] = (testing_df['hours'] % 24 + 4) // 4

  # Make coords even more coarse by rounding to closest multiple of 5 
  # (e.g., 40, 45, 85, 55)
  #testing_df['Latitude_ExtraCoarse'] = 0.1 * round(testing_df['Latitude']/0.1)
  #testing_df['Longitude_ExtraCoarse'] = 0.1 * round(testing_df['Longitude']/0.1)
  X = testing_df.drop(['YYYYMMDDHH','Latitude','Longitude',],axis=1)

# # making prediction
  pred = loaded_model.predict(X)

# adding prediction values to test dataset
  #testing_df['prediction'] = testing_df['CMAQ12KM_O3(ppb)'].tolist()
  testing_df['prediction'] = pred

  testing_df = testing_df[['Latitude', 'Longitude','YYYYMMDDHH','prediction']]
# saving the dataset into local drive
  print(f'Saving: {cmaq_folder}/prediction_files/prediction_rf_{file_dateTime}.csv')
  testing_df.to_csv(f'{cmaq_folder}/prediction_files/prediction_rf_{file_dateTime}.csv',index=False)
