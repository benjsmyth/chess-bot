# chessbot
An artificially intelligent chess player.

Instructions:
    - Run `python3 chess.py`

Completed requirements:
    - Board environment (see `chessboard.py`, but be warned - it's a bit of a mess!)
        - Board display
        - Piece taking
        - Piece movement
            - Although I believe I covered nearly all cases of legal and illegal movements,
                there is quite likely something that I missed.
            - Consequently the AI may choose to make an illegal move that I never considered checking.
            - One significant bug is that the AI does not recognize a 2-Pawn opener as a legal move.
    - AI environment (see `computer.py`)
        - Internal state
        - AB-minimax

Incomplete requirements:
    - Promotion (not attempted)
    - Castling (not attempted)
    - Stalemate (not attempted)
    - Check / Checkmate
        - I wrote quite a bit of code for this but in the end I did not wrap it up.
        - On each turn the program runs a test. It does this by examining the neighbourhood surrounding the opponent's King,
            and then inspecting the lines of fire of the attacking pieces.
        - This is actually a LOT more complicated than I realized ...
        - Since this functionality is incomplete, it may signal Check / Checkmate at the right or wrong times.
        - Consequently the game could possibly crash on ending, because I did not test this far enough.

Evaluation method:
    - Simple weighted sum of (# of attacking pieces - # of opposing pieces).
    - Rather than being simple values, the weights are instead a maximum count of the # of spaces a piece can cover.
    - For example, a Rook can occupy 8 spaces in either direction, for a total of 16.

Overall:
    - Yet another case of starting later than I should have ...
    - Most thoroughly tested modes are 2-player and 1-player as White.
    - Generally works nicely, the important part for me was just getting the AI to work.
    - Enjoy!
    
