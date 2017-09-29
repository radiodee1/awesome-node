#!/usr/bin/python

from __future__ import absolute_import, division, print_function
import os
import gensim.models.word2vec as w2v
import matplotlib.pyplot as plt
import numpy as np



word2vec_game = w2v.Word2Vec.load(os.path.join("trained", "word2vec_game.w2v"))
word2vec_book = w2v.Word2Vec.load(os.path.join("trained", "word2vec_book.w2v"))



print ("\ngo")
print (word2vec_book.most_similar("go", topn=10) )
print ("went")
print (word2vec_book.most_similar("went", topn=60))

print ()

def nearest_similarity_cosmul(model, start1, end1, end2):
    similarities = model.most_similar_cosmul(
        positive=[end2, start1],
        negative=[end1], topn=20
    )

    start2 = similarities[0][0]
    print("{start1} is related to {end1}, as {start2} is related to {end2}".format(**locals()))
    print (similarities)

    return start2

def nearest_similarity(model, start1, end1, end2):
    similarities = model.most_similar(
        positive=[end2, start1],
        negative=[end1], topn=20
    )

    start2 = similarities[0][0]
    print("{start1} is related to {end1}, as {start2} is related to {end2}".format(**locals()))
    print (similarities)

    return start2

def similar_book_to_game(word):
    print ("--"+word+"--")
    out = '' #vec = word2vec_book.wv[word]
    w = [(word,0)]
    w.extend( word2vec_book.wv.most_similar(word, topn=30))
    #w.append((word, 0))
    print (len(w), w)
    for i in w:
        print ( "--"+ i[0])
        try:
            vec = word2vec_game.most_similar(i[0])
            out = vec
            if len(vec) > 1:
                print (">>", i[0])
                break
            pass
        except:
            pass

    for i in out:
        print (i[0])
    print ("---")
    return out


#z = nearest_similarity_cosmul(word2vec_book,"gone", "VBN", "VBP")

print ("---------------")
print ("book")
nearest_similarity_cosmul(word2vec_book,"man", "king", "queen")

nearest_similarity_cosmul(word2vec_book,"north","south", "west")
nearest_similarity_cosmul(word2vec_book,"west", "northwest", "northeast")
nearest_similarity_cosmul(word2vec_book,"go","west", "west")
#nearest_similarity(word2vec_book,"going","west", "west")

#print ("game")
#nearest_similarity_cosmul(word2vec_game,"west", "northwest", "northeast")
#nearest_similarity_cosmul(word2vec_game,"north","south", "west")

print()

print ('go','west',word2vec_book.wv.similarity("go","west"))
print ('going','west',word2vec_book.wv.similarity("going","west"))
print ('goes','west',word2vec_book.wv.similarity("goes","west"))
print ('went','west',word2vec_book.wv.similarity("went","west"))
print ('gone','west',word2vec_book.wv.similarity("gone","west"))

print (word2vec_book.wv.doesnt_match("go goes gone went going".split()))


def graph_compare(word1, word2):
    vec1 = word2vec_book.wv[word1]
    y1 = np.arange(len(vec1))
    vec2 = word2vec_book.wv[word2]
    y2 = np.arange(len(vec2))

    plt.figure(1)
    plt.subplot(211)
    plt.title(word1)
    plt.bar(y1,vec1)
    plt.subplot(212)
    plt.title(word2)
    plt.bar(y2,vec2)
    plt.show()

#graph_compare('going','gone')
graph_compare('westerly','western')

graph_compare("go","gone")
#gone = word2vec_book.wv['gone']
#gone2 = np.zeros_like(gone)
#y_pos = np.arange(len(gone))


#fig, ax = plt.subplots()
#plt.bar(y_pos, gone)
#plt.show()

#print (gone)


'''
similar_book_to_game("west")
similar_book_to_game("gone")
similar_book_to_game("up")
similar_book_to_game("look")

similar_book_to_game("book")
similar_book_to_game("leaflet")
'''