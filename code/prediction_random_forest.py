# NASA Geoweaver
# CMAQ-AI Model: Prediction by random forest
print("predictin_rf")
# import necessary libraries
import pandas as pd
import pickle
from pathlib import Path

# home directory
home = str(Path.home())
# import data
final=pd.read_csv(home+'/cmaq/merged_2020_2021.csv')

# defining  and processing test variables
test=final.loc[final['year']==2022]

test_X = test.drop(['AirNOW_O3','Station.ID','YYYYMMDDHH','year','date','dayofyear'],axis=1)
test_y = test['AirNOW_O3']

# load the model from disk
filename = home+'/cmaq/models/rf.sav'
#filename = 'D:/Research/CMAQ/local_test/rf.sav'
loaded_model = pickle.load(open(filename, 'rb'))

# making prediction
pred = loaded_model.predict(test_X)

# adding prediction values to test dataset
test['prediction'] = pred.tolist()
test.to_csv(home+'/cmaq/prediction_files/prediction_rf.csv',index=False)
