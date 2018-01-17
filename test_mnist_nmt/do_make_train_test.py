#!/usr/bin/python3

import os
from tensorflow.examples.tutorials.mnist import input_data
import csv
import struct
import numpy as np

mnist = input_data.read_data_sets("raw", one_hot=False)

d = 0.5
w = 28

subbatch = 100

both_coords = True

def show_num(s):
    s = s.split()
    for i in range(28):
        for j in range(28):
            z = '/'+ str(i) + '/' + str(j) + '/'
            if z in s:
                print("1",end='')
            else:
                print("0",end='')
        print('|')


def add_to_file(in_line, out_line, name):
    ##
    with open(name+'.from','a', encoding='utf8') as f:
        #for content in df['parent'].values:
        f.write(in_line +'\n')

    with open(name+'.to','a', encoding='utf8') as f:
        #for content in df['comment'].values:
        f.write(out_line+'\n')
    pass

def look_at_image(mnist_part, name='', short=False, batch=1000, subbatch=10, sequence=False):
    if sequence:
        if name == 'train':
            fname_lbl = 'raw/train-labels-idx1-ubyte'
            pass
        if name == 'test':
            fname_lbl = 'raw/t10k-labels-idx1-ubyte'
            pass
        with open(fname_lbl, 'rb') as flbl:
            magic, num = struct.unpack(">II", flbl.read(8))
            lbl = np.fromfile(flbl, dtype=np.int8)
            batch_ys = list(lbl)
            #print(batch_ys[:10])
    if sequence: batch = batch * subbatch
    for ii in range(batch):
        print(ii, 'out of', batch , name)
        if not sequence:
            batch_xs, batch_ys = mnist_part.next_batch(subbatch)

            for i in range(len(batch_ys)): ## possibly batch_xs??
                s = ''
                if True: #not sequence :
                    for j in range(w):
                        for k in range(w):
                            z = 0
                            if batch_xs[i][j * w + k] > d:
                                z = 1
                            if  short: print(z, )
                            if z == 1:
                                if both_coords:
                                    # two coords
                                    s += ' ' + '/' + str(k) + '/' + str(j) + '/'
                                else:
                                    # one coord
                                    s += ' ' + '/' + str(k) + '/'
                        if  short: print('|')
        else:
            s = ''
            with open('raw/sequences/'+ name +'img-'+ str(ii) + '-points.txt', 'r') as f:
                ff = csv.reader(f)
                for row in ff:
                    if row[1] != 'row' and row[0] != 'col' and int(row[0]) >= 0 and int(row[1]) >= 0:
                        s += ' ' + '/' + str(row[1]) + '/' + str(row[0]) + '/'
                #print(s)
                #print(ff[1])
            if not short: add_to_file(s, str(batch_ys[ii]), name)
            pass
        if False: show_num(s)
        if  False: print(name + ' val=', batch_ys[ii])
        if not short and not sequence: add_to_file(s, str(batch_ys[i]), name)
        #if i > 3 and short: break
        #if short: break
    
look_at_image(mnist.train, name='train',short=False, batch=5500, sequence=True)

look_at_image(mnist.test, name='test', short=False, batch=1000, sequence=True)


os.system('mv train.from train.to test.from test.to  data/.')
