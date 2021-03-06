from __future__ import absolute_import, division, print_function
import os.path


class DictVocab:

    START_MUSIC = 1
    START_MOVIE = 2
    START_INTERNET = 3
    START_OFFICE = 4
    START_MAIL = 5
    START_PROGRAM = 6
    START_INTERNAL = 7

    LAUNCH_SYNC = 8
    LAUNCH_ASYNC = 9
    LAUNCH_SEARCH_WEB = 10
    LAUNCH_SEARCH_FILES = 11
    LAUNCH_SEARCH_EXECUTABLE = 12

    COLUMN_VOCAB = 0
    COLUMN_PROGRAM_KEY = 1
    COLUMN_LAUNCH_STRING = 2
    COLUMN_SYNC_ASYNC = 3


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

            'office': 48,
            'program': 49,
            'email': 50,
            'play': 51,
            'the': 52

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

            ['world','wide','web', 18],

            ['start','movie', 16],
            ['start','mail', 17],
            ['start','music', 15],
            ['start','internet',18],
            ['start','office', 24],
            ['start','program', 49],

            ['who','is', 516],
            ['what','is', 517],
            ['when','is', 518],
            ['where','is', 519],
            ['why', 'is', 520],

            ['north','west', 4],
            ['north','east', 5],
            ['south','west', 6],
            ['south','east', 7]
        ]

        self._add_to_vocab_table(list=self.words_phrase)

        self.rooms = {
            ### abbreviation ###
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
            'office-room': 6,

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
            'office': 6,

            'solarium': 8,  #
            'green-house': 8,  # souuth-most room

        }


        moves = [
            #### directional ####
            ['music-room', 's','north-hallway'],
            ['north-hallway', 'n', 'music-room'],

            ['mail-room', 'e', 'north-hallway'],
            ['north-hallway', 'w', 'mail-room'],

            ['internet-room', 'w', 'north-hallway'],
            ['north-hallway','e', 'internet-room'],

            ['north-hallway','s','middle-hallway'],
            ['middle-hallway','n', 'north-hallway'],

            ['movie-room', 'e','middle-hallway'],
            ['middle-hallway', 'w', 'movie-room'],

            ['library-room', 'w', 'middle-hallway'],
            ['middle-hallway', 'e', 'library-room'],

            ['middle-hallway', 's', 'south-hallway'],
            ['south-hallway', 'n', 'middle-hallway'],

            ['south-hallway', 's', 'green-house-room'],
            ['green-house-room', 'n', 'south-hallway'],

            #### go ####
            ['music-room','go' ,'s', 'north-hallway'],
            ['north-hallway','go' , 'n', 'music-room'],

            ['mail-room','go' , 'e', 'north-hallway'],
            ['north-hallway', 'go' ,'w', 'mail-room'],

            ['internet-room','go' , 'w', 'north-hallway'],
            ['north-hallway','go' , 'e', 'internet-room'],

            ['north-hallway', 'go' ,'s', 'middle-hallway'],
            ['middle-hallway','go' , 'n', 'north-hallway'],

            ['movie-room','go' , 'e', 'middle-hallway'],
            ['middle-hallway', 'go' ,'w', 'movie-room'],

            ['library-room', 'go' ,'w', 'middle-hallway'],
            ['middle-hallway', 'go' ,'e', 'library-room'],

            ['middle-hallway','go' , 's', 'south-hallway'],
            ['south-hallway', 'go' ,'n', 'middle-hallway'],

            ['south-hallway', 'go' ,'s', 'green-house-room'],
            ['green-house-room', 'go' ,'n', 'south-hallway'],

            #### general ####
            ['#', 'music', 'music-room'],
            ['#', 'mail', 'mail-room'],
            ['#', 'internet', 'internet-room'],
            ['#', 'web', 'internet-room'],
            ['#', 'movie', 'movie-room'],
            ['#', 'library', 'library-room'],
            ['#', 'office', 'library-room'],
            ['#', 'video', 'movie-room'],
            ['#', 'green-house', 'green-house-room'],
        ]

        #print(self.words_dict)

        self.move_table = {}
        self._add_to_move_table(list=moves)

        text = {
            'music-room': 'Music Room.',
            'north-hallway': 'North Hallway.',
            'mail-room': 'Mail Room.',
            'internet-room': 'Internet Room.',
            'movie-room': 'Video Room.',
            'middle-hallway':'Middle Hallway.',
            'library-room': 'Library and Office.',
            'south-hallway' : 'South Hallway.',
            'green-house-room': 'Green House.'
        }

        self.text_short_table = {}
        self.text_long_table = {}
        self.room_seen_bool = {}

        self._add_to_text_short_table(dict=text)
        self._add_to_text_long_table(dict=text)

        start = [
            ['start-music', DictVocab.START_MUSIC,'/usr/share/applications/rhythmbox.desktop', DictVocab.LAUNCH_SYNC],
            ['start-mail', DictVocab.START_MAIL,'/usr/share/applications/thunderbird.desktop', DictVocab.LAUNCH_ASYNC],
            ['start-movie', DictVocab.START_MOVIE, '/usr/share/applications/vlc.desktop', DictVocab.LAUNCH_SYNC],
            ['start-office', DictVocab.START_OFFICE, '/usr/share/applications/libreoffice-startcenter.desktop', DictVocab.LAUNCH_ASYNC],
            ['start-internet', DictVocab.START_INTERNET, '/usr/share/applications/google-chrome.desktop', DictVocab.LAUNCH_SEARCH_WEB],
            ['start-program', DictVocab.START_PROGRAM, 'exec', DictVocab.LAUNCH_SEARCH_EXECUTABLE],

            ['music', DictVocab.START_MUSIC, '/usr/share/applications/rhythmbox.desktop', DictVocab.LAUNCH_SYNC],
            ['mail', DictVocab.START_MAIL, '/usr/share/applications/thunderbird.desktop', DictVocab.LAUNCH_ASYNC],
            ['email', DictVocab.START_MAIL, '/usr/share/applications/thunderbird.desktop', DictVocab.LAUNCH_ASYNC],
            ['movie', DictVocab.START_MOVIE, '/usr/share/applications/vlc.desktop', DictVocab.LAUNCH_SYNC],
            ['video', DictVocab.START_MOVIE, '/usr/share/applications/vlc.desktop', DictVocab.LAUNCH_SYNC],
            ['office', DictVocab.START_OFFICE, '/usr/share/applications/libreoffice-startcenter.desktop',DictVocab.LAUNCH_ASYNC],
            ['internet', DictVocab.START_INTERNET, '/usr/share/applications/google-chrome.desktop',DictVocab.LAUNCH_SEARCH_WEB],
            ['program', DictVocab.START_PROGRAM, 'exec', DictVocab.LAUNCH_SEARCH_EXECUTABLE]
        ]

        self.start_op_table = {}

        self._add_to_start_op_table(list=start)

        self.search_anywhere_table = [

            ## last item is program to launch !!
            ['music','start-music'],
            ['mail', 'start-mail'],
            ['movie', 'start-movie'],
            ['office', 'start-office'],
            ['write', 'start-office'],
            ['internet', 'start-internet'],
            ['program', 'start-program'],
            ['what-is', 'start-internet'],
            ['who-is', 'start-internet'],
            ['when-is', 'start-internet'],
            ['where-is', 'start-internet'],
            ['why-is', 'start-internet'],
            ['search', 'start-internet'],
            ['search','for', 'start-internet']

        ]

        self.search_anywhere_room_table = []

        self.op_for_room_table = {
            'music': 'start-music',
            'mail': 'start-mail',
            'movie': 'start-movie',
            'office': 'start-office',
            'internet': 'start-internet',
            'program': 'start-program'
        }
        #print(self.start_op_table)
        #exit()
        pass

    def arrange_move_pattern(self,list=[],start_anywhere=False, start=0):
        val = ''
        if start_anywhere or start == -1:
            val += "#"
        else:
            val = str(start)
        val += '+'
        for i in range(len(list)):
            if list[i] in self.words_dict:
                val += str(self.words_dict[list[i]])
            else:
                val += '-'
            if not i == len(list) -1:
                val += '+'
        #print(val)
        return val
        pass

    def arrange_launch_pattern(self, async=LAUNCH_SYNC, launch_code='', enum_type=0):
        val = ''
        val += launch_code
        val += '+'
        val += str(enum_type)
        val += '+'
        val += str(async)
        #else: val += str(DictVocab.LAUNCH_SYNC)

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
            move_word = self.arrange_move_pattern(list=l,start_anywhere=start_anywhere,start=start)
            if move_word not in self.move_table:
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
            #print(word, voc_num[0])

    def _add_to_text_short_table(self,dict={}):
        for key in dict:
            self.text_short_table[self.rooms[key]] = dict[key]

    def _add_to_text_long_table(self,dict={}):
        for key in dict:
            num = self.rooms[key]
            name = 'description-'+ str(num) + '.txt'
            if os.path.exists(os.path.join('operator','txt', name)):
                f = open(os.path.join('operator','txt', name),'r')
                val = f.read()
                self.text_long_table[num] = val
                f.close()
                pass
            self.room_seen_bool[num] = False

    def _add_to_start_op_table(self, list=[]):
        start_anywhere = True
        start = -1
        for line in list:
            code = line[DictVocab.COLUMN_LAUNCH_STRING]
            l = [line[DictVocab.COLUMN_VOCAB]]
            enum = line[DictVocab.COLUMN_PROGRAM_KEY]
            #print(l)
            async = line[DictVocab.COLUMN_SYNC_ASYNC]
            #if line[DictVocab.COLUMN_SYNC_ASYNC] == DictVocab.LAUNCH_SYNC:
            #    async = False
            start_code = self.arrange_launch_pattern(launch_code=code, async=async,enum_type=enum)
            move_word = self.arrange_move_pattern(list=l,start_anywhere=start_anywhere,start=start)
            #print(start_code)
            self.start_op_table[move_word] = start_code
        pass