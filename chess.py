"""Defines the executable script for a running game."""

from modules import chessboard, computer, constants, game, pieces, player

print("\nChess\n")
NUM_PLAYERS = int(input("How many players? (1/2): "))  # Number of players
if NUM_PLAYERS == 1:  # 1-player game (against computer)
    P1_TEAM = input("P1 is White or Black? (w/b): ").lower()  # P1's team selection
    P1_TEAM = constants.TEAM_WHITE if P1_TEAM == 'w' else constants.TEAM_BLACK  # Reformat selection
    if P1_TEAM == constants.TEAM_WHITE:
        P1 = player.Player(constants.TEAM_WHITE, pieces.white_set, True)
        P2 = computer.Computer(constants.TEAM_BLACK, pieces.black_set)
    else:
        P1 = computer.Computer(constants.TEAM_BLACK, pieces.black_set, True)
        P2 = computer.Computer(constants.TEAM_WHITE, pieces.white_set)
    G = game.Game(P1, P2, chessboard.ChessBoard())  # New game
    G.play_one()  # Play
else:  # 2-player game
    P1 = player.Player(constants.TEAM_WHITE, pieces.white_set, True)
    P2 = player.Player(constants.TEAM_BLACK, pieces.black_set)
    G = game.Game(P1, P2, chessboard.ChessBoard())  # New game
    G.play_two()  # Play
G.report()  # Report winner
