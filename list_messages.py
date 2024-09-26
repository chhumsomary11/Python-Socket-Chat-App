import socket

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"

def connect():
    """ Establish a connection to the server """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    return client

def start():
    """ Start listening for incoming messages """
    connection = connect()
    while True:
        try:
            msg = connection.recv(1024).decode(FORMAT)
            if msg:
                print(msg)
        except:
            print("Connection closed.")
            break

start()
