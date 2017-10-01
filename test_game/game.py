from __future__ import print_function, division
import textplayer.textPlayer as player
import os
import gensim.models.word2vec as w2v


class Game:

    def __init__(self):
        self.name = ""
        self.word2vec_game = None
        self.word2vec_book = None

        self.game = None
        self.words_last = []
        self.gameplay_flag = True
        self.words_quit = ['q','quit','exit','save']
                            # 'save' was added so that frotz would not do that

        self.words_game = ['north','n','south','s','west','w','east','e',
                           'look','l','at',
                           'northeast','ne','northwest','nw','southeast','se','southwest','sw',
                           'get','take','drop','up','u','down','d','open','close',
                           'go','inventory','i','walk']
        self.words_all = []
        self.words_suggested = []
        self.words_input = []

        self.words_correct = []
        self.bool_show_lists = False
        self.odd_word = None
        self.odd_vec = None

    def run(self):
        self.game  = player.TextPlayer("zork1.z5")
        self.load_w2v()
        self.read_word_list()
        self.pre_game(odd_word=None,debug_msg=True, special_invert=True, invert_all=True)

    def load_w2v(self):
        self.word2vec_game = w2v.Word2Vec.load(os.path.join("trained", "word2vec_game.w2v"))
        self.word2vec_book = w2v.Word2Vec.load(os.path.join("trained", "word2vec_book.w2v"))

    def read_word_list(self):
        self.words_all = self.words_game[:]
        if os.path.isfile("data/list.txt"):
            f = open("data/list.txt","r")
            for line in f:
                line = line.strip().lower()
                for word in line.split():
                    if not word in self.words_all:
                        self.words_all.append(word)
            f.close()
        #print (self.words_game)
        pass

    def pre_game(self,odd_word=None, invert_all=True, debug_msg=False, special_invert=False):
        ''' randomly reverse one outlying word '''
        if odd_word == None:
            self.odd_word = self.word2vec_book.wv.doesnt_match(self.words_game)
        else:
            self.odd_word = odd_word

        self.odd_vec = self.word2vec_book.wv[self.odd_word]
        if debug_msg: print ("pre-game", self.odd_word)

        if invert_all:
            magnitude = 0
            position = 0
            for i in range(len(self.odd_vec)):
                if debug_msg and i < 5: print (self.odd_vec[i])
                if abs(self.odd_vec[i]) > magnitude:
                    magnitude = abs(self.odd_vec[i])
                    position = i
            for i in range(len(self.odd_vec)):
                if i != position or not special_invert:
                    pass
                    self.odd_vec[i] = self.odd_vec[i] * -1
                    if debug_msg and i < 5: print ("--->", self.odd_vec[i])

            if debug_msg: print ("do invert")
            #self.odd_vec = self.odd_vec * -1

        middle_value = self.word2vec_book.wv.most_similar(positive=[self.odd_vec], negative=[], topn=4)
        if debug_msg: print (middle_value)
        position = 0
        while middle_value[position][0] == odd_word:
            position += 1
        self.odd_word = middle_value[position][0]

        if debug_msg: print (self.odd_word)

    def play_loop(self):
        start_info = self.game.run()
        print(start_info)

        command_in = ''
        self.gameplay_flag = True

        while command_in not in self.words_quit:

            if len(command_in.split()) > 0  and not  all( word in self.words_all for word in command_in.split() ):
                self.gameplay_flag = True #False
                self.words_suggested = []
                self.parse_input(command_in.split())
                self.words_input = command_in.split()
                self.print_list_suggested()

            else : self.gameplay_flag = True

            if self.gameplay_flag and len(command_in) > 0:
                command_output = self.game.execute_command(command_in)
                #self.words_last = command_in.split()
                print(command_output)

            command_in = raw_input("> ")
            command_in = command_in.strip().lower()
            if self.bool_show_lists: print(command_in.split())

    def play_stop(self):
        if self.game.get_score() != None:
            score, possible_score = self.game.get_score()
        self.game.quit()

    def parse_input(self, input):

        if True:
            for word in input:
                self.resolve_word(word,debug_msg=False)
                #self.resolve_word(i[1])
            for word in self.words_last:
                self.resolve_word(word, debug_msg=False)
            #print (input, self.words_last)

            self.words_correct = self.resolve_word_closest(self.words_game, input, debug_msg=True, use_ending=False, odd_word=self.odd_word)

            self.words_last = input


        pass

    def resolve_word(self, word, debug_msg=False):
        if self.bool_show_lists or debug_msg: print ("try resolve")
        results = []
        w = [(word,0)]
        try:
            if debug_msg:
                print (self.word2vec_book)
                print (self.word2vec_game)
            w.extend( self.word2vec_book.wv.most_similar(word, topn=20))
            #if len(w) > 0 : results.append(w[0][0])
            if debug_msg: print(w )
            for i in w:
                if i[0] in self.words_game:
                    if not i in results:
                        results.append(i)
                    if debug_msg: print (i[0], "first-pass")
                pass

            for i in w:
                #print("--" + i[0])
                #if i[0] in self.words_input: continue
                try:
                    vec = self.word2vec_game.wv.most_similar(i[0])
                    results.extend(vec)
                    if len(vec) > 1:
                        results.append(i)
                        if debug_msg: print (results)
                        break
                    pass
                except:
                    pass


            #vec = self.word2vec_book.wv[word]
            #results = self.word2vec_game.wv.similar_by_vector(vec, topn=10)
        except : #ZeroDivisionError:
            pass
        self.print_list(results,heading="resolve-"+ word, add_to_global=True, to_screen=self.bool_show_lists)
        if self.bool_show_lists: print ("done resolve")
        pass

    def resolve_word_closest(self, list_suggested, list_command, odd_word=None , debug_msg=False, use_ending=False):
        list_out = []
        #
        #
        for word in list_command:
            if not  (word in self.words_all):
                num_best = -3
                word_best = ""
                #
                for near in list_suggested:
                    ######
                    if use_ending: near = near + "zzz"
                    try:
                        num = self.word2vec_book.wv.similarity(word, near)
                        if odd_word != None:
                            num = num + self.word2vec_book.wv.similarity(word,odd_word)
                            num = num + self.word2vec_book.wv.similarity(near,odd_word)
                        if debug_msg: print (word, near, odd_word, num)
                        if num > num_best and near != odd_word:
                            num_best = num
                            word_best = near
                    except:
                        pass
                    ######
                    pass
                list_out.append(word_best)
                pass

            pass
        if debug_msg: print (list_out)
        return list_out



    def most_similar(self, word):
        results = []
        try:
            results = self.word2vec_game.most_similar(word)
            pass
        except:
            pass
        self.print_list(results, heading="list-"+word)

        self.resolve_word(word)

    def nearest_similarity(self, model, start1, end1, end2):
        start2 = ""
        try:
            similarities = model.most_similar_cosmul(
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
            if i[0] in self.words_all and add_to_global and i[0] not in self.words_suggested:
                #if not i[0] in self.words_input and not i[0] in self.words_correct:
                self.words_suggested.append(i[0])
            ### add to list??

    def print_list_suggested(self):

        results = []
        for i in self.words_suggested:
            if i in self.words_input or i in self.words_correct: continue
            results.append(i)

        if len(results) == 0 : return
        print ("--suggested--")
        if len(self.words_correct) > 0 and len(self.words_correct[0]) > 0 :
            print ("try: '"+ self.words_correct[0]+ "', or:" )
        for i in range(len(results)):
            if i < len(results) - 1:
                print (results[i], " , ", end="")
            else: print (results[i])
        print ("-------------")

def main():
    print("zork 1")
    g = Game()
    g.run()
    g.play_loop()
    g.play_stop()

if __name__ == "__main__":
    main()
