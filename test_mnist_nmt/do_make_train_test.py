#!/usr/share/python3

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("raw", one_hot=False)

for _ in range(100000):
    batch_xs, batch_ys = mnist.train.next_batch(1)
    print(batch_xs, batch_ys)
    exit()
