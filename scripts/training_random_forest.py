# NASA Geoweaver
# CMAQ-AI Model: Voting-Random Forest

# Importing necessary libraries
print('running training rf')
import pandas as pd
## Voting XGBoost
import sklearn
from sklearn.ensemble import VotingRegressor
from sklearn.ensemble import RandomForestRegressor
import pickle


# importing data
final=pd.read_csv('/home/mislam25/cmaq/merged_2020_2021.csv')
#final=pd.read_csv('D:/Research/CMAQ/local_test/merged_2020_2021.csv')
# defining training variables
train=final.loc[final['year']==2020]

# Processing training  data
X = train.drop(['AirNOW_O3','Station.ID','YYYYMMDDHH','year','date','dayofyear'],axis=1)
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
#filename = 'D:/Research/CMAQ/local_test/rf.sav'
pickle.dump(ensemble, open(filename, 'wb'))

