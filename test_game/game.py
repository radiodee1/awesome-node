from __future__ import print_function, division
import textplayer.textPlayer as player
import os
import gensim.models.word2vec as w2v
import numpy as np
import scipy.spatial as spatial


class MeasureVec:
    def __init__(self):
        self.words_all = []
        self.word2vec_book = None
        self.odd_vec = []

    ## convenience methods
    def set_w2v(self, w2v=None):
        self.word2vec_book = w2v

    def set_odd_vec(self, odd_vec=[]):
        self.odd_vec = odd_vec

    ## crucial methods
    def resolve_word_closest(self, list_suggested, list_command, odd_word=None , debug_msg=False, use_ending=False):
        list_out = []
        #
        #
        for word in list_command:
            if not  (word in self.words_all):
                num_best = -3
                word_best = ""
                vec_best = 1000000

                #
                for near in list_suggested:
                    ######
                    if use_ending: near = near + "zzz"
                    try:
                        ############
                        if len(self.odd_vec) == 0:

                            num = self.word2vec_book.wv.similarity(word, near)
                            if odd_word != None:

                                num = num + self.word2vec_book.wv.similarity(word,odd_word)
                                num = num + self.word2vec_book.wv.similarity(near,odd_word)
                            if debug_msg: print (word, near, odd_word, num)
                            if num > num_best and near != odd_word:
                                num_best = num
                                word_best = near
                        ############
                        if len(self.odd_vec) > 0:

                            word_vec = self._list_sum(positive=[word],negative=[])
                            near_vec = self._list_sum(positive=[near],negative=[])

                            vec = self._distance(near_vec, word_vec - self.odd_vec) ### - (subtraction)

                            if debug_msg: print(word, near, word_best, vec)

                            if vec < vec_best:
                                vec_best = vec
                                word_best = near

                    except NameError:
                        pass
                    ######
                    pass
                list_out.append(word_best)
                pass

            pass
        if debug_msg:
            print (list_out)
            #print (self.odd_vec)
        return list_out

    ### private methods
    def _distance(self, v1, v2):
        return spatial.distance.euclidean(v1,v2)

    def _list_sum(self, positive=[], negative=[]):
        if len(positive) > 0:
            sample = self.word2vec_book.wv[positive[0]]
        else:
            sample = self.word2vec_book.wv[negative[0]]
        tot = np.zeros_like(sample)

        for i in positive:
            sample = self.word2vec_book.wv[i]
            tot = np.add(tot , sample)

        for i in negative:
            sample = self.word2vec_book.wv[i]
            tot = np.subtract(tot ,  sample)
        return tot


class Game(object, MeasureVec):

    def __init__(self):
        MeasureVec.__init__(self)
        self.name = ""
        self.word2vec_game = None
        self.word2vec_book = None

        self.game = None
        self.words_last = []
        #self.gameplay_flag = True
        self.words_quit = ['q','quit','exit','save']
                            # 'save' was added so that frotz would not do that

        self.words_game = ['north','n','south','s','west','w','east','e',
                           'look','l','at',
                           'northeast','ne','northwest','nw','southeast','se','southwest','sw',
                           'get','take','drop','up','u','down','d','open','close',
                           'go','inventory','i','walk']
        self.words_all = []
        #self.words_suggested = []
        self.words_input = []

        self.words_correct = []
        self.bool_show_lists = False
        self.odd_word = None
        self.odd_vec = []

    def run(self):
        self.game  = player.TextPlayer("zork1.z5")
        self.load_w2v(load_special=True)
        self.load_odd_vec()
        self.read_word_list()


    def load_w2v(self,load_special=False):
        self.word2vec_game = w2v.Word2Vec.load(os.path.join("trained", "word2vec_game.w2v"))
        if not load_special:
            self.word2vec_book = w2v.Word2Vec.load(os.path.join("trained", "word2vec_book.w2v"))
        else:
            #print ("google w2v")
            self.word2vec_book = w2v.KeyedVectors.load_word2vec_format(os.path.join('trained','saved_google','GoogleNews-vectors-negative300.bin'),
                                                  binary=True)

    def load_odd_vec(self):
        name = 'word2vec_book_vec.npy.txt'
        if os.path.isfile(os.path.join("trained",name)):
            #print ("odd vec")
            self.odd_vec = np.loadtxt(os.path.join("trained",name), delimiter=',')
            #print (self.odd_vec)



    def read_word_list(self):
        self.words_all = self.words_game[:]
        if os.path.isfile("data/list.txt"):
            f = open("data/list.txt","r")
            for line in f:
                line = line.strip().lower()
                for word in line.split():
                    if not word in self.words_all:
                        self.words_all.append(word)
            f.close()
        #print (self.words_game)
        pass


    def play_loop(self):
        start_info = self.game.run()
        print(start_info)

        command_in = ''
        #self.gameplay_flag = True

        while command_in not in self.words_quit:

            if len(command_in.split()) > 0  and not  all( word in self.words_all for word in command_in.split() ):
                #self.gameplay_flag = True
                #self.words_suggested = []
                self.parse_input(command_in.split())
                self.words_input = command_in.split()
                self.print_list_suggested()

            #else : self.gameplay_flag = True
            if len(self.words_last) > 0:
                command_in = self.words_correct

            if  len(command_in) > 0:
                command_output = self.game.execute_command(command_in)
                ##
                print(command_output)

            command_in = raw_input("> ")
            command_in = command_in.strip().lower()
            if self.bool_show_lists: print(command_in.split())

    def play_stop(self):
        if self.game.get_score() != None:
            score, possible_score = self.game.get_score()
        self.game.quit()

    def parse_input(self, input):

        if True:
            self.set_odd_vec(self.odd_vec)
            self.words_correct = self.resolve_word_closest(self.words_game, input, debug_msg=False, use_ending=False)

            #self.words_last = input
        pass


    def print_list_suggested(self):

        if len(self.words_correct) > 0 and len(self.words_correct[0]) > 0 :
            zz = raw_input ("try: '"+ self.words_correct[0]+ "' [Y/n]:" )
            if zz.strip() == 'n' or zz.strip() == 'N':
                self.words_correct = []
            else:
                pass
                #print (self.words_correct)


def main():
    print("zork 1")
    g = Game()
    g.run()
    g.play_loop()
    g.play_stop()

if __name__ == "__main__":
    main()
