import pygame as pg
import numpy as np

def board_to_fen(board, player):
    """Translates our internal board representation from a 2D-numpy array into the official FEN notation

    Args:
        board: [description]
        player: [description]

    Returns:
        fen: [description]
    """
    fen = ''
    special_fields = [(0, 0), (0, 7), (7, 0), (7, 7)]
    for y in range(7, -1, -1):
        empty_count = 0
        row_fen = ''
        for x in range(8):
            if (x, y) in special_fields:
                continue
            piece = board[y, x]
            if piece == "":
                empty_count += 1
            else:
                if empty_count > 0:
                    row_fen += str(empty_count)
                    empty_count = 0
                if piece == 'b':
                    row_fen += 'b0'
                elif piece == 'r':
                    row_fen += 'r0'
                else:
                    row_fen += piece
        if empty_count > 0:
            row_fen += str(empty_count)
        fen += row_fen
        if y != 0:
            fen += '/'
    fen += ' ' + player
    return fen

def fen_to_board(fen):
    """Translates the official FEN notation into our internal board representation (2D-numpy array)

    Args:
        fen: [description]

    Returns:
        board: [description]
        player: [description]
    """
    board = np.empty((8, 8), dtype='U10')
    special_fields = [(0, 0), (0, 7), (7, 0), (7, 7)]
    for field in special_fields:
        board[field[1], field[0]] = "X"

    x, y = 0, 7
    position, player = fen.split()
    i = 0
    while i < len(position):
        if (x, y) in special_fields:
            x += 1
            continue

        char = position[i]

        if char.isalpha():
            if i + 1 < len(position):
                next_char = position[i + 1]
                if char == next_char:
                    piece = char + next_char
                    board[y, x] = piece
                    i += 1
                elif (char == 'r' and next_char == '0') or (char == 'b' and next_char == '0'):
                    piece = 'r' if char == 'r' else 'b'
                    board[y, x] = piece
                    i += 1
                elif (char == 'r' and next_char == 'b') or (char == 'b' and next_char == 'r'):
                    piece = 'rb' if char == 'r' else 'br'
                    board[y, x] = piece
                    i += 1
            else:
                board[y, x] = char
            x += 1

        elif char.isdigit():
            x += int(char)
        elif char == '/':
            y -= 1
            x = 0
        i += 1
    return board, player
