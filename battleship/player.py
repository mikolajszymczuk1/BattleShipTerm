import os
import socket
import sys
from .board import BattleShipBoard
from .ship import Ship

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
SHIPS_TEMPLATE = os.path.join(THIS_FOLDER, "ships.txt")

def text_to_cords(text_cords):
    """ Function to convert cords from example: A5 to: y=0, x=4 """

    ROWS = "ABCDEFGHIJ"
    y = ROWS.index(text_cords[0])
    x = int(text_cords[1:]) - 1
    return y, x

def text_to_field_type(t):
    """ Function return shot type depending on t """

    if t == "MISS":
        return BattleShipBoard.MISSED
    
    return BattleShipBoard.HIT

def clear():
    """ Clear function to clear terminal """

    os.system("clear")

class BattleShipPlayer():
    """ BattleShip player class """

    def __init__(self, hostname="localhost", port=6060):
        self.board = BattleShipBoard()
        self.board_to_shots = BattleShipBoard()
        self.ships = []
        self.hostname = hostname
        self.port = port
        self.current = False
        self.last_shot = None
        self.new_ships_set()  # Deploy ships on board
        self.client = self.connect_to_server()  # Set up connection
        clear()

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
                else:
                    clear()
                    self.check_shot(msg.decode("utf-8")[1:])  # Check shot
            else:
                self.shot()  # Send shot
                clear()

                check_msg = self.client.recv(1024)
                self.update_board_to_shots(check_msg.decode("utf-8")[1:], self.last_shot)  # Catch check

    def check_shot(self, cords):
        """ Check if shot from second player is missed or hit and 
        send information about it to second player """
        
        y, x = text_to_cords(cords)
        output = "MISS"

        for ship in self.ships:
            if ship.is_my_cords(y, x):
                output = "HIT"
                break
        
        self.board.change_field(y, x, text_to_field_type(output))
        self.show_boards()
        print("Enemy shot: ", cords)

        # if all ships are destroyed, disconnect
        if self.board.are_all_ships_destoryed(self.ships):
            output = "WIN"
            print("You lose :(")
            self.client.send(f"C{output}".encode("utf-8"))
            self.client.close()
            sys.exit()

        self.client.send(f"C{output}".encode("utf-8"))

    def update_board_to_shots(self, check_msg, last_shot):
        """ Add shot to board to shots """
        
        y, x = text_to_cords(last_shot)
        self.board_to_shots.change_field(y, x, text_to_field_type(check_msg))
        self.show_boards()
        print("Check from enemy: ", check_msg)
        self.current = False  # Turn off player

        # if player gets win message, disconnect
        if check_msg == "WIN":
            print("You Win !!!")
            self.client.close()
            sys.exit()

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

        SHOTS_ROWS = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J")
        SHOTS_COLS = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10")

        shot_msg = ""
        while True:
            shot_msg = input("Your shot: ")
            if len(shot_msg) and shot_msg[0] in SHOTS_ROWS and shot_msg[1:] in SHOTS_COLS:
                break
        
        self.last_shot = shot_msg
        self.client.send(("S" + shot_msg).encode("utf-8"))  # Send shot


if __name__ == '__main__':
    print("...")
