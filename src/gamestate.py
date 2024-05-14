import random
from move_gen import legal_moves
from board import fen_to_board, board_to_fen

def random_move(fen):
    moves = legal_moves(fen)
    if not moves:
        return None
    return random.choice(moves)

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

    moving_piece = board[from_pos]
    target_piece = board[to_pos]

    # Handle the movement of knights
    if moving_piece in ['rr', 'bb', 'br', 'rb']:
        # Only the top piece of the knight moves
        board[from_pos] = moving_piece[1]
        moving_piece = moving_piece[0]

    # Handle stepping on a single piece of the opposite color
    if target_piece in ['r', 'b'] and moving_piece in ['r', 'b'] and target_piece != moving_piece:
        # The moving piece eliminates the target piece
        board[to_pos] = moving_piece
    elif target_piece == moving_piece:
        # Handle stepping on a single piece of the same color
        if moving_piece == 'r':
            board[to_pos] = 'rr'
        elif moving_piece == 'b':
            board[to_pos] = 'bb'
    else:
        board[to_pos] = moving_piece

    # Clear the original position if it's not a knight
    board[from_pos] = ''

    # Switch the player
    player = 'b' if player == 'r' else 'r'

    # Convert the board back to a FEN string
    new_fen = board_to_fen(board, player)
    print(new_fen)
    return new_fen
def play_game(starting_fen):
    current_fen = starting_fen

    while not game_over(current_fen):
        move = random_move(current_fen)
        if move is None:
            break
        current_fen = generate_new_board(current_fen, move)

    # Check the final state of the game and print the winner
    if game_over(current_fen):
        board, player = fen_to_board(current_fen)
        for col in range(8):
            if board[7, col] in ['r', 'rr', 'rb']:
                print("Red has won!")
                break
            elif board[0, col] in ['b', 'bb', 'br']:
                print("Blue has won!")
                break
    return current_fen


starting_fen = 'b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0 b'
play_game(starting_fen)
