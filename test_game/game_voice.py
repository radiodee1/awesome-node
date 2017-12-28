#!/usr/bin/python

from __future__ import absolute_import, division, print_function
import os
from gtts import gTTS
from datetime import datetime
from pocketsphinx import LiveSpeech
import speech_recognition as sr

import game
import game_sr

class VoiceOut:
    def __init__(self):
        pass

    def speech_out(self,text=""):
        if len(text) > 0:
            tts = gTTS(text=text, lang='en')
            path = os.path.join("trained","temp_speech.mp3")
            tts.save(path)
            os.system("mpg321 " + path + " > /dev/null 2>&1 ")
        pass

class VoiceSphinxSR( ):

    def __init__(self):
        #self.g = None
        self.force_pocketsphinx = True
        self.r = None
        self.google_key = None
        self.read_google_key()
        pass

    def read_google_key(self):
        if self.force_pocketsphinx: return
        try:
            f = open(os.path.join('scripts','api_key.txt'),'r')
            self.google_key = f.read()
            self.google_key = str(self.google_key.strip())
            print (self.google_key)
        except:
            pass
        finally:
            if self.google_key is not None:
                self.r = sr.Recognizer()
        pass

    def voice_detection(self):

        if self.google_key is None or self.force_pocketsphinx:
            for phrase in LiveSpeech():
                # just one phrase!!
                print(phrase )
                return str(phrase)
            pass
        else:
            with sr.Microphone() as source:
                audio = self.r.listen(source)
                try:
                    phrase = self.r.recognize_google(audio, key=self.google_key)
                    print(phrase)
                    return str(phrase)
                    pass
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print(self.google_key)
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))
                    pass






class VoiceThread(game.Game):
    def __init__(self):
        game.Game.__init__(self)
        self.multithreading = True
        print ("Voice Input: Zork I")
        self.run(load_special=False)

        #self.voice = VoiceSphinxSR()
        self.voice = game_sr.VoiceGoogleSR()
        self.speech_out = VoiceOut()

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
        self.speech_out.speech_out(text)
        pass

def main():
    VoiceThread()



if __name__ == "__main__":
    main()
