#!/usr/bin/python

from __future__ import absolute_import, division, print_function

import os.path , sys

op_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'operator')) + "/"
#print(op_dir)

import game as game
import game_sr as sr
import game_voice as vo

sys.path.append(op_dir)
from op_basic import Op
#print('loaded')


class Operator(game.Game):
    def __init__(self):
        game.Game.__init__(self)
        self.multithreading = True
        print ("Voice Input: Operator I")
        self.play = Op()
        self.run(load_special=False, play=self.play)

        #self.voice = VoiceSphinxSR()
        self.voice = sr.VoiceGoogleSR()
        self.speech_out = vo.VoiceOut()

        self.play_loop()
        print('shutting down')
        self.play_stop()

    def read_word_list(self):
        #super(game.Game, self).read_word_list()
        game.Game.read_word_list(self)
        if os.path.isfile("operator/txt/list.txt"):
            f = open("operator/txt/list.txt","r")
            for line in f:
                line = line.strip().lower()
                for word in line.split():
                    if not word in self.words_all:
                        self.words_all.append(word)
            f.close()
        self.words_game.extend(self.words_all)

    def print_list_suggested(self, apply_on_negate=False):
        if self.play.detect_words_anywhere(self.words_raw_input) == False:

            apply_on_negate = False
            if self.play.get_raw_input_bool: apply_on_negate = True
            game.Game.print_list_suggested(self, apply_on_negate)
        else:
            print('start op')
            self.words_correct = self.words_raw_input
        self.play.set_raw_input(self.words_raw_input)

    def get_input_text(self, prompt=""):
        print('> ',end="")
        return self.voice.voice_detection()
        pass

    def get_input_text_yes_no(self, text="", hint=True):
        if self.play.get_raw_input_bool() is False:
            ## ask about input ##
            text = "try '"+ text + "' ?"
            if hint is True: text = text + " [yes/NO]:"
            #print(text)
            self.set_output_text(text=text)
            v = self.voice.voice_detection()
            if v.lower() == "yes" or v.lower() == "yeah":
                print("accept")
                return True
            else:
                print("reject")
                return False
            pass
        else:
            ## use raw input ##
            print(self.words_raw_input)
            return False

    def set_output_text(self, text=""):
        print(text)
        self.speech_out.speech_out(text)
        pass

def main():
    Operator()



if __name__ == "__main__":
    main()
