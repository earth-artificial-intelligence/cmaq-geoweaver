# NASA GEOWEAVER
# CMAQ-AI Model: Training Voting-XGBoost model

# Importing necessary libraries
import pandas as pd
import sklearn
from numpy import mean
from numpy import std
from sklearn.ensemble import VotingRegressor
from matplotlib import pyplot
from xgboost.sklearn import XGBRegressor

# importing data
final=pd.read_csv('/home/mislam25/cmaq/merged_2020_2021.csv')

# defining training variables
train=final.loc[final['year']==2020]

# Processing training  data
X = train.drop(['AirNOW_O3','Station.ID','YYYYMMDDHH','year','date','dayofyear','datetime'],axis=1)
y = train['AirNOW_O3']

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
filename = '/home/mislam25/cmaq/xgboost.sav'
pickle.dump(ensemble, open(filename, 'wb'))

