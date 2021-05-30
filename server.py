import socket
import threading
import random

HOSTNAME = "localhost"
PORT = 6060

# Players
player1 = None
player2 = None
current_player = None

def who_is_first(p1, p2):
    """ Choice and return first player from players: p1 and p2 """

    if random.randrange(0, 2) == 0:
        return p1

    return p2

def next_player(current, p1, p2):
    """ Change player, return p2 if p1 is current player or return p1 if p2 is current player """

    if current == p1:
        return p2

    return p1

def send_shot(msg, conn):
    if conn == player1:
        player2.send(msg)
    else:
        player1.send(msg)

def send_check(msg, conn):
    if conn == player1:
        player2.send(msg)
        player1.send("current".encode('utf8'))
    else:
        player1.send(msg)
        player2.send("current".encode('utf8'))

def remove_player(conn):
    """ Remove player from players list """

    global player1
    global player2

    if conn == player1:
        player1 = None
    else:
        player2 = None

def handle_player(conn, addr):
    """ Catch and send shots/checks """

    global current_player

    while True:
        message = conn.recv(1024)
        if message:
            if message.decode("utf-8")[0] == "S":
                print("Shot from: ", addr, " -> ", message.decode('utf8')[1:])
                send_shot(message, conn)
            else:
                print("Check from: ", addr, " --> ", message.decode("utf-8")[1:])
                send_check(message, conn)
                current_player = next_player(current_player, player1, player2)
        else:
            print("Disconnect: ", addr)
            remove_player(conn)
            break

def main():
    global player1
    global player2

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOSTNAME, PORT))
    server.listen()

    while True:
        conn, addr = server.accept()
        print("Connected to: ", addr)

        if player1 == None:
            player1 = conn
        else:
            player2 = conn

        if player1 != None and player2 != None:
            current_player = who_is_first(player1, player2)
            current_player.send("current".encode("utf-8"))

        thread = threading.Thread(target=handle_player, args=(conn, addr))
        thread.start()


if __name__ == '__main__':
    main()  # Run server
