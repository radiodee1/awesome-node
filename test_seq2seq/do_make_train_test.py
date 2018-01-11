#!/usr/bin/python3

import sqlite3
import pandas as pd
import codecs
import os

timeframes = ['input']

def format(c):
    #c = bytes(c, 'utf-8')  + bytes('\n','utf-8')
    c = c + '\n'
    return c


for timeframe in timeframes:
    connection = sqlite3.connect('{}.db'.format(timeframe))
    c = connection.cursor()
    limit = 5000
    last_unix = -1
    cur_length = limit
    counter = 0
    test_done = False

    while cur_length > counter * limit:

        df = pd.read_sql("SELECT * FROM parent_reply WHERE unix > {} and parent NOT NULL and score > 0 ".format(last_unix),connection)
        last_unix = -1 #df.tail(1)['unix'].values[0]
        cur_length = len(df)

        if not test_done:
            with codecs.open('test.from','a', 'utf-8-sig') as f:
                for content in df['parent'].values:
                    content = format(content)
                    f.write(content)

            with codecs.open('test.to','a', 'utf-8-sig') as f:
                for content in df['comment'].values:
                    content = format(content)                
                    f.write(content)

            test_done = True

        else:
            with codecs.open('train.from','a', 'utf-8-sig') as f:
                for content in df['parent'].values:
                    content = format(content)
                    f.write(content)

            with codecs.open('train.to','a', 'utf-8-sig') as f:
                for content in df['comment'].values:
                    content = format(content)
                    f.write(content)

        counter += 1
        if counter % 20 == 0:
            print(counter*limit,'rows completed so far')

    os.system('mv test.* tmp/chat_data/.')
    os.system('mv train.* tmp/chat_data/.')
