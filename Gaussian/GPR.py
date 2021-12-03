# -*- coding: utf-8 -*-
"""
Created on Thu Nov  4 15:25:23 2021

@author: malkamm1
"""

import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C

#import json

from GimmePandas import ReadToPandas

data = ReadToPandas()


origdata = data
df = data.sample(frac=1).reset_index(drop=True)

x_sufl = df["Xdata"]
y_sufl = df["Reflectivity"]
x_orig = origdata["Xdata"]
y_orig = origdata["Reflectivity"]

#print(x_sufl.head())
x_sufl_arr = pd.DataFrame(x_sufl.to_list())
y_sufl_arr = pd.DataFrame(y_sufl.to_list())

x_sufl_train = x_sufl_arr.head(440)
x_sufl_test = x_sufl_arr.tail(113)
y_sufl_train = y_sufl_arr.head(440)
y_sufl_test = y_sufl_arr.tail(113)

#print(x_sufl_train.iloc[60])
#print(np.isnan(x_sufl_train))
#print(np.isfinite(x_sufl_train))
#np.random.seed(1)
x_sufl_train[np.isnan(x_sufl_train)== True] = 0
x_sufl_test[np.isnan(x_sufl_test)== True] = 0
y_sufl_train[np.isnan(y_sufl_train)== True] = 0
y_sufl_test[np.isnan(y_sufl_test)== True] = 0
print("Corrected")
print(np.any(np.isnan(x_sufl_train)))
print("x_test")
print(np.any(np.isnan(x_sufl_test)))
print(np.any(np.isfinite(x_sufl_test)))
print("y_test")
print(np.any(np.isnan(y_sufl_test)))
print(np.any(np.isfinite(y_sufl_test)))
print("y_train")
print(np.any(np.isnan(y_sufl_train)))
print(np.any(np.isfinite(y_sufl_train)))


def f(x):
   # """The function to predict."""
    return x


# ----------------------------------------------------------------------
#  First the noiseless case
#X = np.atleast_2d([1.0, 3.0, 5.0, 6.0, 7.0, 8.0]).T
#X_list = [data["SpectralX"],data["SpectralX"], data["SpectralX"], data["SpectralX"], data["SpectralX"], data["SpectralX"], data["SpectralX"], data["SpectralX"]]
#X = np.array(X_list)
#print(X)
# Observations
#y = f(X).ravel()
#list_y = [data["200 nm"]["Data"], data["220 nm"]["Data"], data["240 nm"]["Data"], data["280 nm"]["Data"], data["300 nm"]["Data"], data["325 nm"]["Data"], data["350 nm"]["Data"], data["375 nm"]["Data"]]
#y = np.array(list_y)
#y = data["325 nm"]["Data"]
#print(X)
#print(y)
# Mesh the input space for evaluations of the real function, the prediction and
# its MSE
#x = np.atleast_2d(np.linspace(0, 10, 1000)).T
#x = np.linspace(200, 950, 100)

# Instantiate a Gaussian Process model
kernel = C(1.0, (1e-3, 1e3)) * RBF(10, (1e-2, 1e2))
gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9) #original 9

# Fit to data using Maximum Likelihood Estimation of the parameters
gp.fit(x_sufl_train, y_sufl_train)

R_score = gp.score(x_sufl_train, y_sufl_train)
print(R_score)
# Make the prediction on the meshed x-axis (ask for MSE as well)
y_pred, sigma = gp.predict(x_sufl_test, return_std=True)

# Plot the function, the prediction and the 95% confidence interval based on
# the MSE
plt.figure()
plt.plot(y_sufl_test, y_pred)
#plt.plot(x, f(x))
#plt.plot(x_sufl_train, y_sufl_train, "r.", markersize=10, label="Observations")
#plt.plot(x_sufl_test, y_pred, "b-", label="Prediction")
#plt.fill(
 #   np.concatenate([x_sufl_test, x_sufl_test[::-1]]),
   # np.concatenate([y_pred - 1.9600 * sigma, (y_pred + 1.9600 * sigma)[::-1]]),
    #alpha=0.5,
    #fc="b",
    #ec="None",
    #label="95% confidence interval",
#)
#plt.xlabel("$x$")
#plt.ylabel("$f(x)$")
#plt.ylim(40, 110)
#plt.legend(loc="upper left")

