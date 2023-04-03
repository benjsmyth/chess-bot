"""Defines the chessboard."""

from itertools import chain, zip_longest
from .constants import *

class ChessBoard():
    """The chessboard."""

    BOARD_FILES = BOARD_FILES
    BOARD_POSIT = BOARD_POSIT
    BOARD_RANKS = BOARD_RANKS
    BOARD_WIDTH = BOARD_WIDTH

    @staticmethod
    def _file_to_index(file):
        """Convert a file letter to an index."""
        return ord(file.lower()) - 97

    @staticmethod
    def _pos_to_int(pos):
        """Convert a board position to an integer."""
        return ord(pos[0]) + int(pos[1])

    def __init__(self):
        """Initialize the board."""
        self.matrix = [
            [None for _ in range(ChessBoard.BOARD_WIDTH)] for _ in range(ChessBoard.BOARD_WIDTH)
        ]

    # BOARD DISPLAY
    def display(self):
        """Display the board."""
        print("\n")
        for rank, row in enumerate(self.matrix):
            print(rank + 1, end=' | ')
            for piece in row:
                print(" . " if piece is None else piece, end=' ')
            print("\n")
        print("     ", end='')
        for file in FILE_LETTERS.upper():
            print(file + "   ", end='')
        print("\n")

    def get(self, pos):
        """Get a piece off the board."""
        file, rank = pos
        return self.matrix[int(rank) - 1][ChessBoard._file_to_index(file)]

    def get_attack_points(self, proponent, neighbourhood, king):
        """Compute the lines of fire aiming at a King."""
        attack_points = set()
        for neighbour in neighbourhood:
            if self.get(neighbour) is None:
                to_file, to_rank = neighbour
                # Pawn, Knight, King

        to_file, to_rank = king.pos
        for piece in chain(*proponent.pieces.values()):
            fr_file, fr_rank = piece.pos
            file_dist = ord(to_file) - ord(fr_file)
            rank_dist = int(to_rank) - int(fr_rank)
            action = abs(file_dist), abs(rank_dist)
            if piece.name == 'Pawn':
                if proponent == 0:
                    if to_rank > fr_rank:
                        continue
                else:
                    if to_rank < fr_rank:
                        continue
            else:
                # Initialize pathway.
                pathway = None
                # Match by piece.
                match piece.name:
                    # Determine vertical/horizontal pathway.
                    case 'Rook':
                        if file_dist == 0:
                            rank_path = list(range(
                                min(int(fr_rank), int(to_rank)),
                                max(int(fr_rank), int(to_rank))
                            ))
                            if len(rank_path) > 0:
                                pathway = zip_longest(fr_file, rank_path, fillvalue=fr_file)
                        elif rank_dist == 0:
                            file_path = list(chr(file) for file in range(
                                min(ord(fr_file), ord(to_file)),
                                max(ord(fr_file), ord(to_file))
                            ))
                            if len(file_path) > 0:
                                pathway = zip_longest(file_path, fr_rank, fillvalue=fr_rank)

                    # Determine diagonal pathway.
                    case 'Bishop':
                        if abs(file_dist) == abs(rank_dist):
                            if int(fr_rank) < int(to_rank):
                                rank_path = list(range(
                                    min(int(fr_rank), int(to_rank)),
                                    max(int(fr_rank), int(to_rank))
                                ))
                            else:
                                rank_path = list(range(
                                    max(int(fr_rank), int(to_rank)),
                                    min(int(fr_rank), int(to_rank)), -1
                                ))
                            if ord(fr_file) < ord(to_file):
                                file_path = list(chr(file) for file in range(
                                    min(ord(fr_file), ord(to_file)),
                                    max(ord(fr_file), ord(to_file))
                                ))
                            else:
                                file_path = list(chr(file) for file in range(
                                    max(ord(fr_file), ord(to_file)),
                                    min(ord(fr_file), ord(to_file)), -1
                                ))
                            if len(rank_path) > 0 and len(file_path) > 0:
                                pathway = zip(file_path, rank_path)

                    # Determine any pathway.
                    case 'Queen':
                        if file_dist == 0:
                            rank_path = list(range(
                                min(int(fr_rank), int(to_rank)),
                                max(int(fr_rank), int(to_rank))
                            ))
                            if len(rank_path) > 0:
                                pathway = zip_longest(fr_file, rank_path, fillvalue=fr_file)
                        elif rank_dist == 0:
                            file_path = list(chr(file) for file in range(
                                min(ord(fr_file), ord(to_file)),
                                max(ord(fr_file), ord(to_file))
                            ))
                            if len(file_path) > 0:
                                pathway = zip_longest(file_path, fr_rank, fillvalue=fr_rank)
                        elif abs(file_dist) == abs(rank_dist):
                            if int(fr_rank) < int(to_rank):
                                rank_path = list(range(
                                    min(int(fr_rank), int(to_rank)),
                                    max(int(fr_rank), int(to_rank))
                                ))
                            else:
                                rank_path = list(range(
                                    max(int(fr_rank), int(to_rank)),
                                    min(int(fr_rank), int(to_rank)), -1
                                ))
                            if ord(fr_file) < ord(to_file):
                                file_path = list(chr(file) for file in range(
                                    min(ord(fr_file), ord(to_file)),
                                    max(ord(fr_file), ord(to_file))
                                ))
                            else:
                                file_path = list(chr(file) for file in range(
                                    max(ord(fr_file), ord(to_file)),
                                    min(ord(fr_file), ord(to_file)), -1
                                ))
                            if len(rank_path) > 0 and len(file_path) > 0:
                                pathway = zip(file_path, rank_path)

                # Check for an obstacle in pathway.
                if pathway is not None:
                    pathway = set(map(lambda p: p[0] + str(p[1]), pathway))
                    for pos in pathway:
                        block = self.get(pos)
                        if block is not None:
                            continue
                    # No obstacle, but is there a King?
                    for neighbour in neighbourhood:
                        if neighbour in pathway:
                            for attack_point in pathway:
                                attack_points.add(attack_point)

            # if action in piece.actions:
            #     attack_points.add(neighbour)
        return attack_points

    def get_neighbourhood(self, pos):
        """Compute the neighbourhood at or around a King."""
        neighbourhood = set()
        fr_file, fr_rank = pos
        for pos in BOARD_POSIT:
            to_file, to_rank = pos
            file_dist = ord(to_file) - ord(fr_file)
            rank_dist = int(to_rank) - int(fr_rank)
            distance = max(abs(file_dist), abs(rank_dist))
            if distance <= 1:
                neighbourhood.add(pos)
        return set(filter(lambda p: self.get(p) is None, neighbourhood))

    # CHECK
    def king_in_check(self, proponent, opponent):
        """Determine if opposing King is in check."""
        king = opponent.pieces['King'][0]  # Get opposing King
        neighbourhood = self.get_neighbourhood(king.pos)  # Get neighbourhood
        attack_points = self.get_attack_points(proponent, neighbourhood, king)  # Get first line of fire found
        if len(attack_points) > 0:  # Line of fire exists?
            if any(map(lambda p: p in attack_points, neighbourhood)):  # Any neighbour in line of fire?
                # Check if another piece can defend the king
                for attack_point in attack_points:
                    # for neighbour in neighbourhood:
                    #     if self.get(neighbour) is None:
                    #         to_file, to_rank = neighbour
                    #         # Pawn, Knight, King

                    to_file, to_rank = attack_point
                    for piece in chain(*opponent.pieces.values()):
                        fr_file, fr_rank = piece.pos
                        file_dist = ord(to_file) - ord(fr_file)
                        rank_dist = int(to_rank) - int(fr_rank)
                        action = abs(file_dist), abs(rank_dist)
                        if piece.name == 'Pawn':
                            if proponent == 0:
                                if to_rank > fr_rank:
                                    continue
                            else:
                                if to_rank < fr_rank:
                                    continue
                        else:
                            # Initialize pathway.
                            pathway = None
                            # Match by piece.
                            match piece.name:
                                # Determine vertical/horizontal pathway.
                                case 'Rook':
                                    if file_dist == 0:
                                        rank_path = list(range(
                                            min(int(fr_rank), int(to_rank)) + 1,
                                            max(int(fr_rank), int(to_rank)) + 1
                                        ))
                                        if len(rank_path) > 0:
                                            pathway = zip_longest(fr_file, rank_path, fillvalue=fr_file)
                                    elif rank_dist == 0:
                                        file_path = list(chr(file) for file in range(
                                            min(ord(fr_file), ord(to_file)) + 1,
                                            max(ord(fr_file), ord(to_file)) + 1
                                        ))
                                        if len(file_path) > 0:
                                            pathway = zip_longest(file_path, fr_rank, fillvalue=fr_rank)

                                # Determine diagonal pathway.
                                case 'Bishop':
                                    if abs(file_dist) == abs(rank_dist):
                                        if int(fr_rank) < int(to_rank):
                                            rank_path = list(range(
                                                min(int(fr_rank), int(to_rank)) + 1,
                                                max(int(fr_rank), int(to_rank)) + 1
                                            ))
                                        else:
                                            rank_path = list(range(
                                                max(int(fr_rank), int(to_rank)) - 1,
                                                min(int(fr_rank), int(to_rank)) - 1, -1
                                            ))
                                        if ord(fr_file) < ord(to_file):
                                            file_path = list(chr(file) for file in range(
                                                min(ord(fr_file), ord(to_file)) + 1,
                                                max(ord(fr_file), ord(to_file)) + 1
                                            ))
                                        else:
                                            file_path = list(chr(file) for file in range(
                                                max(ord(fr_file), ord(to_file)) - 1,
                                                min(ord(fr_file), ord(to_file)) - 1, -1
                                            ))
                                        if len(rank_path) > 0 and len(file_path) > 0:
                                            pathway = zip(file_path, rank_path)

                                # Determine any pathway.
                                case 'Queen':
                                    if file_dist == 0:
                                        rank_path = list(range(
                                            min(int(fr_rank), int(to_rank)) + 1,
                                            max(int(fr_rank), int(to_rank)) + 1
                                        ))
                                        if len(rank_path) > 0:
                                            pathway = zip_longest(fr_file, rank_path, fillvalue=fr_file)
                                    elif rank_dist == 0:
                                        file_path = list(chr(file) for file in range(
                                            min(ord(fr_file), ord(to_file)) + 1,
                                            max(ord(fr_file), ord(to_file)) + 1
                                        ))
                                        if len(file_path) > 0:
                                            pathway = zip_longest(file_path, fr_rank, fillvalue=fr_rank)
                                    elif abs(file_dist) == abs(rank_dist):
                                        if int(fr_rank) < int(to_rank):
                                            rank_path = list(range(
                                                min(int(fr_rank), int(to_rank)) + 1,
                                                max(int(fr_rank), int(to_rank)) + 1
                                            ))
                                        else:
                                            rank_path = list(range(
                                                max(int(fr_rank), int(to_rank)) - 1,
                                                min(int(fr_rank), int(to_rank)), -1
                                            ))
                                        if ord(fr_file) < ord(to_file):
                                            file_path = list(chr(file) for file in range(
                                                min(ord(fr_file), ord(to_file)) + 1,
                                                max(ord(fr_file), ord(to_file)) + 1
                                            ))
                                        else:
                                            file_path = list(chr(file) for file in range(
                                                max(ord(fr_file), ord(to_file)) - 1,
                                                min(ord(fr_file), ord(to_file)), -1
                                            ))
                                        if len(rank_path) > 0 and len(file_path) > 0:
                                            pathway = zip(file_path, rank_path)

                            # Check for an obstacle in pathway.
                            blocked = False
                            if pathway is not None:
                                pathway = set(map(lambda p: p[0] + str(p[1]), pathway))
                                for pos in pathway:
                                    block = self.get(pos)
                                    if block is not None and block.team != proponent.team:
                                        blocked = True
                                        break
                                # No obstacle, but defense?
                                if blocked and attack_point in pathway:
                                    return False  # King can be defended
                return True  # King in check
        return False  # King not in check

    # CHECKMATE
    def king_in_checkmate(self, proponent, opponent):
        """Determine if opposing King is in checkmate."""
        king = opponent.pieces['King'][0]  # Get opposing King
        neighbourhood = self.get_neighbourhood(king.pos)  # Get neighbourhood
        attack_points = self.get_attack_points(proponent, neighbourhood, king)  # Get lines of fire
        if len(attack_points) > 0:
            if all(map(lambda p: p in attack_points, neighbourhood)):  # All neighbours in line of fire?
                # Check if another piece can defend the king
                for attack_point in attack_points:
                    # for neighbour in neighbourhood:
                    #     if self.get(neighbour) is None:
                    #         to_file, to_rank = neighbour
                    #         # Pawn, Knight, King

                    to_file, to_rank = attack_point
                    for piece in chain(*opponent.pieces.values()):
                        fr_file, fr_rank = piece.pos
                        file_dist = ord(to_file) - ord(fr_file)
                        rank_dist = int(to_rank) - int(fr_rank)
                        action = abs(file_dist), abs(rank_dist)
                        if piece.name == 'Pawn':
                            if proponent.near:
                                if to_rank > fr_rank:
                                    continue
                            else:
                                if to_rank < fr_rank:
                                    continue
                        else:
                            # Initialize pathway.
                            pathway = None
                            # Match by piece.
                            match piece.name:
                                # Determine vertical/horizontal pathway.
                                case 'Rook':
                                    if file_dist == 0:
                                        rank_path = list(range(
                                            min(int(fr_rank), int(to_rank)) + 1,
                                            max(int(fr_rank), int(to_rank)) + 1
                                        ))
                                        if len(rank_path) > 0:
                                            pathway = zip_longest(fr_file, rank_path, fillvalue=fr_file)
                                    elif rank_dist == 0:
                                        file_path = list(chr(file) for file in range(
                                            min(ord(fr_file), ord(to_file)) + 1,
                                            max(ord(fr_file), ord(to_file)) + 1
                                        ))
                                        if len(file_path) > 0:
                                            pathway = zip_longest(file_path, fr_rank, fillvalue=fr_rank)

                                # Determine diagonal pathway.
                                case 'Bishop':
                                    if abs(file_dist) == abs(rank_dist):
                                        if int(fr_rank) < int(to_rank):
                                            rank_path = list(range(
                                                min(int(fr_rank), int(to_rank)) + 1,
                                                max(int(fr_rank), int(to_rank)) + 1
                                            ))
                                        else:
                                            rank_path = list(range(
                                                max(int(fr_rank), int(to_rank)) - 1,
                                                min(int(fr_rank), int(to_rank)) - 1, -1
                                            ))
                                        if ord(fr_file) < ord(to_file):
                                            file_path = list(chr(file) for file in range(
                                                min(ord(fr_file), ord(to_file)) + 1,
                                                max(ord(fr_file), ord(to_file)) + 1
                                            ))
                                        else:
                                            file_path = list(chr(file) for file in range(
                                                max(ord(fr_file), ord(to_file)) - 1,
                                                min(ord(fr_file), ord(to_file)) - 1, -1
                                            ))
                                        if len(rank_path) > 0 and len(file_path) > 0:
                                            pathway = zip(file_path, rank_path)

                                # Determine any pathway.
                                case 'Queen':
                                    if file_dist == 0:
                                        rank_path = list(range(
                                            min(int(fr_rank), int(to_rank)) + 1,
                                            max(int(fr_rank), int(to_rank)) + 1
                                        ))
                                        if len(rank_path) > 0:
                                            pathway = zip_longest(fr_file, rank_path, fillvalue=fr_file)
                                    elif rank_dist == 0:
                                        file_path = list(chr(file) for file in range(
                                            min(ord(fr_file), ord(to_file)) + 1,
                                            max(ord(fr_file), ord(to_file)) + 1
                                        ))
                                        if len(file_path) > 0:
                                            pathway = zip_longest(file_path, fr_rank, fillvalue=fr_rank)
                                    elif abs(file_dist) == abs(rank_dist):
                                        if int(fr_rank) < int(to_rank):
                                            rank_path = list(range(
                                                min(int(fr_rank), int(to_rank)) + 1,
                                                max(int(fr_rank), int(to_rank)) + 1
                                            ))
                                        else:
                                            rank_path = list(range(
                                                max(int(fr_rank), int(to_rank)) - 1,
                                                min(int(fr_rank), int(to_rank)), -1
                                            ))
                                        if ord(fr_file) < ord(to_file):
                                            file_path = list(chr(file) for file in range(
                                                min(ord(fr_file), ord(to_file)) + 1,
                                                max(ord(fr_file), ord(to_file)) + 1
                                            ))
                                        else:
                                            file_path = list(chr(file) for file in range(
                                                max(ord(fr_file), ord(to_file)) - 1,
                                                min(ord(fr_file), ord(to_file)), -1
                                            ))
                                        if len(rank_path) > 0 and len(file_path) > 0:
                                            pathway = zip(file_path, rank_path)

                            # Check for an obstacle in pathway.
                            blocked = False
                            if pathway is not None:
                                pathway = set(map(lambda p: p[0] + str(p[1]), pathway))
                                for pos in pathway:
                                    block = self.get(pos)
                                    if block is not None and block.team != proponent.team:
                                        blocked = True
                                        break
                                # No obstacle, but defense?
                                if blocked and attack_point in pathway:
                                    return False  # King can be defended
                return True  # King in checkmate
        return False  # King not in checkmate

    def legal_move(self, fr, to, player, feedback=False):
        """Validate a move."""
        team = player.team

        # Off-bounds check
        if fr.lower() not in BOARD_POSIT or to.lower() not in BOARD_POSIT:
            # print("\nYou can't move off the board!")
            return None

        # Extract files, ranks
        fr_file, fr_rank = fr.lower()
        to_file, to_rank = to.lower()

        # Basic error checks
        if fr == to:
            if feedback:
                print("\nYou can't move to the same space!")
            return False
        if self.get(fr) is None:
            if feedback:
                print("\nYou can't move from an empty space!")
            return False
        if self.get(fr).team != team:
            if feedback:
                print("\nYou can't move the other player's pieces!")
            return False

        # Compute distances
        file_dist = ord(to_file) - ord(fr_file)
        rank_dist = int(to_rank) - int(fr_rank)

        # Compute absolute action
        action = abs(file_dist), abs(rank_dist)

        # Get pieces
        piece = self.get(fr)
        other = self.get(to)

        # Error check pawn
        if piece.name == 'Pawn':
            if player.near:
                if to_rank > fr_rank:
                    if feedback:
                        print("\nYou can't move a Pawn backwards!")
                    return False
            else:
                if to_rank < fr_rank:
                    if feedback:
                        print("\nYou can't move a Pawn backwards!")
                    return False
            if action == (0, 1) and other is not None:
                if feedback:
                    print("\nYou can't attack forwards with a Pawn!")
                return False
            if action == (0, 2) and piece.status == True:
                if feedback:
                    print("\nYou can't do that anymore!")
                return False
            if action == (1, 1) and other is None:
                if feedback:
                    print("\nYou can't attack an empty space!")
                return False
            if piece.status == False:
                piece.status = True
        else:
            # Initialize pathway.
            pathway = None
            # Match by piece.
            match piece.name:
                # Determine vertical/horizontal pathway.
                case 'Rook':
                    if file_dist == 0:
                        rank_path = list(range(
                            min(int(fr_rank), int(to_rank)) + 1,
                            max(int(fr_rank), int(to_rank))
                        ))
                        if len(rank_path) > 0:
                            pathway = zip_longest(fr_file, rank_path, fillvalue=fr_file)
                    elif rank_dist == 0:
                        file_path = list(chr(file) for file in range(
                            min(ord(fr_file), ord(to_file)) + 1,
                            max(ord(fr_file), ord(to_file))
                        ))
                        if len(file_path) > 0:
                            pathway = zip_longest(file_path, fr_rank, fillvalue=fr_rank)

                # Determine diagonal pathway.
                case 'Bishop':
                    if abs(file_dist) == abs(rank_dist):
                        if int(fr_rank) < int(to_rank):
                            rank_path = list(range(
                                min(int(fr_rank), int(to_rank)) + 1,
                                max(int(fr_rank), int(to_rank))
                            ))
                        else:
                            rank_path = list(range(
                                max(int(fr_rank), int(to_rank)) - 1,
                                min(int(fr_rank), int(to_rank)), -1
                            ))
                        if ord(fr_file) < ord(to_file):
                            file_path = list(chr(file) for file in range(
                                min(ord(fr_file), ord(to_file)) + 1,
                                max(ord(fr_file), ord(to_file))
                            ))
                        else:
                            file_path = list(chr(file) for file in range(
                                max(ord(fr_file), ord(to_file)) - 1,
                                min(ord(fr_file), ord(to_file)), -1
                            ))
                        if len(rank_path) > 0 and len(file_path) > 0:
                            pathway = zip(file_path, rank_path)

                # Determine any pathway.
                case 'Queen':
                    if file_dist == 0:
                        rank_path = list(range(
                            min(int(fr_rank), int(to_rank)) + 1,
                            max(int(fr_rank), int(to_rank))
                        ))
                        if len(rank_path) > 0:
                            pathway = zip_longest(fr_file, rank_path, fillvalue=fr_file)
                    elif rank_dist == 0:
                        file_path = list(chr(file) for file in range(
                            min(ord(fr_file), ord(to_file)) + 1,
                            max(ord(fr_file), ord(to_file))
                        ))
                        if len(file_path) > 0:
                            pathway = zip_longest(file_path, fr_rank, fillvalue=fr_rank)
                    elif abs(file_dist) == abs(rank_dist):
                        if int(fr_rank) < int(to_rank):
                            rank_path = list(range(
                                min(int(fr_rank), int(to_rank)) + 1,
                                max(int(fr_rank), int(to_rank))
                            ))
                        else:
                            rank_path = list(range(
                                max(int(fr_rank), int(to_rank)) - 1,
                                min(int(fr_rank), int(to_rank)), -1
                            ))
                        if ord(fr_file) < ord(to_file):
                            file_path = list(chr(file) for file in range(
                                min(ord(fr_file), ord(to_file)) + 1,
                                max(ord(fr_file), ord(to_file))
                            ))
                        else:
                            file_path = list(chr(file) for file in range(
                                max(ord(fr_file), ord(to_file)) - 1,
                                min(ord(fr_file), ord(to_file)), -1
                            ))
                        if len(rank_path) > 0 and len(file_path) > 0:
                            pathway = zip(file_path, rank_path)

                # Determine if this puts me in check(mate), or not.
                # If it does, it's an invalid move.
                case 'King':
                    ...

            # Check for an obstacle in pathway.
            if pathway is not None:
                for file, rank in pathway:
                    pos = file + str(rank)
                    block = self.get(pos)
                    if block is not None:
                        if feedback:
                            print(f"\nThere is a {block.name} in the way!")
                        return None
                # No obstacle, this action is valid.
                piece.actions.add(action)

        # Check for captured piece, or not, or invalid action.
        if action in piece.actions:
            if other is not None:
                if other.team != piece.team:
                    return True
                else:
                    if feedback:
                        print(f"\nYou can't attack your own pieces!")
                    return False
            else:
                return True
        else:
            if feedback:
                print(f"\nYou can't do that with a {piece.name}!")
            return False

    # MOVEMENT / TAKING
    def move(self, fr, to, feedback=False):
        """Move a chesspiece from one position to another."""
        piece = self.get(fr)
        captured = self.get(to)
        if captured is not None:
            self.set(piece, to)
            piece.pos = to
            self.set(None, fr)
            if feedback:
                print(f"\n{piece}: {fr} -> {to}")
                print(f"\nCaptured a {captured.name}.")
            return captured
        else:
            self.set(piece, to)
            piece.pos = to
            self.set(None, fr)
            if feedback:
                print(f"\n{piece}: {fr} -> {to}")
            return False

    def set(self, piece, pos):
        """Set a piece on the board."""
        file, rank = pos
        self.matrix[int(rank) - 1][ChessBoard._file_to_index(file)] = piece

    def setup(self, pieces_p1, pieces_p2):
        """Setup the board."""
        # P1 setup
        for pawn, pos in zip(pieces_p1["Pawn"], BOARD_RANKS[7 - 1]):
            pawn.pos = pos
            self.set(pawn, pos)
        for rook, pos in zip(pieces_p1["Rook"], ('a8', 'h8')):
            rook.pos = pos
            self.set(rook, pos)
        for knight, pos in zip(pieces_p1["Knight"], ('b8', 'g8')):
            knight.pos = pos
            self.set(knight, pos)
        for bishop, pos in zip(pieces_p1["Bishop"], ('c8', 'f8')):
            bishop.pos = pos
            self.set(bishop, pos)
        pieces_p1["Queen"][0].pos = 'd8'; self.set(pieces_p1["Queen"][0], 'd8')
        pieces_p1["King"][0].pos = 'e8'; self.set(pieces_p1["King"][0], 'e8')

        # P2 setup
        for pawn, pos in zip(pieces_p2["Pawn"], BOARD_RANKS[2 - 1]):
            pawn.pos = pos
            self.set(pawn, pos)
        for rook, pos in zip(pieces_p2["Rook"], ('a1', 'h1')):
            rook.pos = pos
            self.set(rook, pos)
        for knight, pos in zip(pieces_p2["Knight"], ('b1', 'g1')):
            knight.pos = pos
            self.set(knight, pos)
        for bishop, pos in zip(pieces_p2["Bishop"], ('c1', 'f1')):
            bishop.pos = pos
            self.set(bishop, pos)
        pieces_p2["Queen"][0].pos = 'd1'; self.set(pieces_p2["Queen"][0], 'd1')
        pieces_p2["King"][0].pos = 'e1'; self.set(pieces_p2["King"][0], 'e1')
