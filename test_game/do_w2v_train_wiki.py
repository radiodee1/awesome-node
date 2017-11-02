#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Pan Yang (panyangnlp@gmail.com)
# Copyright 2017

from __future__ import print_function

import logging
import os
import sys
import multiprocessing

from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 4 or True:
        print("Useing: python do_w2v_train_wiki.py input_text "
              "output_gensim_model output_word_vector")
        #sys.exit(1)
    inp = sys.argv[1]

    model = Word2Vec(LineSentence(inp), size=300, window=7, min_count=5,
                     workers=multiprocessing.cpu_count())

    model.save(os.path.join("trained","word2vec_book.wv"))
    model.wv.save_word2vec_format(os.path.join("trained","word2vec_book.wv.vec"), binary=False)