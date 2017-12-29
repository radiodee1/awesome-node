from __future__ import absolute_import, division, print_function



class DictVocab:
    def __init__(self):
        self.words_dict = {
            'north' : 0,
            'n' : 0,
            'south' : 1,
            's': 1,
            'west' : 2,
            'w': 2,
            'east' : 3,
            'e': 3,
            'northwest' : 4,
            'nw': 4,
            'northeast' : 5,
            'ne': 5,
            'southwest' : 6,
            'sw': 6,
            'southeast' : 7,
            'se': 7,
            'up' : 8,
            'u': 8,
            'down' : 9,
            'd': 9,
            'quit':10,
            'exit':10,
            'go': 11,
            'start': 12,

            'room': 13,
            'hallway': 14,
            'music': 15,
            'movie': 16,
            'video': 16,
            'vid': 16,
            'mail': 17,
            'internet':18,
            'world': 19,
            'wide': 20,
            'web': 21,
            'mid': 22,
            'middle': 23,
            'library':24,
            'green':25,
            'house':26,

            'zero': 27,
            'one': 28,
            'two':29,
            'three':30,
            'four':31,
            'five': 32,
            'six': 33,
            'seven': 34,
            'eight': 35,
            'nine': 36,
            'ten': 37,
            'eleven': 38,
            'twelve': 39,
            'thirteen': 40,
            'fourteen': 41,
            'fifteen': 42,
            'sixteen' : 43,
            'seventeen': 44,
            'eighteen': 45,
            'nineteen': 46,
            'twenty': 47,


        }
        self.words_phrase = [
            ['room','zero', 500],
            ['room','one', 501],
            ['room','two', 502],
            ['room', 'three', 503],
            ['room', 'four', 504],
            ['room', 'five', 505],
            ['room', 'six', 506],
            ['room', 'seven', 507],
            ['room', 'eight', 508],
            ['room', 'nine', 509],
            ['room', 'ten', 510],

            ['music', 'room', 500],
            ['mail', 'room', 501],
            ['north', 'hallway', 502],
            ['internet', 'room', 503],
            ['movie', 'room', 504],
            ['mid', 'hallway',505],
            ['middle', 'hallway', 505],
            ['library', 'room', 506],
            ['south', 'hallway', 507],
            ['green', 'house','room', 508],
            ['green','house', 508],

            ['world','wide','web', 509],

            ['north','west', 4],
            ['north','east', 5],
            ['south','west', 6],
            ['south','east', 7]
        ]

        self.rooms = {
            'room-0': 0, # north-most room
            'room-1': 1, # north-west room
            'room-2': 2, # north hallway
            'room-3': 3, # north-east room

            'room-4': 4, # south-west room
            'room-5': 5, # mid hallway
            'room-6': 6, # south-east room

            'room-7': 7, # south hallway
            'room-8': 8, # souuth-most room

            ### spelled out ###
            'room-zero': 0,  # north-most room
            'room-one': 1,  # north-west room
            'room-two': 2,  # north hallway
            'room-three': 3,  # north-east room

            'room-four': 4,  # south-west room
            'room-five': 5,  # mid hallway
            'room-six': 6,  # south-east room

            'room-seven': 7,  # south hallway
            'room-eight': 8,  # souuth-most room

            ### names ###
            'music-room': 0,  # north-most room
            'mail-room': 1,  # north-west room
            'north-hallway': 2,  # north hallway
            'internet-room': 3,  # north-east room

            'movie-room': 4,  # south-west room
            'mid-hallway': 5,  # mid hallway
            'middle-hallway': 5, # middle hallway
            'library-room': 6,  # south-east room ** what goes here?!!

            'south-hallway': 7,  # south hallway
            'green-house-room': 8,  # souuth-most room

            ### short names ###
            'music': 0,  # north-most room
            'mail': 1,  # north-west room
            'internet': 3,  # north-east room
            'web': 3,
            'world-wide-web': 3,

            'movie': 4,  # south-west room
            'video': 4,
            'library': 6,  # south-east room ** what goes here?!!

            'solarium': 8,  #
            'green-house': 8,  # souuth-most room
        }
        moves = [
            #### directional ####
            ['music-room', 's','north-hallway'],
            ['north-hallway', 'n', 'music-room'],

            ['mail-room', 'e', 'north-hallway'],
            ['north-hallway', 'w', 'mail-room'],

            ['movie-room', 'e','middle-hallway'],
            ['middle-hallway', 'w', 'movie-room'],

            ['library-room', 'w', 'middle-hallway'],
            ['middle-hallway', 'e', 'library-room'],

            ['middle-hallway', 's', 'south-hallway'],
            ['south-hallway', 'n', 'middle-hallway'],

            ['south-hallway', 's', 'green-house-room'],
            ['green-house-room', 'n', 'south-hallway'],

            #### general ####
            ['#', 'music', 'music-room'],
            ['#', 'mail', 'mail-room'],
            ['#', 'internet', 'internet-room'],
            ['#', 'web', 'internet-room'],
            ['#', 'movie', 'movie-room'],
            ['#', 'library', 'library-room'],
            ['#', 'video', 'movie-room'],
            ['#', 'green-house', 'green-house-room'],
        ]

        self._add_to_vocab_table(list=self.words_phrase)
        print(self.words_dict)

        self.move_table = {}
        self._add_to_move_table(list=moves)
        print(self.move_table)
        pass

    def _arrange_move_pattern(self,list=[],start_anywhere=False, start=0):
        val = ''
        if start_anywhere or start == -1:
            val += "#"
        else:
            val = str(start)
        val += '+'
        for i in range(len(list)):
            val += str(self.words_dict[list[i]])
            if not i == len(list) -1:
                val += '+'
        #print(val)
        return val
        pass

    def _add_to_move_table(self, list=[]):
        for move in list:
            new_room = 0
            start_anywhere = False
            start = 0
            l = []
            if move[0] == '#' or start < 0:
                start_anywhere = True
                start = 0
            else:
                start = move[0]
                try:
                    if type(move[0]) == str:
                        start = self.rooms[move[0]]
                        pass
                    pass
                except:
                    start = 0
                    start_anywhere = True
                    pass
            new_room = move[-1:][0]
            try:
                if type(new_room) == str:
                    new_room = self.rooms[new_room]
            except:
                print('cannot find new room')
                pass
            l = move[1:-1]
            move_word = self._arrange_move_pattern(list=l,start_anywhere=start_anywhere,start=start)
            if not move_word in self.move_table:
                self.move_table[move_word] = new_room
        pass

    def _add_to_vocab_table(self, list=[]):
        for l in list:
            voc_num = l[-1:]
            word = ''
            for ll in range(len(l)):
                if ll < len(l) - 1:
                    word += l[ll]
                if ll < len(l) - 2:
                    word += '-'
            self.words_dict[word] = voc_num[0]
            print(word, voc_num[0])