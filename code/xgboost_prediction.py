
# Importing necessary libraries
import pandas as pd
import pickle
from pathlib import Path
from time import sleep

# home directory
home = str(Path.home())
# importing data
final=pd.read_csv(home+'/cmaq/testing.csv')
print(final.head())
X = final.drop(['YYYYMMDDHH','Latitude','Longitude',],axis=1)
# defining  testing variables
# processing test data

# load the model from disk
filename = home+'/cmaq/models/xgboost.sav'
#filename = 'D:/Research/CMAQ/local_test/xgboost.sav'
loaded_model = pickle.load(open(filename, 'rb'))

# making prediction
pred = loaded_model.predict(X)

# adding prediction values to test dataset
final['prediction'] = pred.tolist()

final = final[['Latitude', 'Longitude','YYYYMMDDHH','prediction']]
# saving the dataset into local drive
final.to_csv(home+'/cmaq/prediction_files/prediction_xgboost.csv',index=False)
