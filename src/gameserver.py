import pygame as pg
import numpy as np
import random
from board import board_to_fen, fen_to_board
from zuggenerator import legal_moves

class gameserver:
    def __init__(self, fen):
        self.board, self.player = fen_to_board(fen)
        self.fen = fen
        self.running = True

    def switch_player(self):
        self.player = 'r' if self.player == 'b' else 'b'
        self.fen = board_to_fen(self.board, self.player)

    def make_move(self, move):
        start, end = move
        start_piece = self.board[start[0], start[1]]
        end_piece = self.board[end[0], end[1]]

        if end_piece != '':
            # towers
            if start_piece[0] == end_piece[0]:  # one color tower
                new_piece = start_piece[0] * 2
            else:  # different colors
                new_piece = ''.join(sorted(start_piece[0] + end_piece[0]))

            self.board[end[0], end[1]] = new_piece
        else:
            self.board[end[0], end[1]] = start_piece

        self.board[start[0], start[1]] = ''

        self.switch_player()

    def check_game_over(self):
        for x in range(8):
            if self.board[0, x] == 'b' or self.board[0, x] == 'bb':  # Red reaches the opposite side
                print("Blue wins!")
                self.running = False
            if self.board[7, x] == 'r' or self.board[7, x] == 'rr':  # Blue reaches the opposite side
                print("Red wins!")
                self.running = False

    def play_game(self):
        pg.init()
        size = width, height = 800, 800
        SQUARE = width // 8
        window = pg.display.set_mode(size)
        clock = pg.time.Clock()
        FPS = 40

        def sq2xy(sq):
            return sq[0] * SQUARE, sq[1] * SQUARE

        def draw_board():
            for y in range(8):
                for x in range(8):
                    color = '#DFBF93' if (x + y) % 2 == 0 else '#C5844E'
                    if self.board[y, x] == "X":
                        color = (0, 0, 0)
                    pg.draw.rect(window, color, (*sq2xy((x, y)), SQUARE, SQUARE))

        def load_pieces():
            images = {}
            piece_to_file = {
                'r': 'redpawn', 'b': 'bluepawn', 'rr': 'redtower', 'bb': 'bluetower',
                'br': 'redonblue', 'rb': 'blueonred'
            }
            for piece, filename in piece_to_file.items():
                image = pg.image.load(f'graphics/{filename}.png')
                images[piece] = pg.transform.smoothscale(image, (SQUARE, SQUARE))
            return images

        def draw_pieces():
            for y in range(8):
                for x in range(8):
                    piece = self.board[y, x]
                    if piece == "X":
                        continue
                    if piece:
                        window.blit(PIECES[piece], sq2xy((x, y)))

        PIECES = load_pieces()

        while self.running:
            clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

            # Generate and make a move for the current player
            moves = legal_moves(self.fen)
            if not moves:
                print(f"Player {self.player} has no legal moves. Game over.")
                self.running = False
            else:
                move = random.choice(moves)  # Choose a random legal move
                self.make_move(move)

            self.check_game_over()

            window.fill((0, 0, 0))
            draw_board()
            draw_pieces()
            pg.display.flip()

        pg.quit()

if __name__ == "__main__":
    fen_start = 'b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0 b'
    game_server = gameserver(fen_start)
    game_server.play_game()
