#!/usr/bin/python
from __future__ import absolute_import, division, print_function

import os.path , sys

op_dir = os.path.abspath(os.path.join(os.path.dirname(__file__))) + "/"
#print(op_dir)
import op_dictionaries as dict


class Op(dict.DictVocab):
    def __init__(self):
        dict.DictVocab.__init__(self)
        #print("hello")

        pass

    def run(self):
        #print("prep/run")
        return "prep/run"

    def execute_command(self, command):
        text = "command was "+ command
        return text

    def get_score(self): # do not use!!
        return 0,0

    def quit(self):
        print("close/quit")
