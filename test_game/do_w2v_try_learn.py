#!/usr/bin/python

from __future__ import absolute_import, division, print_function

import os
import numpy as np

import game

class LearnerModel:
    def __init__(self):

        np.random.seed(3)
        self.X = np.array([[1],[1],[1]])
        self.y = np.array([1,1,0])

        self.num_examples = len(list(self.X))  # training set size
        self.nn_input_dim = 1  # input layer dimensionality
        self.nn_output_dim = 300  # output layer dimensionality

        self.epsilon = 0.01  # learning rate for gradient descent
        self.reg_lambda = 0.01  # regularization strength

        self.W1 = None

        self.start_list_len = 27
        self.epochs = 1
        #print (self.X)
        #print (self.y)
        self.test_zeros = False

    def check_odd_vector(self, game, odd_vec=[], debug_msg=False, list_try=[], list_correct=[]):

        g = game
        ''' list of possible inputs to try '''
        list_g = list_try

        ''' correct outputs in order '''
        list_i = list_correct

        if True or len(odd_vec) > 0:
            g.set_odd_vec(odd_vec)

        correct = 0
        total = len(list_i)

        for z in range(len(list_g)):
            i = list_g[z]
            j = g.resolve_word_closest(g.words_game, [i] , debug_msg=debug_msg)[0]
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
        self.list_basic_wrong = ['goes', 'gone', 'went', 'going',
                  'western', 'eastern', 'southern', 'northern'
            , 'southward', 'northward', 'westward', 'eastward'
            , 'southeasterly', 'northeasterly', 'southwesterly', 'northwesterly' ## too obscure
            , 'southeastern', 'northeastern', 'southwestern', 'northwestern'
            ,'looking','looks','looked','opens','opens','opened','opening']

        ''' correct outputs in order '''
        self.list_basic_right = ['go', 'go', 'go', 'go',
                  'west', 'east', 'south', 'north'
            , 'south', 'north', 'west', 'east'
            , 'southeast', 'northeast', 'southwest', 'northwest' ## too obscure
            , 'southeast', 'northeast', 'southwest', 'northwest'
            ,'look','look','look','open','open','open','open']

        self.list_basic_wrong = self.list_basic_wrong[:self.start_list_len]
        self.list_basic_right = self.list_basic_right[:self.start_list_len]

    def load_vec(self, name=""):
        odd_vec = []
        if len(name) == 0:
            name = "word2vec_book_vec.npy.txt"
        if os.path.isfile(os.path.join("trained", name)) and not self.test_zeros:
            odd_vec = np.loadtxt(os.path.join("trained", name))
            #print (odd_vec)
        else:
            #odd_vec = np.zeros(300)
            odd_vec = np.random.randn(self.nn_input_dim, 300) / np.sqrt(self.nn_input_dim)

        self.odd_vec = odd_vec
        return odd_vec

    def save_vec(self, name="", odd_vec=[]):
        if len(name) == 0:
            name = "word2vec_book_vec.npy.txt"

        if os.path.isdir('trained') and not self.test_zeros:
            np.savetxt(os.path.join('trained',name), odd_vec)

    # Helper function to evaluate the total loss on the dataset
    def calculate_loss(self, model):
        W1, b1 = model['W1'], model['b1']
        # Forward propagation to calculate our predictions
        z1 = self.X.dot(W1) + b1

        exp_scores = np.exp(z1)
        probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
        # Calculating the loss
        corect_logprobs = -np.log(probs[range(self.num_examples), self.y])
        data_loss = np.sum(corect_logprobs)
        # Add regulatization term to loss (optional)
        data_loss += self.reg_lambda / 2 * np.sum(np.square(W1)) #+ np.sum(np.square(W2)))
        return 1. / self.num_examples * data_loss



    # Helper function to predict an output (0 or 1)
    def predict(self, model, x):
        W1, b1 = model['W1'], model['b1']
        # Forward propagation
        z1 = x.dot(W1) + b1

        exp_scores = np.exp(z1)
        probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
        return np.argmax(probs, axis=1)




    def build_model(self, num_features=300, num_passes=1, print_loss=False):
        # Initialize the parameters to random values. We need to learn these.
        np.random.seed(0)
        W1 = np.random.randn(self.nn_input_dim, num_features) / np.sqrt(self.nn_input_dim)
        b1 = np.zeros((1, num_features))

        print (W1)
        print (self.W1)
        if not self.W1 is None:
            W1 = list(self.W1)

        # This is what we return at the end
        model = {}

        # Gradient descent. For each batch...
        for i in range(0, num_passes):

            # Forward propagation
            z1 = self.X.dot(W1) # + b1
            z1 = z1 + b1
            exp_scores = np.exp(z1)
            probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)

            # Backpropagation
            delta = probs
            delta[range(self.num_examples), self.y] -= 1

            dW1 = np.dot(self.X.T, delta)
            db1 = np.sum(delta, axis=0)

            # Add regularization terms (b1 and b2 don't have regularization terms)
            dW1 += self.reg_lambda * W1

            # Gradient descent parameter update
            W1 += -self.epsilon * dW1
            b1 += -self.epsilon * db1

            # Assign new parameters to the model
            model = {'W1': W1, 'b1': b1}
            self.W1 = W1

            # Optionally print the loss.
            # This is expensive because it uses the whole dataset, so we don't want to do it too often.
            if print_loss and i % 1000 == 0:
                print("Loss after iteration %i: %f" % (i, self.calculate_loss(model)))

        return model

    def generate_perfect_vector(self, game):
        g = game
        for i in range(self.epochs):
            for j in range(self.start_list_len):
                score = self.check_odd_vector(g, odd_vec=self.W1,debug_msg=True
                                             , list_try=[self.list_basic_wrong[j]]
                                             , list_correct=[self.list_basic_right[j]])
                if score == 1.0:
                    print (score)
                    self.y = np.array([int(score)])
                else:
                    self.y = np.array([0])

                self.X = np.array([[1]])
                self.num_examples = 1
                model = l.build_model(print_loss=True,num_passes=1)
            pass

        pass


if __name__ == "__main__":
    game = game.Game()
    game.load_w2v(load_special=False)

    l = LearnerModel()

    l.W1 = l.load_vec()
    l.set_starting_list()
    '''
    l.X = np.array([[1]])
    l.y = np.array([1])
    l.num_examples = len(list(l.X))  # training set size
    '''
    #model = l.build_model(print_loss=True)

    l.generate_perfect_vector(game)
    # Build a model
    #model = build_model(print_loss=True)
