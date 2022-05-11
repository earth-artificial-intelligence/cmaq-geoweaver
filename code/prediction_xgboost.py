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
final=pd.read_csv(home+'/cmaq/merged_2020_2021.csv')

# defining  testing variables
test=final.loc[final['year']==2022]
# processing test data
test_X = test.drop(['AirNOW_O3','Station.ID','YYYYMMDDHH','year','date','dayofyear'],axis=1)
test_y = test['AirNOW_O3']
test_X.head()

# load the model from disk
filename = home+'/cmaq/models/xgboost.sav'
#filename = 'D:/Research/CMAQ/local_test/xgboost.sav'
loaded_model = pickle.load(open(filename, 'rb'))

# making prediction
pred = loaded_model.predict(test_X)

# adding prediction values to test dataset
test['prediction'] = pred.tolist()

# saving the dataset into local drive
test.to_csv(home+'/cmaq/prediction_files/prediction_xgboost.csv',index=False)
sleep(10)
