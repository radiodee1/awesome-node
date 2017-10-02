#!/usr/bin/python

from __future__ import division, print_function

import os

import gensim.models.word2vec as w2v

import sklearn.manifold


import pandas as pd
import matplotlib.pyplot as plt

import seaborn as sns


word2vec_small = w2v.Word2Vec.load(os.path.join("trained", "word2vec_game.w2v"))
word2vec_game = w2v.Word2Vec.load(os.path.join("trained", "word2vec_book.w2v"))

print ("w2v loaded.")

tsne = sklearn.manifold.TSNE(n_components=2, random_state=0)

all_word_vectors_matrix = []
all_word_vectors_vocab = []

if False:
    for i in word2vec_small.wv.vocab:
        j = word2vec_game.wv.vocab[i].index
        all_word_vectors_matrix.append(word2vec_game.wv.syn0[j])
        all_word_vectors_vocab.append(i)

if True:
    list_g = ['goes','gone','went','going','western','eastern','southern','northern',
              'southerly','northerly','westerly','easterly']

    list_v = ['go','west','east','north','south']

    list_g.extend(list_v)
    print (list_g)

    for i in list_g:
        j = word2vec_game.wv.vocab[i].index
        all_word_vectors_matrix.append(word2vec_game.wv.syn0[j])
        all_word_vectors_vocab.append(i)


all_word_vectors_matrix_2d = tsne.fit_transform(all_word_vectors_matrix)

print ("matrix 2d done.")



if True:
    f = open("trained/word2vec_points.csv", "w")
    #z = 0
    for i in range(len(all_word_vectors_vocab)) :
        ii = list(all_word_vectors_vocab)[i]
        print (ii, all_word_vectors_matrix_2d[i][0], all_word_vectors_matrix_2d[i][1])
        f.write(ii +","+ str(all_word_vectors_matrix_2d[i][0])+","+ str(all_word_vectors_matrix_2d[i][1])+"\n")
        #z+=1
    f.close()

exit()
