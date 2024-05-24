import random
from move_gen import legal_moves
from board import fen_to_board, board_to_fen
import time


def random_move(fen):
    board, player = fen_to_board(fen)
    moves = legal_moves(board, player)
    if not moves:
        return None
    return random.choice(moves)

def game_over(board, player):
    # Check if a red piece is on the last row
    #board, player = fen_to_board(fen)
    for col in range(8):
        piece = board[7, col]
        if piece in ['r', 'rr', 'br']:
            return True

    # Check if a blue piece is on the first row
    for col in range(8):
        piece = board[0, col]
        if piece in ['b', 'bb', 'rb']:
            return True

    return False

# instead of copying could make move & unmake move for alpha beta always using same board
def generate_new_board(board, player, move):
    from_pos, to_pos = move
    new_board = board.copy()

    if player == "b":
        # Move logic for blue pieces
        if new_board[to_pos] in ["", "r"]:
            new_board[to_pos] = "b"
        elif new_board[to_pos] == "rr":
            new_board[to_pos] = "rb"
        elif new_board[to_pos] in ["b", "br"]:
            new_board[to_pos] = "bb"

        # Clear the original position
        if new_board[from_pos] == "b":
            new_board[from_pos] = ""
        elif new_board[from_pos] == "bb":
            new_board[from_pos] = "b"
        elif new_board[from_pos] == "rb":
            new_board[from_pos] = "r"

    else:
        # Move logic for red pieces
        if new_board[to_pos] in ["", "b"]:
            new_board[to_pos] = "r"
        elif new_board[to_pos] == "bb":    
            new_board[to_pos] = "br"
        elif new_board[to_pos] in ["r", "rb"]:
            new_board[to_pos] = "rr"

        # Clear the original position
        if new_board[from_pos] == "r":
            new_board[from_pos] = ""
        elif new_board[from_pos] == "rr":
            new_board[from_pos] = "r"
        elif new_board[from_pos] == "br":
            new_board[from_pos] = "b"

    # Switch the player
    new_player = 'b' if player == 'r' else 'r'
    return new_board, new_player

def old_evaluate(board): # i guess slow, inefficient -> KEEP FOR TEST dann können wir sagen wir sind schneller geworden oder so
    piece_values = {'r': -1, 'rr': -2, 'br': -1.5, 'b': 1, 'bb': 2, 'rb': 1.5}
    value = 0

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
                value -= (1.5**row) * 0.2
            elif piece == 'b':
                value += (1.5**(7 - row)) * 0.2
            elif piece == 'rr':
                value -= (1.5**row) * 0.3
            elif piece == 'bb':
                value += (1.5**(7 - row)) * 0.3
            elif piece == 'br':
                value -= (1.5**row) * 0.2
            elif piece == 'rb':
                value += (1.5**(7 - row)) * 0.2

    # Mobilität berücksichtigen
    red_moves = legal_moves(board, 'r')
    blue_moves = legal_moves(board, 'b')
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

    return value

def evaluate(board):
    #piece_values = {'r': -1, 'rr': -2, 'br': -1.5, 'b': 1, 'bb': 2, 'rb': 1.5} # dunno
    pieces = ['r', 'rr', 'br', 'b', 'bb', 'rb']
    value = 0
    red_moves = legal_moves(board, 'r')
    blue_moves = legal_moves(board, 'b')

    helper_eval = {"Position": 0, "Material": 0, "Mobility": 0, "Win": 0} # to understand components

    for row in range(8):
        for col in range(8):
            piece = board[row, col]
            if piece in pieces:

                # Position ((1.5**row) * 0.2) + Materialwert + ?
                if piece == 'r':
                    helper_eval['Position'] -= ((1.5**row) * 0.2)
                    helper_eval['Material'] -= 1
                    value -= ((1.5**row) * 0.2) + 1

                elif piece == 'b':
                    helper_eval['Position'] += ((1.5**(7 - row)) * 0.2)
                    helper_eval['Material'] += 1
                    value += ((1.5**(7 - row)) * 0.2) + 1

                elif piece == 'rr':
                    helper_eval['Position'] -= ((1.5**row) * 0.3)
                    helper_eval['Material'] -= 2
                    value -= ((1.5**row) * 0.3) + 2

                elif piece == 'bb':
                    helper_eval['Position'] += ((1.5**(7 - row)) * 0.3)
                    helper_eval['Material'] += 2
                    value += ((1.5**(7 - row)) * 0.3) + 2

                elif piece == 'br': 
                    helper_eval['Position'] -= ((1.5**row) * 0.2)
                    value -= ((1.5**row) * 0.2) + 0 #mby troll aktuell gibts hier nur punkte für rot und materialwert von b und r gleichen sich aus -> durch faktor steuern 

                elif piece == 'rb':
                    helper_eval['Position'] += ((1.5**row) * 0.2) # same
                    value += ((1.5**(7 - row)) * 0.2) + 0

                # Überprüfen, ob ein rotes Stück auf der letzten Reihe ist
                if row == 7 and piece in ['r', 'rr', 'br']:
                    helper_eval['Win'] = float('-inf')
                    return float('-inf')  # Red wins

                # Überprüfen, ob ein blaues Stück auf der ersten Reihe ist
                if row == 0 and piece in ['b', 'bb', 'rb']:
                    helper_eval['Win'] = float('inf')
                    return float('inf')  # Blue wins

    # Mobilität berücksichtigen
    helper_eval['Mobility'] = 0.1 * len(blue_moves) - 0.1 * len(red_moves)
    value -= 0.1 * len(red_moves)
    value += 0.1 * len(blue_moves)

    print(helper_eval)

    return value



def alpha_beta_search(board, player, depth, alpha, beta, maximizing_player, start_time, max_time):
    if time.time() - start_time > max_time:
        raise TimeoutError("Time limit exceeded")

    moves = legal_moves(board, player)
    if not moves or depth == 0 or game_over(board, player):
        if maximizing_player:
            return evaluate(board), None
        else: return old_evaluate(board), None
        #return evaluate(board, player), None

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in moves:
            new_board, new_player = generate_new_board(board, player, move)
            eval, _ = alpha_beta_search(new_board, new_player, depth - 1, alpha, beta, False, start_time, max_time)
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
            new_board, new_player = generate_new_board(board, player, move)
            eval, _ = alpha_beta_search(new_board, new_player, depth - 1, alpha, beta, True, start_time, max_time)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

def iterative_deepening_alpha_beta_search(board, player, max_time, maximizing_player):
    start_time = time.time()
    depth = 1
    best_move = None
    best_value = float('-inf') if maximizing_player else float('inf')

    while True:
        print(f"Searching depth {depth}")
        try:
            value, move = alpha_beta_search(board, player, depth, float('-inf'), float('inf'), maximizing_player, start_time, max_time)
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
    board, player = fen_to_board(fen)
    maximizing_player = player == 'b'
    return iterative_deepening_alpha_beta_search(board, player, max_time, maximizing_player)
