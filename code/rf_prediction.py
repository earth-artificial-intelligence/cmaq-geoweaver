# use the trained model to predict on the testing data and save the results to prediction_rf.csv

import pandas as pd
import pickle
from pathlib import Path
from time import sleep
import os
from sklearn.metrics import r2_score, mean_squared_error
from cmaq_ai_utils import *

print("create and clean the prediction folder")
create_and_clean_folder(f"{cmaq_folder}/prediction_files/")

# importing data
# final=pd.read_csv(f"{cmaq_folder}/testing_input_hourly/testing.csv")
testing_path = f'{cmaq_folder}/testing_input_hourly'
#all_hourly_files = glob.glob(os.path.join(testing_path, "test_data_*.csv"))
#df_from_each_hourly_file = (pd.read_csv(f) for f in all_hourly_files)

# load the model from disk
# filename = f'{cmaq_folder}/models/rf_pycaret.sav'

print("start to load model")

filename = f'{model_folder}/rf_pycaret_o3_one_year_good.sav'
loaded_model = pickle.load(open(filename, 'rb'))

print("model is loaded")

#for testing_df in df_from_each_hourly_file:
file_list = os.listdir(testing_path)

# Initialize a flag to indicate if the final CSV file needs a header
write_header = True

for file_name in file_list:
    if file_name.endswith('.csv') and file_name.startswith('test_data_'):  # Adjust the file extension as needed
      print(f"adding {file_name}")
      testing_df = pd.read_csv(f)
      # Perform any desired data processing on 'df' here
      # dropping unnecessary variables
      testing_df['YYYYMMDDHH'] = testing_df['YYYYMMDDHH'].map(str)
      testing_df['month'] = testing_df['YYYYMMDDHH'].str[4:6]
      testing_df['day'] = testing_df['YYYYMMDDHH'].str[6:8]
      testing_df['hours'] = testing_df['YYYYMMDDHH'].str[8:10]

      #print(testing_df['YYYYMMDDHH'].values[0])
      file_dateTime = testing_df['YYYYMMDDHH'].values[0]
      #X = testing_df.drop(['YYYYMMDDHH','Latitude','Longitude'],axis=1)
      testing_df['time_of_day'] = (testing_df['hours'] % 24 + 4) // 4

      # Make coords even more coarse by rounding to closest multiple of 5 
      # (e.g., 40, 45, 85, 55)
      #testing_df['Latitude_ExtraCoarse'] = 0.1 * round(testing_df['Latitude']/0.1)
      #testing_df['Longitude_ExtraCoarse'] = 0.1 * round(testing_df['Longitude']/0.1)
      X = testing_df.drop(['YYYYMMDDHH','Latitude','Longitude', 'CO(moles/s)'],axis=1)

      #print(X.columns)

      # # making prediction
      pred = loaded_model.predict(X)

      # adding prediction values to test dataset
      #testing_df['prediction'] = testing_df['CMAQ12KM_O3(ppb)'].tolist()
      testing_df['prediction'] = pred

      testing_df = testing_df[['Latitude', 'Longitude','YYYYMMDDHH','prediction']]
      # saving the dataset into local drive
      print(f'Saving: {cmaq_folder}/prediction_files/prediction_rf_{file_dateTime}.csv')
      testing_df.to_csv(f'{cmaq_folder}/prediction_files/prediction_rf_{file_dateTime}.csv',index=False)
        
print("Prediction is all done.")
