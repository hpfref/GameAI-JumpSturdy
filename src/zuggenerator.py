from board import board_to_fen, fen_to_board
import numpy as np


# probably need to change for zugsortierung -> züge als schlagzug markieren und direkt vorne einsortiern usw...
# -> maybe suche nach zügen für ein ein piece in eigene funktion ausgliedern
# und adden von zügen in moves liste in eigene funktionen ausgleiedern für sortierung
def legal_moves(fen) -> list: 
    """Return all legal moves for the current player

    Args:
        fen: board & player

    Returns:
        moves: list of legal moves e.g. [((6, 1), (6, 0)), ...]
    """
    board, player  = fen_to_board(fen)
    moves = [] # representation hier überlegen, maybe marker mit einbauen ob schlag move, winning move, ... 

    ### BLUE CASE START ###

    if player == "b": # viel doppelter code durch case blue/red
        # Get indices of blue pieces
        indices_b = np.where((board == "b") | (board == "bb") | (board == "rb")) # consider rb as blue piece for this move

        # Set legal target moves
        b_moves_straight = ["", "b"]
        b_moves_diagonal = ["r", "rr", "br"]
        bb_moves = ["", "b", "r", "br", "rr"]

        #Loop through blue pieces
        for index in zip(indices_b[0], indices_b[1]):
            piece = board[index]
            #print("Blue piece at index:", index, "is", piece)

            # Check simple blue piece b
            if piece == "b":

                # Check left
                if index[1] > 0 and board[index[0], index[1]-1] in b_moves_straight:
                    moves.append((index, (index[0], index[1]-1)))  # Append the valid move to the left

                # Check right
                if index[1] < 7 and board[index[0], index[1]+1] in b_moves_straight:
                    moves.append((index, (index[0], index[1]+1)))  # Append the valid move to the right

                # Check top
                if index[0] > 0:
                    # Check top left
                    if index[1] > 0 and board[index[0]-1, index[1]-1] in b_moves_diagonal:
                        moves.append((index, (index[0]-1, index[1]-1)))  # Append the valid move to the top left

                    # Check top right
                    if index[1] < 7 and board[index[0]-1, index[1]+1] in b_moves_diagonal:
                        moves.append((index, (index[0]-1, index[1]+1)))  # Append the valid move to the top right

                    # Check top
                    if board[index[0]-1, index[1]] in b_moves_straight:
                        moves.append((index, (index[0]-1, index[1])))  # Append the valid move to the top

            # Check blue stack bb or rb
            else:

                # Check top
                if index[0] > 0:
                    
                    # Check top left left
                    if index[1] > 1 and board[index[0]-1, index[1]-2] in bb_moves:
                        moves.append((index, (index[0]-1, index[1]-2)))  # Append the valid move to top left left

                    
                    # Check top right right
                    if index[1] < 6 and board[index[0]-1, index[1]+2] in bb_moves:
                        moves.append((index, (index[0]-1, index[1]+2)))  # Append the valid move to top right right

                # Check top top
                if index[0] > 1:

                    # Check top top left
                    if index[1] > 0 and board[index[0]-2, index[1]-1] in bb_moves:
                        moves.append((index, (index[0]-2, index[1]-1)))  # Append the valid move to top top left

                    # Check top top right
                    if index[1] < 7 and board[index[0]-2, index[1]+1] in bb_moves:
                        moves.append((index, (index[0]-2, index[1]+1)))  # Append the valid move to top top right

    ### BLUE CASE END ###
    ### RED CASE START ###
            
    else:
        # Get indices of red pieces
        indices_r = np.where((board == "r") | (board == "rr") | (board == "br")) # consider br as red piece for this move

        # Set legal target moves
        r_moves_straight = ["", "r"]
        r_moves_diagonal = ["b", "bb", "rb"]
        rr_moves = ["", "b", "r", "rb", "bb"]

        # Loop through red pieces indices
        for index in zip(indices_r[0], indices_r[1]):
            piece = board[index]
            #print("Red piece at index:", index)    

            # Check simple red piece r
            if piece == "r":

                # Check left
                if index[1] > 0 and board[index[0], index[1]-1] in r_moves_straight:
                    moves.append((index, (index[0], index[1]-1)))  # Append the valid move to the left

                # Check right
                if index[1] < 7 and board[index[0], index[1]+1] in r_moves_straight:
                    moves.append((index, (index[0], index[1]+1)))  # Append the valid move to the right

                # Check bottom
                if index[0] < 7:

                    # Check bottom left
                    if index[1] > 0 and board[index[0]+1, index[1]-1] in r_moves_diagonal:
                        moves.append((index, (index[0]+1, index[1]-1)))  # Append the valid move to the bottom left

                    # Check bottom right
                    if index[1] < 7 and board[index[0]+1, index[1]+1] in r_moves_diagonal:
                        moves.append((index, (index[0]+1, index[1]+1)))  # Append the valid move to the bottom right

                    # Check bottom
                    if board[index[0]+1, index[1]] in r_moves_straight:
                        moves.append((index, (index[0]+1, index[1])))  # Append the valid move to the bottom

            # Check red stack br or rr
            else:

                # Check bottom 
                if index[0] < 7:

                    # Check bottom left left
                    if index[1] > 1 and board[index[0]+1, index[1]-2] in rr_moves:
                        moves.append((index, (index[0]+1, index[1]-2)))  # Append the valid move to the bottom left left

                    # Check bottom bottom right
                    if index[1] < 6 and board[index[0]+1, index[1]+2] in rr_moves:
                        moves.append((index, (index[0]+1, index[1]+2)))  # Append the valid move to the bottom right right

                # Check bottom bottom
                if index[0] < 6:

                    # Check bottom bottom left
                    if index[1] > 0 and board[index[0]-2, index[1]-1] in rr_moves:
                        moves.append((index, (index[0]-2, index[1]-1)))  # Append the valid move to the bottom bottom left

                    # Check bottom bottom right
                    if index[1] < 7 and board[index[0]-2, index[1]+1] in rr_moves:
                        moves.append((index, (index[0]-2, index[1]+1)))  # Append the valid move to the bottom bottom right
  
    ### RED CASE END ###

    return moves

###

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

if __name__ == "__main__":

    fen0 = "b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0 b"
    fen1 = "6/1b0b0b0b0b0b01/1b0b0b0b0b0b01/8/8/1r0r0r0r0r0r01/1r0r0r0r0r0r01/6 b"
    fen2 = "6/1bb1b02b01/8/2r05/3r01b02/5r0r02/2rr1r03/6 b"
    fen3 = "b0b0b01bb1/2b0b0bbb02/5r02/3b04/4r0b02/8/2rrr01r02/r0r0r0r01r0 r"
    fen4 = "3b02/5r02/3r04/8/8/2b02b02/2r05/6 b"

    moves = legal_moves(fen4)
    print(f"Legal moves: {translate_moves(moves)}")
    print(f"Number of legal moves: {len(moves)}")
    #print("Hellow?")

