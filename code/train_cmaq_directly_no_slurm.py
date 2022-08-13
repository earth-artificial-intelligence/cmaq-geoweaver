# Write first python in Geoweaver# NASA GEOWEAVER
# CMAQ-AI Model: Training Voting-XGBoost model

# Importing necessary libraries
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestRegressor
from xgboost.sklearn import XGBRegressor
import pickle
from cmaq_ai_utils import *

# importing data
final=pd.read_csv(f'{cmaq_folder}/training.csv')
print(final.head())
final=final.dropna()

create_and_clean_folder(f"{cmaq_folder}/models/")

# Processing training  data
X = final.drop(['AirNOW_O3','Latitude_x','Longitude_x','CMAQ12KM_NO2(ppb)', 'CMAQ12KM_CO(ppm)', 'CMAQ_OC(ug/m3)', 'CO(moles/s)', 'PRSFC(Pa)', 'PBL(m)', 'TEMP2(K)','WSPD10(m/s)', 'WDIR10(degree)', 'RGRND(W/m2)', 'CFRAC', 'month', 'day', 'hours'],axis=1)
print("input shape:", X.shape)
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
filename = f'{cmaq_folder}/models/rf_pycaret_o3_only.sav'
#filename = 'D:/Research/CMAQ/local_test/xgboost.sav'
pickle.dump(rf, open(filename, 'wb'))
