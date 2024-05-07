import pygame as pg
import numpy as np

def board_to_fen(board, zugrecht):
    fen = ''
    special_fields = [(0, 0), (0, 7), (7, 0), (7, 7)]
    for z in range(7, -1, -1):
        empty_count = 0
        row_fen = ''
        for s in range(8):
            if (s, z) in special_fields:
                continue  
            piece = board[z, s]
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
        if z != 0:
            fen += '/'
    fen += ' ' + zugrecht
    return fen

def fen_to_board(fen):
    board = np.empty((8, 8), dtype='U10')
    special_fields = [(0, 0), (0, 7), (7, 0), (7, 7)]
    for field in special_fields:
        board[field[1], field[0]] = "X"

    s, z = 0, 7
    figurenstellung, zugrecht = fen.split()
    i = 0
    while i < len(figurenstellung):
        if (s, z) in special_fields:
            s += 1  
            continue

        char = figurenstellung[i]

        if char.isalpha():
            if i + 1 < len(figurenstellung):
                next_char = figurenstellung[i + 1]
                if char == next_char:
                    piece = char + next_char
                    board[z, s] = piece
                    i += 1
                elif (char == 'r' and next_char == '0') or (char == 'b' and next_char == '0'):
                    piece = 'r' if char == 'r' else 'b'
                    board[z, s] = piece
                    i += 1
                elif (char == 'r' and next_char == 'b') or (char == 'b' and next_char == 'r'):
                    piece = 'rb' if char == 'r' else 'br'
                    board[z, s] = piece
                    i += 1
            else:
                board[z, s] = char
            s += 1

        elif char.isdigit():
            s += int(char)
        elif char == '/':
            z -= 1
            s = 0
        i += 1
    return board, zugrecht



if __name__ == "__main__": # only considered if executed as script

    def sz2xy(sz):
        return sz[0]*FELD, sz[1]*FELD

    def xy2sz(xy):
        return xy[0] // FELD, xy[1] // FELD

    def ladeFiguren():
        bilder = {}
        fig2datei = {
            'r': 'redpawn', 'b': 'bluepawn', 'rr': 'redtower', 'bb': 'bluetower',
            'br': 'rotaufblau', 'rb': 'blauaufrot'
        }
        for fig, datei in fig2datei.items():
            bild = pg.image.load(f'graphics/{datei}.png')
            bilder[fig] = pg.transform.smoothscale(bild, (FELD, FELD))
        return bilder

    def zeichneBrett(board):
        for z in range(8):
            for s in range(8):
                farbe = '#DFBF93' if (s + z) % 2 == 0 else '#C5844E'
                if board[z, s] == "X":
                    farbe = (0, 0, 0)  
                pg.draw.rect(fenster, farbe, (*sz2xy((s, z)), FELD, FELD))

    def zeichneFiguren(board):
        for z in range(8):
            for s in range(8):
                fig = board[z, s]
                if fig == "X":  
                    continue
                if fig:  
                    fenster.blit(FIGUREN[fig], sz2xy((s, z)))



    pg.init()
    größe = breite, höhe = 800, 800
    FELD = breite // 8
    FPS = 40
    fenster = pg.display.set_mode(größe)
    BRETT = np.full((8, 8), "", dtype='U10')
    for z in range(8):
        for s in range(8):
            if (s, z) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
                BRETT[z, s] = "X"
            else:
                BRETT[z, s] = ""
    fen = 'b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0 b'
    fen1 = '3b02/2bb2b02/5b0bb1/2r0b04/2rb3b01/1rr1rr2r0r0/5r02/2rr3 b'
    fen2 = "b0b0b01bb1/2b0b0bbb02/5r02/3b04/4r0b02/8/2rrr01r02/r0r0r0r01r0 r"
    fen3 = "6/1bb1b02b01/8/2r05/3r01b02/5r0r02/2rr1r03/6 b"
    
    fen_o_early="b0b02b0b0/1b01bb0b0b01/2b05/3b04/2r05/3r0r03/1r0r02r0r01/r0r01r0r0r0 r"
    fen_o_late="6/1bb1b02b01/8/2r05/3r01b02/5r0r02/2rr1r03/6 b"
    fen_i_early = "b0b0b02bb/1b01b0bb1b01/2b05/5b02/1r06/8/2r0rrr0rr1r0/r0r01r01r0 r"
    fen_u_early = "bb1b0b0b0b0/b01b0b0b01b01/8/3b04/3r04/2r05/1rr2r0r01r0/1r0r0r0r0r0 r"
    fen_test = '1b0b01b0b0/3b0b03/1b03b02/2b01b03/4r0r0b01/4r01r01/1rr1rr4/1r0r01r01 b'

    FIGUREN = ladeFiguren()
    board, zugrecht = fen_to_board(fen_test)
    fen_transformed_back = board_to_fen(board, zugrecht)
    print(board)
    print(fen_transformed_back)
    weitermachen = True
    clock = pg.time.Clock()
    drag = None

    while weitermachen:
        clock.tick(FPS)
        for ereignis in pg.event.get():
            if ereignis.type == pg.QUIT:
                weitermachen = False
            elif ereignis.type == pg.MOUSEBUTTONDOWN and not drag:
                von = xy2sz(pg.mouse.get_pos())
                if board[von[1], von[0]]:  
                    fig = board[von[1], von[0]]
                    drag = FIGUREN[fig]
                    board[von[1], von[0]] = ''  
            elif ereignis.type == pg.MOUSEBUTTONUP and drag:
                zu = xy2sz(pg.mouse.get_pos())
                board[zu[1], zu[0]] = fig  
                drag = None

        fenster.fill((0, 0, 0))
        zeichneBrett(BRETT)
        zeichneFiguren(board)
        if drag:
            rect = drag.get_rect(center=pg.mouse.get_pos())
            fenster.blit(drag, rect)
        pg.display.flip()

    pg.quit()
