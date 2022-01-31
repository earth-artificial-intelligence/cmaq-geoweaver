# Write first python in Geoweaver
import sys
import subprocess
import pkg_resources

# Required packages to run this process.
required = {'pandas','sklearn','xgboost','numpy','matplotlib','pathlib'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    print("Packages missing and will be installed: ", missing)
    python = sys.executable
    subprocess.check_call(
        [python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

################################
#  END OF PACKAGES VALIDATION  #
# Importing data
import os
from pathlib import Path
import pandas as pd
home = str(Path.home())
final=pd.read_csv(f'{home}/Geoweaver/merged_2020_2021.csv')

# defining training and testing variables
train=final.loc[final['year']==2020]
test=final.loc[final['year']==2021]

# processing training  data
X = train.drop(['AirNOW_O3','Station.ID','YYYYMMDDHH','year','date','dayofyear','datetime'],axis=1)
y = train['AirNOW_O3']
X.head()

# processing test data
test_X = test.drop(['AirNOW_O3','Station.ID','YYYYMMDDHH','year','date','dayofyear','datetime'],axis=1)
test_y = test['AirNOW_O3']
test_X.head()


## Voting XGBoost
import sklearn
from numpy import mean
from numpy import std
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import VotingRegressor
from matplotlib import pyplot
from xgboost.sklearn import XGBRegressor


# define the base models
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

# prediction
pred = ensemble.predict(test_X)
# adding prediction values to test dataset
test['prediction'] = pred.tolist()

test.to_csv(f'{home}/Geoweaver/prediction_xgboost.csv')
