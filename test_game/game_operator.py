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



    def print_list_suggested(self, apply_on_negate=False):
        apply_on_negate = False
        game.Game.print_list_suggested(self, apply_on_negate)

    def get_input_text(self, prompt=""):
        #print(prompt,":")
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
            return False

    def set_output_text(self, text=""):
        print(text)
        self.speech_out.speech_out(text)
        pass

def main():
    Operator()



if __name__ == "__main__":
    main()
