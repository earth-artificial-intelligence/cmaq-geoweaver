
import numpy as np
import pandas as pd
from keras import Model
from keras.layers import Layer
import keras.backend as K
from keras.layers import Input, Dense, SimpleRNN
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from sklearn import metrics
import tensorflow as tf
import pickle

from cmaq_ai_utils import *

training_df = pd.read_csv(f'{cmaq_folder}/training_Jul_New.csv')
training_df = training_df.drop([
    'Latitude_x',
    'Longitude_x',
    'Lat_airnow',
    'Lon_airnow',
    'Lat_cmaq',
    'Lon_cmaq',
    'Latitude_y',
    'Longitude_y',
    'StationID',
], axis=1)
training_df.dropna(inplace=True)


training_df['time_of_day'] = (training_df['hours'] % 24 + 4) // 4

# Set up model parameters
time_steps = 7
hidden_units = 64
epochs = 30


def create_dataset(dataset, look_back=7):
    (dataX, dataY) = ([], [])
    for i in range(len(dataset) - look_back - 1):
        dataX.append(dataset[i:i + look_back, 1:])
        dataY.append(dataset[i + look_back, 0])
    return (np.array(dataX), np.array(dataY))


dataset = training_df.values
dataset = dataset.astype('float32')

# normalize the dataset

look_back = 7
scaler = MinMaxScaler(feature_range=(0, 1))

# dataset = scaler.fit_transform(dataset)

# reshape into X=t and Y=t+1
trainX, trainY = create_dataset(dataset, look_back)

# reshape input to be [samples, time steps, features]

trainX = np.reshape(trainX, (trainX.shape[0], trainX.shape[1], 15))
print(trainX.shape, trainY.shape)


class attention(Layer):
    def __init__(self, **kwargs):
        super(attention, self).__init__(**kwargs)

    def build(self, input_shape):
        self.W = self.add_weight(name='attention_weight', shape=(input_shape[-1], 1),
                                 initializer='random_normal', trainable=True)
        self.b = self.add_weight(name='attention_bias', shape=(input_shape[1], 1),
                                 initializer='zeros', trainable=True)
        super(attention, self).build(input_shape)

    def call(self, x):
        # Alignment scores. Pass them through tanh function
        e = K.tanh(K.dot(x, self.W) + self.b)
        # Remove dimension of size 1
        e = K.squeeze(e, axis=-1)
        # Compute the weights
        alpha = K.softmax(e)
        # Reshape to tensorFlow format
        alpha = K.expand_dims(alpha, axis=-1)
        # Compute the context vector
        context = x * alpha
        context = K.sum(context, axis=1)
        return context


def create_RNN_with_attention(
    hidden_units,
    dense_units,
    input_shape,
    activation,
):
    x = Input(shape=input_shape)
    RNN_layer = SimpleRNN(hidden_units, return_sequences=True,
                          activation=activation)(x)
    attention_layer = attention()(RNN_layer)
    outputs = Dense(dense_units, trainable=True,
                    activation=activation)(attention_layer)
    model = Model(x, outputs)
    model.compile(loss='mse', optimizer='adam',
                  metrics=[tf.keras.metrics.mean_squared_error,
                           'accuracy'])
    return model


model_attention = create_RNN_with_attention(hidden_units=hidden_units,
                                            dense_units=1, input_shape=(time_steps, 15), activation='tanh')
print(model_attention.summary())

model_attention.fit(trainX, trainY, epochs=epochs, batch_size=100, verbose=2)


# save the model to disk
filename = f'{cmaq_folder}/models/attnRNN_o3_Jul.sav'
#filename = 'D:/Research/CMAQ/local_test/xgboost.sav'
pickle.dump(model_attention, open(filename, 'wb'))
print(f"Model is trained and saved to {filename}")

