import random
from move_gen import legal_moves
from board import fen_to_board, board_to_fen
import time
import math


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

def evaluate(board,player):
    #piece_values = {'r': -1, 'rr': -2, 'br': -1.5, 'b': 1, 'bb': 2, 'rb': 1.5} # dunno
    pieces = ['r', 'rr', 'br', 'b', 'bb', 'rb']
    value = 0
    #red_moves = legal_moves(board, 'r')
    #blue_moves = legal_moves(board, 'b')

    #helper_eval = {"Position": 0, "Material": 0, "Mobility": 0, "Win": 0} # to understand components

    for row in range(8):
        for col in range(8):
            piece = board[row, col]
            if piece in pieces:
                # Überprüfen, ob ein rotes Stück auf der letzten Reihe ist
                if row == 7 and piece in ['r', 'rr', 'br']:
                    #helper_eval['Win'] = float('-inf')
                    return float('-inf')  # Red wins

                # Überprüfen, ob ein blaues Stück auf der ersten Reihe ist
                if row == 0 and piece in ['b', 'bb', 'rb']:
                    #helper_eval['Win'] = float('inf')
                    return float('inf')  # Blue wins

                # Position ((1.5**row) * 0.2) + Materialwert + ?
                if piece == 'r':
                    #helper_eval['Position'] -= ((1.5**row) * 0.2)
                    #helper_eval['Material'] -= 1
                    value -= ((1.5**row) * 0.2) + 1

                elif piece == 'b':
                    #helper_eval['Position'] += ((1.5**(7 - row)) * 0.2)
                    #helper_eval['Material'] += 1
                    value += ((1.5**(7 - row)) * 0.2) + 1

                elif piece == 'rr':
                    #helper_eval['Position'] -= ((1.5**row) * 0.3)
                    #helper_eval['Material'] -= 2
                    value -= ((1.5**row) * 0.3) + 2

                elif piece == 'bb':
                    #helper_eval['Position'] += ((1.5**(7 - row)) * 0.3)
                    #helper_eval['Material'] += 2
                    value += ((1.5**(7 - row)) * 0.3) + 2

                elif piece == 'br': 
                    #helper_eval['Position'] -= ((1.5**row) * 0.2)
                    value -= ((1.5**row) * 0.2) + 0 #mby troll aktuell gibts hier nur punkte für rot und materialwert von b und r gleichen sich aus -> durch faktor steuern 

                elif piece == 'rb':
                    #helper_eval['Position'] += ((1.5**row) * 0.2) # same
                    value += ((1.5**(7 - row)) * 0.2) + 0

                #123


    # Mobilität berücksichtigen
    #helper_eval['Mobility'] = 0.1 * len(blue_moves) - 0.1 * len(red_moves)
    #value -= 0.1 * len(red_moves)
    #value += 0.1 * len(blue_moves)

    #print(helper_eval)

    return value


def evaluateTest(board,player):
    pieces = ['r', 'rr', 'br', 'b', 'bb', 'rb']
    value = 0
    bonus_positions = [(0, 2), (0, 5), (7, 2), (7, 5)]  # Positions for bonus
    red_directions = [(1, -1), (1, 1)]  # Down-left and down-right for red
    blue_directions = [(-1, -1), (-1, 1)]  # Up-left and up-right for blue
    for row in range(8):
        for col in range(8):
            piece = board[row, col]
            if piece in pieces:

                if piece in pieces:
                    directions = red_directions if piece in ['r', 'rr', 'br'] else blue_directions
                
                    isolated = True
                    for dr, dc in directions:
                        r, c = row + dr, col + dc
                        if 0 <= r < 8 and 0 <= c < 8 and board[r, c] in pieces:
                            if (piece in ['r', 'rr', 'br'] and board[r, c] in ['r', 'rr', 'br']) or \
                            (piece in ['b', 'bb', 'rb'] and board[r, c] in ['b', 'bb', 'rb']):
                                isolated = False
                                break
                    if isolated:
                        if piece in ['r', 'rr', 'br']:
                            value += 0.2  # Penalty for red
                        else:
                            value -= 0.2  # Penalty for blue

                    # Bonus for capturing moves that isolate pieces or damage the enemy structure
                    for dr, dc in directions:
                        r, c = row + dr, col + dc
                        if 0 <= r < 8 and 0 <= c < 8 and board[r, c] not in pieces:
                            if piece in ['r', 'rr', 'br']:
                                value += 0.1  # Bonus for red
                            else:
                                value -= 0.1  # Bonus for blue
                if row == 7 and piece in ['r', 'rr', 'br']:
                    #helper_eval['Win'] = float('-inf')
                    return float('-inf')  # Red wins

                # Überprüfen, ob ein blaues Stück auf der ersten Reihe ist
                if row == 0 and piece in ['b', 'bb', 'rb']:
                    #helper_eval['Win'] = float('inf')
                    return float('inf')  # Blue wins

                # Position ((1.5**row) * 0.2) + Materialwert + ?
                if piece == 'r':
                    #helper_eval['Position'] -= ((1.5**row) * 0.2)
                    #helper_eval['Material'] -= 1
                    value -= ((1.5**row) * 0.2) + 1

                elif piece == 'b':
                    #helper_eval['Position'] += ((1.5**(7 - row)) * 0.2)
                    #helper_eval['Material'] += 1
                    value += ((1.5**(7 - row)) * 0.2) + 1

                elif piece == 'rr':
                    #helper_eval['Position'] -= ((1.5**row) * 0.3)
                    #helper_eval['Material'] -= 2
                    value -= ((1.5**row) * 0.3) + 2

                elif piece == 'bb':
                    #helper_eval['Position'] += ((1.5**(7 - row)) * 0.3)
                    #helper_eval['Material'] += 2
                    value += ((1.5**(7 - row)) * 0.3) + 2

                elif piece == 'br': 
                    #helper_eval['Position'] -= ((1.5**row) * 0.2)
                    value -= ((1.5**row) * 0.2) + 0 #mby troll aktuell gibts hier nur punkte für rot und materialwert von b und r gleichen sich aus -> durch faktor steuern 

                elif piece == 'rb':
                    #helper_eval['Position'] += ((1.5**row) * 0.2) # same
                    value += ((1.5**(7 - row)) * 0.2) + 0
                
                if (row, col) in bonus_positions:
                    if piece in ['r', 'rr', 'br']:
                        value -= 1.5  # Bonus for red
                    else:
                        value += 1.5  # Bonus for blue
    
    # Mobilität berücksichtigen
    #helper_eval['Mobility'] = 0.1 * len(blue_moves) - 0.1 * len(red_moves)
    #value -= 0.1 * len(red_moves)
    #value += 0.1 * len(blue_moves)

    #print(helper_eval)

    return value


def evaluateFREF(board,player):
    pieces = ['r', 'rr', 'br', 'b', 'bb', 'rb']
    value = 0

    #bonus for current player
    if(player=='b'):value += 0.25
    else: value -= 0.25
    
    #bonus positions
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
                    value -= ((1.5**row) * 0.3) + 1

                elif piece == 'b':
                    value += ((1.5**(7 - row)) * 0.3) + 1

                elif piece == 'rr':
                    value -= ((1.5**row) * 0.5) + 2

                elif piece == 'bb':
                    value += ((1.5**(7 - row)) * 0.5) + 2

                elif piece == 'br': 
                    value -= ((1.5**row) * 0.3) + 0 

                elif piece == 'rb':
                    value += ((1.5**(7 - row)) * 0.3) + 0 


    return value

def evaluateFREFseite(board,player):
    pieces = ['r', 'rr', 'br', 'b', 'bb', 'rb']
    value = 0
    
    #bonus for current player
    if(player=='b'):value += 0.25
    else: value -= 0.25
    
    #bonus positions
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
                    value -= ((1.5**row) * 0.3) + 1 + math.log((col*row/2)+1)

                elif piece == 'b':
                    value += ((1.5**(7 - row)) * 0.3) + 1 + math.log((col*row/2)+1)

                elif piece == 'rr':
                    value -= ((1.5**row) * 0.4) + 2 + math.log((col*row/2)+1)

                elif piece == 'bb':
                    value += ((1.5**(7 - row)) * 0.4) + 2 + math.log((col*row/2)+1)

                elif piece == 'br': 
                    value -= ((1.5**row) * 0.2) + 0 + math.log((col*row/2)+1)

                elif piece == 'rb':
                    value += ((1.5**(7 - row)) * 0.2) + 0 + math.log((col*row/2)+1)


    return value

def make_move(board, player, move, start_value, target_value):
    from_pos, to_pos = move

    if player == "b":
        # Move logic for blue pieces
        if target_value in ["", "r"]:
            board[to_pos] = "b"
        elif target_value == "rr":
            board[to_pos] = "rb"
        elif target_value in ["b", "br"]:
            board[to_pos] = "bb"

        # Clear the original position
        if start_value == "b":
            board[from_pos] = ""
        elif start_value == "bb":
            board[from_pos] = "b"
        elif start_value == "rb":
            board[from_pos] = "r"

    else:
        # Move logic for red pieces
        if target_value in ["", "b"]:
            board[to_pos] = "r"
        elif target_value == "bb":    
            board[to_pos] = "br"
        elif target_value in ["r", "rb"]:
            board[to_pos] = "rr"

        # Clear the original position
        if start_value == "r":
            board[from_pos] = ""
        elif start_value == "rr":
            board[from_pos] = "r"
        elif start_value == "br":
            board[from_pos] = "b"

    return 'b' if player == 'r' else 'r' # Switch the player

def unmake_move(board, move, start_value, target_value):
    from_pos, to_pos = move

    board[from_pos] = start_value
    board[to_pos] = target_value
    
    return



def alpha_beta_search(board, player, depth, alpha, beta, maximizing_player, start_time, max_time):
    if time.time() - start_time > max_time:
        return None, None, False, 0  
    nodes_explored = 0 # for testing
    moves = legal_moves(board, player)
    if not moves or depth == 0 or game_over(board, player):
        nodes_explored += 1
        return evaluateFREF(board,player), None, True, nodes_explored

        #if maximizing_player:
        #    return evaluate(board,player), None, True, nodes_explored # to compare eval functions here
        #else: return evaluate(board,player), None, True, nodes_explored
        
    nodes_explored += 1 # for testing 

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in moves:
            start_value = board[move[0]] # save start field value e.g. b
            target_value = board[move[1]] # save target field value e.g. r
            new_player = make_move(board, player, move, start_value, target_value)
            eval, _, completed, child_nodes_explored = alpha_beta_search(board, new_player, depth - 1, alpha, beta, False, start_time, max_time)
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
        return max_eval, best_move, True, nodes_explored  
    else:
        min_eval = float('inf')
        best_move = None
        for move in moves:
            start_value = board[move[0]] # save start field value e.g. r
            target_value = board[move[1]] # save target field value e.g. b
            new_player = make_move(board, player, move, start_value, target_value)
            eval, _, completed, child_nodes_explored = alpha_beta_search(board, new_player, depth - 1, alpha, beta, True, start_time, max_time)
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

        return min_eval, best_move, True, nodes_explored  

def iterative_deepening_alpha_beta_search(board, player, max_time, max_depth, maximizing_player):
    start_time = time.time()
    depth = 0
    best_move = None
    best_value = float('-inf') if maximizing_player else float('inf')
    total_nodes_explored = 0 # for testing

    while True:
        if depth > max_depth:
            break
        print(f"Searching depth {depth}")
        depth_start_time = time.time()
        value, move, completed, nodes_explored = alpha_beta_search(board, player, depth, float('-inf'), float('inf'), maximizing_player, start_time, max_time)
        #if completed:
            #print(f"Search completed for depth {depth}. Best move: {move}")
        depth_end_time = time.time()
        depth_time = depth_end_time - depth_start_time
        total_nodes_explored += nodes_explored
        if not completed:
            break  
        best_value = value
        best_move = move
        if (maximizing_player and best_value == float('inf')) or (not maximizing_player and best_value == float('-inf')):
            break
        
        # Estimate time for next depth
        if depth > 4:
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

total_game_time = 120  # Total game time in seconds
remaining_time = total_game_time 

def select_move(fen):
    global remaining_time, total_game_time
    max_depth = 4  # for testing
    board, player = fen_to_board(fen)
    maximizing_player = player == 'b'
    
    while remaining_time > 0:
        start_time = time.time()
        position = 1 - remaining_time / total_game_time  
        # Gaussfunktion 🤯
        factor = math.exp(-((position - 0.5) ** 2) / (2 * 1 ** 2)) - 0.87 # factor for time in current round
        print(factor)
        max_time = max(remaining_time * factor, 0.5)
        #print(max_time)
        best_move, searched_depth, nodes_explored = iterative_deepening_alpha_beta_search(board, player, max_time, max_depth, maximizing_player)
        end_time = time.time()
        move_time = end_time - start_time  
        remaining_time = max(remaining_time - move_time - 0.01, 0)
        print(f"Best move: {best_move}, Depth: {searched_depth}, Nodes explored: {nodes_explored}, Time spent: {move_time}, Remaining time: {remaining_time}")
        
        return best_move


####################################################################################################################

# Test damit verschiedene eval komplett allein evaluaten in play_local und nicht vermischt



def alpha_beta_searchTEST(board, player, depth, alpha, beta, maximizing_player, start_time, max_time):
    if time.time() - start_time > max_time:
        return None, None, False, 0  
    nodes_explored = 0 # for testing
    moves = legal_moves(board, player)
    if not moves or depth == 0 or game_over(board, player):
        nodes_explored += 1
        return evaluateFREF(board,player), None, True, nodes_explored
        #if maximizing_player:
        #    return evaluate(board,player), None, True, nodes_explored # to compare eval functions here
        #else: return evaluateFREF(board,player), None, True, nodes_explored
        
    nodes_explored += 1 # for testing 

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in moves:
            start_value = board[move[0]] # save start field value e.g. b
            target_value = board[move[1]] # save target field value e.g. r
            new_player = make_move(board, player, move, start_value, target_value)
            eval, _, completed, child_nodes_explored = alpha_beta_searchTEST(board, new_player, depth - 1, alpha, beta, False, start_time, max_time)
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
        return max_eval, best_move, True, nodes_explored  
    else:
        min_eval = float('inf')
        best_move = None
        for move in moves:
            start_value = board[move[0]] # save start field value e.g. r
            target_value = board[move[1]] # save target field value e.g. b
            new_player = make_move(board, player, move, start_value, target_value)
            eval, _, completed, child_nodes_explored = alpha_beta_searchTEST(board, new_player, depth - 1, alpha, beta, True, start_time, max_time)
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

        return min_eval, best_move, True, nodes_explored  

def select_moveTEST(fen):
    global remaining_time, total_game_time
    max_depth = 4  # for testing
    board, player = fen_to_board(fen)
    maximizing_player = player == 'b'
    
    while remaining_time > 0:
        start_time = time.time()
        position = 1 - remaining_time / total_game_time  
        # Gaussfunktion 🤯
        factor = math.exp(-((position - 0.5) ** 2) / (2 * 1 ** 2)) - 0.87 # factor for time in current round
        print(factor)
        max_time = max(remaining_time * factor, 0.5)
        #print(max_time)
        best_move, searched_depth, nodes_explored = iterative_deepening_alpha_beta_searchTEST(board, player, max_time, max_depth, maximizing_player)
        end_time = time.time()
        move_time = end_time - start_time  
        remaining_time = max(remaining_time - move_time - 0.01, 0)
        print(f"Best move: {best_move}, Depth: {searched_depth}, Nodes explored: {nodes_explored}, Time spent: {move_time}, Remaining time: {remaining_time}")
        
        return best_move
    
def iterative_deepening_alpha_beta_searchTEST(board, player, max_time, max_depth, maximizing_player):
    start_time = time.time()
    depth = 0
    best_move = None
    best_value = float('-inf') if maximizing_player else float('inf')
    total_nodes_explored = 0 # for testing

    while True:
        if depth > max_depth:
            break
        print(f"Searching depth {depth}")
        depth_start_time = time.time()
        value, move, completed, nodes_explored = alpha_beta_searchTEST(board, player, depth, float('-inf'), float('inf'), maximizing_player, start_time, max_time)
        #if completed:
            #print(f"Search completed for depth {depth}. Best move: {move}")
        depth_end_time = time.time()
        depth_time = depth_end_time - depth_start_time
        total_nodes_explored += nodes_explored
        if not completed:
            break  
        best_value = value
        best_move = move
        if (maximizing_player and best_value == float('inf')) or (not maximizing_player and best_value == float('-inf')):
            break
        
        # Estimate time for next depth
        if depth > 4:
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













############################################################## Einfacher MinMax (ohne Cutoffs)



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



def min_max_search(board, player, depth, maximizing_player, start_time, max_time):
    nodes_explored = 0

    def min_max_recursive(board, player, depth, maximizing_player):
        nonlocal nodes_explored
        if time.time() - start_time > max_time:
            return None, None, False  

        if depth == 0 or game_over(board, player):
            nodes_explored += 1
            return evaluate(board), None, True  

        moves = legal_moves(board, player)
        if not moves:
            nodes_explored += 1
            return evaluate(board), None, True  

        nodes_explored += 1  

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in moves:
                new_board, new_player = generate_new_board(board, player, move)
                eval, _, completed = min_max_recursive(new_board, new_player, depth - 1, False)
                if not completed:
                    return None, None, False  
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            if best_move == None:
                best_move = moves[0]
            return max_eval, best_move, True  
        else:
            min_eval = float('inf')
            best_move = None
            for move in moves:
                new_board, new_player = generate_new_board(board, player, move)
                eval, _, completed = min_max_recursive(new_board, new_player, depth - 1, True)
                if not completed:
                    return None, None, False  
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            if best_move == None:
                best_move = moves[0]
            return min_eval, best_move, True  
    
    value, best_move, completed = min_max_recursive(board, player, depth, maximizing_player)
    return value, best_move, completed, nodes_explored

def iterative_deepening_min_max_search(board, player, max_time, max_depth, maximizing_player):
    start_time = time.time()
    depth = 1
    best_move = None
    best_value = float('-inf') if maximizing_player else float('inf')
    total_nodes_explored = 0

    while True:
        if depth > max_depth:
            break
        print(f"Searching depth {depth}")
        value, move, completed, nodes_explored = min_max_search(board, player, depth, maximizing_player, start_time, max_time)
        total_nodes_explored += nodes_explored
        if not completed :
            break  
        best_value = value
        best_move = move
        depth += 1

        if (maximizing_player and best_value == float('inf')) or (
                not maximizing_player and best_value == float('-inf')):
            break

    print(f"Best value: {best_value}, Total nodes explored: {total_nodes_explored}")
    return best_move, depth - 1, total_nodes_explored

def select_min_max_move(fen):
    max_time = 1000000  # Maximum time in seconds for each move
    max_depth = 10000  # for testing
    board, player = fen_to_board(fen)
    maximizing_player = player == 'b'
    best_move, searched_depth, nodes_explored = iterative_deepening_min_max_search(board, player, max_time, max_depth, maximizing_player)
    print(f"Best move: {best_move}, Depth: {searched_depth}, Nodes explored: {nodes_explored}")
    return best_move

