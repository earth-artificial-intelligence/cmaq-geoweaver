# NASA Geoweaver
# CMAQ-AI Model: Prediction by random forest

# import necessary libraries
import pandas as pd
import pickle
# import data
final=pd.read_csv('/home/mislam25/cmaq/merged_2020_2021.csv')

# defining  and processing test variables
test=final.loc[final['year']==2021]

test_X = test.drop(['AirNOW_O3','Station.ID','YYYYMMDDHH','year','date','dayofyear','datetime'],axis=1)
test_y = test['AirNOW_O3']

# load the model from disk
filename = '/home/mislam25/cmaq/rf.sav'
loaded_model = pickle.load(open(filename, 'rb'))

# making prediction
pred = loaded_model.predict(test_X)

# adding prediction values to test dataset
test['prediction'] = pred.tolist()
test.to_csv('/home/mislam25/cmaq/prediction_rf.csv')
