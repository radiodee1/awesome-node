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
from nltk.tokenize import TweetTokenizer, sent_tokenize, PunktSentenceTokenizer
from nltk.stem import *
import gensim.models.word2vec as w2v



#########################################

def sentence_to_wordlist(raw, sentence_label="", pos_tag=False):
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

    if pos_tag:
        tag = []
        words = nltk.pos_tag(words)
        for word in words:
            tag.append(word[0])
            tag.append(word[1].decode("utf-8"))
        words = tag
        #print (words)
        pass

    if len(sentence_label) > 0: words.append(sentence_label)
    #print (words)
    return words

########################################

test = []

if False:
    test = [["I go to school."],[" I've gone to school."],[" go north."],[" go south."],[" go east."],[" go west."],[" move south."]]


    new_test = []
    for t in test:
        z = sentence_to_wordlist(t, pos_tag=True)
        new_test.append(z)
        #print (z)
    test = new_test
    print (test)

#exit()

###########################################

def assemble_corpus(glob_txt, stem_words=False, sentence_label="", pos_tag=False, tweet_tag=False, print_sentences=False):
    pass

    #add everything once

    #add zork text twice more
    book_filenames = sorted(glob.glob(glob_txt))

    #book_filenames.extend(sorted(glob.glob("data/z*.txt")))

    print (book_filenames)

    print ("stage: start")

    corpus_raw = u""
    for book_filename in book_filenames:
        print("stage: Reading '{0}'...".format(book_filename))
        with codecs.open(book_filename, "r", "utf-8") as book_file:
            corpus_raw += book_file.read()
        print("stage: Corpus is now {0} characters long".format(len(corpus_raw)))
        print()

    pre_sent = sent_tokenize(corpus_raw)

    corpus_raw = u""

    #########################

    if tweet_tag:
        tokenizer = TweetTokenizer()

        print ("stage: tweet")

        post_sent = []
        for i in pre_sent:
            raw_sentences = tokenizer.tokenize(i) ##tweet style

            post_sent.append(raw_sentences)
            #print (raw_sentences)

        raw_sentences = post_sent
        post_sent = []

    else:
        raw_sentences = pre_sent
        pre_sent = []

    ###########################

    if pos_tag: print ("stage: pos tagging")

    sentences = []
    for raw_sentence in raw_sentences:
        if len(raw_sentence) > 0:
            if not type(raw_sentence) == list: raw_sentence = raw_sentence.split()
            z = sentence_to_wordlist(raw_sentence, sentence_label=sentence_label, pos_tag=pos_tag)
            if len(z) > 0:
                sentences.append(z)

    # stem words and add them
    if stem_words:
        print ("stage: stem")
        stemmer = SnowballStemmer("english", ignore_stopwords=True)
        for raw_sentence in raw_sentences:
            if len(raw_sentence) > 0:
                sent = sentence_to_wordlist(raw_sentence)
                sent = [stemmer.stem(word) for word in sent]
                sentences.append(sent)

    if print_sentences: print(sentences[-1:])
    #print(sentence_to_wordlist(raw_sentences[0], pos_tag=pos_tag))

    token_count = sum([len(sentence) for sentence in sentences])
    print("stage: The corpus contains {0:,} tokens".format(token_count))

    return sentences

####################################################
game_glob1 = "data/zork1-output.txt" ## actual commands processed
game_glob2 = "data/*.txt" ## not for good game corpus
game_glob3 = "data/wiki*.txt"
game_glob4 = "data/zork1-e*.txt"

if True:
    sentences_game = assemble_corpus(game_glob1,    stem_words=False)

if True:
    sentences_zork = assemble_corpus(game_glob2, pos_tag=False)

if True:
    sentences_book = []
    sentences_book = assemble_corpus(game_glob3, pos_tag=False)

if True:
    sentences_book.extend(sentences_zork)
    sentences_book.extend(test)

#print (sentences_book)

if False:
    print ("o text")
    print (assemble_corpus("data/zork1-o*.txt", pos_tag=False))
    exit()
#exit()
####################################################

num_features =   100
# Minimum word count threshold.
min_word_count = 1

# Number of threads to run in parallel.
#more workers, faster we train
num_workers = multiprocessing.cpu_count()

# Context window length.
context_size = 7 # 7

# Downsample setting for frequent words.
#0 - 1e-5 is good for this
downsampling =  0#1e-3

# Seed for the RNG, to make the results reproducible.
#random number generator
#deterministic, good for debugging
seed = 1

epochs = 500

###################################################
if False:
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

    print("stage: Word2Vec game vocabulary length:", len(word2vec_game.wv.vocab))

if False:
    print ("stage: train")

    word2vec_game.train(sentences_game,
                        total_examples=len(word2vec_game.wv.vocab),
                        epochs=epochs)

    if not os.path.exists("trained"):
        os.makedirs("trained")

    word2vec_game.save(os.path.join("trained", "word2vec_game.w2v"))

#exit()
############################################
num_features =  900 #  100
# Minimum word count threshold.
min_word_count = 2 # 3

# Number of threads to run in parallel.
#more workers, faster we train
num_workers = multiprocessing.cpu_count()

# Context window length.
context_size = 7 # 7

# Downsample setting for frequent words.
#0 - 1e-5 is good for this
downsampling = 0 #1e-2

# Seed for the RNG, to make the results reproducible.
#random number generator
#deterministic, good for debugging
seed = 1

epochs = 5

if True:
    word2vec_book = w2v.Word2Vec(
        sg=1,
        seed=seed,
        workers=num_workers,
        size=num_features,
        min_count=min_word_count,
        window=context_size,
        sample=downsampling
    )

    word2vec_book.build_vocab(sentences_book)

    print("stage: Word2Vec book vocabulary length:", len(word2vec_book.wv.vocab))

if True:
    print ("stage: train")

    word2vec_book.train(sentences_book,
                        total_examples=len(word2vec_book.wv.vocab),
                        epochs=epochs)

    if not os.path.exists("trained"):
        os.makedirs("trained")

    word2vec_book.save(os.path.join("trained", "word2vec_book.w2v"))


