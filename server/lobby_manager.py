# server/lobby_manager.py
from config.config import MAX_PLAYERS
import random

class LobbyManager:
    def __init__(self):
        self.lobbies = {}

    def create_lobby(self, lobby_id, player):
        if lobby_id not in self.lobbies:
            self.lobbies[lobby_id] = {
                'players': [player],
                'status': 'waiting',  # can be 'waiting' or 'started'
            }
            return f"Lobby {lobby_id} created. Waiting for players..."
        else:
            return f"Lobby {lobby_id} already exists."

    def join_lobby(self, lobby_id, player):
        if lobby_id in self.lobbies:
            if len(self.lobbies[lobby_id]['players']) < MAX_PLAYERS:
                self.lobbies[lobby_id]['players'].append(player)
                return f"Player {player} joined Lobby {lobby_id}."
            else:
                return f"Lobby {lobby_id} is full."
        else:
            return f"Lobby {lobby_id} does not exist."

    def start_game(self, lobby_id):
        if lobby_id in self.lobbies and len(self.lobbies[lobby_id]['players']) > 1:
            self.lobbies[lobby_id]['status'] = 'started'
            # Randomly place players in the maze
            players = self.lobbies[lobby_id]['players']
            random.shuffle(players)
            return f"Game started in Lobby {lobby_id}. Players: {', '.join(players)}"
        else:
            return f"Cannot start the game. Not enough players or lobby does not exist."

    def get_lobby_info(self, lobby_id):
        if lobby_id in self.lobbies:
            players = self.lobbies[lobby_id]['players']
            status = self.lobbies[lobby_id]['status']
            return f"Lobby {lobby_id} | Status: {status} | Players: {', '.join(players)}"
        else:
            return f"Lobby {lobby_id} does not exist."

    def list_lobbies(self):
        if not self.lobbies:
            return "No lobbies available."
        return "\n".join([self.get_lobby_info(lobby_id) for lobby_id in self.lobbies])
