import random
from move_gen import legal_moves
from board import fen_to_board, board_to_fen

def random_move(fen):
    moves = legal_moves(fen)
    if not moves:
        return None
    return random.choice(moves)
    #return moves[1]

def game_over(fen):
    board, player = fen_to_board(fen)

    # Check if a red piece is on the last row
    for col in range(8):
        piece = board[7, col]
        if piece in ['r', 'rr', 'rb']:
            return True

    # Check if a blue piece is on the first row
    for col in range(8):
        piece = board[0, col]
        if piece in ['b', 'bb', 'br']:
            return True

    return False

def generate_new_board(fen, move):
    board, player = fen_to_board(fen)
    from_pos, to_pos = move

    if player == "b":
        # Move logic for blue pieces
        if board[to_pos] in ["", "r"]:
            board[to_pos] = "b"
                    
        elif board[to_pos] == "rr":
            board[to_pos] = "rb"

        elif board[to_pos] in ["b", "br"]:
            board[to_pos] = "bb"    

        # Clear the original position
        if board[from_pos] == "b":
            board[from_pos] = ""

        elif board[from_pos] == "bb":
            board[from_pos] = "b"

        elif board[from_pos] == "rb":
            board[from_pos] = "r"

    else:
        # Move logic for red pieces
        if board[to_pos] in ["", "b"]:
            board[to_pos] = "r"
                    
        elif board[to_pos] == "bb":
            board[to_pos] = "br"

        elif board[to_pos] in ["r", "rb"]:
            board[to_pos] = "rr"    

        # Clear the original position
        if board[from_pos] == "r":
            board[from_pos] = ""

        elif board[from_pos] == "rr":
            board[from_pos] = "r"

        elif board[from_pos] == "br":
            board[from_pos] = "b"



    # Switch the player
    player = 'b' if player == 'r' else 'r'

    # Convert the board back to a FEN string
    new_fen = board_to_fen(board, player)
    #print(new_fen) # for debugging
    return new_fen


