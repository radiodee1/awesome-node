#!/usr/bin/python

from __future__ import absolute_import, division, print_function
import os
import gensim.models.word2vec as w2v
import numpy as np
import itertools
import math
import signal
import sys

import game


class OddVector( ):

    def __init__(self):
        self.mv = game.MeasureVec()
        self.mv.__init__()

        self.list_basic_wrong = []
        self.list_basic_right = []
        self.list_shift_wrong = []
        self.list_shift_right = []
        self.odd_vec = []
        self.start_list_len = 12
        self.g = None

        ''' test if a vector of all zeros works best of all '''
        self.test_zeros = False
        pass

    def game_setup(self):
        load_special = True
        self.g = game.Game()
        self.g.load_w2v(load_special=load_special)
        self.g.read_word_list()
        self.mv.set_w2v(w2v=self.g.word2vec_book)

    def check_odd_vector(self, game, odd_vec=[], debug_msg=False, list_try=[], list_correct=[]):

        g = game
        ''' list of possible inputs to try '''
        list_g = list_try

        ''' correct outputs in order '''
        list_i = list_correct

        if len(odd_vec) > 0:
            self.mv.set_odd_vec(odd_vec)

        correct = 0
        total = len(list_i)

        for z in range(len(list_g)):
            i = list_g[z]
            j = self.mv.resolve_word_closest(g.words_game, [i] , debug_msg=debug_msg)[0]
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

        self.list_basic_wrong = self.list_basic_wrong[:self.start_list_len]
        self.list_basic_right = self.list_basic_right[:self.start_list_len]

    def set_extra_list(self, list_right, list_wrong, combine=True, limit=20):

        if len(list_right) == 1 and len(list_wrong) > 1:
            y = list_right[0]
            list_right = []
            for x in list_wrong:
                list_right.append(y)

        if len(list_right) == len(list_wrong) and len(list_right) > 0 :
            if len(self.list_shift_right) > limit:
                self.list_shift_right.extend(list_right)
                self.list_shift_wrong.extend(list_wrong)

                self.list_shift_right = self.list_shift_right[- limit:]
                self.list_shift_wrong = self.list_shift_wrong[- limit:]
            if combine:
                self.list_basic_right.extend(self.list_shift_right)
                self.list_basic_wrong.extend(self.list_shift_wrong)
        pass

    def load_vec(self, name=""):
        odd_vec = []
        if len(name) == 0:
            name = "word2vec_book_vec.npy.txt"
        if os.path.isfile(os.path.join("trained", name)) and not self.test_zeros:
            odd_vec = np.loadtxt(os.path.join("trained", name))
            #print (odd_vec)
        else:
            odd_vec = np.zeros(300)
        self.odd_vec = odd_vec
        return odd_vec

    def save_vec(self, name="", odd_vec=[]):
        if len(name) == 0:
            name = "word2vec_book_vec.npy.txt"

        if os.path.isdir('trained') and not self.test_zeros:
            np.savetxt(os.path.join('trained',name), odd_vec)
            self.odd_vec = odd_vec

    def generate_perfect_vector(self, game, feature_mag=4.5,patch_size=50,var_len=300,fill_num=0,debug_msg=True,list_try=[],list_correct=[],tot_correct=12,multi_thread=False):
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
            if i == 0:
                vec_out = self.load_vec()

                #print (vec_out)
                #exit()
            ''' try out vector in game. '''
            #vec_out = np.array(vec_out)
            if (i < 10 and debug_msg) or False: print (vec_out, len(vec_out))

            if debug_msg or True:
                print (i, bin_tot,patch, saved_score,'--',
                   str (int((i / bin_tot) * 100)) + '% complete --', int(saved_score * num_of_correct),
                   'correct of',num_of_correct)

            if len(vec_out) > var_len: vec_out = vec_out[:var_len]

            if self.test_zeros: debug_msg = True
            out = self.check_odd_vector(g,odd_vec=vec_out, debug_msg=debug_msg,
                                   list_try=list_try[:tot_correct],
                                   list_correct=list_correct[:tot_correct])

            ''' save vector if it works. '''
            if i == 0: saved_score = out

            if out > saved_score and i > 1:
                saved_score = out
                self.save_vec(odd_vec=vec_out)
                print (vec_out,"----")
            if out > 0.9 and multi_thread:
                #exit()
                break
                pass
            if i >= bin_tot or self.test_zeros: # or i == 11:
                if debug_msg: print ("exit")
                break
            pass

class VectorOnce(object, OddVector):
    def __init__(self):
        OddVector.__init__(self)
        print ("VectorOnce: ctrl-c to stop")

        self.start_list_len = 12
        self.game_setup()
        self.set_starting_list()

        try:
            self.generate_perfect_vector(self.g,patch_size=10,debug_msg=False,list_try=self.list_basic_wrong,
                                         list_correct=self.list_basic_right,tot_correct=self.start_list_len,
                                         multi_thread=False)
        except KeyboardInterrupt:
            pass
        finally:
            print("---------")
            out = self.check_odd_vector(self.g, odd_vec=self.odd_vec, debug_msg=True,
                                        list_try=self.list_basic_wrong,
                                        list_correct=self.list_basic_right)
            print(out)

def main():
    VectorOnce()



if __name__ == "__main__":
    main()
