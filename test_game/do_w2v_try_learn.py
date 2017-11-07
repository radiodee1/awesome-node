#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np

import matplotlib

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

        print (self.X)
        print (self.y)

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



    # This function learns parameters for the neural network and returns the model.
    # - nn_hdim: Number of nodes in the hidden layer
    # - num_passes: Number of passes through the training data for gradient descent
    # - print_loss: If True, print the loss every 1000 iterations
    def build_model(self, num_features=300, num_passes=20000, print_loss=False):
        # Initialize the parameters to random values. We need to learn these.
        np.random.seed(0)
        W1 = np.random.randn(self.nn_input_dim, num_features) / np.sqrt(self.nn_input_dim)
        b1 = np.zeros((1, num_features))
        #b1 = np.zeros( num_features)


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

            # Optionally print the loss.
            # This is expensive because it uses the whole dataset, so we don't want to do it too often.
            if print_loss and i % 1000 == 0:
                print("Loss after iteration %i: %f" % (i, self.calculate_loss(model)))

        return model


if __name__ == "__main__":
    l = LearnerModel()

    l.X = np.array([[1],[0],[1]])
    l.y = np.array([1,0,0])
    model = l.build_model(print_loss=True)
    # Build a model
    #model = build_model(print_loss=True)
