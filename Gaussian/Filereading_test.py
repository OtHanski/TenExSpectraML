# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 15:18:55 2021

@author: malkamm1
"""

from GimmePandas import ReadToPandas

data = ReadToPandas()

print(len(data))
print(data.head())
origdata = data
df = data.sample(frac=1).reset_index(drop=True)

x_sufl = df["Xdata"]
y_sufl = df["Reflectivity"]
x_orig = origdata["Xdata"]
y_orig = origdata["Reflectivity"]

print(y_sufl.head())
print(y_orig.head())
print(data.head())