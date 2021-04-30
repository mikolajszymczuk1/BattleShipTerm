class Ship():
    """ BattleShip ship class """

    MINI = 1    # *
    SMALL = 2   # **
    MEDIUM = 3  # ***
    LARGE = 4   # ****

    DIRS = {
        #         Y   X
        "left":  [0, -1],
        "right": [0,  1],
        "up":    [-1, 0],
        "down":  [1,  0]
    }

    def __init__(self, size, start_y, start_x, direction=None):
        self.size = size
        self.parts = []
        self.startY = start_y
        self.startX = start_x
        self.create_ship(direction)
    
    def create_ship(self, direction):
        if self.size == 1:
            self.parts.append([self.startY, self.startY])
        else:
            d = self.DIRS[direction]
            for i in range(self.size):
                self.parts.append([self.startY, self.startX])
                self.startY += d[0]
                self.startX += d[1]
