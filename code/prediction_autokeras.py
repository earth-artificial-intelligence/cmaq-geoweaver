## NASA GEOWEAVER##
# CMAQ-AI Model: Autokeras prediction
print("prediction_autokeras")
# Importing necessariy libraries
import pandas as pd
import tensorflow as tf
from keras.models import load_model
import autokeras as ak
from time import sleep

# home directory
home = str(Path.home())

# Import processed data
final=pd.read_csv(home+'/cmaq/merged_2020_2021.csv')

# defining and processing testing variables
test=final.loc[final['year']==2022]
test_X = test.drop(['AirNOW_O3','Station.ID','YYYYMMDDHH','year','date','dayofyear'],axis=1)
test_y = test['AirNOW_O3']
text_X=test_X.values.astype('float32')

# load the model from disk
loaded_model =load_model(home+'/cmaq/models/autokeras',custom_objects=ak.CUSTOM_OBJECTS)
#loaded_model =load_model('D:/Research/CMAQ/local_test/autokeras',custom_objects=ak.CUSTOM_OBJECTS)

# Make prediction
pred = loaded_model.predict(test_X)
# adding prediction values to test dataset and save the result
test['prediction'] = pred.tolist()
test['prediction'] = test['prediction'].str.get(0)
test.to_csv(home+'/cmaq/prediction_files/prediction_autokeras.csv',index=False)
