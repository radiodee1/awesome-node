#!/usr/bin/python

from __future__ import absolute_import, division, print_function
import os
import gensim.models.word2vec as w2v
import logging
import matplotlib.pyplot as plt
import numpy as np
import itertools
import math
import sys
import scipy.spatial as spatial

import game


option_flag = "-no-find"
option_load = "-load-special"

load_book_and_game = False ### False
find_perfect_num = False
patch_size = 50
load_special = False
vocab_num = 12

if len(sys.argv) > 1:
    load_book_and_game = False

    try:
        patch_size = int(sys.argv[1])
        find_perfect_num = True
        if len(sys.argv) > 2 and str(sys.argv[2]) == option_load:
            load_special = True
        pass
    except:

        if len(sys.argv) > 1 and str(sys.argv[1]) == option_flag:
            find_perfect_num = False
        if len(sys.argv) > 1 and (str(sys.argv[1]) == option_load or str(sys.argv[2] == option_load)):
            load_special = True
            if len(sys.argv) == 2: load_book_and_game = True
    if not load_book_and_game: vocab_num = int(raw_input('Num of values in vocab list? [12,20] '))
else:
    load_book_and_game = True

#####################################

if load_book_and_game:
    word2vec_game = w2v.Word2Vec.load(os.path.join("trained", "word2vec_game.w2v"))
    if not load_special:
        word2vec_book = w2v.Word2Vec.load(os.path.join("trained", "word2vec_book.w2v"))

    else:
        word2vec_book = w2v.KeyedVectors.load_word2vec_format(os.path.join('trained','saved_google','GoogleNews-vectors-negative300.bin'), binary=True)
        #word2vec_book = w2v.KeyedVectors.load_word2vec_format(os.path.join('trained','saved_freebase','freebase-vectors-skipgram1000-en.bin'), binary=True)

    if os.path.isfile(os.path.join('trained','word2vec_book_vec.npy')):
        odd_vec = np.load(os.path.join('trained','word2vec_book_vec.npy'))
        print (odd_vec)

if False:
    print ("\ngo")
    print (word2vec_book.most_similar("go", topn=10) )
    print ("went")
    print (word2vec_book.most_similar("went", topn=60))

    print ()

def nearest_similarity_cosmul(model, start1, end1, end2):
    if not load_special or True:
        similarities = model.most_similar_cosmul(
            positive=[end2, start1],
            negative=[end1], topn=20
        )

    if load_special and False:
        similarities = model.most_similar_cosmul(
            positive=[ '/en/'+end2 , '/en/'+start1],
            negative=[ '/en/'+end1], topn=5
        )

    start2 = similarities[0][0]
    print("{start1} is related to {end1}, as {start2} is related to {end2}".format(**locals()))
    #print (similarities)

    return start2

def nearest_similarity(model, start1, end1, end2):
    similarities = model.most_similar(
        positive=[end2, start1],
        negative=[end1], topn=20
    )

    start2 = similarities[0][0]
    print("{start1} is related to {end1}, as {start2} is related to {end2}".format(**locals()))
    #print (similarities)

    return start2

############################################################

def _distance( v1, v2):
    #return spatial.distance.euclidean(v1,v2)
    #return np.linalg.norm(v1 - v2)
    return  spatial.distance.cosine(v1,v2)

def _list_sum(model, positive=[], negative=[]):
    tot = np.zeros(300)

    for i in positive:
        sample = model.wv[i]
        tot = np.add(tot , sample)
        print(tot[0])
    print("---")
    for i in negative:
        sample = model.wv[i]
        tot = np.subtract(tot ,  sample)
        print(tot[0])
    return tot

def mult_similarity(model, vocab=[],list_pos=[], list_neg=[], word=''):
    list_pos.append(word)
    #list_neg.append(word)
    #list_pos.extend(list_neg)
    print(list_pos)
    print(list_neg)
    sum = _list_sum(model, positive=list_pos, negative=list_neg)
    dist_chosen = 10000000
    dist_word = ''
    for i in vocab:
        #vec_voc = np.zeros(300)
        dist = 0
        try:
            vec_voc = model.wv[i]
            dist = _distance(sum,vec_voc)
            if dist < dist_chosen:
                dist_chosen = dist
                dist_word = i
        except:
            #print("word not found",i)
            pass
        finally:
            print(i, dist)
    print("#", dist_word, dist_chosen)
    pass


###########################################################

if load_book_and_game and False:

    #print (list(word2vec_book.vocab))
    print ("---------------")
    print ()
    nearest_similarity_cosmul(word2vec_book,"man", "king", "queen")
    print ()
    nearest_similarity_cosmul(word2vec_book,"north","south", "west")

    print ('\nsometimes non-opposites work')
    nearest_similarity_cosmul(word2vec_book, 'north','west', 'south')
    print ()
    nearest_similarity_cosmul(word2vec_book,"west", "northwest", "northeast")
    nearest_similarity_cosmul(word2vec_book,"northwest","northwestern", "northeastern")
    nearest_similarity_cosmul(word2vec_book,"northwesterly","southwesterly", "northeasterly")
    nearest_similarity_cosmul(word2vec_book,'northwestern','southwestern','southeastern')
    print ('\nopposite directions')
    nearest_similarity_cosmul(word2vec_book,'northerly','north','south')
    nearest_similarity_cosmul(word2vec_book, 'west','western','eastern')
    print ('\nly ending - opposite directions')
    nearest_similarity_cosmul(word2vec_book, 'northerly','north','south')
    nearest_similarity_cosmul(word2vec_book, 'southerly','south','north')
    nearest_similarity_cosmul(word2vec_book, 'easterly','east', 'west')
    print ('\nly more obscure')
    nearest_similarity_cosmul(word2vec_book, 'westerly','west','east')
    print('\nern ending - opposite directions')
    nearest_similarity_cosmul(word2vec_book, 'northern','north','south')
    nearest_similarity_cosmul(word2vec_book, 'western','west','east')
    print ('\nern ending - not opposites')
    nearest_similarity_cosmul(word2vec_book, 'northern','north', 'east')

if True:
    vv = game.Vocab()
    vv.set_starting_list()
    vv.set_game_lists()
    vv.set_graph_list()
    v = vv.words_game
    list_pos = ['northern']#,'southerly','eastward']
    list_neg = ['north']#,'south','east']
    print(v)

    print ("-----")
    mult_similarity(word2vec_book,v,list_pos=list_pos,list_neg=list_neg,word='western')

    nearest_similarity_cosmul(word2vec_book, 'north', 'northern', 'eastern')
    nearest_similarity_cosmul(word2vec_book, 'north', 'northern', 'western')


if False:
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    word2vec_book.wv.accuracy("data/questions-words.txt")
    ## good values 77.1 % with GoogleNews model

if False:
    print ('go','west',word2vec_book.wv.similarity("go","west"))
    print ('going','west',word2vec_book.wv.similarity("going","west"))
    print ('goes','west',word2vec_book.wv.similarity("goes","west"))
    print ('went','west',word2vec_book.wv.similarity("went","west"))
    print ('gone','west',word2vec_book.wv.similarity("gone","west"))

    #print (word2vec_book.wv.doesnt_match("go goes gone went going".split()))


def graph_compare(word1, word2):
    vec1 = word2vec_book.wv[word1]
    y1 = np.arange(len(vec1))
    vec2 = word2vec_book.wv[word2]
    y2 = np.arange(len(vec2))

    plt.figure(1)
    plt.subplot(211)
    plt.title(word1)
    plt.bar(y1,vec1)
    plt.subplot(212)
    plt.title(word2)
    plt.bar(y2,vec2)
    plt.show()

if load_book_and_game and False:
    #graph_compare('going','gone')
    graph_compare('northwest','western')
    #graph_compare("go","gone")


#exit()

########################################################################
