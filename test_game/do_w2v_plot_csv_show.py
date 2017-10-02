#!/usr/bin/python

from __future__ import division, print_function

import os

import gensim.models.word2vec as w2v

import sklearn.manifold


import pandas as pd
import matplotlib.pyplot as plt

import seaborn as sns

plot_words = True
find_z_words = True
find_all_words = True

if True:
    x = []
    y = []
    z = []
    f = open("trained/word2vec_points.csv", "r")
    #z = 0
    for line in f:
        l = line.split(",")
        if (l[0].strip().endswith("-z") and find_z_words) or find_all_words:
            x.append(l[1].strip())
            y.append(l[2].strip())
            z.append(l[0].strip())

    print (x,y)
    #plt.plot(x,y, 'ro',ms=0.5)
    zz = plt.scatter(x,y, marker='o', c='b',s=3, label='word2vec', clip_on=True)
    
if plot_words:
    for i in range(len(z)):
        plt.text(float(x[i]) + 0.005, float(y[i]) + 0.005, z[i], fontsize=12)

#ax = plt.gca()

#print (ax.transAxes)

plt.show()


