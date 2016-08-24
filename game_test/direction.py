class Direction():
    def __init__(self, key, img, walk_img):
        self.key = key
        self.img = img
        self.walk_img = walk_img

    def getKey(self):
        return self.key

    def getImage(self, z = 1):
        return self.img if z % 2 == 1 else self.walk_img

    def setWalkFunc(self, walk_func):
        self.walk_func = walk_func
        return self

    def walk(self, loc):
        return self.walk_func(loc)

    def setMoveFunc(self, move_func):
        self.move_func = move_func
        return self

    def move(self, rect):
        return self.move_func(rect)

    def setMoveScreenFunc(self, move_screen_func):
        self.move_screen_func = move_screen_func
        return self

    def moveScreen(self, imgLoc, screenLoc):
        return self.move_screen_func(imgLoc, screenLoc)