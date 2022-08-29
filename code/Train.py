# Write first python in Geoweaver# NASA GEOWEAVER
# CMAQ-AI Model: Training Voting-XGBoost model

# Importing necessary libraries
import pandas as pd
# import sklearn
from sklearn.ensemble import RandomForestRegressor
# from xgboost.sklearn import XGBRegressor
import pickle
from cmaq_ai_utils import *

from sklearn.preprocessing import MinMaxScaler

# importing data
# final = pd.read_csv('/groups/ESS3/aalnaim/cmaq/training.csv')
final = pd.read_csv('/Users/uhhmed/localCMAQ/training.csv')
print(final.head())
final = final.dropna()

# Initialize a normalizer
# scaler = MinMaxScaler(feature_range=(0, 1))
# final[final.columns] = scaler.fit_transform(final)

# Make coords coarse by removing decimals
# final['Latitude_coarse'] = round(final['Latitude'])
# final['Longitude_coarse'] = round(final['Longitude'])

# Split time of day into value ranges.
# Hours 0 - 3 is value 1 (Midnight), 4 - 7 is value 2 (Early Morning), 8 - 11 is value 3 (Morning), 12 - 15 is value 4 (Noon), 16 - 19 is value 5 (Evening), 20 - 23 is value 6 (Night)
final['time_of_day'] = (final['hours'] % 24 + 4) // 4

# Make coords even more coarse by rounding to closest multiple of 5 
# (e.g., 40, 45, 85, 55)
final['Latitude_Coarse_5_Degree'] = 5 * round(final['Latitude']/5)
final['Longitude_Coarse_5_Degree'] = 5 * round(final['Longitude']/5)

create_and_clean_folder(f"{cmaq_folder}/models/")

# Processing training  data
X = final.drop(['AirNOW_O3', 'Latitude', 'Longitude'], axis=1)
print("input shape:", X.shape)
y = final['AirNOW_O3']
print("used as inputs: ", X.columns)
rf = RandomForestRegressor(bootstrap=False, ccp_alpha=0.0, criterion='mse',
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

