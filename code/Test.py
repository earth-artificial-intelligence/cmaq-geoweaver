# use the trained model to predict on the testing data and save the results to prediction_rf.csv

import pandas as pd
import pickle
from pathlib import Path
from time import sleep
import glob
import os
from sklearn.metrics import r2_score, mean_squared_error
from cmaq_ai_utils import *
from sklearn.preprocessing import MinMaxScaler


create_and_clean_folder(f"{cmaq_folder}/prediction_files/")

# scaler = MinMaxScaler(feature_range=(0, 1))

# importing data
# final=pd.read_csv(f"{cmaq_folder}/testing_input_hourly/testing.csv")
# testing_path = '/groups/ESS3/aalnaim/cmaq/testing_input_hourly'
testing_path = '/Users/uhhmed/localCMAQ/testing_input_hourly'
all_hourly_files = glob.glob(os.path.join(testing_path, "test_data_*.csv"))
df_from_each_hourly_file = (pd.read_csv(f) for f in all_hourly_files)

# load the model from disk
# filename = f'{cmaq_folder}/models/rf_pycaret.sav'

filename = f'{cmaq_folder}/models/rf_pycaret_o3_only.sav'
loaded_model = pickle.load(open(filename, 'rb'))

for testing_df in df_from_each_hourly_file:
    #   print(testing_df['YYYYMMDDHH'].values[0])
    file_dateTime = testing_df['YYYYMMDDHH'].values[0]
    # Make coords coarse by removing decimals
#     testing_df['Latitude_coarse'] = round(testing_df['Latitude'])
#     testing_df['Longitude_coarse'] = round(testing_df['Longitude'])
    testing_df['Latitude_Coarse_5_Degree'] = 5 * round(testing_df['Latitude']/5)
    testing_df['Longitude_Coarse_5_Degree'] = 5 * round(testing_df['Longitude']/5)
    # Split time of day into value ranges.
    # Hours 0 - 3 is value 1 (Midnight), 4 - 7 is value 2 (Early Morning), 8 - 11 is value 3 (Morning), 12 - 15 is value 4 (Noon), 16 - 19 is value 5 (Evening), 20 - 23 is value 6 (Night)
    testing_df['time_of_day'] = (testing_df['hours'] % 24 + 4) // 4
    
    X = testing_df.drop(['YYYYMMDDHH', 'Latitude', 'Longitude'], axis=1)
    
#     X[X.columns] = scaler.fit_transform(X)
    
    print("used as inputs: ", X.columns)
# # making prediction
    pred = loaded_model.predict(X)


# adding prediction values to test dataset
    testing_df['prediction'] = pred.tolist()

    testing_df = testing_df[['Latitude',
                             'Longitude', 'YYYYMMDDHH', 'prediction']]
# saving the dataset into local drive
    print(
        f'Saving: {cmaq_folder}/prediction_files/prediction_rf_{file_dateTime}.csv')
    testing_df.to_csv(
        f'{cmaq_folder}/prediction_files/prediction_rf_{file_dateTime}.csv', index=False)

    
  
imp = loaded_model.feature_importances_
feature_names = [i for i in X.columns]
std = np.std([tree.feature_importances_ for tree in loaded_model.estimators_], axis=0)
forest_importances = pd.Series(imp, index=feature_names)

usedInputs = ", ".join(X.columns)

fig, ax = plt.subplots(figsize=(18, 10))
forest_importances.plot.barh(yerr=std, ax=ax)
# ax.set_title("Model Inputs: "+usedInputs, fontsize=14)
fig.suptitle("Feature importances", fontsize=16)
ax.set_xlabel("Mean decrease in impurity")
plt.savefig(cmaq_folder+"/featImp/rf_importance_20220805_Inputs.png")
