import argparse
import os
import shelve

import keras
import numpy as np
from keras.layers import BatchNormalization, Conv2DTranspose
from keras.layers.convolutional import Conv2D, MaxPooling2D, UpSampling2D
from keras.models import Sequential, load_model
from keras.utils import plot_model

import Config

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
    elif model_name=='perfect_convolutional_autoencoder':
        model = perfect_convolutional_autoencoder()
    else:
        raise ValueError('Unknown model name %s was given' % model_name)

    model.compile(optimizer=Config.OPTIMIZER, loss=Config.LOSS)
    x_train = x_train.reshape(-1,Config.IMAGE_SHAPE_X,Config.IMAGE_SHAPE_Y,1)

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

from keras.layers import Conv2D, Dense, MaxPool2D, UpSampling2D
from keras.models import Sequential


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
