import threading
import socket
import time

# Server setup
PORT = 5050
SERVER = "localhost"  # Localhost for simplicity
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = set()
clients_lock = threading.Lock()

def broadcast(message, _client):
    """ Send a message to all connected clients except the sender """
    with clients_lock:
        for client in clients:
            if client != _client:
                try:
                    client.sendall(message)
                except:
                    client.close()
                    clients.remove(client)

def handle_client(conn, addr):
    """ Handle messages from a single client """
    print(f"[NEW CONNECTION] {addr} connected.")
    try:
        connected = True
        while connected:
            msg = conn.recv(1024).decode(FORMAT)
            if not msg:
                break
            if msg == DISCONNECT_MESSAGE:
                connected = False
            else:
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
                full_message = f"[{timestamp}] {addr}: {msg}"
                print(full_message)
                broadcast(full_message.encode(FORMAT), conn)
    except ConnectionResetError:
        print(f"[ERROR] Connection lost with {addr}")
    finally:
        with clients_lock:
            clients.remove(conn)
        conn.close()

def start():
    """ Start the server to listen for clients """
    print("[SERVER STARTED] Waiting for connections...")
    server.listen()
    while True:
        conn, addr = server.accept()
        with clients_lock:
            clients.add(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
def send_server_messages():
    """ Allow server to send messages to all clients from the terminal """
    while True:
        msg = input("Server: ")  # Get input from server terminal
        if msg.lower() == "exit":  # Type 'exit' to stop the server
            break
        broadcast(f"[SERVER]: {msg}".encode(FORMAT), None)  # Broadcast to all clients, passing None for _client

# Start server and server message thread
threading.Thread(target=send_server_messages, daemon=True).start()

start()
