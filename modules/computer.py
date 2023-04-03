"""Defines the computer (AI) interface."""

from math import inf
from .player import Player

class Computer(Player):
    """The computer (AI)."""

    def __init__(self, team, pieces, near=False):
        super().__init__(team, pieces, near),

    def __str__(self):
        return super().__str__()

    # A-B SEARCH
    def alpha_beta_search(self, game, state, depth):
        _, move = self.max_value(game, state, -inf, inf, depth + 1)
        return move

    # MAX-VALUE
    def max_value(self, game, state, alpha, beta, depth):
        if game.is_cutoff(state, depth) or game.is_terminal(state):
            return game.evaluate(state), None
        value = -inf
        for action in game.actions(state):
            successor, _ = self.min_value(game, game.result(state, action), alpha, beta, depth + 1)
            if successor > value:
                value, move = successor, action
                alpha = max(alpha, value)
            if value >= beta:
                return value, move
        return value, move

    # MIN-VALUE
    def min_value(self, game, state, alpha, beta, depth):
        if game.is_cutoff(state, depth) or game.is_terminal(state):
            return game.evaluate(state), None
        value = inf
        for action in game.actions(state):
            successor, _ = self.max_value(game, game.result(state, action), alpha, beta, depth + 1)
            if successor < value:
                value, move = successor, action
                beta = min(alpha, value)
            if value <= alpha:
                return value, move
        return value, move
