import socket
import threading
import config  # Import the configuration file

class Lobby:
    def __init__(self, lobby_name, max_players):
        self.lobby_name = lobby_name
        self.players = []
        self.max_players = max_players
        self.ready_players = 0
        self.started = False

    def add_player(self, player_name):
        if len(self.players) < self.max_players:
            self.players.append(player_name)
            return True
        return False

    def set_ready(self):
        self.ready_players += 1
        if self.ready_players == len(self.players):
            self.start_game()

    def start_game(self):
        self.started = True
        return "Game Starting!"

class Server:
    def __init__(self):
        self.host = config.SERVER_IP  # Use the configuration from config.py
        self.port = config.SERVER_PORT
        self.lobbies = []
        self.clients = []
        self.max_players = config.MAX_PLAYERS

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

    def handle_client(self, client_socket, client_address):
        client_socket.sendall("Welcome to the Lobby Server!\n".encode())
        
        while True:
            lobby_list = [lobby.lobby_name for lobby in self.lobbies]
            client_socket.sendall(f"Available lobbies: {lobby_list}\n".encode())
            client_socket.sendall("Do you want to join a lobby or create a new one? (join/create): ".encode())
            choice = client_socket.recv(1024).decode().strip()

            if choice == "create":
                client_socket.sendall("Enter a name for the new lobby: ".encode())
                lobby_name = client_socket.recv(1024).decode().strip()
                new_lobby = Lobby(lobby_name, self.max_players)
                self.lobbies.append(new_lobby)
                client_socket.sendall(f"Lobby {lobby_name} created. Waiting for players...\n".encode())
                break
            elif choice == "join":
                client_socket.sendall("Enter the name of the lobby to join: ".encode())
                lobby_name = client_socket.recv(1024).decode().strip()
                lobby = next((l for l in self.lobbies if l.lobby_name == lobby_name), None)
                if lobby:
                    if lobby.add_player(client_address[0]):
                        client_socket.sendall(f"Joined lobby {lobby_name}. Waiting for players...\n".encode())
                        break
                    else:
                        client_socket.sendall("Lobby is full, try another one.\n".encode())
                else:
                    client_socket.sendall("Lobby not found.\n".encode())

        while not lobby.started:
            client_socket.sendall(f"Lobby {lobby_name}: {len(lobby.players)}/{lobby.max_players} players ready.\n".encode())
            client_socket.sendall("Enter your name or code name: ".encode())
            player_name = client_socket.recv(1024).decode().strip()
            client_socket.sendall("Press Ready to start the game: ".encode())
            ready = client_socket.recv(1024).decode().strip()

            if ready.lower() == "ready":
                lobby.set_ready()
                if lobby.started:
                    client_socket.sendall("All players are ready. The game is starting!\n".encode())
                    break

    def start(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection established with {client_address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()

if __name__ == "__main__":
    server = Server()
    server.start()
