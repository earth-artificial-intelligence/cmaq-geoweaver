## NASA GEOWEAVER##
# CMAQ-AI Model: Autokeras prediction

###########################
# Chck required packages
# If required packages are present, install it
##########################

print('running predicion autokeras')
# Importing necessariy libraries
import pandas as pd
import tensorflow as tf
from keras.models import load_model
import autokeras as ak

# create HOPPER job salloc command
#subprocess.run(["salloc", "-p", "gpuq", "-q", "gpu", "--ntasks-per-node=1", "--gres=gpu:A100.40gb:1", "-t", "0-00:10:00" ])

# Import processed data
final=pd.read_csv('/home/mislam25/cmaq/merged_2020_2021.csv')
#final=pd.read_csv('D:/Research/CMAQ/local_test/merged_2020_2021.csv')

# defining and processing testing variables
test=final.loc[final['year']==2021]
test_X = test.drop(['AirNOW_O3','Station.ID','YYYYMMDDHH','year','date','dayofyear'],axis=1)
test_y = test['AirNOW_O3']
text_X=test_X.values.astype('float32')

# load the model from disk
loaded_model =load_model('/home/mislam25/cmaq/autokeras',custom_objects=ak.CUSTOM_OBJECTS)
#loaded_model =load_model('D:/Research/CMAQ/local_test/autokeras',custom_objects=ak.CUSTOM_OBJECTS)

# Make prediction
pred = loaded_model.predict(test_X)
# adding prediction values to test dataset and save the result
test['prediction'] = pred.tolist()
test['prediction'] = test['prediction'].str.get(0)
test.to_csv('/home/mislam25/cmaq/prediction/prediction_autokeras.csv',index=False)
#test.to_csv('D:/Research/CMAQ/local_test/prediction_autokeras.csv',index=False)
