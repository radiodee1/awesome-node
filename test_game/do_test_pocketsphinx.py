#!/usr/bin/python

from pocketsphinx import LiveSpeech

for phrase in LiveSpeech(): print(phrase)