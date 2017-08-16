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


'''

import textplayer.textPlayer as tp
t = tp.TextPlayer('zork1.z5')
start_info = t.run()
print (start_info)

command_in = ''

while command_in != 'q':
    command_in = raw_input("enter command :")
    command_in = command_in.strip()
    command_output = t.execute_command(command_in)
    print (command_output)

if t.get_score() != None:
    score, possible_score = t.get_score()
t.quit()
'''
