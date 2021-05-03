from board import BattleShipBoard
from ship import Ship


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
        self.new_ships_set()  # Deploy ships on board

    def new_ships_set(self):
        """ Create all ships and add to board """

        with open("ships.txt", "r") as file:
            for line in file:
                size, text_cords, direction = line.strip().split(" ")
                self.__create_ship(int(size), text_cords, direction)

    def __create_ship(self, size, text_cords, direction):
        """ Method to create single ship with size 'size' """
        
        y, x = text_to_cords(text_cords)
        new_ship = Ship(size, y, x, direction)
        self.ships.append(new_ship)
        self.board.add_ship(new_ship)

    def show_boards(self):
        """ Print main player's board and board to shot """

        self.board.render_board()
        print("--------------------------------")
        self.board_to_shots.render_board()

    def shot(self):
        """ Shot to second player """

        y, x = text_to_cords(input("Podaj pozycję: "))
        self.board_to_shots.change_field(y, x, BattleShipBoard.MISSED)