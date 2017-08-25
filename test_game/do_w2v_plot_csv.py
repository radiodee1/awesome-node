#!/usr/bin/python

from __future__ import division, print_function

import os

import gensim.models.word2vec as w2v

import sklearn.manifold


import pandas as pd
import matplotlib.pyplot as plt

import seaborn as sns



if True:
    x = []
    y = []
    f = open("data/points.csv", "r")
    #z = 0
    for line in f:
        l = line.split(",")
        x.append(l[1].strip())
        y.append(l[2].strip())

    print (x,y)
    plt.plot(x,y, 'ro')



#sns.set_context("poster")
#points.plot.scatter("x", "y", s=10, figsize=(20, 12))

plt.show()


