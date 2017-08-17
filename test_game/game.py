from __future__ import print_function, division
import textplayer.textPlayer as player
import os
import gensim.models.word2vec as w2v


class Game:

    def __init__(self):
        self.name = ""
        self.word2vec_game = None

        self.words_last = ['direction','direction']
        self.gameplay_flag = True
        self.words_quit = ['q','quit','exit']
        self.words_game = ['north','n','south','s','west','w','east','e',
                           'look','l',
                           'northeast','ne','northwest','nw','southeast','se','southwest','sw',
                           'get','take','drop','leave', 'up','u','down','d',
                           'go','inventory','i','walk']

    def run(self):
        self.game  = player.TextPlayer("zork1.z5")
        self.load_w2v()


    def load_w2v(self):
        self.word2vec_game = w2v.Word2Vec.load(os.path.join("trained", "word2vec_game.w2v"))

    def play_loop(self):
        start_info = self.game.run()
        print(start_info)

        command_in = ''
        self.gameplay_flag = True

        while command_in not in self.words_quit:

            if len(command_in.split()) > 0  and not  all( word in self.words_game for word in command_in.split() ):
                self.gameplay_flag = False
                self.parse_input(command_in.split())
                #if len(command_in.split()) == 1:
                #    self.most_similar(command_in)
            else : self.gameplay_flag = True

            if self.gameplay_flag and len(command_in) > 0:
                command_output = self.game.execute_command(command_in)
                #self.words_last = command_in.split()
                print(command_output)

            command_in = raw_input("enter command :")
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
            self.most_similar(input[0])
        if type(input) == str :
            input = input.split()
            for i in input:
                if not (i in self.words_game):
                    self.most_similar(i)
        i = input
        if len(i) > 1:
            self.most_similar(i[0])
            self.most_similar(i[1])
            second_word = self.words_last[len(self.words_last)-1]
            word = self.nearest_similarity_cosmul( second_word,i[1], i[0])
            print  (word, "??")
            self.most_similar(word)
        pass


    def most_similar(self, word):
        results = []
        try:
            results = self.word2vec_game.most_similar(word)
        except:
            pass
        self.print_list(results, heading="list-"+word)

    def nearest_similarity_cosmul(self, start1, end1, end2):
        start2 = ""
        try:
            similarities = self.word2vec_game.most_similar_cosmul(
                positive=[end2.lower(), start1.lower()],
                negative=[end1.lower()],
                topn=10
            )
            self.print_list(similarities, heading= similarities[0][0] +"??")
            start2 = similarities[0][0]
            print("{start1} is related to {end1}, as {start2} is related to {end2}".format(**locals()))
        except:
            pass
        return start2

    def print_list(self, list, heading="list"):
        results = list
        if (len(results) > 0) :print ("--" + heading +"--")
        for i in results:
            print (i[0], end="")
            if i[0] in self.words_game:
                print (" <---")
            else: print (" xxx")

def main():
    print("zork 1")
    g = Game()
    g.run()
    g.play_loop()
    g.play_stop()

if __name__ == "__main__":
    main()
