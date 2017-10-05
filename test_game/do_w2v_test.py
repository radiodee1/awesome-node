#!/usr/bin/python

from __future__ import absolute_import, division, print_function
import os
import gensim.models.word2vec as w2v
import matplotlib.pyplot as plt
import numpy as np
import game



word2vec_game = w2v.Word2Vec.load(os.path.join("trained", "word2vec_game.w2v"))
word2vec_book = w2v.Word2Vec.load(os.path.join("trained", "word2vec_book.w2v"))

if False:
    word2vec_book = w2v.KeyedVectors.load_word2vec_format(os.path.join('trained','saved_google','GoogleNews-vectors-negative300.bin'),
                                                  binary=True)

if False:
    print ("\ngo")
    print (word2vec_book.most_similar("go", topn=10) )
    print ("went")
    print (word2vec_book.most_similar("went", topn=60))

    print ()

def nearest_similarity_cosmul(model, start1, end1, end2):
    similarities = model.most_similar_cosmul(
        positive=[end2, start1],
        negative=[end1], topn=20
    )

    start2 = similarities[0][0]
    print("{start1} is related to {end1}, as {start2} is related to {end2}".format(**locals()))
    print (similarities)

    return start2

def nearest_similarity(model, start1, end1, end2):
    similarities = model.most_similar(
        positive=[end2, start1],
        negative=[end1], topn=20
    )

    start2 = similarities[0][0]
    print("{start1} is related to {end1}, as {start2} is related to {end2}".format(**locals()))
    print (similarities)

    return start2


if False:

    print ("---------------")
    print ("book")
    nearest_similarity_cosmul(word2vec_book,"man", "king", "queen")

    nearest_similarity_cosmul(word2vec_book,"north","south", "west")
    nearest_similarity_cosmul(word2vec_book,"west", "northwest", "northeast")
    nearest_similarity_cosmul(word2vec_book,"go","west", "west")

    print()

    print ('go','west',word2vec_book.wv.similarity("go","west"))
    print ('going','west',word2vec_book.wv.similarity("going","west"))
    print ('goes','west',word2vec_book.wv.similarity("goes","west"))
    print ('went','west',word2vec_book.wv.similarity("went","west"))
    print ('gone','west',word2vec_book.wv.similarity("gone","west"))

    print (word2vec_book.wv.doesnt_match("go goes gone went going".split()))


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

if False:
    #graph_compare('going','gone')
    graph_compare('northwest','western')
    #graph_compare("go","gone")

def list_sum(positive=[], negative=[]):
    sample = word2vec_book.wv[positive[0]]
    tot = np.zeros_like(sample)

    for i in positive:
        sample = word2vec_book.wv[i]
        tot = tot + sample

    for i in negative:
        sample = word2vec_book.wv[i]
        tot = tot - sample
    return tot



def check_odd_vector(g, odd_vec=[], debug_msg=False):

    odd_word='inventory' #"monadologia"
    ''' by chance saved_37500_600 gives some good output with the word -monadologia- '''

    list_g = ['goes','gone','went','going','western','eastern','southern','northern'
              ,'southerly','northerly','westerly','easterly']
    ''' list of possible inputs to try '''

    list_h = ['go','go','go','go','north','south','west','east','north','south','west','east']
    ''' list of words to subtract from possible inputs - no particular order '''

    #list_h = ['go','north','south','west','east'] #,'northeast','southeast','southwest','northwest']

    list_i = ['go','go','go','go','west','east','south','north','south','north','west','east']
    ''' correct outputs in order '''

    choose_string_input = True

    if debug_msg: print ('====')

    middle_value_string = [[odd_word]]
    middle_value_vec = [[list_sum(positive=list_h, negative=list_g)]]
    #middle_value_vec = [[g.list_sum(negative=['inventory'])]]
    #middle_value_vec = [[g.list_sum(positive=['monadologia'])]]

    if len(odd_vec) > 0:
        middle_value_vec = [[odd_vec]]
        choose_string_input = False

    correct = 0
    total = len(list_i)

    if choose_string_input:
        ''' string input '''
        if debug_msg: print(middle_value_string, len(middle_value_string[0][0]))
        g.pre_game(odd_word=middle_value_string[0][0], odd_vec=[],debug_msg=debug_msg,special_invert=True, invert_all=True)
    else:
        ''' vector input '''
        if debug_msg: print (middle_value_vec, len(middle_value_vec[0][0]))
        g.pre_game(odd_word=[], odd_vec=middle_value_vec[0][0], debug_msg=debug_msg, special_invert=False, invert_all=False)

    for z in range(len(list_g)):
        i = list_g[z]
        j = g.resolve_word_closest(g.words_game, [i] ,odd_word=g.odd_word, debug_msg=debug_msg)[0]
        if j == list_i[z]: correct += 1
        pass

    if debug_msg: print ('-----')
    print (correct, "/", total, "or:", correct / total)
    
    if debug_msg: word = word2vec_book.wv.most_similar(positive=[middle_value_vec[0][0]],negative=[],topn=5)
    if debug_msg: print (word)

    return correct / total

#############################
g = game.Game()
g.load_w2v()
g.read_word_list()

check_odd_vector(g)