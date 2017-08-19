#!/usr/bin/python

from __future__ import absolute_import, division, print_function
import codecs

import glob

import logging

import multiprocessing

import os

import pprint

import re

import nltk

import gensim.models.word2vec as w2v

import sklearn.manifold

import numpy as np

import matplotlib.pyplot as plt

import pandas as pd

import seaborn as sns


word2vec_game = w2v.Word2Vec.load(os.path.join("trained", "word2vec_game.w2v"))
word2vec_book = w2v.Word2Vec.load(os.path.join("trained", "word2vec_book.w2v"))



print ("\nwest")
print (word2vec_game.most_similar("west") )


print ()

def nearest_similarity_cosmul(model, start1, end1, end2):
    similarities = model.most_similar_cosmul(
        positive=[end2.lower(), start1.lower()],
        negative=[end1.lower()]
    )
    start2 = similarities[0][0]
    print("{start1} is related to {end1}, as {start2} is related to {end2}".format(**locals()))
    return start2

def similar_book_to_game(word):
    print ("--"+word+"--")
    out = '' #vec = word2vec_book.wv[word]
    w = [(word,0)]
    w.extend( word2vec_book.wv.most_similar(word))
    #w.append((word, 0))
    print (len(w))
    for i in w:
        print ( "--"+ i[0])
        try:
            vec = word2vec_game.most_similar(i[0])
            out = vec
            if len(vec) > 1: break
            pass
        except:
            pass

    for i in out:
        print (i[0])
    print ("---")
    return out


nearest_similarity_cosmul(word2vec_book,"west", "northwest", "northeast")
nearest_similarity_cosmul(word2vec_book,"north","south", "west")

nearest_similarity_cosmul(word2vec_game,"west", "northwest", "northeast")
nearest_similarity_cosmul(word2vec_game,"north","south", "west")

print()

#nearest_similarity_cosmul(word2vec_game,"game","gone","west")
#nearest_similarity_cosmul(word2vec_game,"game","west","gone")
nearest_similarity_cosmul(word2vec_game,"game","look","out")
nearest_similarity_cosmul(word2vec_game,"game","inventory","book")

similar_book_to_game("west")
similar_book_to_game("gone")
similar_book_to_game("up")
similar_book_to_game("look")

similar_book_to_game("book")
similar_book_to_game("game")
