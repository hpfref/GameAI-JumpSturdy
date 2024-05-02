import pygame as pg
import zuggenerator as gen

def sz2xy(sz):
  return sz[0]*FELD, sz[1]*FELD
def xy2sz(xy):
  return xy[0]//FELD, xy[1]//FELD

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
FPS = 40
fenster = pg.display.set_mode(größe)
BRETT = {(s, z): s % 2 == z % 2 for s in range(8) for z in range(8) if (s, z) != (0, 0) and (s, z) != (0, 7) and (s, z) != (7, 0) and (s, z) != (7, 7)}
fen = 'b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0 b'
fen1 = '3b02/2b2b02/5b0b1/2r0b04/2b3b01/1r1r2r0r0/5r02/2r3 b'
FIGUREN = ladeFiguren()
position, zugrecht = fen2position(fen)
print(position)
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
      if von in position:
        fig = position[von]
        drag = FIGUREN[fig]
        del position[von]
    elif ereignis.type == pg.MOUSEBUTTONUP and drag:
      zu = xy2sz(pg.mouse.get_pos())
      position[zu] = fig
      drag = None

  fenster.fill((0, 0, 0))
  zeichneBrett(BRETT)
  zeichneFiguren(position)
  if drag:
    rect = drag.get_rect(center=pg.mouse.get_pos())
    fenster.blit(drag, rect)
  pg.display.flip()

pg.quit()