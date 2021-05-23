import shelve

import keras
from keras.utils import plot_model
import numpy as np
from keras.layers import Conv2DTranspose, BatchNormalization
from keras.layers.convolutional import Conv2D, MaxPooling2D, UpSampling2D
from keras.models import Sequential, load_model
import Config
import os
import argparse

model_name = Config.MODEL_NAME
re = re=Config.RELOAD_MODEL

# Encoder
def get_model(x_train):
    # cache = shelve.open(Config.CACHE_PATH + "model")
    if not re:
        return load_model(Config.MODEL_PATH)
    if model_name=='autoencoder':
        model = autoencoder()
    elif model_name=='deep_autoencoder':
        model = deep_autoencoder()
    elif model_name=='convolutional_autoencoder':
        model = convolutional_autoencoder()
    else:
        raise ValueError('Unknown model name %s was given' % model_name)

    model.compile(optimizer=Config.OPTIMIZER, loss=Config.LOSS)
    x_train = x_train.reshape(-1,128,128,1)

    model.fit(
        x=x_train,
        y=x_train,
        epochs=Config.EPOCHS,
        batch_size=Config.BATCH_SIZE
    )
    #cache["model"] = model

    #cache.close()
    model.save(Config.MODEL_PATH)
    # delete model for saving memory
    del model
    return load_model(Config.MODEL_PATH)

from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPool2D, UpSampling2D

def autoencoder():
    input_shape=(784,)
    model = Sequential()
    model.add(Dense(64, activation='relu', input_shape=input_shape))
    model.add(Dense(784, activation='sigmoid'))
    return model

def deep_autoencoder():
    input_shape=(784,)
    model = Sequential()
    model.add(Dense(128, activation='relu', input_shape=input_shape))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(784, activation='sigmoid'))
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

def perfect_convolutional_autoencoder():
    input_shape=(256,256,1)
    n_channels = input_shape[-1]
    model = Sequential()
    model.add(Conv2D(256, (3,3), activation='relu', padding='same', input_shape=input_shape))
    model.add(MaxPool2D(padding='same'))
    model.add(Conv2D(128, (3,3), activation='relu', padding='same'))
    model.add(MaxPool2D(padding='same'))
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
    model.add(Conv2D(128, (3,3), activation='relu', padding='same'))
    model.add(UpSampling2D())
    model.add(Conv2D(256, (3,3), activation='relu', padding='same'))
    model.add(Conv2D(n_channels, (3,3), activation='sigmoid', padding='same'))
    return model