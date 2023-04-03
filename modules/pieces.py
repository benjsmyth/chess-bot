# Defines the chess pieces.

from .chessboard import BOARD_WIDTH
from .constants import TEAM_BLACK, TEAM_WHITE

class ChessPiece():
    """A generic chesspiece."""

    def __init__(self, team, actions):
        """Defines a particular chesspiece."""
        self.team = team
        self.actions = actions
        self.moves = set()
        self.pos = None
        self.name = self.__class__.__name__

    def __str__(self):
        """Returns a string representation of the chesspiece."""
        return f"{self.team[0].lower()}{self.name[:2]}"

# Standard chesspieces
class Pawn(ChessPiece):
    """The Pawn chesspiece."""
    WEIGHT = 3
    def __init__(self, team):
        super().__init__(
            team, {(-1, 1), (0, 1), (0, 2), (1, 1)}
        ),
        self.status = False

class Rook(ChessPiece):
    """The Rook chesspiece."""
    WEIGHT = 16
    def __init__(self, team):
        super().__init__(
            team, {(-1, 0), (0, -1), (0, 1), (1, 0)}
        )

class Knight(ChessPiece):
    """The Knight chesspiece."""
    WEIGHT = 24
    def __init__(self, team):
        super().__init__(
            team, {(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)}
        )

class Bishop(ChessPiece):
    """The Bishop chesspiece."""
    WEIGHT = 16
    def __init__(self, team):
        super().__init__(
            team, {(-1, -1), (-1, 1), (1, -1), (1, 1)}
        )

class Queen(ChessPiece):
    """The Queen chesspiece."""
    WEIGHT = 40
    def __init__(self, team):
        super().__init__(
            team, {(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)}
        )

class King(ChessPiece):
    """The King chesspiece."""
    WEIGHT = 8
    def __init__(self, team):
        super().__init__(
            team, {(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)}
        )

# Chesspiece sets
black_set = {
    'Pawn': [Pawn(TEAM_BLACK) for _ in range(BOARD_WIDTH)],
    'Rook': [Rook(TEAM_BLACK), Rook(TEAM_BLACK)],
    'Knight': [Knight(TEAM_BLACK), Knight(TEAM_BLACK)],
    'Bishop': [Bishop(TEAM_BLACK), Bishop(TEAM_BLACK)],
    'Queen': [Queen(TEAM_BLACK)],
    'King': [King(TEAM_BLACK)]
}

white_set = {
    'Pawn': [Pawn(TEAM_WHITE) for _ in range(BOARD_WIDTH)],
    'Rook': [Rook(TEAM_WHITE), Rook(TEAM_WHITE)],
    'Knight': [Knight(TEAM_WHITE), Knight(TEAM_WHITE)],
    'Bishop': [Bishop(TEAM_WHITE), Bishop(TEAM_WHITE)],
    'Queen': [Queen(TEAM_WHITE)],
    'King': [King(TEAM_WHITE)]
}
