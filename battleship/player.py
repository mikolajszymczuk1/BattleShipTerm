import os
import socket
import sys
from .board import BattleShipBoard
from .ship import Ship

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
SHIPS_TEMPLATE = os.path.join(THIS_FOLDER, "ships.txt")

def text_to_cords(text_cords):
    ROWS = "ABCDEFGHIJ"
    y = ROWS.index(text_cords[0])
    x = int(text_cords[1:]) - 1
    return y, x

class BattleShipPlayer():
    """ BattleShip player class """

    def __init__(self, hostname="localhost", port=6060):
        self.board = BattleShipBoard()
        self.board_to_shots = BattleShipBoard()
        self.ships = []
        self.hostname = hostname
        self.port = port
        self.current = False
        self.new_ships_set()  # Deploy ships on board
        self.client = self.connect_to_server()  # Set up connection

    def connect_to_server(self):
        """ Connect to server and run main player loop """

        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.hostname, self.port))
            return client
        except Exception as e:
            print("Can't connect to server: ", e)
            sys.exit()

    def player_loop(self):
        """ Main player loop """
        
        while True:
            if not self.current:
                msg = self.client.recv(1024)
                if msg.decode("utf-8") == "current":
                    self.current = True
                    continue
            
                print("Enemy shot: ", msg.decode('utf8')[1:])  # Catch shot
                self.client.send("CMISSED".encode("utf-8"))  # Check shot
            else:
                shot_msg = input("Your shot: ")
                self.client.send(("S" + shot_msg).encode("utf-8"))  # Send shot
                
                # Catch check
                check_msg = self.client.recv(1024)
                print("Check from enemy: ", check_msg.decode('utf-8')[1:])
                self.current = False  # Turn off player

    def new_ships_set(self):
        """ Create all ships and add to board """

        with open(SHIPS_TEMPLATE, "r") as file:
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


if __name__ == '__main__':
    print("...")
