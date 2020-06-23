# -*- coding: utf-8 -*-
"""Classify an image input generated from random RGB values.ipynb


## Importing Libraries
"""

import PIL
from PIL import Image

from IPython.display import display #to display image

import numpy as np
import pandas as pd

# Importing Tensorflow
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers

print(tf.__version__)

"""## Functions to Generate Images from Random R,G,B Values"""

# Generate Random R,G,B value 
import random
def generate_random_rgb(): 
    return (int(random.uniform(0,255)), int(random.uniform(0,255)), int(random.uniform(0,255)))

# Create a new image with the given size
def create_image(i, j):
  image = Image.new("RGB", (i, j), color=generate_random_rgb())
  return image

# Get the pixel from the given image
def get_pixel(image, i, j):
  # Inside image bounds?
  width, height = image.size
  if i > width or j > height:
    return None
  # Get Pixel
  pixel = image.getpixel((i, j))
  return pixel

"""## Importing Trained Model"""

#Load model from github into colab
import os
import urllib.request
urllib.request.urlretrieve('https://github.com/AjinkyaChavan9/RGB-Color-Classifier-with-Deep-Learning-using-Keras-and-Tensorflow/blob/master/RGB%20Color%20Classifier%20ML%20Model/colormodel_trained_89.h5?raw=true', 'colormodel_trained_89.h5')

ls

# Recreate the exact same model, including its weights and the optimizer
model = tf.keras.models.load_model('colormodel_trained_89.h5') 

# Show the model architecture
model.summary()

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

"""## Input from User to generate 'n' Random RGB images & Predicting their Color Class(Label)"""

# User input for number of images to be classified
n = int(input('Enter number of images to be classified: '))
print() #blank line for spacing

#predicting from loaded trained_model
for i in range(n) :
    img = create_image(235,235) #(235,235) is the (width,heigth) of the image
    rgb = get_pixel(img,200,200) # any pixel within the image is given
    rgb = np.asarray(rgb) #rgb to numpy array
    input_rgb = np.reshape(rgb, (-1,3)) #reshaping as per input to ANN model
    display(img)
    color_class_confidence = model.predict(input_rgb) # Output of layer is in terms of Confidence of the 11 classes
    color_index = np.argmax(color_class_confidence, axis=1) #finding the color_class index from confidence
    color = color_dict[int(color_index)]
    print('            ' + color)
    print()
