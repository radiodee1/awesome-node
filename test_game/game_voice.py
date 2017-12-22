#!/usr/bin/python

from __future__ import absolute_import, division, print_function
import os
from gtts import gTTS
from datetime import datetime
from pocketsphinx import LiveSpeech

import game


class VoiceSphinx( ):

    def __init__(self):

        self.g = None

        pass



    def voice_detection(self):
        #return
        for phrase in LiveSpeech():
            
            print(phrase )
            return str(phrase)
        pass

    def speech_out(self,text=""):
        tts = gTTS(text=text, lang='en')
        path = os.path.join("trained","temp_speech.mp3")
        tts.save(path)
        os.system("mpg321 " + path + " > /dev/null 2>&1 ")
        pass




class VoiceThread(game.Game):
    def __init__(self):
        game.Game.__init__(self)
        self.multithreading = True
        print ("Voice Input: Zork I")
        self.run(load_special=False)

        self.voice = VoiceSphinx()

        #print('loop start')
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

    def set_output_text(self, text=""):
        print(text)
        self.voice.speech_out(text)
        pass

def main():
    VoiceThread()



if __name__ == "__main__":
    main()
