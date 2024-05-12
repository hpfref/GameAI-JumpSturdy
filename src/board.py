import pygame as pg
import numpy as np

def board_to_fen(board, player):
    """Translates our internal board representation from a 2D-numpy array into the official FEN notation

    Args:
        board: [description]
        player: [description]

    Returns:
        fen: [description]
    """
    fen = ''
    special_fields = [(0, 0), (0, 7), (7, 0), (7, 7)]
    for y in range(7, -1, -1):
        empty_count = 0
        row_fen = ''
        for x in range(8):
            if (x, y) in special_fields:
                continue
            piece = board[y, x]
            if piece == "":
                empty_count += 1
            else:
                if empty_count > 0:
                    row_fen += str(empty_count)
                    empty_count = 0
                if piece == 'b':
                    row_fen += 'b0'
                elif piece == 'r':
                    row_fen += 'r0'
                else:
                    row_fen += piece
        if empty_count > 0:
            row_fen += str(empty_count)
        fen += row_fen
        if y != 0:
            fen += '/'
    fen += ' ' + player
    return fen

def fen_to_board(fen):
    """Translates the official FEN notation into our internal board representation (2D-numpy array)

    Args:
        fen: [description]

    Returns:
        board: [description]
        player: [description]
    """
    board = np.empty((8, 8), dtype='U10')
    special_fields = [(0, 0), (0, 7), (7, 0), (7, 7)]
    for field in special_fields:
        board[field[1], field[0]] = "X"

    x, y = 0, 7
    position, player = fen.split()
    i = 0
    while i < len(position):
        if (x, y) in special_fields:
            x += 1
            continue

        char = position[i]

        if char.isalpha():
            if i + 1 < len(position):
                next_char = position[i + 1]
                if char == next_char:
                    piece = char + next_char
                    board[y, x] = piece
                    i += 1
                elif (char == 'r' and next_char == '0') or (char == 'b' and next_char == '0'):
                    piece = 'r' if char == 'r' else 'b'
                    board[y, x] = piece
                    i += 1
                elif (char == 'r' and next_char == 'b') or (char == 'b' and next_char == 'r'):
                    piece = 'rb' if char == 'r' else 'br'
                    board[y, x] = piece
                    i += 1
            else:
                board[y, x] = char
            x += 1

        elif char.isdigit():
            x += int(char)
        elif char == '/':
            y -= 1
            x = 0
        i += 1
    return board, player

if __name__ == "__main__":

    # THIS PART IS FOR VISUAL REPRESENTATION OF FEN's AND DOESN'T HAVE ANY FUNCTIONALITY FOR OUR GAME AI
    # inspired by: ... github repo ergänzen ig

    def sq2xy(sq):
        return sq[0]*SQUARE, sq[1]*SQUARE

    def xy2sq(xy):
        return xy[0] // SQUARE, xy[1] // SQUARE

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

    def draw_board(board):
        for y in range(8):
            for x in range(8):
                color = '#DFBF93' if (x + y) % 2 == 0 else '#C5844E'
                if board[y, x] == "X":
                    color = (0, 0, 0)
                pg.draw.rect(window, color, (*sq2xy((x, y)), SQUARE, SQUARE))

    def draw_pieces(board):
        for y in range(8):
            for x in range(8):
                piece = board[y, x]
                if piece == "X":
                    continue
                if piece:
                    window.blit(PIECES[piece], sq2xy((x, y)))

    pg.init()
    size = width, height = 800, 800
    SQUARE = width // 8
    FPS = 40
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
    
    fen_o_early="b0b02b0b0/1b01bb0b0b01/2b05/3b04/2r05/3r0r03/1r0r02r0r01/r0r01r0r0r0 r"
    fen_o_late="6/1bb1b02b01/8/2r05/3r01b02/5r0r02/2rr1r03/6 b"
    fen_i_early = "b0b0b02bb/1b01b0bb1b01/2b05/5b02/1r06/8/2r0rrr0rr1r0/r0r01r01r0 r"
    fen_u_early = "bb1b0b0b0b0/b01b0b0b01b01/8/3b04/3r04/2r05/1rr2r0r01r0/1r0r0r0r0r0 r"
    fen_test = '1b0b01b0b0/3b0b03/1b03b02/2b01b03/4r0r0b01/4r01r01/1rr1rr4/1r0r01r01 b'

    PIECES = load_pieces()
    board, player = fen_to_board(fen_test)
    fen_transformed_back = board_to_fen(board, player)
    print(board)
    print(fen_transformed_back)
    running = True
    clock = pg.time.Clock()
    drag = None

    while running:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN and not drag:
                from_sq = xy2sq(pg.mouse.get_pos())
                if board[from_sq[1], from_sq[0]]:
                    piece = board[from_sq[1], from_sq[0]]
                    drag = PIECES[piece]
                    board[from_sq[1], from_sq[0]] = ''
            elif event.type == pg.MOUSEBUTTONUP and drag:
                to_sq = xy2sq(pg.mouse.get_pos())
                board[to_sq[1], to_sq[0]] = piece
                drag = None

        window.fill((0, 0, 0))
        draw_board(BOARD)
        draw_pieces(board)
        if drag:
            rect = drag.get_rect(center=pg.mouse.get_pos())
            window.blit(drag, rect)
        pg.display.flip()

    pg.quit()
