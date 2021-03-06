import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import warnings

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from GimmePandas import ReadToPandas, ReadToPandas2, ReadToNumpy

warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

def build_and_compile_model(norm):
    model = keras.Sequential([
        norm,
        layers.Dense(512, activation='relu'),
        layers.Dense(256, activation='relu'),
        layers.Dense(1)
        ])

    model.compile(loss='mean_absolute_error',
                    optimizer=tf.keras.optimizers.Adam(0.001))
    
    return model

def plot_loss(history):
  plt.plot(history.history['loss'], label='loss')
  plt.plot(history.history['val_loss'], label='val_loss')
  #plt.ylim([0, 10])
  plt.xlabel('Epoch')
  plt.ylabel('Error')
  plt.legend()
  plt.grid(True)

# Helpottaa numpy-outputin lukemista
np.set_printoptions(precision=3, suppress=True)

# Pandan output: column_names = "Excitation", "Baseline", "Peak", "FWHM points" plus kaik datapisteet
raw_dataset = ReadToPandas()
#raw_dataset = raw_dataset.astype("float32")

dataset = raw_dataset.copy()
#print(dataset.tail())

test_results = {}

# Split dataset into training data and testing data
train_dataset = dataset.sample(frac=0.8, random_state=0)
test_dataset = dataset.drop(train_dataset.index)
#print(train_dataset.tail())

# Show some statistics of dataset
#print(train_dataset.describe().transpose())

# Split off the trainable labels
train_features = train_dataset.copy()
test_features = test_dataset.copy()

train_labels = pd.concat([train_features.pop(x) for x in ["Peak", "Baseline"]], axis=1)
#print(train_labels)
test_labels = pd.concat([test_features.pop(x) for x in ["Peak", "Baseline"]], axis=1)

# Normalize data
normalizer = tf.keras.layers.Normalization(axis=-1)
normalizer.adapt(np.asarray(train_features).astype('float32'))
normalizer.mean.numpy()

# DNN regression for peak
print("\n Training model for peak\n")
peak_model = build_and_compile_model(normalizer)
history = peak_model.fit(
    train_features,
    np.asarray(train_labels["Peak"]),
    validation_split=0.2,
    verbose=0, epochs=2500)
plot_loss(history)
plt.show()

test_results['peak_model [nm]'] = peak_model.evaluate(test_features, test_labels["Peak"], verbose=0)


# Test dat shit
peak_predictions = peak_model.predict(test_features).flatten()

a = plt.axes(aspect='equal')
plt.scatter(test_labels["Peak"], peak_predictions)
plt.xlabel('True Values [nm]')
plt.ylabel('Predictions [nm]')
limsx = [400, 900]
limsy = [200,1600]
plt.xlim(limsx)
plt.ylim(limsy)
_ = plt.plot([0,1200], [0,1200])
plt.show()

# Same for baselines

print("\n Training model for baseline\n")
baseline_model = build_and_compile_model(normalizer)
history = baseline_model.fit(
    train_features,
    np.asarray(train_labels["Baseline"]),
    validation_split=0.2,
    verbose=0, epochs=2500)
plot_loss(history)
plt.show()

test_results['baseline_model [Ref-%]'] = baseline_model.evaluate(test_features, test_labels["Baseline"], verbose=0)
print(pd.DataFrame(test_results, index=['Mean absolute error']).T)


# Test dat shit
baseline_predictions = baseline_model.predict(test_features).flatten()

a = plt.axes(aspect='equal')
plt.scatter(test_labels["Baseline"], baseline_predictions)
plt.xlabel('True Values [%]')
plt.ylabel('Predictions [%]')
limsx = [80, 120]
limsy = [40, 160]
plt.xlim(limsx)
plt.ylim(limsy)
_ = plt.plot([0,120], [0,120])
plt.show()


# Save test results
#test_results['dnn_model'] = dnn_model.evaluate(test_features, test_labels, verbose=0)
