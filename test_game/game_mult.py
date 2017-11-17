#!/usr/bin/python

from __future__ import absolute_import, division, print_function
import gensim.models.word2vec as w2v
import scipy.spatial as spatial
import os
import numpy as np

import game as game_learn


class MeasureVecMult:
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
                    word_print_near = "[" + near + "]"
                    word_print_word = "[" + word + "]"
                    word_print_bool = True
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
                            word_print_word = word
                            near_vec = self._list_sum(positive=[near],negative=[])
                            word_print_near = near
                            word_print_bool = False
                            vec = self._distance(near_vec, word_vec * self.odd_vec) ### - (multipllication)

                            if debug_msg:
                                if not word_print_bool and True:
                                    print(word, near, word_best, vec)
                                else:
                                    print (word_print_word + " ---- " + word_print_near)

                            if vec < vec_best:
                                vec_best = vec
                                word_best = near


                        pass
                    except KeyboardInterrupt:
                        raise KeyboardInterrupt()
                        pass
                    except:
                        if debug_msg: print(word_print_word + " ---- " + word_print_near)
                        pass
                    ######
                    pass
                list_out.append(word_best)
                pass
            print ("mult here")
            pass
        if debug_msg:
            print (list_out)
            #print (self.odd_vec)
        return list_out

    ### private methods
    def _distance(self, v1, v2):
        return spatial.distance.euclidean(v1,v2)

    def _list_sum(self, positive=[], negative=[]):
        ######
        try:
            if len(positive) > 0:
                sample = self.word2vec_book.wv[positive[0]]
            else:
                sample = self.word2vec_book.wv[negative[0]]
            tot = np.zeros_like(sample)
        except:
            tot = np.zeros(300)
        ######
        #tot = np.zeros_like(sample)

        for i in positive:
            sample = self.word2vec_book.wv[i]
            tot = np.add(tot , sample)

        for i in negative:
            sample = self.word2vec_book.wv[i]
            tot = np.subtract(tot ,  sample)
        return tot


class LearnerModelMult(MeasureVecMult):
    def __init__(self):
        MeasureVecMult.__init__(self)

        #game = game_l.Game()
        #game.load_w2v(load_special=False)

        np.random.seed(3)
        self.X = [] #np.array([[1],[1],[1]])
        self.y = [] #np.array([1,1,0])

        self.num_examples = 1 #len(list(self.X))  # training set size
        self.nn_input_dim = 1 # input layer dimensionality
        self.nn_output_dim = 300  # output layer dimensionality

        self.epsilon = 0.01  # learning rate for gradient descent
        self.reg_lambda = 0.01  # regularization strength

        self.W1 = None
        self.b1 = None

        self.start_list_len = 27
        self.epochs = 1
        self.total_correct_old = self.start_list_len
        self.total_correct_old_loaded = 0
        #print (self.X)
        #print (self.y)
        self.test_zeros = False
        self.saved_once = False

        self.mag = 1.0 #10.0


    def check_odd_vector(self, game, odd_vec=[], debug_msg=False, list_try=[], list_correct=[]):

        g = game
        ''' list of possible inputs to try '''
        list_g = list_try

        ''' correct outputs in order '''
        list_i = list_correct

        ## must remove and mult elsewhere ##
        #odd_vec = np.multiply(odd_vec, self.mag)

        if True or len(odd_vec) > 0:
            self.set_odd_vec(odd_vec)

        correct = 0
        total = len(list_i)

        for z in range(len(list_g)):
            i = list_g[z]
            j = self.resolve_word_closest(g.words_game, [i] , debug_msg=debug_msg)[0]
            if j == list_i[z]: correct += 1
            pass

        if total == 0:
            if debug_msg: print ("zero list")
            return 0

        if debug_msg: print (correct, "/", total, "or:", correct / total)

        return correct / total

    #############################


    def set_starting_list(self):
        ''' list of possible inputs to try '''
        self.list_basic_wrong = [ #'goes', 'gone', 'went', 'going',
                  'western', 'eastern', 'southern', 'northern'
            , 'southward', 'northward', 'westward', 'eastward'
            , 'southeasterly', 'northeasterly', 'southwesterly', 'northwesterly' ## too obscure
            , 'southeastern', 'northeastern', 'southwestern', 'northwestern'
            #,'looking','looks','looked','opens','opens','opened','opening'
        ]

        ''' correct outputs in order '''
        self.list_basic_right = [ #'go', 'go', 'go', 'go',
                  'west', 'east', 'south', 'north'
            , 'south', 'north', 'west', 'east'
            , 'southeast', 'northeast', 'southwest', 'northwest' ## too obscure
            , 'southeast', 'northeast', 'southwest', 'northwest'
            #,'look','look','look','open','open','open','open'
        ]

        self.list_basic_wrong = self.list_basic_wrong[:self.start_list_len]
        self.list_basic_right = self.list_basic_right[:self.start_list_len]

    def load_vec(self, name=""):
        odd_vec = []
        if len(name) == 0:
            name = "word2vec_book_vec.npy.txt"
        if os.path.isfile(os.path.join("trained", name)) and not self.test_zeros:
            odd_vec = np.loadtxt(os.path.join("trained", name))
            odd_vec = np.array([odd_vec])
            #print (odd_vec,"here")
            odd_vec = np.divide(np.array(odd_vec) ,  self.mag)
        else:
            self.total_correct_old = 0
            if self.test_zeros:
                odd_vec = np.zeros((self.nn_input_dim,300))
            else:
                odd_vec = np.random.randn(self.nn_input_dim, 300) / np.sqrt(self.nn_input_dim)
                odd_vec.tolist()
                pass

        self.odd_vec = odd_vec
        #print (self.odd_vec,'odd')
        #exit()

        return odd_vec

    def save_vec(self, name="", odd_vec=[]):
        self.saved_once = True
        if len(name) == 0:
            name = "word2vec_book_vec.npy.txt"

        if os.path.isdir('trained') and not self.test_zeros:
            np.savetxt(os.path.join('trained',name), np.multiply(np.array(odd_vec) , self.mag))


    # Helper function to evaluate the total loss on the dataset
    def calculate_loss(self, model, sample=None,list_len=1):
        W1, b1 = model['W1'], model['b1']
        #W1 = W1 - sample
        # Forward propagation to calculate our predictions
        #z1 = self.X.dot(W1) #+ b1

        z1 = self.X.dot(W1)  # + b1
        z1 += b1
        a1 = np.tanh(z1)
        exp_scores = a1

        #exp_scores = np.exp(z1)
        probs = exp_scores #/ np.sum(exp_scores, axis=1, keepdims=True)
        # Calculating the loss
        #corect_logprobs = -np.log(probs[range(list_len), self.y])
        data_loss = np.sum(probs)
        # Add regulatization term to loss (optional)
        #data_loss += self.reg_lambda / 2 * np.sum(np.square(W1)) #+ np.sum(np.square(W2)))
        return 1. / self.num_examples * data_loss





    def build_model(self, num_features=300, num_passes=1, print_loss=False, game_ref=None,word_compare=None):
        # Initialize the parameters to random values. We need to learn these.
        np.random.seed(0)
        W1 = None #np.random.randn(self.nn_input_dim, num_features) / np.sqrt(self.nn_input_dim)
        b1 = np.zeros((1, num_features))


        # This is what we return at the end
        model = {}

        ######
        for i in range( num_passes):
            W1 = np.array(self.W1)

            self.odd_vec = [(self.W1[0])[:]]

            try:
                if word_compare is None:
                    sample = np.zeros(num_features)
                else:
                    sample = game_ref.word2vec_book.wv[word_compare]
                    #print ('...', self.list_basic_wrong[i])
                pass
            except: # NameError:
                continue

            # Forward propagation
            z1 = self.X.dot(W1) #+ b1

            #z1 += b1
            a1 = np.tanh(z1)
            #exp_scores = a1
            #probs = exp_scores #/ np.sum(exp_scores, axis=1, keepdims=True) #axis=1

            # Backpropagation
            delta = a1 #= probs

            if self.y[0] == 0:
                dW1 = np.dot(np.array(self.X).T, delta) + sample # R1
                print ("zero")
            else:
                dW1 = np.dot(np.array(self.X).T, delta) - sample
                print ("not zero")

            # Add regularization terms (b1 and b2 don't have regularization terms)
            dW1 += self.reg_lambda * W1

            # Gradient descent parameter update
            W1 += -self.epsilon * dW1
            #b1 += -self.epsilon * db1

            # Assign new parameters to the model

            self.W1 = W1

            model = {'W1': W1, 'b1': b1}

        # Optionally print the loss.
        if print_loss:
            loss = self.calculate_loss(model, sample=sample, list_len=num_passes)
            print("Loss after iteration %i:  %f" % (self.total_correct_old,loss))
        else:
            print ("found:",self.total_correct_old)

        return model

    def generate_perfect_vector(self, game, debug_msg=False):
        g = game
        total_tested = self.start_list_len
        score = 1.0
        for i in range(self.epochs):

            total_correct = 0
            for x in range(len(self.list_basic_right)):
                X = []
                y = []


                score = self.check_odd_vector(game, odd_vec=self.W1
                                           , debug_msg=False
                                           , list_try=[self.list_basic_wrong[x]]
                                           , list_correct=[self.list_basic_right[x]])


                if score == 1.0:
                    y.append(1)
                else:
                    y.append(0)

                X.append([1]) #[1]

                self.X = np.array(X)
                self.y = np.array(y)

                if score == 1.0:
                    total_correct += score

                if total_correct <= self.total_correct_old :
                    ### this condition seems to make no sense ###
                    self.build_model(print_loss=False
                                    ,num_passes=1
                                    ,game_ref=g
                                    ,word_compare=self.list_basic_right[x])


            if total_correct > self.total_correct_old :
                self.total_correct_old = total_correct
                self.save_vec(odd_vec=self.W1)
                print("--->", end="")



        print ("totals",self.total_correct_old / total_tested, self.total_correct_old, total_tested)
        total_correct = 0
        pass
        if (not self.saved_once) and self.total_correct_old_loaded < self.total_correct_old:
            #self.save_vec(odd_vec=self.W1)
            pass


if __name__ == "__main__":
    game = game_learn.Game()
    game.load_w2v(load_special=False)

    l = LearnerModelMult()

    l.set_w2v(w2v=game.word2vec_book)

    l.W1 = l.load_vec().tolist()
    l.set_starting_list()
    l.start_list_len = len(l.list_basic_right)

    score = l.check_odd_vector(game, odd_vec=l.W1 #* l.mag
                               , debug_msg=True
                               , list_try=l.list_basic_wrong
                               , list_correct=l.list_basic_right)

    if l.total_correct_old >= l.start_list_len:
        l.total_correct_old = score * l.start_list_len
        #l.saved_once = True
        #print (l.total_correct_old, 'load time')
        #exit()
    else:
        pass
        #l.saved_once = True

    l.total_correct_old_loaded = l.total_correct_old # total correct we start with

    '''
    print (l.total_correct_old)
    print (l.W1,'W1')
    exit()
    '''

    l.epochs = 1000
    l.generate_perfect_vector(game)

    print ("----------------")
    if False:

        l.W1 = l.load_vec().tolist()
        score = l.check_odd_vector(game, odd_vec=l.W1 #* l.mag
                                  , debug_msg=True
                                  , list_try=l.list_basic_wrong
                                  , list_correct=l.list_basic_right)
    print ("----------------")
    if False:
        for i in range(l.start_list_len):
            try:
                sample = game.word2vec_book.wv[l.list_basic_wrong[i]]
                #print (self.list_basic_right[i], self.list_basic_wrong[i])
                pass
            except: # NameError:
                continue

            score = l.check_odd_vector(game, odd_vec=l.W1 # - sample
                                       , debug_msg=True
                                       , list_try=[l.list_basic_wrong[i]]
                                       , list_correct=[l.list_basic_right[i]])

    if True:

        l.W1 = l.load_vec().tolist()

        score = l.check_odd_vector(game, odd_vec=l.W1  # * l.mag
                                   , debug_msg=True
                                   , list_try=l.list_basic_wrong
                                   , list_correct=l.list_basic_right)
        print (l.W1 )
        print (len(l.W1[0]), l.total_correct_old, l.total_correct_old_loaded)
        print (score * len(l.list_basic_right),'reload score')

