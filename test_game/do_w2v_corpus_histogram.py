#!/usr/bin/python

from __future__ import absolute_import, division, print_function
import codecs
import glob
import sys
import os
import io
import game


class Histogram(object, game.Vocab ):
    def __init__(self):
        game.Vocab.__init__(self)
        self.set_starting_list()
        self.set_graph_list()
        length = len(self.list_basic_graph)
        self.list_label = [ 0 for i in range(length)]
        self.list_score = [ 0 for i in range(length)]

        for i in range(len(self.list_basic_graph)):
            self.list_label[i] = self.list_basic_graph[i]

        self.examine_all_words(print_sentences=False)

    def examine_all_words(self, print_sentences=False):
        glob_txt = sys.argv[1]

        book_filenames = sorted(glob.glob(glob_txt))

        for book_filename in book_filenames:
            with io.open(book_filename, "r", encoding="utf-8") as book_file: ## codecs.open
                for line in book_file:
                    # corpus_raw += line
                    # corpus_raw.append(line)
                    xx = line.split()
                    yy = 0
                    if len(xx) != 0:
                        for i in range(len(xx)):
                            self.check_game_words(str(xx[i].encode("utf-8")))
                            yy += 1
                            try:
                                if print_sentences: print(xx[i], end="")
                            except:
                                pass
                            if yy % 1000 == 0:
                                if print_sentences: print(". ")
                                yy = 0
                            elif not i == len(xx) - 1:
                                if print_sentences: print(" ", end="")
                        if print_sentences: print(". ")

    def check_game_words(self, word=''):
        for i in range(len(self.list_label)):
            if self.list_label[i] == word:
                self.list_score[i] += 1
                #print("here")

    def print_results(self):
        #print(self.list_label)
        for i in range(len(self.list_label)):
            print(("word " + self.list_label[i] + " -> " + str(self.list_score[i])))

if __name__ == "__main__":
    h = Histogram()
    h.print_results()