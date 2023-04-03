from itertools import groupby

TEAM_WHITE = 'WHITE'
TEAM_BLACK = 'BLACK'

FILE_LETTERS = "abcdefgh"
RANK_NUMBERS = "12345678"

BOARD_WIDTH = 8
BOARD_POSIT = [f"{file}{rank}" for file in FILE_LETTERS for rank in RANK_NUMBERS]
BOARD_FILES = [list(group) for _, group in groupby(BOARD_POSIT, key=lambda pos: pos[0])]
BOARD_RANKS = [list(col) for col in zip(*BOARD_FILES)]
