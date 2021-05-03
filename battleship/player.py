from board import BattleShipBoard
from ship import Ship


def text_to_cords(text_cords):
    ROWS = "ABCDEFGHIJ"
    y = ROWS.index(text_cords[0])
    x = int(text_cords[1:]) - 1
    return y, x

class BattleShipPlayer():
    """ BattleShip player class """

    SHIPS_COUNT = {
        "Czteromasztowiec": 1,
        "Trojmasztowiec": 2,
        "Dwumasztowiec": 3,
        "Jednomasztowiec": 4
    }

    def __init__(self):
        self.board = BattleShipBoard()
        self.ships = []

    def new_ships_set(self):
        for ship_type in self.SHIPS_COUNT:
            print(ship_type)

    def create_ship(self, size):
        y, x = text_to_cords(input("Podaj pozycję początkową: "))
        direction = input("Podaj kierunek: ")
        new_ship = Ship(size, y, x, direction)
        self.ships.append(new_ship)
        self.board.add_ship(new_ship)

    def show_board(self):
        self.board.render_board()
