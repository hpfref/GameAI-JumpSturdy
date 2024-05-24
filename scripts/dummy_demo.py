### To import from src:
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
###
import numpy as np
import pygame as pg
from visuals import load_pieces, draw_board, draw_pieces
from board import fen_to_board, board_to_fen
from gamestate import random_move, game_over, generate_new_board, select_move

if __name__ == "__main__":
    pg.init()
    size = width, height = 800, 800
    SQUARE = width // 8
    FPS = 1
    window = pg.display.set_mode(size)
    BOARD = np.full((8, 8), "", dtype='U10')
    for y in range(8):
        for x in range(8):
            if (x, y) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
                BOARD[y, x] = "X"
            else:
                BOARD[y, x] = ""
                
    starting_fen = '2b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0 b'
    midgame_fen = 'b01b0b0b0b0/1b0b01b01b01/3b01b02/2b05/8/2r0r01rr2/1r04r01/r0r0r0r0r0r0 r'
    endgame_fen = '6/8/8/4b03/6r01/8/8/6 b'
    PIECES = load_pieces()
    board, player = fen_to_board(endgame_fen)
    running = True
    clock = pg.time.Clock() 

    while running:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        if not game_over(board, player):
            move = random_move(board_to_fen(board, player))
            if move is not None:
                board, player = generate_new_board(board, player, move)
                #board, player = fen_to_board(endgame_fen)
        
        window.fill((0, 0, 0))
        draw_board(BOARD, window)
        draw_pieces(board, window, PIECES)
        pg.display.flip()

    pg.quit()