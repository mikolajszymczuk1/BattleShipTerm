from board import BattleShipBoard
from ship import Ship


SHIPS_COUNT = {
    "Czteromasztowiec": {
        "count": 1,
        "size": Ship.LARGE
    },

    "Trojmasztowiec": {
        "count": 2,
        "size": Ship.MEDIUM
    },

    "Dwumasztowiec": {
        "count": 3,
        "size": Ship.SMALL
    },

    "Jednomasztowiec": {
        "count": 4,
        "size": Ship.MINI
    }
}

def text_to_cords(text_cords):
    ROWS = "ABCDEFGHIJ"
    y = ROWS.index(text_cords[0])
    x = int(text_cords[1:]) - 1
    return y, x

class BattleShipPlayer():
    """ BattleShip player class """

    def __init__(self):
        self.board = BattleShipBoard()
        self.board_to_shots = BattleShipBoard()
        self.ships = []

    def new_ships_set(self):
        """ Create all ships and add to board """

        for ship_type in SHIPS_COUNT:
            print(" === ", ship_type, " === ")
            for _ in range(SHIPS_COUNT[ship_type]["count"]):
                self.__create_ship(SHIPS_COUNT[ship_type]["size"])

    def __create_ship(self, size):
        """ Method to create single ship with size 'size' """
        
        y, x = text_to_cords(input("Podaj pozycję początkową: "))
        direction = input("Podaj kierunek: ")
        new_ship = Ship(size, y, x, direction)
        self.ships.append(new_ship)
        self.board.add_ship(new_ship)

    def show_boards(self):
        """ Print main player's board and board to shot """
        
        self.board.render_board()
        print("--------------------------------")
        self.board_to_shots.render_board()

    def shot(self):
        pass