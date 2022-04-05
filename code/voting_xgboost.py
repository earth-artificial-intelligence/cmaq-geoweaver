# NASA GEOWEAVER
# CMAQ-AI Model: Training Voting-XGBoost model

# Importing necessary libraries
import pandas as pd
import sklearn
from sklearn.ensemble import VotingRegressor
from xgboost.sklearn import XGBRegressor
import pickle
from pathlib import Path

# home directory
home = str(Path.home())

# importing data
final=pd.read_csv(home+'/cmaq/training.csv')

final=final.dropna()

# Processing training  data
X = final.drop(['AirNOW_O3'],axis=1)
y = final['AirNOW_O3']

# Defining voting-ensemble based xgboost model
models = list()
models.append(('cart1', XGBRegressor(max_depth=1)))
models.append(('cart2', XGBRegressor(max_depth=2)))
models.append(('cart3', XGBRegressor(max_depth=3)))
models.append(('cart4', XGBRegressor(max_depth=4)))
models.append(('cart5', XGBRegressor(max_depth=5)))
models.append(('cart6', XGBRegressor(max_depth=6)))
# define the voting ensemble
ensemble = VotingRegressor(estimators=models)

# fit the model on all available data
ensemble.fit(X, y)

# save the model to disk
filename = home+'/cmaq/models/xgboost.sav'
#filename = 'D:/Research/CMAQ/local_test/xgboost.sav'
pickle.dump(ensemble, open(filename, 'wb'))

