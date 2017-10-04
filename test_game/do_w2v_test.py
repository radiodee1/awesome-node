#!/usr/bin/python

from __future__ import absolute_import, division, print_function
import os
import gensim.models.word2vec as w2v
import matplotlib.pyplot as plt
import numpy as np
import game

g = game.Game()


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

'''
def similar_book_to_game(word):
    print ("--"+word+"--")
    out = '' #vec = word2vec_book.wv[word]
    w = [(word,0)]
    w.extend( word2vec_book.wv.most_similar(word, topn=30))
    #w.append((word, 0))
    print (len(w), w)
    for i in w:
        print ( "--"+ i[0])
        try:
            vec = word2vec_game.most_similar(i[0])
            out = vec
            if len(vec) > 1:
                print (">>", i[0])
                break
            pass
        except:
            pass

    for i in out:
        print (i[0])
    print ("---")
    return out
'''
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




if True:

    odd_word='inventory' #"monadologia"
    ''' by chance saved_37500_600 gives some good output with the word -monadologia- '''

    list_g = ['goes','gone','went','going','western','eastern','southern','northern'
              ,'southerly','northerly','westerly','easterly']
    list_h = ['go','go','go','go','north','south','west','east','north','south','west','east'] #,'northeast','southeast','southwest','northwest']

    #middle_value = word2vec_book.wv.most_similar(positive=list_h, negative=list_g, topn=4)

    middle_value_string = [[odd_word]]
    middle_value_vec = [[list_sum(positive=list_h, negative=list_g)]]
    middle_value_vec = [[list_sum(positive=['inventory'])]]

    print ('====')
    print (middle_value_string, len(middle_value_string[0][0]))
    g.load_w2v()
    g.read_word_list()

    if False:
        ''' string input '''
        g.pre_game(odd_word=middle_value_string[0][0], odd_vec=[],debug_msg=True,special_invert=True, invert_all=True)
    else:
        ''' vector input '''
        g.pre_game(odd_word=[], odd_vec=middle_value_vec[0][0], debug_msg=True, special_invert=False, invert_all=False)

    for i in list_g:
        g.resolve_word_closest(g.words_game, [i] ,odd_word=g.odd_word, debug_msg=True)
        pass

    print ('-----')
    x = list_sum(positive=list_h,negative=list_g)
    word = word2vec_book.wv.most_similar(positive=[x],negative=[],topn=5)
    g.pre_game(odd_word=word, debug_msg=True,special_invert=True,invert_all=False)