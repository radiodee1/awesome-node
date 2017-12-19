#!/usr/bin/python

from __future__ import absolute_import, division, print_function
import os
import gensim.models.word2vec as w2v
import numpy as np
import itertools
import math
import threading
import Queue
import sys
from datetime import datetime

import game


class InfoVoice:

    NEW_VALUES_1 = 1
    STOP_2 = 2
    QUIT_3 = 3
    CHECK_SHOW_4 = 4

    def __init__(self):
        self.message = 0
        self.list_right = []
        self.list_wrong = []

class VoiceThread( game.Game):
    def __init__(self):
        game.Game.__init__(self)

        print ("VoiceThread:")
        self.start_list_len = 12
        self.multithreading = True
        self.run()

        self.multithreading = True
        self.vec = OddVector()
        self.vec.game_setup(g=self)

        t = threading.Thread(target=self.vec.multi_run)
        t.daemon = True

        t.start()

        #self.run()
        self.play_loop()
        self.play_stop()

        i = InfoVoice()
        i.message = InfoVoice.QUIT_3
        self.vec.q.put(i)


    def enqueue_voice_out(self, list_wrong=[], list_right=[] ,check=False):

        if isinstance(list_right,str): list_right=[list_right]
        if isinstance(list_wrong,str): list_wrong=[list_wrong]

        if len(list_right) > 1:
            list_right = [list_right[-1]]

        if len(list_right) == 1 and len(list_wrong) > 1:
            y = list_right[0]
            list_right = []
            for x in list_wrong:
                list_right.append(y)

        i = InfoVoice()
        i.message = InfoVoice.STOP_2
        print ("stop")
        self.vec.q.put(i)

        if not check:
            i = InfoVoice()
            i.message = InfoVoice.NEW_VALUES_1
            i.list_wrong = list_wrong
            i.list_right = list_right
            print (i.list_wrong, "wrong")
            print (i.list_right, "right")
            self.vec.q.put(i)
        if check:
            i = InfoVoice()
            i.message = InfoVoice.CHECK_SHOW_4
            print ("check")
            self.vec.q.put(i)

    def enqueue_voice_in(self):
        pass


def main():
    VoiceThread()



if __name__ == "__main__":
    main()
