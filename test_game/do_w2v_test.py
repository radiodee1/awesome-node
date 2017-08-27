#!/usr/bin/python

from __future__ import absolute_import, division, print_function


import os


import gensim.models.word2vec as w2v



word2vec_game = w2v.Word2Vec.load(os.path.join("trained", "word2vec_game.w2v"))
word2vec_book = w2v.Word2Vec.load(os.path.join("trained", "word2vec_book.w2v"))



print ("\nwest")
print (word2vec_game.most_similar("west") )


print ()

def nearest_similarity_cosmul(model, start1, end1, end2):
    similarities = model.most_similar_cosmul(
        positive=[end2, start1],
        negative=[end1], topn=20
    )
    start2 = similarities[0][0]
    print("{start1} is related to {end1}, as {start2} is related to {end2}".format(**locals()))
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

#similar_book_to_game(z)


print ("---------------")
print ("book")
nearest_similarity_cosmul(word2vec_book,"man", "king", "queen")

nearest_similarity_cosmul(word2vec_book,"north","south", "west")
nearest_similarity_cosmul(word2vec_book,"west", "northwest", "northeast")
#nearest_similarity_cosmul(word2vec_book,"go","west","south")

print ("game")
nearest_similarity_cosmul(word2vec_game,"west", "northwest", "northeast")
nearest_similarity_cosmul(word2vec_game,"north","south", "west")

print()

#nearest_similarity_cosmul(word2vec_game,"game","gone","west")
#nearest_similarity_cosmul(word2vec_game,"game","west","gone")
#nearest_similarity_cosmul(word2vec_book,"game","look","out")
#nearest_similarity_cosmul(word2vec_book,"game","inventory","book")

similar_book_to_game("west")
similar_book_to_game("gone")
similar_book_to_game("up")
similar_book_to_game("look")

similar_book_to_game("book")
similar_book_to_game("leaflet")
