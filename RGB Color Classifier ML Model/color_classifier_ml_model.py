# -*- coding: utf-8 -*-
"""Color Classifier ML Model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cctFFiuy24ce3xSReavRmVGhHHPgUoRr

# Importing Libraries
"""

import numpy as np
import pandas as pd
import seaborn as sns
import pathlib
import matplotlib.pyplot as plt

# Importing Tensorflow
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers

print(tf.__version__)

!pip install git+https://github.com/tensorflow/docs # Use some functions from tensorflow_docs

import tensorflow_docs as tfdocs
import tensorflow_docs.plots
import tensorflow_docs.modeling

#plotly used for plotting Interactive Graphs
!pip install plotly
import plotly.offline as py
import plotly.express as px
import plotly.graph_objs as go

"""# Loading Dataset"""

dataset = pd.read_csv('final_data.csv')
dataset

dataset.describe()

dataset.info()

"""# Pre Process, Clean the Data

## Eliminate Null if it exists
"""

#To find whether null entries are present 
dataset.isnull().sum()

"""## Converting Categorical Data of 'label` into Numerical"""

dataset.label.unique()

# One-Hot-Encoding
dataset = pd.get_dummies(dataset, columns=['label'])
dataset

"""## Reorder"""

dataset = dataset[['red', 'green', 'blue', 'label_Red', 'label_Green', 'label_Blue', 'label_Yellow', 'label_Orange', 'label_Pink', 'label_Purple', 'label_Brown', 'label_Grey', 'label_Black', 'label_White']]
dataset

"""# Data Correlation"""

# Correlation Matrix Heatmap
f, ax = plt.subplots(figsize=(15, 9))
corr = dataset.corr()
hm = sns.heatmap(round(corr,2), annot=True, ax=ax, cmap="coolwarm",fmt='.2f',
                 linewidths=.05)
f.subplots_adjust(top=0.93)
t= f.suptitle('Correlation Heatmap', fontsize=15)

"""# Split the data into train and test"""

train_dataset = dataset.sample(frac=0.8, random_state=9) #train = 80%,  random_state = any int value means every time when you run your program you will get the same output for train and test dataset, random_state is None by default which means every time when you run your program you will get different output because of splitting between train and test varies within 
test_dataset = dataset.drop(train_dataset.index) #remove train_dataset from dataframe to get test_dataset
train_dataset

test_dataset

"""## Split features: `red`, `green`, `blue` and labels"""

train_labels = pd.DataFrame([train_dataset.pop(x) for x in ['label_Red', 'label_Green', 'label_Blue', 'label_Yellow', 'label_Orange', 'label_Pink', 'label_Purple', 'label_Brown', 'label_Grey', 'label_Black', 'label_White']]).T
train_labels

train_dataset

test_labels = pd.DataFrame([test_dataset.pop(x) for x in ['label_Red', 'label_Green', 'label_Blue', 'label_Yellow', 'label_Orange', 'label_Pink', 'label_Purple', 'label_Brown', 'label_Grey', 'label_Black', 'label_White']]).T
test_labels

test_dataset

"""# Build & Compile the Model

## Set up the layers
"""

from keras import regularizers
model = keras.Sequential([
    layers.Dense(3, kernel_regularizer=regularizers.l2(0.001), activation='relu', input_shape=[len(train_dataset.keys())]), #inputshape=[3]
    layers.Dense(24, kernel_regularizer=regularizers.l2(0.001), activation='relu'),
    layers.Dense(11)
  ])

"""## Compile the model"""

optimizer = keras.optimizers.Adam(learning_rate=0.001)
loss_function = tf.keras.losses.CategoricalCrossentropy(from_logits=True)

model.compile(loss=loss_function,
                optimizer=optimizer,
                metrics=['accuracy'])

model.summary()

"""## Train the model"""

history = model.fit(x=train_dataset, y=train_labels, 
                    validation_split=0.3, 
                    epochs=10001, 
                    batch_size=48, 
                    verbose=0,
                    callbacks=[tfdocs.modeling.EpochDots()], 
                    shuffle=True)

hist = pd.DataFrame(history.history)
hist['epoch'] = history.epoch
hist.tail()

plotter = tfdocs.plots.HistoryPlotter(smoothing_std=2)

plotter.plot({'Basic': history}, metric = "accuracy")
plt.ylim([0, 1])
plt.ylabel('accuracy [Color]')

plotter.plot({'Basic': history}, metric = "loss")
plt.ylim([0, 1])
plt.ylabel('loss [Color]')

"""# Save Model"""

#Install PyDrive library into Google Colab notebook
!pip install -U -q PyDrive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive 
from google.colab import auth 
from oauth2client.client import GoogleCredentials

#Authenticate and create the PyDrive client
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()                       
drive = GoogleDrive(gauth)

!pip install pyyaml h5py  # Required to save models in HDF5 format

# Save Model or weights on google drive and create on Colab directory in Google Drive

# Save the entire model to a HDF5 file.
# The '.h5' extension indicates that the model should be saved to HDF5.
model.save('colormodel_acu_89.h5')
model_file = drive.CreateFile({'title' : 'colormodel_acu_89.h5'}) # colormodel_acu_  .h5 is the name of the model uploaded to Drive                   
model_file.SetContentFile('colormodel_acu_89.h5')                       
model_file.Upload()

# download to google drive                       
drive.CreateFile({'id': model_file.get('id')}) ### very important to run this last cell for loading the model in new notebook

#Load model from google drive into colab
file_obj = drive.CreateFile({'id': '14Jxscgqc0bF34V7Nlh7dmqS9rL0EV-Yy'})                       
file_obj.GetContentFile('colormodel_trained_89.h5') #colormodel_trained.h5 is the name of model uploaded to colab

ls

# Recreate the exact same model, including its weights and the optimizer
model = tf.keras.models.load_model('colormodel_trained_89.h5') #very important

# Show the model architecture
model.summary()

"""# Make Prediction

The prediction by the ANN model is an array of 11 numbers. 

They represent the model's "confidence" that the RGB color corresponds to each of the 11 different classes of color as follows:

* 0 for Red
* 1 for Green
* 2 for Blue 
* 3 for Yellow
* 4 for Orange
* 5 for Pink
* 6 for Purple
* 7 for Brown
* 8 for Grey
* 9 for Black
* 10 for White 




You can see which out of the 11 labels has the highest confidence value

## Train Dataset Prediction
"""

train_predictions = model.predict(train_dataset)
train_predictions

"""### Selecting Class with highest confidence"""

actual_encoded_train_labels = np.argmax(train_labels.to_numpy(), axis=1) #train_labels were originally in one-hot
actual_encoded_train_labels

predicted_encoded_train_labels = np.argmax(train_predictions, axis=1)
predicted_encoded_train_labels

"""### Converting numpy array to pandas dataframe"""

actual_encoded_train_labels = pd.DataFrame(actual_encoded_train_labels, columns=['Labels'])
actual_encoded_train_labels

predicted_encoded_train_labels = pd.DataFrame(predicted_encoded_train_labels, columns=['Labels'])
predicted_encoded_train_labels

"""### Visualize Prediction for Train Dataset"""

#Plot Actual vs Predicted Class for Training Dataset
actual_chart = go.Scatter(x=actual_encoded_train_labels.index, y=actual_encoded_train_labels.Labels, name= 'Actual Label')
predict_chart = go.Scatter(x=actual_encoded_train_labels.index, y=predicted_encoded_train_labels.Labels, name= 'Predicted Label')
py.iplot([predict_chart, actual_chart])

"""## Test Dataset Prediction"""

test_predictions = model.predict(test_dataset)
test_predictions

"""### Selecting Class with highest confidence"""

actual_encoded_test_labels = np.argmax(test_labels.to_numpy(), axis=1) 
actual_encoded_test_labels

predicted_encoded_test_labels = np.argmax(test_predictions, axis=1)
predicted_encoded_test_labels

"""### Converting numpy array to pandas dataframe"""

actual_encoded_test_labels = pd.DataFrame(actual_encoded_test_labels, columns=['Labels'])
actual_encoded_test_labels

predicted_encoded_test_labels = pd.DataFrame(predicted_encoded_test_labels, columns=['Labels'])
predicted_encoded_test_labels

"""### Visualize Prediction for Test Dataset"""

#Plot Actual vs Predicted Class for Test Dataset
actual_chart = go.Scatter(x=actual_encoded_test_labels.index, y=actual_encoded_test_labels.Labels, name= 'Actual Label')
predict_chart = go.Scatter(x=actual_encoded_test_labels.index, y=predicted_encoded_test_labels.Labels, name= 'Predicted Label')
py.iplot([predict_chart, actual_chart])

"""# Evaluate Model

## Evaluating for Training Dataset
"""

model.evaluate(x=train_dataset, y=train_labels)

from sklearn.metrics import confusion_matrix, classification_report
confusion_matrix_train = confusion_matrix(actual_encoded_train_labels, predicted_encoded_train_labels)
confusion_matrix_train

f,ax = plt.subplots(figsize=(16,12))
categories = ['Red', 'Green', 'Blue', 'Yellow', 'Orange', 'Pink', 'Purple', 'Brown', 'Grey', 'Black', 'White']
sns.heatmap(confusion_matrix_train, annot=True, cmap='Blues', fmt='d',
            xticklabels = categories,
            yticklabels = categories)
plt.show()

target_names = ['Red', 'Green', 'Blue', 'Yellow', 'Orange', 'Pink', 'Purple', 'Brown', 'Grey', 'Black', 'White']
print(classification_report(actual_encoded_train_labels, predicted_encoded_train_labels, target_names=target_names))

"""## Evaluating for Test Dataset"""

model.evaluate(x=test_dataset, y=test_labels)

confusion_matrix_test = confusion_matrix(actual_encoded_test_labels, predicted_encoded_test_labels)
confusion_matrix_test

f,ax = plt.subplots(figsize=(16,12))
categories = ['Red', 'Green', 'Blue', 'Yellow', 'Orange', 'Pink', 'Purple', 'Brown', 'Grey', 'Black', 'White']
sns.heatmap(confusion_matrix_test, annot=True, cmap='Blues', fmt='d',
            xticklabels = categories,
            yticklabels = categories)
plt.show()

target_names = ['Red', 'Green', 'Blue', 'Yellow', 'Orange', 'Pink', 'Purple', 'Brown', 'Grey', 'Black', 'White']
print(classification_report(actual_encoded_test_labels, predicted_encoded_test_labels, target_names=target_names))