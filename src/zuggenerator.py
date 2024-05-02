import pygame as pg

def sz2xy(sz):
  return sz[0]*FELD, sz[1]*FELD


def zeichneBrett(BRETT):
  for sz, feld in BRETT.items():
    farbe = '#DFBF93' if feld else '#C5844E'
    pg.draw.rect(fenster, farbe, (*sz2xy(sz), FELD, FELD))

def fen2position(fen):
  position, s, z = {}, 0, 7
  figurenstellung, zugrecht = fen.split()
  for char in figurenstellung:
    if (s, z) in [(0, 0), (0, 7), (7, 0), (7, 7)]: 
        s += 1  
    if char.isalpha(): #hier fehlt noch case/übersetzung für knights
        position[(s, z)] = char
        s += 1
    elif char.isnumeric():
        s += int(char)
    else:
        s, z = 0, z-1
  return position, zugrecht

def ladeFiguren():
  bilder = {}
  fig2datei = dict(r='redpawn', b='bluepawn') #grafik für knights fehlt noch
  for fig, datei in fig2datei.items():
    bild = pg.image.load(f'GameAI-JumpSturdy\graphics/{datei}.png')
    bilder[fig] = pg.transform.smoothscale(bild, (FELD, FELD))
  return bilder

def zeichneFiguren(p):
  for sz, fig in p.items():
    fenster.blit(FIGUREN[fig], sz2xy(sz))

pg.init()
größe = breite, höhe = 800, 800
FELD = breite // 8
fenster = pg.display.set_mode(größe)
BRETT = {(s, z): s % 2 == z % 2 for s in range(8) for z in range(8) if (s, z) != (0, 0) and (s, z) != (0, 7) and (s, z) != (7, 0) and (s, z) != (7, 7)}
fen = 'b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0 b'
fen1 = '3b02/2b2b02/5b0b1/2r0b04/2b3b01/1r1r2r0r0/5r02/2r3 b'
FIGUREN = ladeFiguren()
position, zurecht = fen2position(fen1)
print(position)


clock = pg.time.Clock()
FPS = 40

while True:
  clock.tick(FPS)
  fenster.fill('black')
  zeichneBrett(BRETT)
  zeichneFiguren(position)
  
  for ereignis in pg.event.get():
    if ereignis.type == pg.QUIT or ereignis.type == pg.KEYDOWN and ereignis.key == pg.K_ESCAPE: quit()
  
  pg.display.flip()




def legal_moves_board(fen) -> list:
    """Return all legal moves for the current player

    Args:
        fen: board & player

    Returns:
        list: legal moves e.g. B1-B2, ...
    """
    board, player = fen.split(" ")
    moves = []
    



    return moves


def legal_moves_piece(fen, piece) -> list:
    """Return all legal moves of a single piece

    Args:
        fen: board & player
        piece: position of piece to move

    Returns:
        list: legal moves e.g. B1-B2, ...
    """
    board, player = fen.split(" ")
    moves = []
    



    return moves