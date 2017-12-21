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

        pass



    def multi_run_detection(self):
        #return
        for phrase in LiveSpeech():
            i = InfoVoice()
            i.message = InfoVoice.NEW_VALUES_1
            i.input_string = phrase
            #self.q.put(i)
            print(phrase ,'<- input')
            return str(phrase)
        pass



class InfoVoice:

    NEW_VALUES_1 = 1
    STOP_2 = 2  # special meaning
    QUIT_3 = 3
    CHECK_SHOW_4 = 4

    def __init__(self):
        self.message = 0
        self.input_string = ''


class VoiceThread(game.Game):
    def __init__(self):
        game.Game.__init__(self)

        print ("VoiceThread:")
        self.run(load_special=False)

        self.voice = VoiceSphinx()

        print('loop start')
        self.play_loop()
        print('shutting down')
        self.play_stop()


    def get_input_text(self, prompt=""):
        print(prompt,":")
        return self.voice.multi_run_detection()
        pass

    def get_input_text_yes_no(self, text="", hint=True):
        text = "try '"+ text + "' ?"
        if hint is True: text = text + " [yes/NO]:"
        print(text)
        v = self.voice.multi_run_detection()
        if v.lower() == "yes" or v.lower() == "yeah": return True
        else: return False
        pass

    def set_output_text(self, text=""):
        print(text)
        pass

def main():
    VoiceThread()



if __name__ == "__main__":
    main()
