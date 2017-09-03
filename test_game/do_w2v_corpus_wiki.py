#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Pan Yang (panyangnlp@gmail.com)
# Copyrigh 2017

#########################
# $ wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2
#########################

from __future__ import print_function

import logging
import os.path
import six
import sys

from gensim.corpora import WikiCorpus

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) != 3:
        print("Usage: python do_w2v_corpus_wiki.py enwiki.xxx.xml.bz2 data/wiki.en.txt")
        sys.exit(1)
    inp, outp = sys.argv[1:3]
    if not outp.startswith("data/"):
        outp = "data/" + outp  #wiki.en.txt"
    space = " "
    i = 0

    index = 0
    output = open(outp, 'w')
    wiki = WikiCorpus(inp, lemmatize=False, dictionary={})
    for text in wiki.get_texts():
        if six.PY3:
            output.write(b' '.join(text).decode('utf-8') + '.\n')
        # ###another method###
        #    output.write(
        #            space.join(map(lambda x:x.decode("utf-8"), text)) + '\n')
        else:
            output.write(space.join(text).encode('utf-8') + ".\n")
        i = i + 1
        if (i % 2500 == 0):
            logger.info("Saved " + str(i) + " articles")
            #index += 1
            if index >= 9  : break ## 20,000 articles
            index += 1


    output.close()
    logger.info("Finished Saved " + str(i) + " articles")