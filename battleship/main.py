from board import BattleShipBoard
from ship import Ship


def text_to_cords(text_cords):
    ROWS = "ABCDEFGHIJ"
    y = ROWS.index(text_cords[0])
    x = int(text_cords[1:]) - 1
    return y, x


class BattleShip():
    """ BattleShip game class """

    pass
