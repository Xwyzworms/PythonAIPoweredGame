#%%
from state import make_rules, State

TicTacRules= make_rules(cols=3, rows=3, score=3)

class TicTacToeState(State):
    def __init__(self, cells=None):
        print("classTicState Initiated")
        super().__init__(cells, cols=3, rows=3, rules=TicTacRules)


# %%
