class Ship():
    """ BattleShip ship class """

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
        self.direction = direction
        self.__create_ship()
    
    def __create_ship(self):
        """ Generate ship and add save ship's cords """

        if self.size == 1:
            self.parts.append([self.startY, self.startX])
        else:
            d = self.DIRS[self.direction]
            for i in range(self.size):
                self.parts.append([self.startY, self.startX])
                self.startY += d[0]
                self.startX += d[1]

    def is_my_cords(self, y, x):
        """ Method to check if cords belong to ship """

        for p in self.parts:
            if p == [y, x]:
                return True
        
        return False
