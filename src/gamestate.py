'''MIT TT UND ASPIRATION WINDOW'''
import random
from move_gen import legal_moves
from board import fen_to_board, board_to_fen
import time
import math


from transposition_table import TranspositionTable, EXACT, UPPERBOUND, LOWERBOUND



def random_move(fen):
    """
    Selects a random legal move for the current player from a given FEN string. For testing purposes.
    
    Parameters:
    - fen (str): The FEN string representing the current game state.
    
    Returns:
    - str or None: A random legal move for the current player in algebraic notation if there are any legal moves available.
      Returns None if there are no legal moves available (e.g., in a checkmate or stalemate situation).
    """
    
    # Convert the FEN string to a board representation and determine the current player
    board, player = fen_to_board(fen)
    
    # Retrieve the first element from the tuple returned by legal_moves, which contains all legal moves for the player
    moves = legal_moves(board, player)[0]
    
    # If there are no legal moves available, return None
    if not moves:
        return None
    
    # Otherwise, return a random move from the list of legal moves
    return random.choice(moves)


def game_over(board, player):
    """
    Determines if the game is over based on the current board state and player.
    
    The game is considered over if a red piece reaches the last row or a blue piece reaches the first row.
    This function checks the board for these conditions.
    
    Parameters:
    - board (2D Array): A 2D Array representing our game board.
    - player (str): The current player's color ('r' for red or 'b' for blue). This parameter is currently unused in the function,
                    but could be used for future enhancements or checks specific to the current player.
    
    Returns:
    - bool: True if the game is over (a red piece is on the last row or a blue piece is on the first row), False otherwise.
    """
    
    # Check if a red piece is on the last row
    for col in range(8):
        piece = board[7, col]  # Access the piece in the last row and current column
        if piece in ['r', 'rr', 'br']:  # Check if the piece is a red piece (including promoted and both-color pieces)
            return True  # Game is over if a red piece is found on the last row

    # Check if a blue piece is on the first row
    for col in range(8):
        piece = board[0, col]  # Access the piece in the first row and current column
        if piece in ['b', 'bb', 'rb']:  # Check if the piece is a blue piece (including promoted and both-color pieces)
            return True  # Game is over if a blue piece is found on the first row

    return False  # If no winning conditions are met, the game is not over


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


def evaluateFREF(board, player):
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

def evaluateFREF2(board, player):
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

def check_midgame(board):
    """
    Determines if the game has reached the midgame phase based on the number of pieces beaten.
    
    The midgame phase is considered to have started once at least 10 pieces have been beaten (removed from the board).
    This includes both single and promoted pieces. Promoted pieces are counted as two pieces since they represent
    a piece that has reached the opponent's end of the board and returned.
    
    Parameters:
    - board (2D Array): A 2D Array representing our game board.

    Returns:
    - bool: True if at least 10 pieces have been beaten (indicating the start of the midgame phase), False otherwise.
    """
    
    initial_piece_count = 24  # The total number of pieces at the start of the game (12 red and 12 blue)
    current_piece_count = 0  # Initialize the current piece count
    
    for row in board:
        for piece in row:
            if piece in ['r', 'b']:
                current_piece_count += 1
            elif piece in ['rr', 'br', 'bb', 'rb']:
                current_piece_count += 2
    
    pieces_beaten = (initial_piece_count * 2) - current_piece_count

    return pieces_beaten >= 10

def evalDynamic(board, player):
    isMidgame = check_midgame(board)
    if isMidgame:
        return evaluateFREFseite(board, player)
    else:
        return evaluateFREF(board, player)


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

##### RUHESUCHE
# would be very good to inspect check moves too here, but finding check moves would be another big overhead (prob in legal_moves())

#changes: legal_moves returns, quiescence_search methode, check in alpha beta, neuer alpha beta parameter

def quiescence_search(board_alpaha_beta, player, stack_capture, single_capture):
    nodes_explored = 0
    board = board_alpaha_beta.copy() #so i dont need to unmake moves afterwards

    capture_moves = single_capture + stack_capture
    current_player = player
    max_depth = 6 # is tipically less than that
    curr_depth = 1

    while curr_depth <= max_depth:
        
        # move blue
        if current_player == 'b':
            #search for best capture move (depth 1 basically)
            best_eval = float('-inf')
            best_move = capture_moves[0]
            
            for move in capture_moves:
                nodes_explored += 1
                start_value = board[move[0]]
                target_value = board[move[1]]
                make_move(board, current_player, move, start_value, target_value)
                eval_i = evaluateFREF(board,'r') 
                if eval_i > best_eval:
                    best_eval = eval_i 
                    best_move = move
                unmake_move(board, move, start_value, target_value)
            
            #play the move
            start_value = board[best_move[0]]
            target_value = board[best_move[1]]
            current_player = make_move(board, current_player, best_move, start_value, target_value)
            
        
        # move red
        else:
            #search for best capture move (depth 1 basically)
            best_eval = float('inf')
            best_move = capture_moves[0]
            
            for move in capture_moves:
                nodes_explored += 1
                start_value = board[move[0]]
                target_value = board[move[1]]
                make_move(board, current_player, move, start_value, target_value)
                eval_i = evaluateFREF(board,'b') 
                if eval_i < best_eval:
                    best_eval = eval_i 
                    best_move = move
                unmake_move(board, move, start_value, target_value)
            
            #play the move
            start_value = board[best_move[0]]
            target_value = board[best_move[1]]
            current_player = make_move(board, current_player, best_move, start_value, target_value)

        # compute moves for opponent in next iteration
        _, is_quiescent, stack_capture, single_capture = legal_moves(board, current_player)
        capture_moves = stack_capture + single_capture

        if is_quiescent: #check if capture possible, if not break the lopp
            break
        #print(len(capture_moves)) # tipically 1-3 moves possible

        curr_depth+=1
        
    
    return evaluateFREF(board, current_player), nodes_explored

##### MAIN ALPHA BETA 

def alpha_beta_search(board, player, depth, alpha, beta, maximizing_player, start_time, max_time, tt, zobrist_hash):
    if time.time() - start_time > max_time:
        return None, None, False, 0  
    nodes_explored = 1 # 1 für aktuelles board

    tt_entry = tt.lookup(zobrist_hash)
    if tt_entry:
        tt_depth, tt_value, tt_flag, tt_best_move = tt_entry[0]
        if tt_depth >= depth:
            if tt_flag == EXACT:
                return tt_value, tt_best_move, True, nodes_explored
            elif tt_flag == LOWERBOUND:
                alpha = max(alpha, tt_value)
            elif tt_flag == UPPERBOUND:
                beta = min(beta, tt_value)
            if alpha >= beta:
                return tt_value, tt_best_move, True, nodes_explored
            
    moves, is_quiescent, stack_capture, single_capture = legal_moves(board, player) 

    if not moves or game_over(board, player): # or depth==0 jetzt in ruhesuche
        eval = evaluateFREF(board,player)
        tt.store(zobrist_hash, depth, eval, EXACT, None)
        return eval, None, True, nodes_explored
        #return evalDynamic(board,player), None, True, nodes_explored 
    
    global current_iterative_max_depth # too expensive to do for depths 1,2,3

    if depth==0: # RUHESUCHE ab horizont
        #return evaluateFREF(board,player), None, True, nodes_explored # uncomment to disable quiscent search
        if current_iterative_max_depth >= 4 and not is_quiescent: # if there are captures possible and searching depth of min. 4
            eval_quiescence, child_nodes_explored = quiescence_search(board, player, stack_capture, single_capture)
            tt.store(zobrist_hash, depth, eval_quiescence, EXACT, None) # unsure if its smart to also store this result
            nodes_explored += child_nodes_explored
            return eval_quiescence, None, True, nodes_explored # comment to enable the comparison

            # Idea: playing capture moves can be very bad for a player, but quiescence_search basically forces the player to do so
            # --> compare result of quiescence_search and eval without it and choose better value
            # ! seems reasonable but looses against variant without it
            eval_normal = evaluateFREF(board,player)
            if maximizing_player:
                if eval_quiescence > eval_normal:
                    return eval_quiescence, None, True, nodes_explored
                else:
                    return eval_normal, None, True, nodes_explored
            else:
                if eval_quiescence > eval_normal:
                    return eval_normal, None, True, nodes_explored
                else:
                    return eval_quiescence, None, True, nodes_explored

        else: # wenn es keine Schlagzüge gibt, also situation 'ruhig' ist
            return evaluateFREF(board,player), None, True, nodes_explored
    
    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in moves:
            start_value = board[move[0]] # save start field value e.g. b
            target_value = board[move[1]] # save target field value e.g. r
            new_player = make_move(board, player, move, start_value, target_value)
            new_zobrist_hash = tt.update_zobrist_hash(zobrist_hash, move, board, player)
            eval, _, completed, child_nodes_explored = alpha_beta_search(board, new_player, depth - 1, alpha, beta, False, start_time, max_time, tt, new_zobrist_hash)
            nodes_explored += child_nodes_explored
            unmake_move(board, move, start_value, target_value) # restore board 
            if not completed:
                return None, None, False, nodes_explored  
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:  
                break
            #print(f"Time elapsed for move {move}: {time.time() - start_time}")
        if best_move == None:
            best_move = moves[0]
        tt.store(zobrist_hash, depth, max_eval, LOWERBOUND if alpha >= beta else EXACT, best_move)
        return max_eval, best_move, True, nodes_explored  
    else:
        min_eval = float('inf')
        best_move = None
        for move in moves:
            start_value = board[move[0]] # save start field value e.g. r
            target_value = board[move[1]] # save target field value e.g. b
            new_player = make_move(board, player, move, start_value, target_value)
            new_zobrist_hash = tt.update_zobrist_hash(zobrist_hash, move, board, player)
            eval, _, completed, child_nodes_explored = alpha_beta_search(board, new_player, depth - 1, alpha, beta, True, start_time, max_time, tt, new_zobrist_hash)
            nodes_explored += child_nodes_explored
            unmake_move(board, move, start_value, target_value) # restore board 
            if not completed:
                return None, None, False, nodes_explored  
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:  
                break
        if best_move == None:
            best_move = moves[0]
        tt.store(zobrist_hash, depth, min_eval, LOWERBOUND if alpha >= beta else EXACT, best_move)
        return min_eval, best_move, True, nodes_explored  

current_iterative_max_depth = 1

def iterative_deepening_alpha_beta_search(board, player, max_time, max_depth, maximizing_player, tt, zobrist_hash):
    start_time = time.time()
    depth = 1
    best_move = None
    best_value = float('-inf') if maximizing_player else float('inf')
    total_nodes_explored = 0 # for testing
    aspiration_window = 100 # toggled off

    while True:
        if depth > max_depth:
            break
        alpha = best_value - aspiration_window
        beta = best_value + aspiration_window

        global current_iterative_max_depth 
        current_iterative_max_depth = depth # FOR QUIESCENCE CHECK

        print(f"Searching depth {depth}")
        depth_start_time = time.time()
        value, move, completed, nodes_explored = alpha_beta_search(board, player, depth, float('-inf'), float('inf'),
                                                                   maximizing_player, start_time, max_time, tt, zobrist_hash)
        # if completed:
        # print(f"Search completed for depth {depth}. Best move: {move}")
        depth_end_time = time.time()
        depth_time = depth_end_time - depth_start_time
        total_nodes_explored += nodes_explored


        if not completed:
            break


        if value <= alpha:
            # Research with a larger window
            alpha = float('-inf')
            beta = best_value + aspiration_window * 2
            value, move, completed, nodes_explored = alpha_beta_search(board, player, depth, alpha, beta,
                                                                       maximizing_player, start_time, max_time, tt, zobrist_hash
                                                                       )
            total_nodes_explored += nodes_explored
            if not completed:
                break
        elif value >= beta:
            # Research with a larger window
            alpha = best_value - aspiration_window * 2
            beta = float('inf')
            value, move, completed, nodes_explored = alpha_beta_search(board, player, depth, alpha, beta,
                                                                       maximizing_player, start_time, max_time, tt, zobrist_hash
                                                                       )
            total_nodes_explored += nodes_explored
            if not completed:
                break


        best_value = value
        best_move = move
        if (maximizing_player and best_value == float('inf')) or (not maximizing_player and best_value == float('-inf')):
            break
        
        # Estimate time for next depth
        if depth > 5:
            next_depth_time = depth_time * 10
            print(f"Nodes explored: {nodes_explored}, Estimated time for next depth: {next_depth_time}")
        else:  
            next_depth_time = depth_time * depth
        # Check if estimated time for next depth is less than remaining time
        remaining_time = max_time - (time.time() - start_time)
        if next_depth_time > remaining_time:
            print(f"Skipping depth {depth+1} as estimated time {next_depth_time} is greater than remaining time {remaining_time}")
            depth += 1
            break

        depth += 1
        #print(f"Incremented depth: {depth}")

    print(f"Best value: {best_value}, Total nodes explored: {total_nodes_explored}")
    #print(f"Decremented depth: {depth-1}")
    return best_move, depth-1, total_nodes_explored

total_game_time = 120  # Total game time in s

def select_move(fen,remaining_time):
    global total_game_time
    remaining_time = remaining_time / 1000 # keine lust time management auf ms umzubauen

    #remaining_time = 1000000 # for testing!
    #total_game_time = 1000000 # for testing!

    max_depth = 7  # for testing
    board, player = fen_to_board(fen)
    maximizing_player = player == 'b'
    tt = TranspositionTable()
    zobrist_hash = tt.compute_zobrist_hash(board, player)
    
    while remaining_time > 0:
        start_time = time.time()
        position = 1 - remaining_time / total_game_time  
        # Gaussfunktion 🤯
        factor = math.exp(-((position - 0.5) ** 2) / (2 * 1 ** 2)) - 0.87 # factor for time in current round
        print(factor)
        max_time = max(remaining_time * factor, 0.5)
        #print(max_time)
        best_move, searched_depth, nodes_explored = iterative_deepening_alpha_beta_search(board, player, max_time, max_depth, maximizing_player, tt, zobrist_hash)
        end_time = time.time()
        move_time = end_time - start_time  
        remaining_time = max(remaining_time - move_time - 0.01, 0)
        print(f"Best move: {best_move}, Depth: {searched_depth}, Nodes explored: {nodes_explored}, Time spent: {move_time}, Remaining time: {remaining_time}")
        
        return best_move
    


####################################################################################################################

# Test 


def alpha_beta_searchTEST(board, player, depth, alpha, beta, maximizing_player, start_time, max_time, tt, zobrist_hash):
    if time.time() - start_time > max_time:
        return None, None, False, 0  
    nodes_explored = 1 # 1 für aktuelles board

    tt_entry = tt.lookup(zobrist_hash)
    if tt_entry:
        tt_depth, tt_value, tt_flag, tt_best_move = tt_entry[0]
        if tt_depth >= depth:
            if tt_flag == EXACT:
                return tt_value, tt_best_move, True, nodes_explored
            elif tt_flag == LOWERBOUND:
                alpha = max(alpha, tt_value)
            elif tt_flag == UPPERBOUND:
                beta = min(beta, tt_value)
            if alpha >= beta:
                return tt_value, tt_best_move, True, nodes_explored
            
    moves, is_quiescent, stack_capture, single_capture = legal_moves(board, player) 

    if not moves or game_over(board, player): # or depth==0 jetzt in ruhesuche
        eval = evaluateFREF(board,player)
        tt.store(zobrist_hash, depth, eval, EXACT, None)
        return eval, None, True, nodes_explored
        #return evalDynamic(board,player), None, True, nodes_explored 
    
    global current_iterative_max_depth # too expensive to do for depths 1,2,3

    if depth==0: # RUHESUCHE ab horizont
        #return evaluateFREF(board,player), None, True, nodes_explored # uncomment to disable quiscent search
        if current_iterative_max_depth >= 4 and not is_quiescent: # if there are captures possible and searching depth of min. 4
            eval_quiescence, child_nodes_explored = quiescence_search(board, player, stack_capture, single_capture)
            tt.store(zobrist_hash, depth, eval_quiescence, EXACT, None) # unsure if its smart to also store this result
            nodes_explored += child_nodes_explored
            return eval_quiescence, None, True, nodes_explored # comment to enable the comparison

            # Idea: playing capture moves can be very bad for a player, but quiescence_search basically forces the player to do so
            # --> compare result of quiescence_search and eval without it and choose better value
            # ! seems reasonable but looses against variant without it
            eval_normal = evaluateFREF(board,player)
            if maximizing_player:
                if eval_quiescence > eval_normal:
                    return eval_quiescence, None, True, nodes_explored
                else:
                    return eval_normal, None, True, nodes_explored
            else:
                if eval_quiescence > eval_normal:
                    return eval_normal, None, True, nodes_explored
                else:
                    return eval_quiescence, None, True, nodes_explored

        else: # wenn es keine Schlagzüge gibt, also situation 'ruhig' ist
            return evaluateFREF(board,player), None, True, nodes_explored
    
    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in moves:
            start_value = board[move[0]] # save start field value e.g. b
            target_value = board[move[1]] # save target field value e.g. r
            new_player = make_move(board, player, move, start_value, target_value)
            new_zobrist_hash = tt.update_zobrist_hash(zobrist_hash, move, board, player)
            eval, _, completed, child_nodes_explored = alpha_beta_searchTEST(board, new_player, depth - 1, alpha, beta, False, start_time, max_time, tt, new_zobrist_hash)
            nodes_explored += child_nodes_explored
            unmake_move(board, move, start_value, target_value) # restore board 
            if not completed:
                return None, None, False, nodes_explored  
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:  
                break
            #print(f"Time elapsed for move {move}: {time.time() - start_time}")
        if best_move == None:
            best_move = moves[0]
        tt.store(zobrist_hash, depth, max_eval, LOWERBOUND if alpha >= beta else EXACT, best_move)
        return max_eval, best_move, True, nodes_explored  
    else:
        min_eval = float('inf')
        best_move = None
        for move in moves:
            start_value = board[move[0]] # save start field value e.g. r
            target_value = board[move[1]] # save target field value e.g. b
            new_player = make_move(board, player, move, start_value, target_value)
            new_zobrist_hash = tt.update_zobrist_hash(zobrist_hash, move, board, player)
            eval, _, completed, child_nodes_explored = alpha_beta_searchTEST(board, new_player, depth - 1, alpha, beta, True, start_time, max_time, tt, new_zobrist_hash)
            nodes_explored += child_nodes_explored
            unmake_move(board, move, start_value, target_value) # restore board 
            if not completed:
                return None, None, False, nodes_explored  
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:  
                break
        if best_move == None:
            best_move = moves[0]
        tt.store(zobrist_hash, depth, min_eval, LOWERBOUND if alpha >= beta else EXACT, best_move)
        return min_eval, best_move, True, nodes_explored  

current_iterative_max_depth = 1

def iterative_deepening_alpha_beta_searchTEST(board, player, max_time, max_depth, maximizing_player, tt, zobrist_hash):
    start_time = time.time()
    depth = 1
    best_move = None
    best_value = float('-inf') if maximizing_player else float('inf')
    total_nodes_explored = 0 # for testing
    aspiration_window = 100 # toggled off

    while True:
        if depth > max_depth:
            break
        alpha = best_value - aspiration_window
        beta = best_value + aspiration_window

        global current_iterative_max_depth 
        current_iterative_max_depth = depth # FOR QUIESCENCE CHECK

        print(f"Searching depth {depth}")
        depth_start_time = time.time()
        value, move, completed, nodes_explored = alpha_beta_searchTEST(board, player, depth, float('-inf'), float('inf'),
                                                                   maximizing_player, start_time, max_time, tt, zobrist_hash)
        # if completed:
        # print(f"Search completed for depth {depth}. Best move: {move}")
        depth_end_time = time.time()
        depth_time = depth_end_time - depth_start_time
        total_nodes_explored += nodes_explored


        if not completed:
            break


        if value <= alpha:
            # Research with a larger window
            alpha = float('-inf')
            beta = best_value + aspiration_window * 2
            value, move, completed, nodes_explored = alpha_beta_searchTEST(board, player, depth, alpha, beta,
                                                                       maximizing_player, start_time, max_time, tt, zobrist_hash
                                                                       )
            total_nodes_explored += nodes_explored
            if not completed:
                break
        elif value >= beta:
            # Research with a larger window
            alpha = best_value - aspiration_window * 2
            beta = float('inf')
            value, move, completed, nodes_explored = alpha_beta_searchTEST(board, player, depth, alpha, beta,
                                                                       maximizing_player, start_time, max_time, tt, zobrist_hash
                                                                       )
            total_nodes_explored += nodes_explored
            if not completed:
                break


        best_value = value
        best_move = move
        if (maximizing_player and best_value == float('inf')) or (not maximizing_player and best_value == float('-inf')):
            break
        
        # Estimate time for next depth
        if depth > 5:
            next_depth_time = depth_time * 10
            print(f"Nodes explored: {nodes_explored}, Estimated time for next depth: {next_depth_time}")
        else:  
            next_depth_time = depth_time * depth
        # Check if estimated time for next depth is less than remaining time
        remaining_time = max_time - (time.time() - start_time)
        if next_depth_time > remaining_time:
            print(f"Skipping depth {depth+1} as estimated time {next_depth_time} is greater than remaining time {remaining_time}")
            depth += 1
            break

        depth += 1
        #print(f"Incremented depth: {depth}")

    print(f"Best value: {best_value}, Total nodes explored: {total_nodes_explored}")
    #print(f"Decremented depth: {depth-1}")
    return best_move, depth-1, total_nodes_explored

total_game_time = 120  # Total game time in s

def select_moveTEST(fen,remaining_time):
    global total_game_time
    remaining_time = remaining_time / 1000 # keine lust time management auf ms umzubauen

    #remaining_time = 1000000 # for testing!
    #total_game_time = 1000000 # for testing!

    max_depth = 7  # for testing
    board, player = fen_to_board(fen)
    maximizing_player = player == 'b'
    tt = TranspositionTable()
    zobrist_hash = tt.compute_zobrist_hash(board, player)
    
    while remaining_time > 0:
        start_time = time.time()
        position = 1 - remaining_time / total_game_time  
        # Gaussfunktion 🤯
        factor = math.exp(-((position - 0.5) ** 2) / (2 * 1 ** 2)) - 0.87 # factor for time in current round
        print(factor)
        max_time = max(remaining_time * factor, 0.5)
        #print(max_time)
        best_move, searched_depth, nodes_explored = iterative_deepening_alpha_beta_searchTEST(board, player, max_time, max_depth, maximizing_player, tt, zobrist_hash)
        end_time = time.time()
        move_time = end_time - start_time  
        remaining_time = max(remaining_time - move_time - 0.01, 0)
        print(f"Best move: {best_move}, Depth: {searched_depth}, Nodes explored: {nodes_explored}, Time spent: {move_time}, Remaining time: {remaining_time}")
        
        return best_move
    

def quiescence_search2(board_alpaha_beta, player, stack_capture, single_capture):
    nodes_explored = 0
    board = board_alpaha_beta.copy() #so i dont need to unmake moves afterwards

    capture_moves = single_capture + stack_capture
    current_player = player
    max_depth = 6 # is tipically less than that
    curr_depth = 1

    while curr_depth <= max_depth:
        
        # move blue
        if current_player == 'b':
            #search for best capture move (depth 1 basically)
            best_eval = float('-inf')
            best_move = capture_moves[0]
            
            for move in capture_moves:
                nodes_explored += 1
                start_value = board[move[0]]
                target_value = board[move[1]]
                make_move(board, current_player, move, start_value, target_value)
                eval_i = evaluateFREF2(board,'r') 
                if eval_i > best_eval:
                    best_eval = eval_i 
                    best_move = move
                unmake_move(board, move, start_value, target_value)
            
            #play the move
            start_value = board[best_move[0]]
            target_value = board[best_move[1]]
            current_player = make_move(board, current_player, best_move, start_value, target_value)
            
        
        # move red
        else:
            #search for best capture move (depth 1 basically)
            best_eval = float('inf')
            best_move = capture_moves[0]
            
            for move in capture_moves:
                nodes_explored += 1
                start_value = board[move[0]]
                target_value = board[move[1]]
                make_move(board, current_player, move, start_value, target_value)
                eval_i = evaluateFREF2(board,'b') 
                if eval_i < best_eval:
                    best_eval = eval_i 
                    best_move = move
                unmake_move(board, move, start_value, target_value)
            
            #play the move
            start_value = board[best_move[0]]
            target_value = board[best_move[1]]
            current_player = make_move(board, current_player, best_move, start_value, target_value)

        # compute moves for opponent in next iteration
        _, is_quiescent, stack_capture, single_capture = legal_moves(board, current_player)
        capture_moves = stack_capture + single_capture

        if is_quiescent: #check if capture possible, if not break the lopp
            break
        #print(len(capture_moves)) # tipically 1-3 moves possible

        curr_depth+=1
        
    
    return evaluateFREF2(board, current_player), nodes_explored