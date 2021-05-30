class BattleShipBoard():
    """ BattleShip board class """
    
    __ROWS = "ABCDEFGHIJ"
    EMPTY = "[ ]"
    BUSY = "[O]"
    HIT = "[X]"
    MISSED = "[*]"

    def __init__(self):
        self.__board = self.create_board()
        # self.render_board()

    def create_board(self):
        """ Method to generate game board """
        
        b = []
        for y in range(10):
            col = []
            for x in range(10):
                col.append(self.EMPTY)
            
            b.append(col)
        
        return b
    
    def render_board(self):
        """ Print board method """

        print("   1  2  3  4  5  6  7  8  9  10")
        for y in range(10):
            print(self.__ROWS[y], "", end="")
            for x in range(10):
                print(self.__board[y][x], end="")
            
            print("")
    
    def add_ship(self, ship):
        """ Method add ship's cords to board """

        for cord in ship.parts:
            self.__board[cord[0]][cord[1]] = self.BUSY

    def change_field(self, y, x, shot_type):
        self.__board[y][x] = shot_type

    def are_all_ships_destoryed(self, ships):
        """ Return True if all ships on board are destroyed """

        for ship in ships:
            for p in ship.parts:
                y, x = p
                if self.__board[y][x] != self.HIT:
                    return False

        return True


if __name__ == '__main__':
    print("...")
