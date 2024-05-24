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


'''OLD EVALUATE
def evaluate(fen):
    piece_values = {'r': 1, 'rr': 1, 'br': 1, 'b': -1, 'bb': -1, 'rb': -1}
    value = 0
    # Split the FEN string to get the piece placement
    piece_placement = fen.split(' ')[0]

    # Iterate over each character in the piece placement
    for piece in piece_placement:
        # If the character is in the piece_values dictionary, add its value to the total
        if piece in piece_values:
            value += piece_values[piece]

    board, player = fen_to_board(fen)

    # Add bonus for pieces closer to the opponent's row
    for row in range(8):
        for col in range(8):
            piece = board[row, col]
            if piece in ['r', 'rr', 'br']:
                value += (7 - row) / 7.0  # Red pieces get closer to winning as row number decreases
            elif piece in ['b', 'bb', 'rb']:
                value -= row / 7.0  # Blue pieces get closer to winning as row number increases

    # Check if a red piece is on the last row
    for col in range(8):
        piece = board[7, col]
        if piece in ['r', 'rr', 'rb']:
            return float('inf')  # Red wins

    # Check if a blue piece is on the first row
    for col in range(8):
        piece = board[0, col]
        if piece in ['b', 'bb', 'br']:
            return float('-inf')  # Blue wins

    return value
'''



def evaluate(fen):
    piece_values = {'r': -1, 'rr': -2, 'br': -1.5, 'b': 1, 'bb': 2.5, 'rb': 1.5}
    value = 0

    board, player = fen_to_board(fen)

    # Materialwert berechnen
    for row in range(8):
        for col in range(8):
            piece = board[row, col]
            if piece in piece_values:
                value += piece_values[piece]

    # Positionelle Faktoren berücksichtigen
    for row in range(8):
        for col in range(8):
            piece = board[row, col]
            if piece == 'r':
                value += (7 - row) * 0.2  # Red pieces closer to winning
            elif piece == 'b':
                value -= row * 0.2  # Blue pieces closer to winning
            elif piece == 'rr':
                value += (7 - row) * 0.3  # Red towers closer to winning
            elif piece == 'bb':
                value -= row * 0.3  # Blue towers closer to winning
            elif piece == 'br':
                value += (7 - row) * 0.2  # Red on blue pieces closer to winning
            elif piece == 'rb':
                value -= row * 0.2  # Blue on red pieces closer to winning

    # Mobilität berücksichtigen
    red_moves = legal_moves(board_to_fen(board, 'r'))
    blue_moves = legal_moves(board_to_fen(board, 'b'))
    value -= 0.01 * len(red_moves)
    value += 0.01 * len(blue_moves)

    # Überprüfen, ob ein rotes Stück auf der letzten Reihe ist
    for col in range(8):
        piece = board[7, col]
        if piece in ['r', 'rr', 'br']:
            return float('-inf')  # Red wins

    # Überprüfen, ob ein blaues Stück auf der ersten Reihe ist
    for col in range(8):
        piece = board[0, col]
        if piece in ['b', 'bb', 'rb']:
            return float('inf')  # Blue wins
    print(value)
    return value


import time

def alpha_beta_search(fen, depth, alpha, beta, maximizing_player, start_time, max_time):
    if time.time() - start_time > max_time:
        raise TimeoutError("Time limit exceeded")

    moves = legal_moves(fen)
    if not moves or depth == 0 or game_over(fen):
        return evaluate(fen), None

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in moves:
            new_fen = generate_new_board(fen, move)
            eval, _ = alpha_beta_search(new_fen, depth - 1, alpha, beta, False, start_time, max_time)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in moves:
            new_fen = generate_new_board(fen, move)
            eval, _ = alpha_beta_search(new_fen, depth - 1, alpha, beta, True, start_time, max_time)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

def iterative_deepening_alpha_beta_search(fen, max_time, maximizing_player):
    start_time = time.time()
    depth = 1
    best_move = None
    best_value = float('-inf') if maximizing_player else float('inf')

    while True:
        print(f"Searching depth {depth}")
        try:
            value, move = alpha_beta_search(fen, depth, float('-inf'), float('inf'), maximizing_player, start_time, max_time)
            if (maximizing_player and value > best_value) or (not maximizing_player and value < best_value):
                best_value = value
                best_move = move
            depth += 1
        except TimeoutError:
            break
    print(best_move, best_value)
    return best_move

def select_move(fen):
    max_time = 3  # Maximum time in seconds for each move
    _, player = fen_to_board(fen)
    maximizing_player = player == 'b'
    return iterative_deepening_alpha_beta_search(fen, max_time, maximizing_player)
