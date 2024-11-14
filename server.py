import socket
import threading

class Lobby:
    def __init__(self, lobby_name):
        self.lobby_name = lobby_name
        self.players = []
        self.max_players = 4
        self.ready_players = 0

    def add_player(self, player_name):
        if len(self.players) < self.max_players:
            self.players.append(player_name)
            return True
        return False

    def remove_player(self, player_name):
        if player_name in self.players:
            self.players.remove(player_name)

    def set_ready(self, player_name):
        if player_name in self.players:
            self.ready_players += 1

    def is_full(self):
        return len(self.players) >= self.max_players

    def is_ready(self):
        return self.ready_players == len(self.players)

    def get_players(self):
        return self.players

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
        # Handle client interaction
        player_name = client_socket.recv(1024).decode()
        print(f"Player {player_name} connected from {client_address}")
        
        self.clients[client_address] = player_name

        # Send list of available lobbies
        available_lobbies = ",".join([lobby.lobby_name for lobby in self.lobbies])
        client_socket.sendall(available_lobbies.encode())

        while True:
            try:
                # Receive the client's request (join or create)
                request = client_socket.recv(1024).decode()
                if request.startswith("create"):
                    lobby_name = request.split(" ")[1]
                    new_lobby = Lobby(lobby_name)
                    self.lobbies.append(new_lobby)
                    print(f"New lobby created: {lobby_name}")
                    client_socket.sendall(f"Lobby {lobby_name} created.".encode())
                    self.broadcast_lobbies()  # Update all clients with the new lobby
                    break
                elif request.startswith("join"):
                    lobby_name = request.split(" ")[1]
                    lobby = next((l for l in self.lobbies if l.lobby_name == lobby_name), None)
                    if lobby and not lobby.is_full():
                        lobby.add_player(player_name)
                        print(f"Player {player_name} joined lobby {lobby_name}")
                        client_socket.sendall(f"Joined lobby {lobby_name}".encode())
                        self.broadcast_lobbies()  # Update all clients with the new player in the lobby
                        break
                elif request.startswith("ready"):
                    lobby_name = request.split(" ")[1]
                    lobby = next((l for l in self.lobbies if l.lobby_name == lobby_name), None)
                    if lobby:
                        lobby.set_ready(player_name)
                        print(f"Player {player_name} is ready in lobby {lobby_name}")
                        if lobby.is_ready():
                            client_socket.sendall("All players are ready. Starting game!".encode())
            except Exception as e:
                print(f"Error: {e}")
                break

    def broadcast_lobbies(self):
        # Broadcast the updated lobby list to all connected clients
        available_lobbies = ",".join([lobby.lobby_name for lobby in self.lobbies])
        for client_socket in self.clients.values():
            try:
                client_socket.sendall(available_lobbies.encode())
            except Exception as e:
                print(f"Error broadcasting to client: {e}")

    def start(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()

if __name__ == "__main__":
    server = Server("0.0.0.0", 5000)
    server.start()
