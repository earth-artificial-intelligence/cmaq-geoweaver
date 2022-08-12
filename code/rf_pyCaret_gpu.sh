# Write first python in Geoweaver# NASA GEOWEAVER
# CMAQ-AI Model: Training Voting-XGBoost model

# Importing necessary libraries
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestRegressor
from xgboost.sklearn import XGBRegressor
import pickle
from pathlib import Path

# home directory
home = str(Path.home())

# importing data
final=pd.read_csv('/groups/ESS/zsun/cmaq/training.csv')
print(final.head())
final=final.dropna()

# Processing training  data
X = final.drop(['AirNOW_O3','Latitude_x','Longitude_x'],axis=1)
y = final['AirNOW_O3']

rf = RandomForestRegressor(bootstrap=True, ccp_alpha=0.0, criterion='mse',
                      max_depth=None, max_features='auto', max_leaf_nodes=None,
                      max_samples=None, min_impurity_decrease=0.0,
                      min_samples_leaf=1,
                      min_samples_split=2, min_weight_fraction_leaf=0.0,
                      n_estimators=100, n_jobs=-1, oob_score=False,
                      random_state=3086, verbose=0, warm_start=False)

rf.fit(X, y)

# save the model to disk
filename = '/groups/ESS/zsun/cmaq/models/rf_from_hourly_fixed.sav'=
#filename = 'D:/Research/CMAQ/local_test/xgboost.sav'
pickle.dump(rf, open(filename, 'wb'))
