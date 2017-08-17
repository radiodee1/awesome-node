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
from nltk.tokenize import TweetTokenizer, sent_tokenize
from nltk.stem import *
import gensim.models.word2vec as w2v

import sklearn.manifold

import numpy as np

import matplotlib.pyplot as plt

import pandas as pd

import seaborn as sns

nltk.download("punkt")
nltk.download("stopwords")

#book_filenames = sorted(glob.glob("data/*.txt"))

#########################################

def sentence_to_wordlist(raw):
    pre = raw #raw.split()
    raw = ""
    #w = []
    if not (type(pre) is list): return [pre.lower()]
    for x in pre:
        if not x.endswith( u"'s"):
            #w.append(x)
            raw = raw + " " + x
        else:
            #print("missed s")
            pass
    clean = re.sub("[^a-zA-Z]"," ", raw)

    words = clean.split()
    words = [x.lower() for x in words]

    #print (words)
    return words

###########################################

def assemble_corpus(glob_txt, stem_words=False):
    pass

    #add everything once

    #add zork text twice more
    book_filenames = sorted(glob.glob(glob_txt))

    #book_filenames.extend(sorted(glob.glob("data/z*.txt")))

    print (book_filenames)

    corpus_raw = u""
    for book_filename in book_filenames:
        print("Reading '{0}'...".format(book_filename))
        with codecs.open(book_filename, "r", "utf-8") as book_file:
            corpus_raw += book_file.read()
        print("Corpus is now {0} characters long".format(len(corpus_raw)))
        print()

    pre_sent = sent_tokenize(corpus_raw)

    tokenizer = TweetTokenizer()


    post_sent = []
    for i in pre_sent:
        raw_sentences = tokenizer.tokenize(i) ##tweet style

        post_sent.append(raw_sentences)
        #print (raw_sentences)

    raw_sentences = post_sent

    sentences = []
    for raw_sentence in raw_sentences:
        if len(raw_sentence) > 0:
            sentences.append(sentence_to_wordlist(raw_sentence))

    # stem words and add them
    if stem_words:
        stemmer = SnowballStemmer("english", ignore_stopwords=True)
        for raw_sentence in raw_sentences:
            if len(raw_sentence) > 0:
                sent = sentence_to_wordlist(raw_sentence)
                sent = [stemmer.stem(word) for word in sent]
                sentences.append(sent)

    print(raw_sentences[10])
    print(sentence_to_wordlist(raw_sentences[10]))

    token_count = sum([len(sentence) for sentence in sentences])
    print("The book corpus contains {0:,} tokens".format(token_count))

    return sentences

####################################################

sentences = assemble_corpus("data/got*.txt", stem_words=False)
sentences_game = assemble_corpus("data/z*.txt", stem_words=False)


num_features =  100 # 300
# Minimum word count threshold.
min_word_count = 3

# Number of threads to run in parallel.
#more workers, faster we train
num_workers = multiprocessing.cpu_count()

# Context window length.
context_size = 4 # 7

# Downsample setting for frequent words.
#0 - 1e-5 is good for this
downsampling = 1e-3

# Seed for the RNG, to make the results reproducible.
#random number generator
#deterministic, good for debugging
seed = 1

###################################################

word2vec_game = w2v.Word2Vec(
    sg=1,
    seed=seed,
    workers=num_workers,
    size=num_features,
    min_count=min_word_count,
    window=context_size,
    sample=downsampling
)

word2vec_game.build_vocab(sentences_game)

print("Word2Vec vocabulary length:", len(word2vec_game.wv.vocab))

word2vec_game.train(sentences_game,
                    total_examples=len(word2vec_game.wv.vocab),
                    epochs=50)

if not os.path.exists("trained"):
    os.makedirs("trained")

word2vec_game.save(os.path.join("trained", "word2vec_game.w2v"))

############################################


word2vec_book = w2v.Word2Vec(
    sg=1,
    seed=seed,
    workers=num_workers,
    size=num_features,
    min_count=min_word_count,
    window=context_size,
    sample=downsampling
)

word2vec_book.build_vocab(sentences)

print("Word2Vec vocabulary length:", len(word2vec_book.wv.vocab))

word2vec_book.train(sentences,
                    total_examples=len(word2vec_book.wv.vocab),
                    epochs=50)

if not os.path.exists("trained"):
    os.makedirs("trained")

word2vec_book.save(os.path.join("trained", "word2vec_book.w2v"))


