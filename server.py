import socket
import threading
import time

class Lobby:
    def __init__(self, lobby_name):
        self.lobby_name = lobby_name
        self.players = []
        self.max_players = 4

    def add_player(self, player_name):
        if len(self.players) < self.max_players:
            self.players.append(player_name)
            return True
        return False

    def remove_player(self, player_name):
        if player_name in self.players:
            self.players.remove(player_name)

    def is_empty(self):
        return len(self.players) == 0

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.lobbies = []
        self.clients = {}

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

    def handle_client(self, client_socket, client_address):
        player_name = client_socket.recv(1024).decode()
        print(f"{player_name} connected from {client_address}")
        self.clients[client_address] = player_name

        try:
            while True:
                # Send the list of available lobbies
                lobby_list = ",".join([lobby.lobby_name for lobby in self.lobbies if not lobby.is_empty()])
                client_socket.sendall(lobby_list.encode())

                # Wait for the client to either create or join a lobby
                request = client_socket.recv(1024).decode()
                if request.startswith("create"):
                    lobby_name = request.split(" ")[1]
                    new_lobby = Lobby(lobby_name)
                    self.lobbies.append(new_lobby)
                    client_socket.sendall(f"Created lobby {lobby_name}".encode())
                elif request.startswith("join"):
                    lobby_name = request.split(" ")[1]
                    lobby = next((l for l in self.lobbies if l.lobby_name == lobby_name), None)
                    if lobby and lobby.add_player(player_name):
                        client_socket.sendall(f"Joined lobby {lobby_name}".encode())
                    else:
                        client_socket.sendall("Lobby is full or doesn't exist.".encode())

                # Remove empty lobbies
                self.lobbies = [lobby for lobby in self.lobbies if not lobby.is_empty()]

        except ConnectionResetError:
            print(f"Connection lost with {client_address}")
        finally:
            del self.clients[client_address]
            for lobby in self.lobbies:
                lobby.remove_player(player_name)

    def start(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()

if __name__ == "__main__":
    server = Server("0.0.0.0", 5000)
    server.start()
