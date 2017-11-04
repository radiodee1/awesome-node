#!/usr/bin/python

from __future__ import absolute_import, division, print_function
import codecs

import glob

import sys

import multiprocessing

import os

import io
import re


if True:

    glob_txt = sys.argv[1]

    book_filenames = sorted(glob.glob(glob_txt))

    corpus_raw = [u""]

    for book_filename in book_filenames:
        print("stage: Reading '{0}'...".format(book_filename))
        with io.open(book_filename, "r", encoding="utf-8") as book_file: ## codecs.open
            for line in book_file:
                # corpus_raw += line
                # corpus_raw.append(line)
                xx = line.split()
                yy = 0
                if len(xx) != 0:
                    for i in range(len(xx)):
                        yy += 1
                        try:
                            print(xx[i], end="")
                        except:
                            pass
                        if yy % 1000 == 0:
                            print(". ")
                            yy = 0
                        elif not i == len(xx) - 1:
                            print(" ", end="")
                    print(". ")
