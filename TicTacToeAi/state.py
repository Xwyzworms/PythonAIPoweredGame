"""
This Script consist of all State required For The AI to learn
"""
from re import A
from typing import List, Counter
SYMBOLS : List = [".", "X", "O"]

class State:
    def __init__(self, cells, cols, rows, rules):
        self._cols = cols
        self._rows = rows
        self._rulse = rules
        ## Copy For Create A new object that has references to the Passed
        # If there are a change in this, then it will not affect the passed objects 
        # If no Cells Then just PUt 0 At that Cells
        self.cells = cells.copy() if cells else [0]*(cols * rows)
    
    def actions(self):
        return [i for i, c in enumerate(self.cells) if c == 0 ]
    
    def gameOver(self):
        return self.winner() != 0 or len(self.actions()) == 0
    
    def winner(self):
        strikes = list(self.strikes())
        if(len(strikes) == 0) :
            return 0
        _, winners = zip(*strikes)
        value, _ = Counter(winners).most_common(1)[0]
        print("hello WInner", value)
        return value
    
    def rows(self):
        """
        Return Seluruh Cells Pada Row
        """
        return [self.cells[i * self._rows : (i+1) *self._rows] for i in range(self._rows)]
    
    def cols(self):
        """ 
        Return seluruh Cells pada kolom
        """
        return [self.cells[i::self._cols] for i in range(self._cols)]

    def player(self):
        return [1, -1][sum(self.cells)]


    def strikes(self):
        """ 
        Check if the strikes already occured
        Dengan kata LAIN menang bang
        """
        for rule in self._rulse:
            ## Loop through Winning Rules
            score = sum(self.cells[i] for i in rule)
            ## Score itu diapatkan dari Penjumlahan untuk setiap sel 
            ## 1 untuk player 1
            ## -1 Untuk player 2

            if abs(score) == len(rule):
                ...
                yield rule, self.cells[rule[0]]

    def move(self, action):
        state = self.__class__(self.cells)
        if state.cells[action] != 0:
            raise ValueError(f'{state.cells} invalid move {action}')
        state.cells[action] = state.player()
        return state
    
    def __str__(self):
        return f"Hello Freak"
    
    def __repr__(self):
        rows = [" ".join(SYMBOLS[row]) for row in range(self._rows)]
        board = "\n".join(rows)

        if self.winner() != 0:
            msg = f"Winner is {SYMBOLS[self.winner()]}"
        elif self.gameOver():
            msg = "it's a Draw"
        else:
            msg = f"It's {SYMBOLS[self.player()]} 's Turn"
        final_message = f"\n{board}\n\n{msg}\n"
        
        return final_message
def make_rules(cols, rows, score):
    """ 
    Rules For winning 
    Vertical
    Diagonal
    Horizontal
    """

    rules = []
    ## 3 - 3 + 1 = 1 
    lim_rows = rows - score + 1
    lim_cols = cols - score + 1

    def index(c, r) : 
        """ 
            Untuk Index Aja Kalau mau ngambil nilai pada tiktaktoe kambing
            ntar dah paham pas Yang vertical check
        """
        return r * rows + c

    # Vertical Check
    # Untuk setiap Kolom Bakalan Di cek
    # nanti Masing masing kolom tadi bakalan di cek setiap row pada kolom tersebut
    for col in range(cols):
        for _ in range(lim_rows): #Pada dasarnya lim Rows ini ya cuman satu aja 
            ## Ini Untuk Ngelakuin cek aja
            ### Untuk setiap kolom kan tadi bakalan dilakuin pengecakn
            ## Rules pertama pada kolom ini bakalan append index nya, kalau bener ya udah
            ## [1, 4, ]
            rules.append([index(col, row) for row in range(score)])

    ### Horizontal
    for row in range(rows):
        for _ in range(lim_cols):
            rules.append([index(col , row) for col in range(score)])
    
    ### For Menyinglang
    for row in range(lim_rows):
        for col in range(lim_cols):
            rules.append([index(col+j, row + j) for j in range(score)])
            ## index yang ini Ruwet Kah ? 
            ## Mudahnya asumsi, nilai row 3 dan score 3 ya 
            ## iter 1 index[0, 0 - 0 + 3 - 1 (2)] ( 6 )
            ## iter 2 index[1, 0 - 1 + 3 - 1 (1)] ( 4 )
            ## iter 3 index[2, ] ... (2)
            ##
            rules.append([index(col+j, row-j + score-1) for j in range(score)])
    return rules 
        
    
    





