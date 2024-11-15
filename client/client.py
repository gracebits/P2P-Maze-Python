# client.py

import sys
import os

# Add the parent directory to sys.path to allow module discovery
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now the network module should be accessible
from network.connection import Connection
from network.message_handler import MessageHandler
from config.config import SERVER_IP, SERVER_PORT

class GameClient:
    def __init__(self):
        self.connection = Connection(host=False)
        self.message_handler = MessageHandler(self.connection)

    def request_create_lobby(self):
        self.connection.send_message("CREATE_LOBBY")

    def request_join_lobby(self):
        self.connection.send_message("JOIN_LOBBY")

    def handle_server_response(self):
        while True:
            response = self.connection.receive_message()
            print(response)
            if response == "GAME_STARTED":
                self.start_game()

    def start_game(self):
        # Start the game logic
        pass

    def start(self):
        # This is where you can decide whether to join or create a lobby
        threading.Thread(target=self.handle_server_response).start()
        # Wait for the user to either create or join a lobby
        pass

if __name__ == "__main__":
    client = GameClient()
    client.start()
