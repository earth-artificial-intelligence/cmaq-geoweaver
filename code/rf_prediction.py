
# Importing necessary libraries
import pandas as pd
import pickle
from pathlib import Path
from time import sleep
import glob, os
from sklearn.metrics import r2_score, mean_squared_error

# home directory
home = str(Path.home())
# importing data
final=pd.read_csv("/groups/ESS/aalnaim/cmaq/input_hourly/testing.csv")
print(final.head())
X = final.drop(['YYYYMMDDHH','Latitude','Longitude',],axis=1)
y= final['CMAQ12KM_O3(ppb)']
# defining  testing variables
# processing test data

# load the model from disk
filename = '/groups/ESS/aalnaim/cmaq/models/rf_from_hourly_aug3.sav'
#filename = 'D:/Research/CMAQ/local_test/xgboost.sav'
loaded_model = pickle.load(open(filename, 'rb'))

# making prediction
pred = loaded_model.predict(X)
print(r2_score(y, pred))
print(mean_squared_error(y, pred))
# adding prediction values to test dataset
final['prediction'] = pred.tolist()

final = final[['Latitude', 'Longitude','YYYYMMDDHH','prediction']]
# saving the dataset into local drive
final.to_csv('/groups/ESS/aalnaim/cmaq/prediction_files/prediction_rf.csv',index=False)
