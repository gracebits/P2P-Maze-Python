# ui.py
import tkinter as tk

class GameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Escape")
        self.create_lobby_button = tk.Button(self.root, text="Create Lobby", command=self.create_lobby)
        self.join_lobby_button = tk.Button(self.root, text="Join Lobby", command=self.join_lobby)
        self.create_lobby_button.pack()
        self.join_lobby_button.pack()

    def create_lobby(self):
        # Logic to create a new lobby
        pass

    def join_lobby(self):
        # Logic to join an existing lobby
        pass
