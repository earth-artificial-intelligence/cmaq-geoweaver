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
colnames=["Latitude_x","Longitude_x","CMAQ12KM_O3(ppb)","CMAQ12KM_NO2(ppb)","CMAQ12KM_CO(ppm)","CMAQ_OC(ug/m3)","PRSFC(Pa)","PBL(m)","TEMP2(K)","WSPD10(m/s)","WDIR10(degree)","RGRND(W/m2)","CFRAC","month","day","hours","Lat_airnow","Lon_airnow","Lat_cmaq","Lon_cmaq","StationID","Latitude_y","Longitude_y","AirNOW_O3"]
final=pd.read_csv(f'{cmaq_folder}/training_one_year.csv', names=colnames, header=None)
print(final.head())
final=final.dropna()
#print("shape before: ", final.shape)
#final = final.loc[(final['CMAQ12KM_O3(ppb)']-final['AirNOW_O3'])/final['AirNOW_O3']<0.05]
#print("shape 1 after: ", final.shape)
#final = final.loc[(final['CMAQ12KM_O3(ppb)']-final['AirNOW_O3'])/final['AirNOW_O3']>-0.05]
#print("shape 2 after: ", final.shape)

final['time_of_day'] = (final['hours'] % 24 + 4) // 4

# Make coords even more coarse by rounding to closest multiple of 5
# (e.g., 40, 45, 85, 55)
#final['Latitude_ExtraCoarse'] = 0.1 * round(final['Latitude_x']/0.1)
#final['Longitude_ExtraCoarse'] = 0.1 * round(final['Longitude_x']/0.1)



create_and_clean_folder(f"{cmaq_folder}/models/")

# Processing training  data
X = final.drop(['AirNOW_O3','Latitude_x','Longitude_x','Lat_airnow','Lon_airnow', 'Lat_cmaq', 'Lon_cmaq', 'Latitude_y', 'Longitude_y', 'StationID'],axis=1)
print("input shape:", X.shape)
print("input variables: ", X.columns)
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
filename = f'{cmaq_folder}/models/rf_pycaret_o3_one_year_1.5g.sav'
#filename = 'D:/Research/CMAQ/local_test/xgboost.sav'
pickle.dump(rf, open(filename, 'wb'))
print(f"Model is trained and saved to {filename}")
