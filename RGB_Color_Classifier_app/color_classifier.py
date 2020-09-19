# -*- coding: utf-8 -*-

## Importing Libraries
import numpy as np

# Importing Tensorflow
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

#print(tf.__version__)

"""## Loading Trained Model"""
# Recreate the exact same model, including its weights and the optimizer
model = tf.keras.models.load_model('colormodel_trained_90.h5') 

"""## Initializing Color Classes for Prediction"""

# Mapping the Color Index with the respective 11 Classes (More Explained in RGB Color Classifier ML Model jupyter notebook)
color_dict={
    0 : 'Red',
    1 : 'Green',
    2 : 'Blue',
    3 : 'Yellow',
    4 : 'Orange',
    5 : 'Pink',
    6 : 'Purple',
    7 : 'Brown',
    8 : 'Grey',
    9 : 'Black',
    10 : 'White'
}

#predicting from loaded trained_model
def predict_color(Red, Green, Blue):
    rgb = np.asarray((Red, Green, Blue)) #rgb tuple to numpy array
    input_rgb = np.reshape(rgb, (-1,3)) #reshaping as per input to ANN model
    color_class_confidence = model.predict(input_rgb) # Output of layer is in terms of Confidence of the 11 classes
    color_index = np.argmax(color_class_confidence, axis=1) #finding the color_class index from confidence
    color = color_dict[int(color_index)]
    return color
	
