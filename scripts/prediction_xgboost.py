# NASA Geoweaver
# CMAQ-AI model: Prediction by Voting-XGBoost
print('running prediction xgboost')
# Importing necessary libraries
import pandas as pd
import pickle
# importing data
final=pd.read_csv('/home/mislam25/cmaq/merged_2020_2021.csv')
#final=pd.read_csv('D:/Research/CMAQ/local_test/merged_2020_2021.csv')

# defining  testing variables
test=final.loc[final['year']==2021]
# processing test data
test_X = test.drop(['AirNOW_O3','Station.ID','YYYYMMDDHH','year','date','dayofyear'],axis=1)
test_y = test['AirNOW_O3']
test_X.head()

# load the model from disk
filename = '/home/mislam25/cmaq/xgboost.sav'
#filename = 'D:/Research/CMAQ/local_test/xgboost.sav'
loaded_model = pickle.load(open(filename, 'rb'))

# making prediction
pred = loaded_model.predict(test_X)

# adding prediction values to test dataset
test['prediction'] = pred.tolist()

# saving the dataset into local drive
test.to_csv('/home/mislam25/cmaq/prediction/prediction_xgboost.csv',index=False)
#test.to_csv('D:/Research/CMAQ/local_test/prediction_xgboost.csv',index=False)
