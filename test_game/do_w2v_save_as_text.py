#!/usr/bin/python

from __future__ import absolute_import, division, print_function
import codecs

import glob

import logging

import multiprocessing

import os

import pprint
import io
import re

import nltk
from nltk.tokenize import TweetTokenizer, sent_tokenize, PunktSentenceTokenizer
from nltk.stem import *
import gensim.models.word2vec as w2v

if True:
    print("stage: load model")
    word2vec_book = w2v.Word2Vec.load(os.path.join("trained", "word2vec_book.w2v"))
    print("stage: save model")
    word2vec_book.wv.save_word2vec_format(os.path.join("trained", "word2vec_book.w2v.txt"),binary=False)
