#!/usr/bin/python

from __future__ import division, print_function

import os

import gensim.models.word2vec as w2v

import sklearn.manifold


import pandas as pd
import matplotlib.pyplot as plt

import seaborn as sns


word2vec_game = w2v.Word2Vec.load(os.path.join("trained", "word2vec_game.w2v"))
#word2vec_game = w2v.Word2Vec.load(os.path.join("trained", "word2vec_book.w2v"))



tsne = sklearn.manifold.TSNE(n_components=2, random_state=0)

all_word_vectors_matrix = word2vec_game.wv.syn0

all_word_vectors_matrix_2d = tsne.fit_transform(all_word_vectors_matrix)


points = pd.DataFrame(
    [
        (word, coords[0], coords[1])
        for word, coords in [
            (word, all_word_vectors_matrix_2d[word2vec_game.wv.vocab[word].index])
            for word in word2vec_game.wv.vocab
        ]
    ],
    columns=["word", "x", "y"]
)

print (points)
#points.head[10]

sns.set_context("poster")
points.plot.scatter("x", "y", s=10, figsize=(20, 12))

plt.show()

'''
def plot_region(x_bounds, y_bounds):
    slice = points[
        (x_bounds[0] <= points.x) &
        (points.x <= x_bounds[1]) &
        (y_bounds[0] <= points.y) &
        (points.y <= y_bounds[1])
        ]
    #ax = slice.plot.scatter("x", "y", s=35, figsize=(10, 8))

    ax = slice.plot.scatter("x", "y", s=35, figsize=(10, 8))
    for i, point in slice.iterrows():
        ax.text(point.x + 0.005, point.y + 0.005, point.word, fontsize=11)

plot_region(x_bounds=(4.0, 4.2), y_bounds=(-0.5, -0.1))

plot_region(x_bounds=(0, 1), y_bounds=(4, 4.5))

plt.show()

'''