
class Surface():
    def __init__(self, pygame, map, height, width):
        self.map = map
        self.mapHeight = height
        self.screenHeight = self.mapHeight
        self.screenWidth = width
        self.surface = pygame.display.set_mode((int(self.screenWidth), int(self.screenHeight)), 0, 32)

    def get_width(self):
        return self.screenWidth

    def get_height(self):
        return self.mapHeight

    def get_rect(self):
        return  self.surface.get_rect()

    def get_surface(self):
        return self.surface

    def blit(self, source, dest=None, area=None, special_flags = 0):
        if dest is None:
            dest = (0, 0)
        self.surface.blit(source, dest , area, special_flags)

    def fill(self, color, rect=None, special_flags=0):
        self.surface.fill(color, rect, special_flags)