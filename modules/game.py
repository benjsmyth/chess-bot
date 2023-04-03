"""Defines the game process."""

from copy import deepcopy
from itertools import chain
from .constants import BOARD_POSIT, TEAM_WHITE
from .pieces import *

class Game:
    """A game of chess."""

    WINNER = None

    def __init__(self, player_one, player_two, chessboard):
        """Initialize game."""
        chessboard.setup(player_one.pieces, player_two.pieces)
        self.P1 = player_one
        self.P2 = player_two
        self.board = chessboard
        self.turn = player_one \
            if player_one.team == TEAM_WHITE \
            else player_two

    # ACTIONS
    def actions(self, state):
        """Return the set of legal moves."""
        legal_moves = set()
        for piece_type in state['player'].pieces.values():
            for piece in piece_type:
                for pos in BOARD_POSIT:
                    if state['board'].legal_move(piece.pos, pos, state['player']):
                        legal_moves.add((piece.pos, pos))
        return legal_moves

    # EVALUATE
    def evaluate(self, state):
        """Evaluate the board state."""
        return sum((
            Pawn.WEIGHT * (len(state['player'].pieces['Pawn']) - len(state['opponent'].pieces['Pawn'])),
            Rook.WEIGHT * (len(state['player'].pieces['Rook']) - len(state['opponent'].pieces['Rook'])),
            Knight.WEIGHT * (len(state['player'].pieces['Knight']) - len(state['opponent'].pieces['Knight'])),
            Bishop.WEIGHT * (len(state['player'].pieces['Bishop']) - len(state['opponent'].pieces['Bishop'])),
            Queen.WEIGHT * (len(state['player'].pieces['Queen']) - len(state['opponent'].pieces['Queen']))
        ))

    def loop_one(self):
        """Loop through a one-player game."""
        while True:
            print(f"\n{self.turn.team} TO PLAY")
            self.board.display()
            if self.turn is self.P1:  # Player turn
                while True:
                    fr, to = input("\nMove: ").split()
                    if self.board.legal_move(fr, to, self.P1, True):
                        if captured := self.board.move(fr, to, True):
                            self.P1.pieces_won.add(captured)
                            self.P2.pieces[captured.name].remove(captured)
                        break
                    else:
                        print("Please try again.\n")
            else:  # Computer turn
                state = {
                    'board': deepcopy(self.board),
                    'max_depth': 3,
                    'opponent': deepcopy(self.P1),
                    'player': deepcopy(self.P2)
                }
                fr, to = self.P2.alpha_beta_search(self, state, 0)
                if captured := self.board.move(fr, to):
                    self.P2.pieces_won.add(captured)
                    self.P1.pieces[captured.name].remove(captured)

            if self.turn is self.P1:
                print("P2 King in check: ", self.board.king_in_check(self.P1, self.P2))
                print("P2 King in checkmate: ", self.board.king_in_checkmate(self.P1, self.P2))
            else:
                print("P1 King in check: ", self.board.king_in_check(self.P2, self.P1))
                print("P1 King in checkmate: ", self.board.king_in_checkmate(self.P2, self.P1))

            self.turn = self.P1 \
                if self.turn is self.P2 \
                else self.P2

            print("\nPieces won:")
            print("P1:", end=' ')
            for piece in self.P1.pieces_won:
                print(piece, end=', ')
            print()
            print("P2:", end=' ')
            for piece in self.P2.pieces_won:
                print(piece, end=', ')
            print()

    def loop_two(self):
        """Loop through a two-player game."""
        while True:
            print(f"\n{self.turn.team} TO PLAY")
            self.board.display()
            if self.turn is self.P1:  # P1 turn
                while True:
                    fr, to = input("\nMove: ").split()
                    if self.board.legal_move(fr, to, self.P1, True):
                        if captured := self.board.move(fr, to, True):
                            self.P1.pieces_won.add(captured)
                            self.P2.pieces[captured.name].remove(captured)
                        break
                    else:
                        print("Please try again.\n")
            else:  # P2 turn
                while True:
                    fr, to = input("\nMove: ").split()
                    if self.board.legal_move(fr, to, self.P2, True):
                        if captured := self.board.move(fr, to, True):
                            self.P2.pieces_won.add(captured)
                            self.P1.pieces[captured.name].remove(captured)
                        break
                    else:
                        print("Please try again.\n")

            if self.turn is self.P1:
                print("P2 King in check: ", self.board.king_in_check(self.P1, self.P2))
                print("P2 King in checkmate: ", self.board.king_in_checkmate(self.P1, self.P2))
            else:
                print("P1 King in check: ", self.board.king_in_check(self.P2, self.P1))
                print("P1 King in checkmate: ", self.board.king_in_checkmate(self.P2, self.P1))

            self.turn = self.P1 \
                if self.turn is self.P2 \
                else self.P2

            print("\nPieces won:")
            print("P1:", end=' ')
            for piece in self.P1.pieces_won:
                print(piece, end=', ')
            print()
            print("P2:", end=' ')
            for piece in self.P2.pieces_won:
                print(piece, end=', ')
            print()

            if self.board.king_in_checkmate(self.P1, self.P2):
                Game.WINNER = self.P1
                break
            elif self.board.king_in_checkmate(self.P2, self.P1):
                Game.WINNER = self.P2
                break

    def play_one(self):
        """Play a one-player game."""
        print("\nGAME START")
        self.loop_one()

    def play_two(self):
        """Play a two-player game."""
        print("\nGAME START")
        self.loop_two()

    # IS-CUTOFF
    def is_cutoff(self, state, depth):
        """Test for cut-off in game tree."""
        return depth == state['max_depth']

    # IS-TERMINAL
    def is_terminal(self, state):
        """Test for terminal in game tree."""
        return self.board.king_in_checkmate(state['player'], state['opponent'])

    def report(self):
        """Report game statistics."""
        print("\nGAME END")
        print(f"\n{Game.WINNER.team} WINS\n")

    # RESULT
    def result(self, state, action):
        """Return new state from action."""
        player, opponent = deepcopy(state['opponent']), deepcopy(state['player'])
        for piece_type in player.pieces:
            player.pieces[piece_type].clear()
        for piece_type in opponent.pieces:
            opponent.pieces[piece_type].clear()
        board = deepcopy(state['board'])
        fr, to = action
        board.move(fr, to)
        for pos in BOARD_POSIT:
            piece = board.get(pos)
            if piece is not None:
                if piece.team == player.team:
                    player.pieces[piece.name].append(piece)
                else:
                    opponent.pieces[piece.name].append(piece)
        return {
            'board': board,
            'max_depth': state['max_depth'],
            'opponent': opponent,
            'player': player
        }
