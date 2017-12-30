#!/usr/bin/python
from __future__ import absolute_import, division, print_function

import os.path , sys

op_dir = os.path.abspath(os.path.join(os.path.dirname(__file__))) + "/"
#print(op_dir)
import op_dictionaries as dict


class Op(dict.DictVocab):
    def __init__(self):
        dict.DictVocab.__init__(self)
        self.room_num = 0 ## start in music room
        self.room_num_old = -1
        self.raw_input_bool = False
        self.speak_aloud_bool = True
        pass

    def get_raw_input_bool(self):
        return self.raw_input_bool

    def run(self):

        text = self.output_text(self.room_num)
        self.room_num_old = self.room_num

        return text

    def execute_command(self, command):
        com = command.split()
        com = self.find_phrases(list=com)
        move_word = self.arrange_move_pattern(list=com, start_anywhere=True, start=self.room_num)
        if move_word in self.move_table:
            self.room_num = self.move_table[move_word]
        else:
            move_word = self.arrange_move_pattern(list=com, start_anywhere=False, start=self.room_num)
            if move_word in self.move_table:
                self.room_num = self.move_table[move_word]
                #return ''
        move_word = self.arrange_move_pattern(list=com, start_anywhere=True, start=self.room_num)
        if move_word in self.start_op_table:
            self.start_op(self.start_op_table[move_word])
            return ''
        text = self.output_text(self.room_num)
        self.room_num_old = self.room_num

        return text

    def get_score(self): # do not use!!
        return 0,0

    def quit(self):
        #print("close/quit")
        pass

    def output_text(self,num):
        txt = ''
        if num in self.text_short_table:
            txt += self.text_short_table[num]
        txt += '\n'
        if num in self.text_long_table and self.room_seen_bool[num] is False:
            txt += self.text_long_table[num]
        self.room_seen_bool[num] = True
        if num == self.room_num_old or self.speak_aloud_bool is False:
            print(txt)
            return '' ## Don't say it out loud!!
        return txt

    def find_phrases(self, list=[]):
        if self.raw_input_bool == True:
            return list
        nlist = []
        index = 0
        match = False
        while index < len(list):

            for phrase in self.words_phrase:
                match = False
                p = phrase[0:-1]
                if index + len(p) - 1 < len(list) :
                    match = True
                    l = list[index: index + len(p) ]
                    for x in range(len(p)):
                        if l[x].startswith('#'): l[x] = l[x][1:]
                        if p[x] != l[x]:
                            match = False
                        pass
                ######################
                if match == True:
                    l = phrase
                    word = ''
                    for ll in range(len(l)):
                        if ll < len(l) - 1:
                            word += l[ll]
                        if ll < len(l) - 2:
                            word += '-'
                    ########################

                    nlist.append(word)
                    index = index + len(p)
                    break


            if match == False:
                if index  < len(list):
                    nlist.append(list[index ])
                index = index + 1

            pass
        return nlist

    def start_op(self, op, list=[]):
        exec_line = ''
        op = str(op).split('+')
        op = op[0] ## magic index number
        if os.path.exists(op):
            f = open(op, 'r')
            for l in f:
                if l.startswith('Exec='):
                    exec_line = l[len('Exec='):]
                    break
            f.close()
            exec_line = exec_line.split()
            exec_line = exec_line[0]
            if len(list) == 0:
                os.system(exec_line)
            else:
                exec_line += ' ' + ' '.join(list)
                os.system(exec_line)
        pass
