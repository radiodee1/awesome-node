#!/usr/bin/python3

import os
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("raw", one_hot=False)

d = 0.5
w = 28

subbatch = 100

both_coords = True

def add_to_file(in_line, out_line, name):
    ##
    with open(name+'.from','a', encoding='utf8') as f:
        #for content in df['parent'].values:
        f.write(in_line +'\n')

    with open(name+'.to','a', encoding='utf8') as f:
        #for content in df['comment'].values:
        f.write(out_line+'\n')
    pass

def look_at_image(mnist_part, name='', short=False, batch=1000, subbatch=10):
    for ii in range(batch):
        batch_xs, batch_ys = mnist_part.next_batch(subbatch)
        print(ii, 'out of', batch , name)
        for i in range(len(batch_xs)):
            s = ''
            for j in range(w):
                for k in range(w):
                    z = 0
                    if batch_xs[i][j * w + k] > d:
                        z = 1
                    if  short: print(z, end='')
                    if z == 1: 
                        if both_coords:
                            # two coords
                            s += ' ' + '/' + str(k) + '/' + str(j) + '/'
                        else:
                            # one coord
                            s += ' ' + '/' + str(k) + '/'
                if  short: print('|')
            if  short: print(name + ' val=', batch_ys[i])
            if not short: add_to_file(s, str(batch_ys[i]), name)
            if i > 3 and short: break
        if short: break
    
look_at_image(mnist.train, name='train',short=False, batch=5500)

look_at_image(mnist.test, name='test', short=False, batch=1000)

look_at_image(mnist.validation, name='validation', short=False, batch=500)

os.system('mv train.from train.to test.from test.to validation.from validation.to data/.')
