import numpy as np
import pygame as pg
from board import board_to_fen, fen_to_board
from move_gen import legal_moves
from gamestate import random_move, game_over, generate_new_board, alpha_beta_search, iterative_deepening_alpha_beta_search, select_move

def sq2xy(sq):
    return sq[0] * 100, sq[1] * 100

def xy2sq(xy):
    return xy[0] // 100, xy[1] // 100

def load_pieces():
    images = {}
    piece_to_file = {
        'r': 'redpawn', 'b': 'bluepawn', 'rr': 'redtower', 'bb': 'bluetower',
        'br': 'redonblue', 'rb': 'blueonred'
    }
    for piece, filename in piece_to_file.items():
        image = pg.image.load(f'graphics/{filename}.png')
        images[piece] = pg.transform.smoothscale(image, (100, 100))
    return images

def draw_board(board, window):
    for y in range(8):
        for x in range(8):
            color = '#DFBF93' if (x + y) % 2 == 0 else '#C5844E'
            if board[y, x] == "X":
                color = (0, 0, 0)
            pg.draw.rect(window, color, (*sq2xy((x, y)), 100, 100))

def draw_pieces(board, window, PIECES):
    for y in range(8):
        for x in range(8):
            piece = board[y, x]
            if piece == "X":
                continue
            if piece:
                window.blit(PIECES[piece], sq2xy((x, y)))

def print_legal_moves(moves):
    move_strings = []
    for move in moves:
        from_pos, to_pos = move
        move_strings.append(f"{from_pos}->{to_pos}")
    print("Legal moves:", ", ".join(move_strings))

def parse_move(move_str):
    try:
        from_str, to_str = move_str.split("->")
        from_pos = tuple(map(int, from_str.strip("()").split(",")))
        to_pos = tuple(map(int, to_str.strip("()").split(",")))
        return (from_pos, to_pos)
    except ValueError:
        return None

def human_move(fen):
    board, player = fen_to_board(fen)
    legal_moves_list = legal_moves(board, player)
    print_legal_moves(legal_moves_list)

    while True:
        user_input = input("Enter your move (e.g., (1,2)->(1,3)): ")
        move = parse_move(user_input)
        if move in legal_moves_list:
            board, player = fen_to_board(fen)
            return generate_new_board(board, player, move)
        else:
            print("Invalid move. Please try again.")

def simulate_game(fen_start, window, pieces, clock, fps=40):
    board, player = fen_to_board(fen_start)
    running = True

    while running and not game_over(board, player):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # Draw the current board state
        window.fill((0, 0, 0))
        draw_board(board, window)
        draw_pieces(board, window, pieces)
        pg.display.flip()

        # Wait for a bit to visually see the move
        clock.tick(fps)

        # Make a move
        if player == 'b':
            best_move = select_move(board_to_fen(board, player))  # Blau verwendet Alpha-Beta-Suche
            if best_move is None:
                break
            board, player = generate_new_board(board, player, best_move)
        else:
            board, player = human_move(board_to_fen(board, player))

    
    for col in range(8):
        if board[7, col] in ['r', 'rr', 'rb']:
            print("Red has won!")
            break
        elif board[0, col] in ['b', 'bb', 'br']:
            print("Blue has won!")
            break

    return board_to_fen(board, player)

if __name__ == "__main__":
    pg.init()
    size = width, height = 800, 800
    SQUARE = width // 8
    FPS = 1.5
    window = pg.display.set_mode(size)
    BOARD = np.full((8, 8), "", dtype='U10')
    for y in range(8):
        for x in range(8):
            if (x, y) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
                BOARD[y, x] = "X"
            else:
                BOARD[y, x] = ""

    fen = 'b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0 b'
    fen1 = '3b02/2bb2b02/5b0bb1/2r0b04/2rb3b01/1rr1rr2r0r0/5r02/2rr3 b'
    fen2 = "b0b0b01bb1/2b0b0bbb02/5r02/3b04/4r0b02/8/2rrr01r02/r0r0r0r01r0 r"
    fen3 = "6/1bb1b02b01/8/2r05/3r01b02/5r0r02/2rr1r03/6 b"

    fen_o_early = "b0b02b0b0/1b01bb0b0b01/2b05/3b04/2r05/3r0r03/1r0r02r0r01/r0r01r0r0r0 r"
    fen_o_late = "6/1bb1b02b01/8/2r05/3r01b02/5r0r02/2rr1r03/6 b"
    fen_i_early = "b0b0b02bb/1b01b0bb1b01/2b05/5b02/1r06/8/2r0rrr0rr1r0/r0r01r01r0 r"
    fen_u_early = "bb1b0b0b0b0/b01b0b0b01b01/8/3b04/3r04/2r05/1rr2r0r01r0/1r0r0r0r0r0 r"
    fen_test = '2bb01b0b0/3b0b03/1b03b02/2b01r03/4r01b01/4r01r01/1rr1rr4/1r0r01r01 b'

    PIECES = load_pieces()
    clock = pg.time.Clock()

    # Start the simulation
    final_fen = simulate_game(fen, window, PIECES, clock, FPS)
    print("Final FEN:", final_fen)

    pg.quit()
