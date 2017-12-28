#!/usr/bin/python
from __future__ import absolute_import, division, print_function



class Op:
    def __init__(self):
        print("hello")

    def run(self):
        print("prep/run")
        return "prep/run"

    def execute_command(self, command):
        text = "command was "+ command
        return "text: " + text

    def get_score(self):
        return 0,0

    def quit(self):
        print("close/quit")
