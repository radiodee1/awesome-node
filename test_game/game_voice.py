#!/usr/bin/python

from __future__ import absolute_import, division, print_function
import os
import numpy as np
import itertools
import math
import threading
import Queue
import time
import sys
from datetime import datetime
from pocketsphinx import LiveSpeech

import game


class VoiceSphinx( ):

    def __init__(self):

        self.g = None
        self.q = Queue.PriorityQueue()
        self.q_size = self.q.qsize()


        pass

    def game_setup(self, g = None):
        load_special = False
        if g is None:
            self.g = game.Game()
        else:
            self.g = g
        self.g.load_w2v(load_special=load_special)
        self.g.read_word_list()
        #self.mv.set_w2v(w2v=self.g.word2vec_book)

    def multi_run_detection(self):
        for phrase in LiveSpeech():
            i = InfoVoice()
            i.message = InfoVoice.NEW_VALUES_1
            i.input_string = phrase
            self.q.put((1,i))
            print(phrase ,'<- input')
        pass

    def multi_run(self):
        print ("thread", self.q.qsize())

        z = None

        run_once = False
        while True and not run_once:
            run_once = True
            #time.sleep(1)

            z = self.q.get()
            self.q_size = self.q.qsize()

            while self.q.qsize() is 0: time.sleep(1)

            while self.q.qsize() > 0 or z is not None:
                ##############

                ''' process z - generate perfect vector '''
                if z.message == InfoVoice.NEW_VALUES_1:
                    #start_time = datetime.now()


                    #end_time = datetime.now() - start_time
                    #print('Time elpased (hh:mm:ss.ms) {}'.format(end_time))
                    z = self.q.get()
                    return z.message

                if z.message == InfoVoice.STOP_2:
                    self.q = Queue.PriorityQueue()
                    ### clear queue
                    pass
                if z.message == InfoVoice.QUIT_3:
                    break
                    pass

                if z.message == InfoVoice.CHECK_SHOW_4:
                    pass


                ''' get new z '''
                #z = self.q.get()

                self.q_size = self.q.qsize()

                pass
                ###############


        print ("stop")


class InfoVoice:

    NEW_VALUES_1 = 1
    STOP_2 = 2  # special meaning
    QUIT_3 = 3
    CHECK_SHOW_4 = 4

    def __init__(self):
        self.message = 0
        self.input_string = ''


class VoiceThread( game.Game):
    def __init__(self):
        game.Game.__init__(self)

        print ("VoiceThread:")
        self.start_list_len = 12
        #self.multithreading = True
        #self.run()

        self.multithreading = True
        self.voice = VoiceSphinx()
        self.voice.game_setup(g=self)

        tt = threading.Thread(target=self.run)
        tt.daemon = True
        tt.start()

        print("start stt")
        t = threading.Thread(target=self.voice.multi_run)
        t.daemon = True
        t.start()

        self.voice.multi_run_detection()

        #self.run()
        self.play_loop()
        self.play_stop()

        i = InfoVoice()
        i.message = InfoVoice.QUIT_3
        self.voice.q.put((i,1))




    def enqueue_voice_in(self):
        return ""
        pass

    def get_input_text(self, prompt=""):

        if self.voice.q.qsize() > 1:
            i = InfoVoice()
            i.message = InfoVoice.STOP_2
            self.voice.q.put((0, i))

        return self.voice.multi_run()


        pass


    def set_output_text(self,text=""):
        pass

def main():
    VoiceThread()



if __name__ == "__main__":
    main()
