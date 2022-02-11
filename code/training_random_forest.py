# NASA Geoweaver
# CMAQ-AI Model: Voting-Random Forest

# Importing necessary libraries

import pandas as pd
## Voting XGBoost
import sklearn
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold
from sklearn.ensemble import VotingRegressor
from sklearn.ensemble import RandomForestRegressor

# import data
final=pd.read_csv('/home/mislam25/cmaq/merged_2020_2021.csv')

# defining and processing training variables
train=final.loc[final['year']==2020]

X = train.drop(['AirNOW_O3','Station.ID','YYYYMMDDHH','year','date','dayofyear','datetime'],axis=1)
y = train['AirNOW_O3']

# define the voting-random forest model
models = list()
models.append(('cart1', RandomForestRegressor(max_depth=1)))
models.append(('cart2', RandomForestRegressor(max_depth=2)))
models.append(('cart3', RandomForestRegressor(max_depth=3)))
models.append(('cart4', RandomForestRegressor(max_depth=4)))
models.append(('cart5', RandomForestRegressor(max_depth=5)))
models.append(('cart6', RandomForestRegressor(max_depth=6)))
# define the voting ensemble
ensemble = VotingRegressor(estimators=models)

# fit the model on all available data
ensemble.fit(X, y)

# save the model to disk
filename = '/home/mislam25/cmaq/rf.sav'
pickle.dump(ensemble, open(filename, 'wb'))

