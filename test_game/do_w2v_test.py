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



print ("\nwest")
print (word2vec_game.most_similar("west") )


#print ("\nAerys")
#print (word2vec_game.most_similar("Aerys".lower() ) )

#print ("\ndirewolf")
#print (word2vec_game.most_similar("direwolf".lower() ) )

print ()

def nearest_similarity_cosmul(start1, end1, end2):
    similarities = word2vec_game.most_similar_cosmul(
        positive=[end2.lower(), start1.lower()],
        negative=[end1.lower()]
    )
    start2 = similarities[0][0]
    print("{start1} is related to {end1}, as {start2} is related to {end2}".format(**locals()))
    return start2

#nearest_similarity_cosmul("Stark", "Winterfell", "Riverrun")
#nearest_similarity_cosmul("Jaime", "sword", "wine")
#nearest_similarity_cosmul("Arya", "Nymeria", "dragons")

print ("\ngo")
print (word2vec_game.most_similar("go"))
print ("\ngone")
print (word2vec_game.most_similar("gone"))
print ()
nearest_similarity_cosmul("go","west","west")
print ("\nw")
print (word2vec_game.most_similar("w"))



