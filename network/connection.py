# network/connection.py
import socket
import threading
from config.config import SERVER_IP, SERVER_PORT

class Connection:
    def __init__(self, host=True):
        self.host = host
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        if self.host:
            self.sock.bind((SERVER_IP, SERVER_PORT))
            self.sock.listen(5)
            print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")
        else:
            self.sock.connect((SERVER_IP, SERVER_PORT))
            print("Connected to server")

    def accept_client(self):
        client_socket, client_address = self.sock.accept()
        return client_socket, client_address

    def send_message(self, message):
        self.sock.sendall(message.encode())

    def receive_message(self):
        return self.sock.recv(1024).decode()

    def close_connection(self):
        self.sock.close()
