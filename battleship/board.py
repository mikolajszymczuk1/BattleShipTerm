# BattleShip board class

class BattleShipBoard():
    ROWS = "ABCDEFGHIJ"

    def __init__(self):
        self.board = self.create_board()
        self.render_board()

    def create_board(self):
        """ Method to generate game board """
        
        b = []
        for y in range(10):
            col = []
            for x in range(10):
                col.append("[ ]")
            
            b.append(col)
        
        return b
    
    def render_board(self):
        """ Print board method """

        print("   1  2  3  4  5  6  7  8  9  10")
        for y in range(10):
            print(self.ROWS[y], "", end="")
            for x in range(10):
                print(self.board[y][x], end="")
            
            print("")
