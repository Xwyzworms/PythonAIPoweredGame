from abc import ABC, abstractmethod
from numpy import argmax
from random import randint

class Player(ABC):
    """
    Abstract class For Player 
    So this can be easily expandable
    Args: ABC is Just A Class So that Player have abstract Behaviour
    """
    @abstractmethod
    def next_action(self, state):
        ...

class IndecisivePlayer(Player):
    """
    This Class For Both Player And AI inherited to
    The purpose of this class is to provide ...
    """
    def next_action(self, state):
        """
        This method is for traverse Node within Tree
        """
        moves = self.next_action(state)
        return moves[randint(0, len(moves) - 1)]

    @abstractmethod
    def next_actions(self, state):
        ...

class minimaxplayer(IndecisivePlayer):
    def __init__(self, lookahead):
        assert lookahead > 0
        self.lookahead = lookahead

    def next_actions(self, state):
        moves, _ = self.value(state, self.lookahead)
        return moves

    def value(self, state, lookahead):
        if lookahead == 0 or state.gameover():
            return [], 1.0*state.winner()*(lookahead+1)
        behaviour = max if state.player() == 1 else min
        return self.minimax(state, behaviour, lookahead)

    def minimax(self, state, behaviour, lookahead):
        moves, res = [], -10000*state.player()
        for cell in state.actions():
            _, v = self.value(state.move(cell), lookahead-1)
            if res == v:
                moves.append(cell)
            elif behaviour(res, v) == v:
                moves, res = [cell], v
        return moves, res


class NeuralNetPlayer(Player):
    def __init__(self, model):
        self.model = model

    def next_action(self, state):
        # Get all Actions the served while taking a node
        actions = state.actions()
        # What is The Player Situation 
        current_player = state.player()
        # Get All states if taking action for some cell ( Win Or Lose for example)
        states = [state.move(action).cells for action in actions]
        # Get the Probabilites Of opponent will win For all States
        probabilites = self.model.predict(states)
        player_probabilities = [p[current_player] for p in probabilites]
        ## Take The Actions With the highest Winning for player probabilities
        return actions[argmax(player_probabilities)]