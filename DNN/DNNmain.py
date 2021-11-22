import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from GimmePandas import ReadToPandas2

# Helpottaa numpy-outputin lukemista
np.set_printoptions(precision=3, suppress=True)

# Pandan output: column_names = "Excitation", "Baseline", "Peak", "FWHM points" plus kaik datapisteet
raw_dataset = ReadToPandas2()

dataset = raw_dataset.copy()
#print(dataset.tail())

# Split dataset into training data and testing data
train_dataset = dataset.sample(frac=0.8, random_state=0)
test_dataset = dataset.drop(train_dataset.index)
#print(train_dataset.tail())

# Show some statistics of dataset
#print(train_dataset.describe().transpose())

# Split off the trainable labels
train_features = train_dataset.copy()
test_features = test_dataset.copy()

train_labels = train_features.pop("Peak", "Baseline")
test_labels = test_features.pop("Peak", "Baseline")

# Normalize data
normalizer = tf.keras.layers.Normalization(axis=-1)
normalizer.adapt(np.array(train_features))
normalizer.mean.numpy()