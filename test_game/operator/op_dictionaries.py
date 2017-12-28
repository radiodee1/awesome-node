
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
            'go': 11
        }

        self.move_pattern = {
            self._arrange_move_pattern(list=['go', 'n'], start_anywhere=True): 1,
            self._arrange_move_pattern(list=['go','s'],start_anywhere=True) : 2
        }
        print(self.move_pattern)
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
        print(val)
        return val
        pass