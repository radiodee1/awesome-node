#!/usr/bin/python3

import os

name = 'vocab'

with open(name+'.from','a', encoding='utf8') as f:
    in_line = '<unk>\n<s>\n</s>\n' + '\n'.join([ str(x) for x in range(28)])
    f.write(in_line +'\n')
    
with open(name+'.to','a', encoding='utf8') as f:
    in_line = '<unk>\n<s>\n</s>\n' +'\n'.join( [ str(x) for x in range(10)])
    f.write(in_line +'\n')
    
os.system('mv vocab.from vocab.to data/.')
