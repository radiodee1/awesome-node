#!/usr/bin/python3

import os

name = 'vocab'
both_coords = True

with open(name+'.from','a', encoding='utf8') as f:
    if both_coords:
        s = ''
        in_line = '<unk>\n<s>\n</s>\n' 
        for x in range(28):
            for y in range(28):
                s =  '/' + str(x) + '/' + str(y) + '/'
                in_line += s + '\n'
    else:
        in_line = '<unk>\n<s>\n</s>\n' + '\n'.join([ str(x) for x in range(28)]) + '\n'
    f.write(in_line)
    
with open(name+'.to','a', encoding='utf8') as f:
    in_line = '<unk>\n<s>\n</s>\n' +'\n'.join( [ str(x) for x in range(10)])
    f.write(in_line +'\n')
    
os.system('mv vocab.from vocab.to data/.')
