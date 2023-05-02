import tensorflow as tf
import numpy as np
from re import X
from keras.applications import ResNet50

from keras.applications.resnet import ResNet152
from keras.layers import Dense, Flatten, Dropout
from keras import Sequential
from keras.models import Model

from preprocess import get_labels, unpickle, preprocess_images

from re import X

def train_model(images, one_hots):

    # load in the pre-trained resnet
    # vgg16 = tf.keras.applications.VGG16(include_top=False, weights = 'imagenet', input_shape = (256,256,3))
    # resnet50 = tf.keras.applications.ResNet152(include_top=False, weights='imagenet', input_shape=(256,256,3))
    
    # dataset = tf.data.Dataset.from_tensor_slices((images, one_hots))

    # # Shuffle the dataset and split into batches of size 32
    # batch_size = 16
    # dataset = dataset.shuffle(buffer_size=len(images))
    # dataset = dataset.batch(batch_size)
    # # freeze the pre-trained layers, and only train the newly added layers
    # for layer in resnet152.layers:
    #   layer.trainable = False



    # add new layers
    # x = Flatten()(resnet152.output)
    # x = Dense(128, activation='relu')(x)
    # predictions = Dense(2, activation='sigmoid')(x)

    # train_model = Sequential([
    # flatten=Flatten()(resnet50.output)
    # dense1=Dense(128, activation='relu')(flatten)
    # dropout1=Dropout(rate=0.3)(dense1)
    # dense2=Dense(64, activation='relu')(dropout1)
    # dropout2=Dropout(rate=0.3)(dense2)
    # predictions=Dense(2, activation='sigmoid')(dropout2)

    # PREPROCESSING WITH VGG 
    vgg_model = tf.keras.applications.VGG16(include_top = False, weights = 'imagenet', input_shape=(256,256,3))

    slice_model = Model(inputs = vgg_model.input, outputs = vgg_model.get_layer('block1_conv1').output)

    preprocessed = slice_model.predict(images, batch_size = 16)

    print('preprocessed shape: {preprocessed.shape}')

    # ABSTRACTING WITH RESNET50

    resnet50 = tf.keras.applications.ResNet50(include_top=False, weights='imagenet', input_shape=(256,256,64))

    for layer in resnet50.layers:
        layer.trainable = False

    flatten=Flatten()(resnet50.output)
    dense1=Dense(512, activation='leaky_relu')(flatten)
    dropout1=Dropout(rate=0.3)(dense1)
    dense2=Dense(256, activation='leaky_relu')(dropout1)
    dropout2=Dropout(rate=0.5)(dense2)
    dense3 = Dense(64, activation = 'leaky_relu')(dropout2)
    predictions=Dense(2, activation='softmax')(dense3)

    model = Model(inputs=preprocessed, outputs=predictions)



    # compile the models
    model.compile(optimizer=tf.keras.optimizers.Adam(0.0004), loss='binary_crossentropy', metrics=['accuracy'])

    history = model.fit(images[:5200], one_hots[:5200], batch_size=64, epochs=5, 
                        validation_data=(images[5200:], one_hots[5200:]))
    



if __name__ == "__main__":
    # preprocess_images()
    get_labels()
    images, one_hots = unpickle()
    train_model(images, one_hots)


