# use trained model to predict on the testing data and save hourly results to prediction_attnRNN_{file_dateTime}.csv

import pandas as pd
import pickle
from pathlib import Path
from time import sleep
import glob, os
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import MinMaxScaler

from cmaq_ai_utils import *

def create_dataset(dataset, look_back=7):
    dataX  = []
    for i in range(len(dataset) - look_back - 1):
        dataX.append(dataset[i:i + look_back])
    return np.array(dataX)

create_and_clean_folder(f"{cmaq_folder}/prediction_files/")

# importing data
# final=pd.read_csv(f"{cmaq_folder}/testing_input_hourly/testing.csv")
print("Reading all test_data files...")
testing_path = f'{cmaq_folder}/testing_input_hourly'
all_hourly_files = glob.glob(os.path.join(testing_path, "test_data_*.csv"))
df_from_each_hourly_file = (pd.read_csv(f) for f in all_hourly_files)
print("Done reading all test_data files!!!")
# load the model from disk
# filename = f'{cmaq_folder}/models/rf_pycaret.sav'
print("Loading Model...")
filename = f'{cmaq_folder}/models/attnRNN_o3_Jul.sav'
loaded_model = pickle.load(open(filename, 'rb'))
print("Loaded Model!!!")

scaler = MinMaxScaler(feature_range=(0, 1))

for testing_df in df_from_each_hourly_file:
  print(testing_df['YYYYMMDDHH'].values[0])
  file_dateTime = testing_df['YYYYMMDDHH'].values[0]
    
  #X = testing_df.drop(['YYYYMMDDHH','Latitude','Longitude'],axis=1)
  testing_df['time_of_day'] = (testing_df['hours'] % 24 + 4) // 4
  
  # Make coords even more coarse by rounding to closest multiple of 5 
  # (e.g., 40, 45, 85, 55)
  #testing_df['Latitude_ExtraCoarse'] = 0.1 * round(testing_df['Latitude']/0.1)
  #testing_df['Longitude_ExtraCoarse'] = 0.1 * round(testing_df['Longitude']/0.1)

  X_features = testing_df.drop(['YYYYMMDDHH','Latitude','Longitude', 'CO(moles/s)'],axis=1)
#   print(X_features.columns)
  
  dataset = X_features.values
  dataset = dataset.astype('float32')

  
#   scaled = scaler.fit_transform(testing_df)
  X = create_dataset(dataset, 7)
#   X = np.reshape(X, (X.shape[0], X.shape[1], 15))

# # making prediction
  pred = loaded_model.predict(X)
  print("PREDICTION VALUE: ", pred[0:5])
#   pred = scaler.inverse_transform(pred)

  # adding prediction values to test dataset
  #testing_df['prediction'] = testing_df['CMAQ12KM_O3(ppb)'].tolist()
  testing_df['prediction'] = pd.Series(pred.flatten())

  testing_df = testing_df[['Latitude', 'Longitude','YYYYMMDDHH','prediction']]
# saving the dataset into local drive
  print(f'Saving: {cmaq_folder}/prediction_files/prediction_attnRNN_{file_dateTime}.csv')
  testing_df.to_csv(f'{cmaq_folder}/prediction_files/prediction_attnRNN_{file_dateTime}.csv',index=False)
