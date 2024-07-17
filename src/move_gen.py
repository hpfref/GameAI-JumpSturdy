import numpy as np
from collections import deque


def legal_moves(board, player): 
    """Return all legal moves for the current player

    Args:
        fen: board & player

    Returns:
        moves: list of legal moves e.g. [((6, 1), (6, 0)), ...]
        is_quiescent: ...
        stack_capture: ...
        single_capture: ...
    """
    single_capture = deque([])
    stack_capture = deque([])
    stack_nocapture = deque([])
    single_forwards = deque([])
    single_sideways = deque([])

    # Use for quiesence search
    is_quiescent = True

    ### BLUE CASE START ###

    if player == "b": 
        # Get indices of blue pieces
        indices_b = np.where((board == "b") | (board == "bb") | (board == "rb")) # consider rb as blue piece for this move

        # Set legal target moves
        b_moves_straight = ["", "b"]
        b_moves_diagonal = ["r", "rr", "br"]
        #bb_moves = ["", "b", "r", "br", "rr"]
        bb_capture = ["r", "br", "rr"]
        bb_nocapture = ["", "b"]
        #target = None # to temporarily store target moves

        #Loop through blue pieces
        for index in zip(indices_b[0], indices_b[1]):
            piece = board[index]
            #print("Blue piece at index:", index, "is", piece)

            # Check simple blue piece b
            if piece == "b":

                # Check left
                target = index[0], index[1]-1
                if index[1] > 0 and board[target] in b_moves_straight:
                    single_sideways.append((index, (target)))  # Append the valid move to the left

                # Check right
                target = index[0], index[1]+1
                if index[1] < 7 and board[target] in b_moves_straight:
                    single_sideways.append((index, (target)))  # Append the valid move to the right

                # Check top
                if index[0] > 0:
                    # Check top left
                    target = index[0]-1, index[1]-1
                    if index[1] > 0 and board[target] in b_moves_diagonal:
                        single_capture.append((index, (target)))  # Append the valid move to the top left
                        is_quiescent = False

                    # Check top right
                    target = index[0]-1, index[1]+1
                    if index[1] < 7 and board[target] in b_moves_diagonal:
                        single_capture.append((index, (target)))  # Append the valid move to the top right
                        is_quiescent = False

                    # Check top
                    target = index[0]-1, index[1]
                    if board[target] in b_moves_straight:
                        single_forwards.append((index, (target)))  # Append the valid move to the top

            # Check blue stack bb or rb
            else:

                # Check top
                if index[0] > 0:
                    
                    # Check top left left
                    if index[1] > 1:
                        target = index[0]-1, index[1]-2
                        if board[target] in bb_capture:
                            stack_capture.append((index, (target)))  # Append the valid move to top left left
                            is_quiescent = False
                        elif board[target] in bb_nocapture:
                            stack_nocapture.append((index, (target)))  # Append the valid move to top left left

                    
                    # Check top right right
                    if index[1] < 6:
                        target = index[0]-1, index[1]+2
                        if board[target] in bb_capture:
                            stack_capture.append((index, (target)))  # Append the valid move to top right right
                            is_quiescent = False
                        elif board[target] in bb_nocapture:
                            stack_nocapture.append((index, (target)))  # Append the valid move to top right right

                # Check top top
                if index[0] > 1:

                    # Check top top left
                    if index[1] > 0:
                        target = index[0]-2, index[1]-1
                        if board[target] in bb_capture:
                            stack_capture.append((index, (target))) # Append the valid move to top top left
                            is_quiescent = False
                        elif board[target] in bb_nocapture:
                            stack_nocapture.append((index, (target))) # Append the valid move to top top left

                    # Check top top right
                    if index[1] < 7:
                        target = index[0]-2, index[1]+1
                        if board[target] in bb_capture:
                            stack_capture.append((index, (target))) # Append the valid move to top top right
                            is_quiescent = False
                        elif board[target] in bb_nocapture:
                            stack_nocapture.append((index, (target))) # Append the valid move to top top right
            

    ### BLUE CASE END ###
    ### RED CASE START ###
            
    else:
        # Get indices of red pieces
        indices_r = np.where((board == "r") | (board == "rr") | (board == "br")) # consider br as red piece for this move

        # Set legal target moves
        r_moves_straight = ["", "r"]
        r_moves_diagonal = ["b", "bb", "rb"]
        #rr_moves = ["", "b", "r", "rb", "bb"]
        rr_capture = ["b", "rb", "bb"]
        rr_nocapture = ["","r"]

        # Loop through red pieces indices
        for index in zip(indices_r[0], indices_r[1]):
            piece = board[index]
            #print("Red piece at index:", index)    

            # Check simple red piece r
            if piece == "r":

                # Check left
                target = index[0], index[1]-1
                if index[1] > 0 and board[target] in r_moves_straight:
                    single_sideways.append((index, (target)))  # Append the valid move to the left

                # Check right
                target = index[0], index[1]+1
                if index[1] < 7 and board[target] in r_moves_straight:
                    single_sideways.append((index, (target)))  # Append the valid move to the right

                # Check bottom
                if index[0] < 7:

                    # Check bottom left
                    target = index[0]+1, index[1]-1
                    if index[1] > 0 and board[target] in r_moves_diagonal:
                        single_capture.append((index, (target)))  # Append the valid move to the bottom left
                        is_quiescent = False

                    # Check bottom right
                    target = index[0]+1, index[1]+1
                    if index[1] < 7 and board[target] in r_moves_diagonal:
                        single_capture.append((index, (target)))  # Append the valid move to the bottom right
                        is_quiescent = False

                    # Check bottom
                    target = index[0]+1, index[1]
                    if board[target] in r_moves_straight:
                        single_forwards.append((index, (target)))  # Append the valid move to the bottom

            # Check red stack br or rr
            else:

                # Check bottom 
                if index[0] < 7:

                    # Check bottom left left
                    if index[1] > 1:
                        target = index[0]+1, index[1]-2
                        if board[target] in rr_capture:
                            stack_capture.append((index, (target))) # Append the valid move to the bottom left left
                            is_quiescent = False
                        elif board[target] in rr_nocapture:
                            stack_nocapture.append((index, (target))) # Append the valid move to the bottom left left

                    # Check bottom bottom right
                    if index[1] < 6:
                        target = index[0]+1, index[1]+2
                        if board[target] in rr_capture:
                            stack_capture.append((index, (target))) # Append the valid move to the bottom right right
                            is_quiescent = False
                        elif board[target] in rr_nocapture:
                            stack_nocapture.append((index, (target))) # Append the valid move to the bottom right right

                # Check bottom bottom
                if index[0] < 6:

                    # Check bottom bottom left
                    if index[1] > 0:
                        target = index[0]+2, index[1]-1
                        if board[target] in rr_capture:
                            stack_capture.append((index, (target))) # Append the valid move to the bottom bottom left
                            is_quiescent = False
                        elif board[target] in rr_nocapture:
                            stack_nocapture.append((index, (target))) # Append the valid move to the bottom bottom left

                    # Check bottom bottom right
                    if index[1] < 7:
                        target = index[0]+2, index[1]+1
                        if board[target] in rr_capture:
                            stack_capture.append((index, (target))) # Append the valid move to the bottom bottom right
                            is_quiescent = False
                        elif board[target] in rr_nocapture:
                            stack_nocapture.append((index, (target))) # Append the valid move to the bottom bottom right
  
  
    ### RED CASE END ###
    moves = stack_capture.copy()
    moves.extend(single_capture)
    moves.extend(stack_nocapture)
    moves.extend(single_forwards)
    moves.extend(single_sideways)

    return moves, is_quiescent, stack_capture, single_capture # extend is in place operation, this contains all moves now

    

def translate_single_move(move): # for gameserver
    """Translate indexes of move into the official field names

    Args:
        moves: List of moves e.g. ((2, 2), (2, 1))

    Returns:
        list: List 0f moves e.g. 'C6-B6'
    """

    index_to_position = { 
    (0, 0): "A8", (0, 1): "B8", (0, 2): "C8", (0, 3): "D8", (0, 4): "E8", (0, 5): "F8", (0, 6): "G8", (0, 7): "H8",
    (1, 0): "A7", (1, 1): "B7", (1, 2): "C7", (1, 3): "D7", (1, 4): "E7", (1, 5): "F7", (1, 6): "G7", (1, 7): "H7",
    (2, 0): "A6", (2, 1): "B6", (2, 2): "C6", (2, 3): "D6", (2, 4): "E6", (2, 5): "F6", (2, 6): "G6", (2, 7): "H6",
    (3, 0): "A5", (3, 1): "B5", (3, 2): "C5", (3, 3): "D5", (3, 4): "E5", (3, 5): "F5", (3, 6): "G5", (3, 7): "H5",
    (4, 0): "A4", (4, 1): "B4", (4, 2): "C4", (4, 3): "D4", (4, 4): "E4", (4, 5): "F4", (4, 6): "G4", (4, 7): "H4",
    (5, 0): "A3", (5, 1): "B3", (5, 2): "C3", (5, 3): "D3", (5, 4): "E3", (5, 5): "F3", (5, 6): "G3", (5, 7): "H3",
    (6, 0): "A2", (6, 1): "B2", (6, 2): "C2", (6, 3): "D2", (6, 4): "E2", (6, 5): "F2", (6, 6): "G2", (6, 7): "H2",
    (7, 0): "A1", (7, 1): "B1", (7, 2): "C1", (7, 3): "D1", (7, 4): "E1", (7, 5): "F1", (7, 6): "G1", (7, 7): "H1",
}
    
    start_pos = index_to_position[move[0]]
    end_pos = index_to_position[move[1]]
    return f"{start_pos}-{end_pos}"


def translate_moves(moves)->list: # don't know if needed for our move representation - ig only for testing legal moves from wiki?
    """Translate indexes of moves into the official field names

    Args:
        moves: List of moves e.g. [((2, 2), (2, 1)), ((2, 2), (2, 3)), ...]

    Returns:
        list: List 0f moves e.g. ['C6-B6', 'C6-D6', ...]
    """
    translated_moves = []

    index_to_position = { 
    (0, 0): "A8", (0, 1): "B8", (0, 2): "C8", (0, 3): "D8", (0, 4): "E8", (0, 5): "F8", (0, 6): "G8", (0, 7): "H8",
    (1, 0): "A7", (1, 1): "B7", (1, 2): "C7", (1, 3): "D7", (1, 4): "E7", (1, 5): "F7", (1, 6): "G7", (1, 7): "H7",
    (2, 0): "A6", (2, 1): "B6", (2, 2): "C6", (2, 3): "D6", (2, 4): "E6", (2, 5): "F6", (2, 6): "G6", (2, 7): "H6",
    (3, 0): "A5", (3, 1): "B5", (3, 2): "C5", (3, 3): "D5", (3, 4): "E5", (3, 5): "F5", (3, 6): "G5", (3, 7): "H5",
    (4, 0): "A4", (4, 1): "B4", (4, 2): "C4", (4, 3): "D4", (4, 4): "E4", (4, 5): "F4", (4, 6): "G4", (4, 7): "H4",
    (5, 0): "A3", (5, 1): "B3", (5, 2): "C3", (5, 3): "D3", (5, 4): "E3", (5, 5): "F3", (5, 6): "G3", (5, 7): "H3",
    (6, 0): "A2", (6, 1): "B2", (6, 2): "C2", (6, 3): "D2", (6, 4): "E2", (6, 5): "F2", (6, 6): "G2", (6, 7): "H2",
    (7, 0): "A1", (7, 1): "B1", (7, 2): "C1", (7, 3): "D1", (7, 4): "E1", (7, 5): "F1", (7, 6): "G1", (7, 7): "H1",
}
    for move in moves:
        start_pos = index_to_position[move[0]]
        end_pos = index_to_position[move[1]]
        translated_moves.append(f"{start_pos}-{end_pos}")

    return translated_moves
