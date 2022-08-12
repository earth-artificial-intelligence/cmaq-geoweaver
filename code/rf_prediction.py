# use the trained model to predict on the testing data and save the results to prediction_rf.csv

import pandas as pd
import pickle
from pathlib import Path
from time import sleep
import glob, os
from sklearn.metrics import r2_score, mean_squared_error
from cmaq_ai_utils import *

# importing data
final=pd.read_csv(f"{cmaq_folder}/testing_input_hourly/testing.csv")
print(final.head())
X = final.drop(['YYYYMMDDHH','Latitude','Longitude',],axis=1)
y= final['CMAQ12KM_O3(ppb)']
# defining  testing variables
# processing test data

# load the model from disk
filename = f'{cmaq_folder}/models/rf_pycaret.sav'
#filename = 'D:/Research/CMAQ/local_test/xgboost.sav'
loaded_model = pickle.load(open(filename, 'rb'))

# making prediction
pred = loaded_model.predict(X)

# adding prediction values to test dataset
final['prediction'] = pred.tolist()

final = final[['Latitude', 'Longitude','YYYYMMDDHH','prediction']]
# saving the dataset into local drive
create_and_clean_folder(f"{cmaq_folder}/prediction_files/")
final.to_csv(f'{cmaq_folder}/prediction_files/prediction_rf.csv',index=False)


