
test_FEN = "b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0 b"


def legal_moves_board(fen) -> list:
    """Return all legal moves for the current player

    Args:
        fen: board & player

    Returns:
        list: legal moves e.g. B1-B2, ...
    """
    board, player = fen.split(" ")
    moves = []
    



    return moves


def legal_moves_piece(fen, piece) -> list:
    """Return all legal moves of a single piece

    Args:
        fen: board & player
        piece: position of piece to move

    Returns:
        list: legal moves e.g. B1-B2, ...
    """
    board, player = fen.split(" ")
    moves = []
    



    return moves