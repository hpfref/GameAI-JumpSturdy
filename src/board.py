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
#walla
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

def make_move(board, player, move, start_value, target_value):
    """
    Executes a move on the board for a given player, updating the board state accordingly.
    
    This function handles the logic for moving both blue and red pieces, including the promotion of pieces
    (e.g., a blue piece becoming 'bb' after moving on another blue piece and vice versa) and the capturing of opponent's pieces.
    After a move is made, the function clears the original positiono f the moved piece and updates the target position
    based on the move's start and end positions, the player making the move, and the values at the start and target positions.
    
    Parameters:
    - board (dict): A dictionary representing our game board.
    - player (str): The current player's color
    - move (tuple): A tuple containing two tuples, representing the start and end positions of the move, respectively.
    - start_value (str): The value (piece type) at the start position before the move.
    - target_value (str): The value (piece type) at the target position before the move.
    
    Returns:
    - str: The color of the next player ('b' if the current player is 'r', and 'r' if the current player is 'b').
    """
    
    from_pos, to_pos = move  # Unpack the start and end positions from the move

    if player == "b":
        # Move logic for blue pieces
        if target_value in ["", "r"]:  # If the target is empty or contains a red piece
            board[to_pos] = "b"  # Place a blue piece at the target
        elif target_value == "rr":  # If the target contains a promoted red piece
            board[to_pos] = "rb"  # Promote the blue piece by capturing the red piece
        elif target_value in ["b", "br"]:  # If the target contains a blue piece or a promoted blue piece
            board[to_pos] = "bb"  # Promote the blue piece

        # Clear the original position based on the start value
        if start_value == "b":
            board[from_pos] = ""  # Clear the position if it was a single blue piece
        elif start_value == "bb":
            board[from_pos] = "b"  # Demote the piece if it was a promoted blue piece
        elif start_value == "rb":
            board[from_pos] = "r"  # Leave a red piece if it was a promoted piece captured by blue

    else:
        # Move logic for red pieces
        if target_value in ["", "b"]:  # If the target is empty or contains a blue piece
            board[to_pos] = "r"  # Place a red piece at the target
        elif target_value == "bb":  # If the target contains a promoted blue piece
            board[to_pos] = "br"  # Promote the red piece by capturing the blue piece
        elif target_value in ["r", "rb"]:  # If the target contains a red piece or a promoted red piece
            board[to_pos] = "rr"  # Promote the red piece

        # Clear the original position based on the start value
        if start_value == "r":
            board[from_pos] = ""  # Clear the position if it was a single red piece
        elif start_value == "rr":
            board[from_pos] = "r"  # Demote the piece if it was a promoted red piece
        elif start_value == "br":
            board[from_pos] = "b"  # Leave a blue piece if it was a promoted piece captured by red

    return 'b' if player == 'r' else 'r'  # Switch the player after the move


def unmake_move(board, move, start_value, target_value):
    """
    Reverses a move on the board, restoring the board to its previous state.
    
    Parameters:
    - board (2D Array): A 2D Array representing our game board.
    - move (tuple): A tuple containing two tuples, representing the start and end positions of the move, respectively.
    - start_value (str): The value (piece type) that was originally at the start position before the move was made.
    - target_value (str): The value (piece type) that was originally at the target position before the move was made.
    
    Returns:
    - None: This function does not return a value but instead directly modifies the board dictionary to reflect the reversed move.
    """
    
    from_pos, to_pos = move  # Unpack the start and end positions from the move

    # Restore the original values at the start and target positions
    board[from_pos] = start_value
    board[to_pos] = target_value

    # No return value is needed as the board is modified in place