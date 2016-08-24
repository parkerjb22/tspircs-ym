import pygame


class Tools():
    def __init__(self, dir):
        self.dir = dir

    def getImage(self, name):
        img = pygame.image.load(self.dir + name + ".png")
        return pygame.transform.scale2x(img)