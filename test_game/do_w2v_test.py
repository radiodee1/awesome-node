#!/usr/bin/python

from __future__ import absolute_import, division, print_function
import os
import gensim.models.word2vec as w2v
import matplotlib.pyplot as plt
import numpy as np
import itertools
import math
import sys

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

print ('''
        usage: do_w2v_test.py 0 -load-special     (list words and translations)
               do_w2v_test.py 20 -load-special    (generate odd_vec and save)
               do_w2v_test.py -load-special       (show key analogies)
    ''')

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


if load_book_and_game:

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

def list_sum(model, positive=[], negative=[]):
    sample = model.wv[positive[0]]
    tot = np.zeros_like(sample)

    for i in positive:
        sample = model.wv[i]
        tot = tot + sample

    for i in negative:
        sample = model.wv[i]
        tot = tot - sample
    return tot



def check_odd_vector(g, odd_vec=[], debug_msg=False, list_try=[], list_correct=[]):

    ''' by chance saved_37500_600 gives some good output with the word -monadologia- '''
    odd_word=None#'inventory' #"monadologia"

    ''' list of possible inputs to try '''
    list_g = list_try

    ''' correct outputs in order '''
    list_i = list_correct

    choose_string_input = False

    if debug_msg: print ('====')

    middle_value_string = [[odd_word]]

    if True:
        middle_value_vec = [[list_sum(g.word2vec_book,positive=list_i, negative=list_g)]]
        pass

    if len(odd_vec) > 0:
        middle_value_vec = [[odd_vec]]
        choose_string_input = False

    correct = 0
    total = len(list_i)

    if choose_string_input:
        ''' string input '''
        if debug_msg: print(middle_value_string)#, len(middle_value_string[0][0]))
        #g.pre_game(odd_word=middle_value_string[0][0], odd_vec=[],debug_msg=debug_msg,special_invert=True, invert_all=False)
    else:
        ''' vector input '''
        #if debug_msg: print (middle_value_vec, len(middle_value_vec[0][0]))
        if debug_msg: print ('vector input')
        #g.pre_game(odd_word=[], odd_vec=middle_value_vec[0][0], debug_msg=debug_msg, special_invert=False, invert_all=False)

    for z in range(len(list_g)):
        i = list_g[z]
        j = g.resolve_word_closest(g.words_game, [i] ,odd_word=g.odd_word, debug_msg=debug_msg)[0]
        if j == list_i[z]: correct += 1
        pass

    if debug_msg: print ('-----')
    print (correct, "/", total, "or:", correct / total)

    if debug_msg: vec = np.array(middle_value_vec[0][0])
    if debug_msg: word = g.word2vec_book.wv.most_similar(positive=[vec],negative=[],topn=5)
    if debug_msg: print (word)

    return correct / total

#############################


if not load_book_and_game:
    ''' list of possible inputs to try '''
    list_g = ['goes', 'gone', 'went', 'going',
              'western', 'eastern', 'southern', 'northern'
        , 'southerly', 'northerly', 'westerly', 'easterly'
        , 'southeasterly', 'northeasterly', 'southwesterly', 'northwesterly'
        , 'southeastern', 'northeastern', 'southwestern', 'northwestern']

    ''' correct outputs in order '''
    list_i = ['go', 'go', 'go', 'go',
              'west', 'east', 'south', 'north'
        , 'south', 'north', 'west', 'east'
        , 'southeast', 'northeast', 'southwest', 'northwest'
        , 'southeast', 'northeast', 'southwest', 'northwest']

    g = game.Game()
    g.load_w2v(load_special=load_special)
    g.read_word_list()

if not load_book_and_game:
    odd_vec = []
    if os.path.isfile(os.path.join("trained", "word2vec_book_vec.npy")):
        odd_vec = np.load(os.path.join("trained", "word2vec_book_vec.npy"))
    check_odd_vector(g, odd_vec=odd_vec, debug_msg=True,list_try=list_g[:vocab_num],list_correct=list_i[:vocab_num])
    print (np.mean(np.abs(g.word2vec_book.wv['west'])),":mean of 'west'")

if False and len(odd_vec)> 0:
    print (g.word2vec_book.wv.most_similar(positive=[odd_vec], topn=10))


def generate_perfect_vector(g, feature_mag=4.5,patch_size=50,var_len=600,fill_num=0,debug_msg=True,list_try=[],list_correct=[],tot_correct=12):
    ''' find vector that satisfies special requirements '''

    if patch_size == 0 or tot_correct == 0: exit()

    #var_len = len(word2vec_book.wv['west'])
    num_of_correct = tot_correct #20
    patch = patch_size
    binary_len = int(math.ceil(var_len / patch))
    saved_score = 0
    if fill_num == 0 or fill_num >= patch:
        fill_num = patch
    print (binary_len)

    bin_string = ''
    for i in range(binary_len):
        bin_string = bin_string + '1'
    bin_tot = int(bin_string,2)
    print (bin_tot)
    for i in itertools.count(start=0,step=1): #xrange(bin_tot):
        ''' make vector here. '''
        vec_out = []
        for j in range(binary_len):
            xxx = 1 << j
            zzz = (i & xxx) >> j

            if i > xxx -1:
                if zzz == 0:
                    for k in range(patch):
                        if k <= fill_num:
                            #vec_out.append(- feature_mag)
                            vec_out.insert(0, -feature_mag)
                        else:
                            #vec_out.append(0.0)
                            vec_out.insert(0, 0.0)
                else:
                    for k in range(patch):
                        if k <= fill_num:
                            #vec_out.append(+ feature_mag)
                            vec_out.insert(0, feature_mag)
                        else:
                            #vec_out.append(0.0)
                            vec_out.insert(0, 0.0)
            else:
                for k in range(patch):
                    vec_out.append(0.0)
                    #vec_out.insert(0, 0.0)

        ''' try saved vector '''
        if i == 1:
            if os.path.isfile(os.path.join("trained","word2vec_book_vec.npy")):
                vec_out = np.load(os.path.join("trained","word2vec_book_vec.npy"))
        ''' try out vector in game. '''
        #vec_out = np.array(vec_out)
        if i < 10 and False: print (vec_out, len(vec_out))

        print (i, bin_tot,patch, saved_score,'--',
               str (int((i / bin_tot) * 100)) + '% complete --', int(saved_score * num_of_correct),
               'correct of',num_of_correct)

        if len(vec_out) > var_len: vec_out = vec_out[:var_len]

        out = check_odd_vector(g,odd_vec=vec_out, debug_msg=False,
                               list_try=list_try[:tot_correct], list_correct=list_correct[:tot_correct])
        ''' save vector if it works. '''
        if out > saved_score:
            saved_score = out
            np.save(os.path.join("trained","word2vec_book_vec"), vec_out)
        if out > 0.5:
            #exit()
            pass
        if i >= bin_tot: # or i == 11:
            print ("exit")
            break
        pass

if find_perfect_num and not load_book_and_game:
    generate_perfect_vector(g, feature_mag=0.5, patch_size=patch_size, fill_num=0,var_len=300,
                            list_try=list_g, list_correct=list_i,tot_correct=vocab_num) ## 20