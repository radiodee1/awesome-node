#!/usr/bin/python
from __future__ import absolute_import, division, print_function

import os.path , sys
import os

op_dir = os.path.abspath(os.path.join(os.path.dirname(__file__))) + "/"
#print(op_dir)
import op_dictionaries as dict
import op_do as opdo



class Op(dict.DictVocab, opdo.DoCommands):
    def __init__(self):
        dict.DictVocab.__init__(self)
        opdo.DoCommands.__init__(self)

        self.room_num = 0 ## start in music room
        self.room_num_old = -1
        self.raw_input_bool = False ### should start false!!
        self.speak_aloud_bool = True

        self.words_raw_input = ''
        self.words_anywhere_bool = False


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
        try:
            ### anywhere text ###
            self.words_anywhere_bool = False
            move_word = self.find_words_anywhere(list=com)
            if move_word in self.start_op_table:
                self.words_anywhere_bool = True
                if move_word in self.move_table:
                    self.room_num = self.move_table[move_word]
                self.start_op(self.start_op_table[move_word],list=com)
                return ''
            ### move from anywhere ###
            move_word = self.arrange_move_pattern(list=com, start_anywhere=True, start=self.room_num)
            if move_word in self.move_table:
                self.room_num = self.move_table[move_word]
            else:
                ### move from one location ###
                move_word = self.arrange_move_pattern(list=com, start_anywhere=False, start=self.room_num)
                if move_word in self.move_table:
                    self.room_num = self.move_table[move_word]

            ### start an application ###
            self.words_anywhere_bool = False
            move_word = self.arrange_move_pattern(list=com, start_anywhere=True, start=self.room_num)
            if move_word in self.start_op_table:
                if move_word in self.move_table:
                    self.room_num = self.move_table[move_word]
                self.start_op(self.start_op_table[move_word])
                return ''
        except KeyboardInterrupt:
            if self.raw_input_bool == True:
                return 'raw text'
            else:
                return ''
            pass
        ### output text ###
        text = self.output_text(self.room_num)
        self.room_num_old = self.room_num

        return text

    def get_score(self): # do not use!!
        return 0,0

    def quit(self):
        #print("close/quit")
        pass

    def output_text(self,num):
        #print(self.words_raw_input)
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

    def set_raw_input(self,input):
        self.words_raw_input = input
        pass

    def start_op(self, op, list=[]):
        exec_line = ''
        op = str(op).split('+')
        start = int(op[1])
        launch = int(op[2])
        op = op[0] ## magic index number

        if os.path.exists(op) : #and start != int(self.START_INTERNAL):
            f = open(op, 'r')
            for l in f:
                if l.startswith('Exec='):
                    exec_line = l[len('Exec='):]
                    break
            f.close()
            exec_line = exec_line.split()
            exec_line = exec_line[0]
            if launch == int(self.LAUNCH_SEARCH_WEB) or start == int(self.START_INTERNET) :
                LAUNCH_URL = ' "http://www.google.com/search?q='
                exec_line += LAUNCH_URL
                exec_line += ' '.join(list)
                exec_line += '"'
                os.system(exec_line)
                pass
            elif True:
                os.system(exec_line)
        elif launch == self.LAUNCH_SEARCH_FILES:
            print('search files')
            pass
        elif launch == self.LAUNCH_SEARCH_EXECUTABLE:
            print('search exec')
            pass
        else:
            print('skip all')
        pass


    def find_words_anywhere(self, list=[]):
        ## return an op code so that start_op() can be called next ##

        ### create table for each room with preferred outcome on top ###
        self.room_determined_table_order(self.room_num)

        com = []
        for z in self.search_anywhere_room_table:
            tot = 0
            zz = z[:-1]
            #print(zz,'- start list')
            for i in zz:
                for j in list:
                    if i == j:
                        tot += 1
            if tot == len(zz):
                com = z[-1:]
                #print(com,'- new list')
                break

        move_word = self.arrange_move_pattern(list=com, start_anywhere=True, start=self.room_num)
        return move_word
        pass

    def detect_words_anywhere(self , list=[]):
        word = self.find_words_anywhere(list=list)
        if word in self.start_op_table:
            self.words_anywhere_bool = True
            return True
        else:
            self.words_anywhere_bool = False
            return False

    def room_determined_table_order(self, num):
        ## make a table with preferred op on top ##
        room = self.rooms['room-' + str(num)]

        zz = []
        for z in self.search_anywhere_table:
            if z[0] in self.rooms and self.rooms[z[0]] == room:

                zz = z
                break
        if len(zz) > 0:
            self.search_anywhere_room_table = [zz]
        else:
            self.search_anywhere_room_table = []
        self.search_anywhere_room_table.extend(self.search_anywhere_table)
        pass