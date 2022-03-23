# NASA Geoweaver
# CMAQ-AI model: Prediction by Voting-XGBoost
print("prediction_xgboost")
# Importing necessary libraries
import pandas as pd
import pickle
from pathlib import Path
from time import sleep

# home directory
home = str(Path.home())
# importing data
final=pd.read_csv(home+'/cmaq/daily_cmaq.csv')
print(final.head())
# defining  testing variables
# processing test data
test_X = final.drop(['YYYYMMDDHH','year'],axis=1)
# load the model from disk
filename = home+'/cmaq/models/xgboost.sav'
#filename = 'D:/Research/CMAQ/local_test/xgboost.sav'
loaded_model = pickle.load(open(filename, 'rb'))

# making prediction
pred = loaded_model.predict(test_X)

# adding prediction values to test dataset
final['prediction'] = pred.tolist()

# saving the dataset into local drive
final.to_csv(home+'/cmaq/prediction_files/prediction_xgboost.csv',index=False)
