#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np

import matplotlib


np.random.seed(3)
X = np.array([[1],[1],[1]])
y = np.array([1,1,0]) #np.zeros(300)

num_examples = len(list(X))  # training set size
nn_input_dim = 1  # input layer dimensionality
nn_output_dim = 300  # output layer dimensionality

epsilon = 0.01  # learning rate for gradient descent
reg_lambda = 0.01  # regularization strength

print (X)
print (y)

# Helper function to evaluate the total loss on the dataset
def calculate_loss(model):
    W1, b1 = model['W1'], model['b1']
    # Forward propagation to calculate our predictions
    z1 = X.dot(W1) + b1

    exp_scores = np.exp(z1)
    probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
    # Calculating the loss
    corect_logprobs = -np.log(probs[range(num_examples), y])
    data_loss = np.sum(corect_logprobs)
    # Add regulatization term to loss (optional)
    data_loss += reg_lambda / 2 * np.sum(np.square(W1)) #+ np.sum(np.square(W2)))
    return 1. / num_examples * data_loss



# Helper function to predict an output (0 or 1)
def predict(model, x):
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
def build_model(num_features=300, num_passes=20000, print_loss=False):
    # Initialize the parameters to random values. We need to learn these.
    np.random.seed(0)
    W1 = np.random.randn(nn_input_dim, num_features) / np.sqrt(nn_input_dim)
    b1 = np.zeros((1, num_features))
    #b1 = np.zeros( num_features)


    # This is what we return at the end
    model = {}

    # Gradient descent. For each batch...
    for i in range(0, num_passes):

        # Forward propagation
        z1 = X.dot(W1) # + b1
        z1 = z1 + b1
        exp_scores = np.exp(z1)
        probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)

        # Backpropagation
        delta = probs
        delta[range(num_examples), y] -= 1

        dW1 = np.dot(X.T, delta)
        db1 = np.sum(delta, axis=0)

        # Add regularization terms (b1 and b2 don't have regularization terms)
        dW1 += reg_lambda * W1

        # Gradient descent parameter update
        W1 += -epsilon * dW1
        b1 += -epsilon * db1

        # Assign new parameters to the model
        model = {'W1': W1, 'b1': b1}

        # Optionally print the loss.
        # This is expensive because it uses the whole dataset, so we don't want to do it too often.
        if print_loss and i % 1000 == 0:
            print("Loss after iteration %i: %f" % (i, calculate_loss(model)))

    return model



# Build a model
model = build_model(print_loss=True)
