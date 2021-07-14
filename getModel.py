import argparse
import os
import pickle
import shelve

import keras
import numpy as np
from keras.layers import (LSTM, BatchNormalization, Conv2DTranspose, Dense,
                          Dropout, Input, RepeatVector, TimeDistributed)
from keras.layers.convolutional import Conv2D, MaxPooling2D, UpSampling2D
from keras.models import Sequential, load_model
from keras.utils import plot_model

import Config
import utils

model_name = Config.MODEL_NAME
re = re=Config.RELOAD_MODEL

# Encoder
def get_model(x_train):
    # cache = shelve.open(Config.CACHE_PATH + "model")
    if not re:
        return load_model(Config.MODEL_PATH)
    if Config.USE_BINARIZED_OPTICAL_FLOW:
        model = binarized_optical_flow_model()
        model.compile(optimizer=Config.OPTIMIZER, loss=Config.LOSS)
    elif model_name=='autoencoder':
        model = autoencoder()
        model.compile(optimizer=Config.OPTIMIZER, loss=Config.LOSS)
    elif model_name=='deep_autoencoder':
        model = deep_autoencoder()
        model.compile(optimizer=Config.OPTIMIZER, loss=Config.LOSS)
    elif model_name=='convolutional_autoencoder':
        model = convolutional_autoencoder()
        model.compile(optimizer=Config.OPTIMIZER, loss=Config.LOSS)
    elif model_name=='perfect_convolutional_autoencoder':
        model = perfect_convolutional_autoencoder() #con_autoEncoder_32() #perfect_convolutional_autoencoder()
        model.compile(optimizer=Config.OPTIMIZER, loss=Config.LOSS)

    elif model_name=='lstm_autoencoder':
        model = lstm_autoencoder()
    else:
        raise ValueError('Unknown model name %s was given' % model_name)

    
    x_train = x_train.reshape(-1,Config.IMAGE_SHAPE_X,Config.IMAGE_SHAPE_Y,1)
    if model_name=='lstm_autoencoder':
        x_train = x_train.reshape(-1, Config.IMAGE_SHAPE_X*Config.IMAGE_SHAPE_Y,1)
    
    if Config.TRACE_ACCURACY:
        accuracyIndex = {}
        try:
            with open("cachedaccuracyIndex", 'rb') as ind:
                accuracyIndex = pickle.load(ind)
                print("starting from", accuracyIndex)
        except:
            accuracyIndex[-1] = 0
            print("starting fresh")
        maxAccuracy = 0
        for epoch in accuracyIndex:
            maxAccuracy = max(maxAccuracy, accuracyIndex[epoch])
        for i in range(max(accuracyIndex.keys()) + 1, Config.EPOCHS+1):
            print("Epoch ", i, "/",Config.EPOCHS)
            if i>0 or Config.RETRAIN_MODEL:
                if i == max(accuracyIndex.keys()) + 1:
                    print("retraining model from the existing model")
                model = load_model(Config.MODEL_PATH)
            model.fit(
                x=x_train,
                y=x_train,
                epochs=1,
                batch_size=Config.BATCH_SIZE
            )
            model.save(Config.MODEL_PATH)
        
            accuracyIndex[i] = utils.getModelAccuracy(model)
            print("Epoch: ", i, "Accuracy: ", accuracyIndex[i])
            if maxAccuracy < accuracyIndex[i]:
                model.save(Config.RESULT_PATH + "/bestModel")
            # delete model for saving memory
            del model
            with open("cachedaccuracyIndex","wb") as f:
                pickle.dump(accuracyIndex, f)
    else:
        print("here no trace accuracy")
        model.fit(
            x=x_train,
            y=x_train,
            epochs=Config.EPOCHS,
            batch_size=Config.BATCH_SIZE
        )
    return load_model(Config.MODEL_PATH)

from keras.layers import Conv2D, Dense, MaxPool2D, UpSampling2D
from keras.models import Sequential


def autoencoder():
    input_shape=(784,)
    model = Sequential()
    model.add(Dense(64, activation='relu', input_shape=input_shape))
    model.add(Dense(784, activation='sigmoid'))
    return model

def deep_autoencoder():
    input_shape=(Config.IMAGE_SHAPE_X,Config.IMAGE_SHAPE_Y,1)
    model = Sequential()
    model.add(Dense(64, activation='relu', input_shape=input_shape))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(64, activation='sigmoid'))
    
    return model

def convolutional_autoencoder():

    input_shape=(128,128,1)
    n_channels = input_shape[-1]
    model = Sequential()
    model.add(Conv2D(32, (3,3), activation='relu', padding='same', input_shape=input_shape))
    model.add(MaxPool2D(padding='same'))
    model.add(Conv2D(16, (3,3), activation='relu', padding='same'))
    model.add(MaxPool2D(padding='same'))
    model.add(Conv2D(8, (3,3), activation='relu', padding='same'))
    model.add(UpSampling2D())
    model.add(Conv2D(16, (3,3), activation='relu', padding='same'))
    model.add(UpSampling2D())
    model.add(Conv2D(32, (3,3), activation='relu', padding='same'))
    model.add(Conv2D(n_channels, (3,3), activation='sigmoid', padding='same'))
    return model

def con_autoEncoder_32():
    print("Gone case")
    input_shape=(Config.IMAGE_SHAPE_X,Config.IMAGE_SHAPE_Y,1)
    n_channels = input_shape[-1]
    model = Sequential()
    model.add(Conv2D(16, (3,3), activation='relu', padding='same', input_shape=input_shape))
    model.add(Conv2D(8, (3,3), activation='relu', padding='same'))
    model.add(Conv2D(16, (3,3), activation='relu', padding='same'))
    model.add(Conv2D(n_channels, (3,3), activation='sigmoid', padding='same'))
    return model


def perfect_convolutional_autoencoder():
    print("perfect_convolutional_autoencoder is loaded")
    input_shape=(Config.IMAGE_SHAPE_X,Config.IMAGE_SHAPE_Y,1)
    n_channels = input_shape[-1]
    model = Sequential()
    model.add(Conv2D(128, (3,3), activation='relu', padding='same', input_shape=input_shape))
    model.add(MaxPool2D(padding='same'))
    # model.add(Conv2D(128, (3,3), activation='relu', padding='same'))
    # model.add(MaxPool2D(padding='same'))
    model.add(Conv2D(64, (3,3), activation='relu', padding='same'))
    model.add(MaxPool2D(padding='same'))
    model.add(Conv2D(32, (3,3), activation='relu', padding='same'))
    model.add(MaxPool2D(padding='same'))
    model.add(Conv2D(16, (3,3), activation='relu', padding='same'))
    model.add(MaxPool2D(padding='same'))
    model.add(Conv2D(8, (3,3), activation='relu', padding='same'))
    model.add(UpSampling2D())
    model.add(Conv2D(16, (3,3), activation='relu', padding='same'))
    model.add(UpSampling2D())
    model.add(Conv2D(32, (3,3), activation='relu', padding='same'))
    model.add(UpSampling2D())
    model.add(Conv2D(64, (3,3), activation='relu', padding='same'))
    model.add(UpSampling2D())
    # model.add(Conv2D(128, (3,3), activation='relu', padding='same'))
    # model.add(UpSampling2D())
    model.add(Conv2D(128, (3,3), activation='relu', padding='same'))
    model.add(Conv2D(n_channels, (3,3), activation='sigmoid', padding='same'))
    return model

def lstm_autoencoder():
    input_shape=(Config.IMAGE_SHAPE_X*Config.IMAGE_SHAPE_Y,1)
    model = Sequential()
    model.add(LSTM(128, activation='relu', input_shape=input_shape, return_sequences=True))
    model.add(LSTM(64, activation='relu', return_sequences=False))
    model.add(RepeatVector(input_shape[0]))
    model.add(LSTM(64, activation='relu', return_sequences=True))
    model.add(LSTM(128, activation='relu', return_sequences=True))
    model.add(TimeDistributed(Dense(input_shape[1])))

    model.compile(optimizer='adam', loss='mse')
    model.summary()
    return model

def binarized_optical_flow_model():
    input_shape=(Config.IMAGE_SHAPE_X,Config.IMAGE_SHAPE_Y,2)
    n_channels = input_shape[-1]
    model = Sequential()
    model.add(Conv2D(128, (3,3), activation='relu', padding='same', input_shape=input_shape))
    model.add(MaxPool2D(padding='same'))
    # model.add(Conv2D(128, (3,3), activation='relu', padding='same'))
    # model.add(MaxPool2D(padding='same'))
    model.add(Conv2D(64, (3,3), activation='relu', padding='same'))
    model.add(MaxPool2D(padding='same'))
    model.add(Conv2D(32, (3,3), activation='relu', padding='same'))
    model.add(MaxPool2D(padding='same'))
    model.add(Conv2D(16, (3,3), activation='relu', padding='same'))
    model.add(MaxPool2D(padding='same'))
    model.add(Conv2D(8, (3,3), activation='relu', padding='same'))
    model.add(UpSampling2D())
    model.add(Conv2D(16, (3,3), activation='relu', padding='same'))
    model.add(UpSampling2D())
    model.add(Conv2D(32, (3,3), activation='relu', padding='same'))
    model.add(UpSampling2D())
    model.add(Conv2D(64, (3,3), activation='relu', padding='same'))
    model.add(UpSampling2D())
    # model.add(Conv2D(128, (3,3), activation='relu', padding='same'))
    # model.add(UpSampling2D())
    model.add(Conv2D(128, (3,3), activation='relu', padding='same'))
    model.add(Conv2D(n_channels, (3,3), activation='sigmoid', padding='same'))
    return model
