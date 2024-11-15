# network/message_handler.py
from network.connection import Connection

class MessageHandler:
    def __init__(self, connection):
        self.connection = connection

    def handle_message(self, message):
        if message.startswith("CREATE_LOBBY"):
            self.create_lobby(message)
        elif message.startswith("JOIN_LOBBY"):
            self.join_lobby(message)
        elif message.startswith("START_GAME"):
            self.start_game()

    def create_lobby(self, message):
        # Logic to create a new lobby and notify players
        pass

    def join_lobby(self, message):
        # Logic to join an existing lobby and notify server
        pass

    def start_game(self):
        # Logic to start the game when all players are ready
        pass
