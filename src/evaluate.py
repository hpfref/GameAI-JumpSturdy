import math 

def evaluate(board, player):
    # piece_values = {'r': -1, 'rr': -2, 'br': -1.5, 'b': 1, 'bb': 2, 'rb': 1.5} # dunno
    pieces = ['r', 'rr', 'br', 'b', 'bb', 'rb']
    value = 0
    # red_moves = legal_moves(board, 'r')
    # blue_moves = legal_moves(board, 'b')

    # helper_eval = {"Position": 0, "Material": 0, "Mobility": 0, "Win": 0} # to understand components

    for row in range(8):
        for col in range(8):
            piece = board[row, col]
            if piece in pieces:
                # Überprüfen, ob ein rotes Stück auf der letzten Reihe ist
                if row == 7 and piece in ['r', 'rr', 'br']:
                    # helper_eval['Win'] = float('-inf')
                    return float('-inf')  # Red wins

                # Überprüfen, ob ein blaues Stück auf der ersten Reihe ist
                if row == 0 and piece in ['b', 'bb', 'rb']:
                    # helper_eval['Win'] = float('inf')
                    return float('inf')  # Blue wins

                # Position ((1.5**row) * 0.2) + Materialwert + ?
                if piece == 'r':
                    # helper_eval['Position'] -= ((1.5**row) * 0.2)
                    # helper_eval['Material'] -= 1
                    value -= ((1.5 ** row) * 0.2) + 1

                elif piece == 'b':
                    # helper_eval['Position'] += ((1.5**(7 - row)) * 0.2)
                    # helper_eval['Material'] += 1
                    value += ((1.5 ** (7 - row)) * 0.2) + 1

                elif piece == 'rr':
                    # helper_eval['Position'] -= ((1.5**row) * 0.3)
                    # helper_eval['Material'] -= 2
                    value -= ((1.5 ** row) * 0.3) + 2

                elif piece == 'bb':
                    # helper_eval['Position'] += ((1.5**(7 - row)) * 0.3)
                    # helper_eval['Material'] += 2
                    value += ((1.5 ** (7 - row)) * 0.3) + 2

                elif piece == 'br':
                    # helper_eval['Position'] -= ((1.5**row) * 0.2)
                    value -= ((
                                          1.5 ** row) * 0.2) + 0  # mby troll aktuell gibts hier nur punkte für rot und materialwert von b und r gleichen sich aus -> durch faktor steuern

                elif piece == 'rb':
                    # helper_eval['Position'] += ((1.5**row) * 0.2) # same
                    value += ((1.5 ** (7 - row)) * 0.2) + 0

                # 123

    # Mobilität berücksichtigen
    # helper_eval['Mobility'] = 0.1 * len(blue_moves) - 0.1 * len(red_moves)
    # value -= 0.1 * len(red_moves)
    # value += 0.1 * len(blue_moves)

    # print(helper_eval)

    return value


def evaluateEarlygame(board, player):
    pieces = ['r', 'rr', 'br', 'b', 'bb', 'rb']
    value = 0

    # bonus for current player
    if (player == 'b'):
        value += 0.25
    else:
        value -= 0.25

    # bonus positions
    if board[(0, 2)] == 'r':
        value -= 0.5

    if board[(0, 5)] == 'r':
        value -= 0.5

    if board[(7, 2)] == 'b':
        value += 0.5

    if board[(7, 5)] == 'b':
        value += 0.5

    for row in range(8):
        for col in range(8):
            piece = board[row, col]
            if piece in pieces:
                # Überprüfen, ob ein rotes Stück auf der letzten Reihe ist
                if row == 7 and piece in ['r', 'rr', 'br']:
                    return float('-inf')  # Red wins

                # Überprüfen, ob ein blaues Stück auf der ersten Reihe ist
                if row == 0 and piece in ['b', 'bb', 'rb']:
                    return float('inf')  # Blue wins

                if piece == 'r':
                    value -= ((1.5 ** row) * 0.3) + 1

                elif piece == 'b':
                    value += ((1.5 ** (7 - row)) * 0.3) + 1

                elif piece == 'rr':
                    value -= ((1.5 ** row) * 0.5) + 2

                elif piece == 'bb':
                    value += ((1.5 ** (7 - row)) * 0.5) + 2

                elif piece == 'br':
                    value -= ((1.5 ** row) * 0.3) + 0

                elif piece == 'rb':
                    value += ((1.5 ** (7 - row)) * 0.3) + 0

    return value

def evaluateMidgame(board, player):
    pieces = ['r', 'rr', 'br', 'b', 'bb', 'rb']
    value = 0

    # bonus for current player
    if (player == 'b'):
        value += 0.25
    else:
        value -= 0.25

    # bonus positions
    if board[(0, 2)] == 'r':
        value -= 0.5

    if board[(0, 5)] == 'r':
        value -= 0.5

    if board[(7, 2)] == 'b':
        value += 0.5

    if board[(7, 5)] == 'b':
        value += 0.5

    for row in range(8):
        for col in range(8):
            piece = board[row, col]
            if piece in pieces:
                # Überprüfen, ob ein rotes Stück auf der letzten Reihe ist
                if row == 7 and piece in ['r', 'rr', 'br']:
                    return float('-inf')  # Red wins

                # Überprüfen, ob ein blaues Stück auf der ersten Reihe ist
                if row == 0 and piece in ['b', 'bb', 'rb']:
                    return float('inf')  # Blue wins

                if piece == 'r':
                    value -= ((1.5 ** row) * 0.3) + 1

                elif piece == 'b':
                    value += ((1.5 ** (7 - row)) * 0.3) + 1

                elif piece == 'rr':
                    value -= ((1.5 ** row) * 0.5) + 2

                elif piece == 'bb':
                    value += ((1.5 ** (7 - row)) * 0.5) + 2

                elif piece == 'br':
                    value -= ((1.5 ** row) * 0.3) + 0

                elif piece == 'rb':
                    value += ((1.5 ** (7 - row)) * 0.3) + 0


    under_attack_penalty, density_bonus = piece_under_attack_density(board, player)
    value -= under_attack_penalty * 0.5
    value += density_bonus * 0.1  
    return value

def evaluateLategame(board, player):
    pieces = ['r', 'rr', 'br', 'b', 'bb', 'rb']
    value = 0

    # bonus for current player
    if (player == 'b'):
        value += 0.25
    else:
        value -= 0.25

    # bonus positions
    if board[(0, 2)] == 'r':
        value -= 0.5

    if board[(0, 5)] == 'r':
        value -= 0.5

    if board[(7, 2)] == 'b':
        value += 0.5

    if board[(7, 5)] == 'b':
        value += 0.5

    for row in range(8):
        for col in range(8):
            piece = board[row, col]
            if piece in pieces:
                if row == 7 and piece in ['r', 'rr', 'br']:
                    return float('-inf')  # Red wins

                if row == 0 and piece in ['b', 'bb', 'rb']:
                    return float('inf')  # Blue wins

                if piece == 'r':
                    value -= ((1.5 ** row) * 0.3) + 1.25

                elif piece == 'b':
                    value += ((1.5 ** (7 - row)) * 0.3) + 1.25

                elif piece == 'rr':
                    value -= ((1.5 ** row) * 0.5) + 2.5

                elif piece == 'bb':
                    value += ((1.5 ** (7 - row)) * 0.5) + 2.5

                elif piece == 'br':
                    value -= ((1.5 ** row) * 0.3) + 0

                elif piece == 'rb':
                    value += ((1.5 ** (7 - row)) * 0.3) + 0


    under_attack_penalty, density_bonus = piece_under_attack_density(board, player)
    value -= under_attack_penalty * 0.5
    value += density_bonus * 0.1  
    return value

def piece_under_attack_density(board, player):
    """Calculate both the number of friendly pieces under attack and the piece density in one pass."""
    enemy = 'b' if player == 'r' else 'r'
    attack_positions = [(1, -1), (1, 1), (-1, -1), (-1, 1)]
    under_attack = 0
    positions = []
    total_distance_squared = 0
    board_size = len(board)
    row_size = len(board[0]) if board_size > 0 else 0

    # Iterate through the board once
    for row in range(board_size):
        for col in range(row_size):
            current_piece = board[row][col]
            if current_piece == '':
                continue
            positions.append((col, row))
            if current_piece.startswith(player):
                for d_row, d_col in attack_positions:
                    adj_row, adj_col = row + d_row, col + d_col
                    if 0 <= adj_row < board_size and 0 <= adj_col < row_size:
                        adjacent_piece = board[adj_row][adj_col]
                        if adjacent_piece.startswith(enemy):
                            under_attack += 1
                            break

    num_positions = len(positions)
    for i in range(num_positions):
        for j in range(i + 1, num_positions):
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            distance_squared = (x2 - x1) ** 2 + (y2 - y1) ** 2
            total_distance_squared += distance_squared

    avg_distance_squared = total_distance_squared / (num_positions * (num_positions - 1) / 2) if num_positions > 1 else 0

    return under_attack, avg_distance_squared

def evaluateFREFseite(board, player):
    pieces = ['r', 'rr', 'br', 'b', 'bb', 'rb']
    value = 0

    # bonus for current player
    if (player == 'b'):
        value += 0.25
    else:
        value -= 0.25

    # bonus positions
    if board[(0, 2)] == 'r':
        value -= 0.9

    if board[(0, 5)] == 'r':
        value -= 0.9

    if board[(7, 2)] == 'b':
        value += 0.9

    if board[(7, 5)] == 'b':
        value += 0.9

    for row in range(8):
        for col in range(8):
            piece = board[row, col]
            if piece in pieces:
                # Überprüfen, ob ein rotes Stück auf der letzten Reihe ist
                if row == 7 and piece in ['r', 'rr', 'br']:
                    return float('-inf')  # Red wins

                # Überprüfen, ob ein blaues Stück auf der ersten Reihe ist
                if row == 0 and piece in ['b', 'bb', 'rb']:
                    return float('inf')  # Blue wins

                if piece == 'r':
                    value -= ((1.5 ** row) * 0.3) + 1 + math.log((col * row / 2) + 1)

                elif piece == 'b':
                    value += ((1.5 ** (7 - row)) * 0.3) + 1 + math.log((col * row / 2) + 1)

                elif piece == 'rr':
                    value -= ((1.5 ** row) * 0.4) + 2 + math.log((col * row / 2) + 1)

                elif piece == 'bb':
                    value += ((1.5 ** (7 - row)) * 0.4) + 2 + math.log((col * row / 2) + 1)

                elif piece == 'br':
                    value -= ((1.5 ** row) * 0.2) + 0 + math.log((col * row / 2) + 1)

                elif piece == 'rb':
                    value += ((1.5 ** (7 - row)) * 0.2) + 0 + math.log((col * row / 2) + 1)
    return value