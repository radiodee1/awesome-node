from __future__ import absolute_import, division, print_function
import os
import gensim.models.word2vec as w2v
import matplotlib.pyplot as plt
import numpy as np
import itertools
import math
import sys

import game


class OddVector:

    def __init__(self):
        self.list_basic_wrong = []
        self.list_basic_right = []
        self.odd_vec = []
        pass

    def run(self):
        load_special = True
        g = game.Game()
        g.load_w2v(load_special=load_special)
        g.read_word_list()

    def check_odd_vector(self, game, odd_vec=[], debug_msg=False, list_try=[], list_correct=[]):

        g = game
        ''' list of possible inputs to try '''
        list_g = list_try

        ''' correct outputs in order '''
        list_i = list_correct

        if len(odd_vec) > 0:
            g.set_odd_vec(odd_vec)

        correct = 0
        total = len(list_i)

        for z in range(len(list_g)):
            i = list_g[z]
            j = g.resolve_word_closest(g.words_game, [i] ,odd_word=g.odd_word, debug_msg=debug_msg)[0]
            if j == list_i[z]: correct += 1
            pass

        if debug_msg: print (correct, "/", total, "or:", correct / total)

        return correct / total

    #############################


    def set_starting_list(self):
        ''' list of possible inputs to try '''
        self.list_basic_wrong = ['goes', 'gone', 'went', 'going',
                  'western', 'eastern', 'southern', 'northern'
            , 'southerly', 'northerly', 'westerly', 'easterly'
            , 'southeasterly', 'northeasterly', 'southwesterly', 'northwesterly'
            , 'southeastern', 'northeastern', 'southwestern', 'northwestern']

        ''' correct outputs in order '''
        self.list_basic_right = ['go', 'go', 'go', 'go',
                  'west', 'east', 'south', 'north'
            , 'south', 'north', 'west', 'east'
            , 'southeast', 'northeast', 'southwest', 'northwest'
            , 'southeast', 'northeast', 'southwest', 'northwest']



    def load_vec(self, name=""):
        odd_vec = []
        if len(name) == 0:
            name = "word2vec_book_vec.npy"
        if os.path.isfile(os.path.join("trained", name)):
            odd_vec = np.load(os.path.join("trained", name))
        return odd_vec

    def save_vec(self, name="", odd_vec=[]):
        if len(name) == 0:
            name = "word2vec_book_vec.npy"
        np.save(os.path.join("trained", name), odd_vec)

    def generate_perfect_vector(self, game, feature_mag=4.5,patch_size=50,var_len=600,fill_num=0,debug_msg=True,list_try=[],list_correct=[],tot_correct=12):
        ''' find vector that satisfies special requirements '''

        if patch_size == 0 or tot_correct == 0: exit()

        g = game
        #var_len = len(word2vec_book.wv['west'])
        num_of_correct = tot_correct #20
        patch = patch_size
        binary_len = int(math.ceil(var_len / patch))
        saved_score = 0
        if fill_num == 0 or fill_num >= patch:
            fill_num = patch
        if debug_msg: print (binary_len)

        bin_string = ''
        for i in range(binary_len):
            bin_string = bin_string + '1'
        bin_tot = int(bin_string,2)
        if debug_msg: print (bin_tot)
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
                self.load_vec()
                #if os.path.isfile(os.path.join("trained","word2vec_book_vec.npy")):
                #    vec_out = np.load(os.path.join("trained","word2vec_book_vec.npy"))
            ''' try out vector in game. '''
            #vec_out = np.array(vec_out)
            if i < 10 and False: print (vec_out, len(vec_out))

            if debug_msg:
                print (i, bin_tot,patch, saved_score,'--',
                   str (int((i / bin_tot) * 100)) + '% complete --', int(saved_score * num_of_correct),
                   'correct of',num_of_correct)

            if len(vec_out) > var_len: vec_out = vec_out[:var_len]

            out = self.check_odd_vector(g,odd_vec=vec_out, debug_msg=False,
                                   list_try=list_try[:tot_correct], list_correct=list_correct[:tot_correct])
            ''' save vector if it works. '''
            if out > saved_score:
                saved_score = out
                self.save_vec(odd_vec=vec_out)
                #np.save(os.path.join("trained","word2vec_book_vec"), vec_out)
            if out > 0.5:
                #exit()
                pass
            if i >= bin_tot: # or i == 11:
                if debug_msg: print ("exit")
                break
            pass
