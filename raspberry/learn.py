#!/usr/bin/env python3
import argparse
from keras.models import Model
from keras.layers import Dense, Dropout, ELU, Lambda, merge, MaxPooling2D, Input, Activation, GlobalAveragePooling2D
from keras.layers import concatenate
from keras.layers.convolutional import Convolution2D
from keras.callbacks import Callback
from keras.optimizers import Adam
import numpy as np
from sklearn.utils import shuffle
from preprocess_dataset import prepare_from_paths
import matplotlib.pyplot as plt
from collections import Counter

#hyperparameters
INPUT_SHAPE = (64, 64, 1)
LEARNING_RATE = 1e-1
BATCH_SIZE = 128
EPOCHS = 40

def parse_dirnames():
    parser = argparse.ArgumentParser(description='Correlates steering with images')
    parser.add_argument('dirnames', metavar='dirname', nargs='+', help='a directory with saved session')
    return parser.parse_args().dirnames

def fire_module(x, fire_id, squeeze=16, expand=64):
    """
    This is a modified version of: https://github.com/rcmalli/keras-squeezenet/blob/master/squeezenet.py#L14
    Changes made:
    * Uses ELU activation
    * Only supports tf
    """
    s_id = 'fire' + str(fire_id) + '/'
    c_axis = 3
    sq1x1 = "squeeze1x1"
    exp1x1 = "expand1x1"
    exp3x3 = "expand3x3"
    elu = "elu_"

    x = Convolution2D(squeeze, (1, 1), padding='valid', name=s_id + sq1x1)(x)
    x = Activation('elu', name=s_id + elu + sq1x1)(x)

    left = Convolution2D(expand, (1, 1), padding='valid', name=s_id + exp1x1)(x)
    left = Activation('elu', name=s_id + elu + exp1x1)(left)

    right = Convolution2D(expand, (3, 3), padding='same', name=s_id + exp3x3)(x)
    right = Activation('elu', name=s_id + elu + exp3x3)(right)

    # x = merge([left, right], mode='concat', concat_axis=c_axis, name=s_id + 'concat')
    x = concatenate([left, right], axis=c_axis, name=s_id + 'concat')
    return x

def squeeze_model_52():
    """
    This model is a modification from the reference:
    https://github.com/rcmalli/keras-squeezenet/blob/master/squeezenet.py
    Normalizing will be done in the model directly for GPU speedup
    """
    input_shape=(64, 64, 1)
    input_img = Input(shape=input_shape)
    x = Lambda(lambda x: x/127.5 - 1.,input_shape=input_shape)(input_img)

    x = Convolution2D(2, (3, 3), strides=(2, 2), padding='valid', name='conv1')(x)
    x = Activation('elu', name='elu_conv1')(x)
    x = MaxPooling2D(pool_size=(3, 3), strides=(2, 2), name='pool1')(x)

    x = fire_module(x, fire_id=2, squeeze=1, expand=2)
    x = Dropout(0.2, name='drop3')(x)


    x = GlobalAveragePooling2D()(x)
    out = Dense(1, name='loss')(x)
    model = Model(inputs=[input_img], outputs=[out])

    model.compile(optimizer=Adam(lr=LEARNING_RATE), loss='mse')
    return model

def visualize_dataset(labels):
    plt.plot(labels)
    plt.show()
    
    values, freq = zip(*Counter(labels).items())
    plt.bar(values, freq)
    plt.show()

def visualize_history(history):
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.show()

if __name__ == '__main__':
    model = squeeze_model_52()

    features, labels = prepare_from_paths(parse_dirnames())
    # visualize(labels)
    features = np.array(features).reshape(len(features), 64, 64, 1)
    history = model.fit(x=features,
                        y=labels,
                        verbose=1,
                        batch_size=BATCH_SIZE,
                        epochs=EPOCHS,
                        validation_split=0.3)

    model.save_weights('out.h5')
    print("Training complete!")
    visualize_history(history)
