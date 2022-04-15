# NASA Geoweaver
# CMAQ-AI Model: Autokeras for Automated-Deep Learning
print("training_autokeras")
# Importing necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from autokeras import StructuredDataRegressor
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import tensorflow as tf
from pathlib import Path
from time import sleep

# home directory
home = str(Path.home())

# load dataset
final=pd.read_csv(home+'/cmaq/merged_2020_2021.csv')

# defining training variables
train=final.loc[final['year']==2022]

# processing training  data
X = train.drop(['AirNOW_O3','Station.ID','YYYYMMDDHH','year','date','dayofyear'],axis=1)
y = train['AirNOW_O3']
X.head()
X=X.values.astype('float32')
y=y.values.astype('float32')

# load dataset
# separate into train and test sets
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=1)
#print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
# define the search
search = StructuredDataRegressor(max_trials=15, loss='mean_absolute_error')
# perform the search
#search.fit(x=X_train, y=y_train, verbose=0)
search.fit(x=X, y=y, verbose=0)
# evaluate the model
#mae, _ = search.evaluate(X_test, y_test, verbose=0)
#print('MAE: %.3f' % mae)
# use the model to make a prediction
#X_new = asarray([[108]]).astype('float32')
#yhat = search.predict(X_new)
#print('Predicted: %.3f' % yhat[0])
# get the best performing model
model = search.export_model()
# summarize the loaded model
model.summary()
print(search)
# save the best performing model to file
model.save(home+'/cmaq/models/autokeras',save_format="tf")
sleep(10)

