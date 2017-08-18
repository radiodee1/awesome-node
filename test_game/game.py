from __future__ import print_function, division
import textplayer.textPlayer as player
import os
import gensim.models.word2vec as w2v


class Game:

    def __init__(self):
        self.name = ""
        self.word2vec_game = None
        self.word2vec_book = None

        self.words_last = ['direction','direction']
        self.gameplay_flag = True
        self.words_quit = ['q','quit','exit']
        self.words_game = ['north','n','south','s','west','w','east','e',
                           'look','l',
                           'northeast','ne','northwest','nw','southeast','se','southwest','sw',
                           'get','take','drop','leave', 'up','u','down','d',
                           'go','inventory','i','walk']
        self.words_suggested = []

        self.bool_show_lists = False

    def run(self):
        self.game  = player.TextPlayer("zork1.z5")
        self.load_w2v()


    def load_w2v(self):
        self.word2vec_game = w2v.Word2Vec.load(os.path.join("trained", "word2vec_game.w2v"))
        self.word2vec_book = w2v.Word2Vec.load(os.path.join("trained", "word2vec_book.w2v"))

    def play_loop(self):
        start_info = self.game.run()
        print(start_info)

        command_in = ''
        self.gameplay_flag = True

        while command_in not in self.words_quit:

            if len(command_in.split()) > 0  and not  all( word in self.words_game for word in command_in.split() ):
                self.gameplay_flag = True #False
                self.words_suggested = []
                self.parse_input(command_in.split())
                self.print_list_suggested()


            else : self.gameplay_flag = True

            if self.gameplay_flag and len(command_in) > 0:
                command_output = self.game.execute_command(command_in)
                #self.words_last = command_in.split()
                print(command_output)

            command_in = raw_input("> ")
            command_in = command_in.strip().lower()
            print(command_in.split())

    def play_stop(self):
        if self.game.get_score() != None:
            score, possible_score = self.game.get_score()
        self.game.quit()

    def parse_input(self, input):
        #if type(input) is not list and type(input) is str:
        #    self.most_similar(input)
        if type(input) is list and len(input) == 1:
            self.resolve_word(input[0])
        if type(input) == str :
            input = input.split()
            for i in input:
                if not (i in self.words_game):
                    self.resolve_word(i)
        i = input
        if len(i) > 1:
            self.resolve_word(i[0])
            self.resolve_word(i[1])

            #second_word ='go' # self.words_last[len(self.words_last)-1]
            #word = self.nearest_similarity_game( i[1], i[0], second_word)
            #word2 = self.nearest_similarity_book( i[1], i[0], second_word)
            #print  (word,word2, "??")
            #self.most_similar(word2)

        pass

    def resolve_word(self, word):
        if self.bool_show_lists: print ("try resolve")
        results = []
        try:
            vec = self.word2vec_book.wv[word]
            results = self.word2vec_game.wv.similar_by_vector(vec, topn=10)
        except:
            pass
        self.print_list(results,heading="resolve-"+ word, add_to_global=True, to_screen=self.bool_show_lists)
        if self.bool_show_lists: print ("done resolve")
        pass

    def most_similar(self, word):
        results = []
        try:
            results = self.word2vec_game.most_similar(word)
            pass
        except:
            pass
        self.print_list(results, heading="list-"+word)

        self.resolve_word(word)

    def nearest_similarity_book(self, start1, end1, end2):
        start2 = ""
        try:
            similarities = self.word2vec_book.most_similar_cosmul(
                positive=[end2.lower(), start1.lower()],
                negative=[end1.lower()],
                topn=10
            )
            self.print_list(similarities, heading= similarities[0][0] +"-(book)??")
            start2 = similarities[0][0]
            print("{start1} is related to {end1}, as {start2} is related to {end2} in books".format(**locals()))
        except:
            print ("not similar enough?")
            pass
        return start2

    def nearest_similarity_game(self, start1, end1, end2):
        start2 = ""
        try:
            similarities = self.word2vec_game.most_similar_cosmul(
                positive=[end2.lower(), start1.lower()],
                negative=[end1.lower()],
                topn=10
            )
            self.print_list(similarities, heading= similarities[0][0] +"-(game)??")
            start2 = similarities[0][0]
            print("{start1} is related to {end1}, as {start2} is related to {end2} in games".format(**locals()))
        except:
            print ("not similar enough?")
            pass
        return start2

    def print_list(self, list, heading="list", to_screen=True, add_to_global=False):
        results = list
        if to_screen:
            if (len(results) > 0) :print ("--" + heading +"--")
            else: print ("--none--")
        for i in results:
            if to_screen:
                if i[0] in self.words_game:
                    print (" --> ", end="")
                else: print (" xxx ", end="")
                print (i[0])
            if i[0] in self.words_game and add_to_global and i[0] not in self.words_suggested:
                self.words_suggested.append(i[0])
            ### add to list??

    def print_list_suggested(self):
        results = self.words_suggested
        print ("--suggested--")
        for i in results:
            print (i, " , ", end="")
        print ("\n-----")

def main():
    print("zork 1")
    g = Game()
    g.run()
    g.play_loop()
    g.play_stop()

if __name__ == "__main__":
    main()
