"""Defines the player interface."""

class Player:
    """The player."""

    def __init__(self, team, pieces, near=False):
        self.team = team
        self.pieces = pieces
        self.pieces_won = set()
        self.near = near

    def __str__(self):
        return f"{self.team}\n"
