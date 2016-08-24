import pygame, sys, time
from pygame.locals import *
from tools import Tools
from direction import Direction
from surface import Surface

tools = Tools("link")
pygame.init()
pygame.key.set_repeat()

map = tools.getImage("full_map")
windowSurface = Surface(pygame, map, map.get_height() / 8, map.get_width() / 16)

caves = tools.getImage("caves")
sprites = tools.getImage("sprites")
enemies = tools.getImage("sprites")
detailHeight = int(map.get_height() / 8 / 4)
# windowSurface = pygame.display.set_mode((int(map.get_width() / 16), int(map.get_height() / 8)), 0, 32)
pygame.display.set_caption('Totally not Zelda')

BLACK = (0, 0, 0)
BG_COLOR = (252, 216, 168)

UP = [pygame.K_UP, [2, 0], [2, 1], lambda loc : [loc[0], loc[1] - width/4]]
DOWN = [pygame.K_DOWN, [0, 0], [0, 1], lambda loc : [loc[0], loc[1] + width/4]]

tier = 0
width = height = 32
loc = [windowSurface.get_rect().centerx - width/2, windowSurface.get_rect().centery - height/2]

movements = []
dir = Direction(pygame.K_LEFT, [1, 0], [1, 1]).setWalkFunc(lambda loc : [loc[0] - width/4, loc[1]])
dir.setMoveFunc(lambda rect : [rect[0] - width/8, rect[3] - height/4, rect[0] - 1, rect[3]])
dir.setMoveScreenFunc(lambda imgLoc, screenLoc : [windowSurface.get_width() - width, imgLoc[1], screenLoc[0] - windowSurface.get_width(), screenLoc[1]])
movements.append(dir)

dir = Direction(pygame.K_RIGHT, [3, 1], [3, 0]).setWalkFunc(lambda loc : [loc[0] + width/4, loc[1]])
dir.setMoveFunc(lambda rect : [rect[2] + 1, rect[3] - height/4, rect[2] + width/8, rect[3]])
dir.setMoveScreenFunc(lambda imgLoc, screenLoc : [0, imgLoc[1], screenLoc[0] + windowSurface.get_width(), screenLoc[1]])
movements.append(dir)

dir = Direction(pygame.K_UP, [2, 0], [2, 1]).setWalkFunc(lambda loc : [loc[0], loc[1] - width/4])
dir.setMoveFunc(lambda rect : [rect[0], rect[1] - height/8, rect[2], rect[1] - 1])
dir.setMoveScreenFunc(lambda imgLoc, screenLoc : [imgLoc[0], windowSurface.get_height() - height, screenLoc[0], screenLoc[1] - windowSurface.get_height()])
movements.append(dir)

dir = Direction(pygame.K_DOWN, [0, 0], [0, 1]).setWalkFunc(lambda loc : [loc[0], loc[1] + width/4])
dir.setMoveFunc(lambda rect : [rect[0], rect[3] + 1, rect[2], rect[3] + height/8])
dir.setMoveScreenFunc(lambda imgLoc, screenLoc : [imgLoc[0], 0, screenLoc[0], screenLoc[1] + windowSurface.get_height()])
movements.append(dir)

FACE = movements[0].getImage()

def walk(dir):
    global FACE
    global loc

    if FACE != dir.getImage():
        redrawLink(loc, dir.getImage())
        FACE = dir.getImage()
        return

    for z in range(0, 2):

        if not canMove(windowSurface, loc, dir):
           time.sleep(0.025)
           return

        eraseLink(loc)

        loc = dir.walk(loc)
        img = dir.getImage(z)

        drawLink(loc, img)
        pygame.display.update()
        time.sleep(0.05)

def canMove(surface, loc, dir):

    x1, y1 = loc
    x2 = x1 + width
    y2 = y1 + height

    x1, y1, x2, y2 = dir.move([x1, y1, x2, y2])

    if x1 < 0 or y1 < 0 or x2 > surface.get_width() or y2 > surface.get_height():
        moveScreen(loc, dir)
        return False

    pixArray = pygame.PixelArray(surface.get_surface())
    for yCord in range (int(y1), int(y2)):
        for xCord in range (int(x1), int(x2)):
            curr = pixArray[xCord][yCord]
            if curr != 16570536:
                return False

    del pixArray

    return True

def drawScreen(bg_img, bg_area, link_img, link_loc):
    windowSurface.fill(BLACK)
    windowSurface.blit(bg_img, area=(bg_area[0], bg_area[1], windowSurface.get_width(), windowSurface.get_height()))
    drawLink(link_loc, link_img)
    pygame.display.update()

def redrawLink(loc, img):
    eraseLink(loc)
    drawLink(loc, img)
    pygame.display.update()

def drawLink(loc, img):
    windowSurface.blit(sprites, loc, (img[0] * 60 + tier * 240, img[1] * 60, width, height))

def eraseLink(loc):
    pygame.draw.rect(windowSurface.get_surface(), BLACK, (loc[0], loc[1], width, height))
    windowSurface.blit(map, loc, (startX + loc[0], startY + loc[1], width, height))

def cheerLink(loc, img, cheerType):
    eraseLink(loc)
    windowSurface.blit(sprites, loc, (cheerType * 60 + tier * 240, 300, width, height))
    pygame.display.update()
    time.sleep(0.25)
    redrawLink(loc, img)

def moveScreen(location, dir):
    global startX
    global startY
    global loc

    loc[0], loc[1], startX, startY = dir.moveScreen(location, [startX, startY])
    drawScreen(map, (startX, startY), dir.getImage(), loc)

startY = map.get_height() - windowSurface.get_height()
startX = map.get_width()/2 - windowSurface.get_width()
drawScreen(map, (startX, startY), FACE, loc)

direction = None
while True:
    for event in pygame.event.get():
        if event.type == KEYUP:
            direction = None
        elif event.type == KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_0] or keys[pygame.K_KP0]:
                tier = (tier + 1) % 3
                redrawLink(loc, FACE)
            elif keys[pygame.K_a]:
                cheerLink(loc, FACE, 0)
            elif keys[pygame.K_s]:
                cheerLink(loc, FACE, 1)
            elif keys[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            else:
                for dir in movements:
                    if (keys[dir.getKey()]):
                        direction = dir
                        break
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()

    if direction is not None:
        walk(direction)