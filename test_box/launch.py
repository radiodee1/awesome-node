#!/usr/bin/python

'''
import subprocess
from subprocess import PIPE, STDOUT
import os

#read, write = os.pipe()

command = ['/usr/bin/wine', 'dfrotz.exe' ,'BADGUYS.Z5']

p = subprocess.Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)

key = input("enter key ")

key = bytearray(key,'utf-8')
out = p.communicate(input=key)[0]

print(out)
#p.stdin.write(write, key)
'''



import textplayer.textPlayer as tp
t = tp.TextPlayer('zork1.z5')
start_info = t.run()
print start_info

command_in = ''

while command_in != 'q':
    command_in = raw_input("enter command :")
    command_in = command_in.strip()
    command_output = t.execute_command(command_in)
    print command_output

if t.get_score() != None:
    score, possible_score = t.get_score()
t.quit()
