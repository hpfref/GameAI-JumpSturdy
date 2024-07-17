import math 

def evaluate(board, player):
    """
    Evaluates the board state for a given player, taking into account piece positions,  and piece values. Puts emphasis on piece development.
    First version of our evaluation function. Still in the code for reference, but not used in the final version.

    Parameters:
        - board (2D Array): Responsible for storing the current state of the board, including the placement of pieces and special fields.
        - player (str): The current player ('b' for blue, 'r' for red) being evaluated.

    Returns:
        float: The evaluation score of the board state. A positive score favors the blue player, while a negative score favors the red player.
               Returns float('inf') if the blue player wins, and float('-inf') if the red player wins.
    """
    # piece_values = {'r': -1, 'rr': -2, 'br': -1.5, 'b': 1, 'bb': 2, 'rb': 1.5} # to be refined
    pieces = ['r', 'rr', 'br', 'b', 'bb', 'rb']
    value = 0
    # red_moves = legal_moves(board, 'r')
    # blue_moves = legal_moves(board, 'b')

    # helper_eval = {"Position": 0, "Material": 0, "Mobility": 0, "Win": 0} # to understand components

    for row in range(8):
        for col in range(8):
            piece = board[row, col]
            if piece in pieces:
                # Red piece on the last row
                if row == 7 and piece in ['r', 'rr', 'br']:
                    # helper_eval['Win'] = float('-inf')
                    return float('-inf')  # Red wins

                # Blue piece on the first row
                if row == 0 and piece in ['b', 'bb', 'rb']:
                    # helper_eval['Win'] = float('inf')
                    return float('inf')  # Blue wins

                # Position ((1.5**row) * 0.2) + Material + ?
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
                                          1.5 ** row) * 0.2) + 0 

                elif piece == 'rb':
                    # helper_eval['Position'] += ((1.5**row) * 0.2) 
                    value += ((1.5 ** (7 - row)) * 0.2) + 0

    # helper_eval['Mobility'] = 0.1 * len(blue_moves) - 0.1 * len(red_moves)
    # value -= 0.1 * len(red_moves)
    # value += 0.1 * len(blue_moves)

    # print(helper_eval)

    return value


def evaluateEarlygame(board, player):
    """
    Evaluates the board state during the earlygamme phase for a given player, taking into account piece positions, 
    and piece values. Puts emphasis on piece development.

    Parameters:
        - board (2D Array): Responsible for storing the current state of the board, including the placement of pieces and special fields.
        - player (str): The current player ('b' for blue, 'r' for red) being evaluated.

    Returns:
        float: The evaluation score of the board state. A positive score favors the blue player, while a negative score favors the red player.
               Returns float('inf') if the blue player wins, and float('-inf') if the red player wins.
    """
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
                # Red piece on the last row
                if row == 7 and piece in ['r', 'rr', 'br']:
                    return float('-inf')  # Red wins

                # Blue piece on the first row
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
    """
    Evaluates the board state during the midgame phase for a given player, taking into account piece positions, 
    piece values, board control and piece density. 

    Parameters:
        - board (2D Array): Responsible for storing the current state of the board, including the placement of pieces and special fields.
        - player (str): The current player ('b' for blue, 'r' for red) being evaluated.

    Returns:
        float: The evaluation score of the board state. A positive score favors the blue player, while a negative score favors the red player.
               Returns float('inf') if the blue player wins, and float('-inf') if the red player wins.
    """
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
                # Red piece on the last row
                if row == 7 and piece in ['r', 'rr', 'br']:
                    return float('-inf')  # Red wins

                # Blue piece on the first row
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
    """
    Evaluates the board state during the lategame phase for a given player, taking into account piece positions, 
    piece values, board control and piece density. Puts emphasis on the value of single pieces, as they have higher weighting. 

    Parameters:
        - board (2D Array): Responsible for storing the current state of the board, including the placement of pieces and special fields.
        - player (str): The current player ('b' for blue, 'r' for red) being evaluated.

    Returns:
        float: The evaluation score of the board state. A positive score favors the blue player, while a negative score favors the red player.
               Returns float('inf') if the blue player wins, and float('-inf') if the red player wins.
    """
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
                # Red piece on the last row
                if row == 7 and piece in ['r', 'rr', 'br']:
                    return float('-inf')                  
                # Blue piece on the first row
                if row == 0 and piece in ['b', 'bb', 'rb']:
                    return float('inf')                 

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
    value += density_bonus * 0.05  
    return value

def piece_under_attack_density(board, player):
    """
    Calculates the number of pieces belonging to the player that are under attack and the average squared distance between all pieces on the board.
    This function iterates through the board to identify pieces under attack by checking adjacent positions based on predefined attack vectors. 
    It also calculates the average squared distance between all pieces on the board to assess piece density. This dual calculation is performed in a single pass for efficiency.
    Parameters:
    - board (2D Array): Responsible for storing the current state of the board, including the placement of pieces and special fields.
    - player (str): The player ('r' for red or 'b' for blue) for whom to calculate the under-attack status and piece density.
    
    Returns:
        tuple: A tuple containing two elements:
            - The first element is an integer representing the number of pieces belonging to the player that are under attack.
            - The second element is a float representing the average squared distance between all pieces on the board, which serves as a measure of piece density.
    """
    enemy = 'b' if player == 'r' else 'r'
    attack_positions = [(1, -1), (1, 1), (-1, -1), (-1, 1)] # Define attack vectors for adjacent positions
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
            positions.append((col, row)) # Add position to the list for density calculation
            if current_piece.startswith(player): # Check if the piece belongs to the current player
                # Check adjacent positions for enemy pieces to determine if the current piece is under attack
                for d_row, d_col in attack_positions:
                    adj_row, adj_col = row + d_row, col + d_col
                    if 0 <= adj_row < board_size and 0 <= adj_col < row_size:
                        adjacent_piece = board[adj_row][adj_col]
                        if adjacent_piece.startswith(enemy):
                            under_attack += 1
                            break

    num_positions = len(positions)
    # Calculate the sum of squared distances between all pairs of pieces
    for i in range(num_positions):
        for j in range(i + 1, num_positions):
            x1, y1 = positions[i]
            x2, y2 = positions[j]
            distance_squared = (x2 - x1) ** 2 + (y2 - y1) ** 2
            total_distance_squared += distance_squared

    # Calculate the average squared distance between all pairs of pieces
    avg_distance_squared = total_distance_squared / (num_positions * (num_positions - 1) / 2) if num_positions > 1 else 0

    return under_attack, avg_distance_squared

def evaluateFREFseite(board, player):
    """
    Experimental evaluation, taking into account piece positions and piece values, while putting focus on overloading one side of the board 
    to damamge the opponents structure.
    Parameters:
        - board (2D Array): Responsible for storing the current state of the board, including the placement of pieces and special fields.
        - player (str): The current player ('b' for blue, 'r' for red) being evaluated.

    Returns:
        float: The evaluation score of the board state. A positive score favors the blue player, while a negative score favors the red player.
               Returns float('inf') if the blue player wins, and float('-inf') if the red player wins.
    """
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
                # Red piece on the last row
                if row == 7 and piece in ['r', 'rr', 'br']:
                    return float('-inf')  # Red wins

                # Blue piece on the first row
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