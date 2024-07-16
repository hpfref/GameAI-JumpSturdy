import pygame as pg
import numpy as np

def board_to_fen(board, player):
    """
    Translates our internal board representation from a 2D-numpy array into the official FEN notation.
    This function is designed to convert the current state of the board into a string format that represents 
    the placement of pieces on the board, excluding special fields (corners in this case), and indicates the current player. 

    Args:
        board (2D Array): Responsible for storing the current state of the board, including the placement of pieces and special fields.
        player (str): A string indicating the current player ('b' for blue or 'r' for red).

    Returns:
        str: A string representing the board state in FEN notation. The notation includes the arrangement of pieces on the board,
             excluding the pieces on special fields (corners), followed by the current player ('b' or 'r').

    Note:
        - The FEN notation generated by this function includes a custom adaptation for representing pieces: 'b0' for blue and 'r0' for red.
        - Special fields (corners of the board) are excluded from the notation.
        - The function iterates over the board in reverse order (starting from the top row) to match the FEN notation standard,
          where the board is described from the 8th row to the 1st row.
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
    """
    Translates the official FEN notation into our internal 2D-numpy array board representation.
    This function is designed to convert the string format into the current state of the board that represents 
    the placement of pieces on the board, excluding special fields (corners in this case), and indicates the current player. 

    Args:
        str: A string representing the board state in FEN notation. The notation includes the arrangement of pieces on the board,
             excluding the pieces on special fields (corners), followed by the current player ('b' or 'r').

    Returns:
        board (2D Array): Responsible for storing the current state of the board, including the placement of pieces and special fields.
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