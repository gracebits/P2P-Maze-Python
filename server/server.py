# server.py
import threading
from network.connection import Connection
from network.message_handler import MessageHandler
from server.lobby_manager import LobbyManager
from server.logger import log_player_activity, log_server_event

class GameServer:
    def __init__(self):
        self.connection = Connection(host=True)
        self.lobby_manager = LobbyManager()

    def handle_new_connection(self, client_socket, client_address):
        player_name = self.connection.receive_message()  # Assuming first message is the player's name
        log_player_activity(player_name, "connected", client_address[0])
        
        message_handler = MessageHandler(self.connection)
        while True:
            message = self.connection.receive_message()
            message_handler.handle_message(message)

    def start(self):
        while True:
            client_socket, client_address = self.connection.accept_client()
            print(f"New connection from {client_address}")
            log_server_event(f"New connection from {client_address}")
            threading.Thread(target=self.handle_new_connection, args=(client_socket, client_address)).start()

if __name__ == "__main__":
    server = GameServer()
    server.start()
