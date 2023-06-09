import socket
from  threading import Thread
import time, random

SERVER = None
IP_ADDRESS = '127.0.0.1'
PORT = 8080

CLIENTS = {}

playersJoined = False

def handleClient():
    global CLIENTS
    global playersJoined

    while True:
        try:
            if(len(list(CLIENTS.keys())) >=2):
                if(not playersJoined):
                    playersJoined = True
                    time.sleep(1)
        except:
            pass



def recvMessage():
    pass



def acceptConnections():
    global CLIENTS
    global SERVER

    while True:
        player_socket, addr = SERVER.accept()
        player_name = player_socket.recv(1024).decode().strip()

        CLIENTS[player_name] = {}
        CLIENTS[player_name]["player_socket"] = player_socket
        CLIENTS[player_name]["address"] = addr
        CLIENTS[player_name]["player_name"] = player_name

        print(f"Connection established with {player_name} : {addr}")

        thread1 = Thread(target = recvMessage, args=(player_socket,))
        thread1.start()



def setup():
    print("\n\t\t\t\t\t*** Welcome To Tambola Game ***\n")

    global SERVER
    global PORT
    global IP_ADDRESS


    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))

    SERVER.listen(10)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...\n")

    thread = Thread(target = handleClient, args=())
    thread.start()


    acceptConnections()


setup()
