import socket
import tkinter as tk
from tkinter import messagebox
import threading

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lobby Client")

        self.server_ip = "127.0.0.1"  # Change this to your server's IP address
        self.server_port = 5000
        self.client_socket = None
        self.player_name = None

        # Create widgets for connection frame
        self.connect_frame = tk.Frame(self.root)
        self.connect_label = tk.Label(self.connect_frame, text="Enter your player name:")
        self.player_name_entry = tk.Entry(self.connect_frame)
        self.connect_button = tk.Button(self.connect_frame, text="Connect", command=self.connect_to_server)

        self.lobby_frame = tk.Frame(self.root)
        self.lobby_label = tk.Label(self.lobby_frame, text="Available Lobbies:")
        self.lobby_listbox = tk.Listbox(self.lobby_frame, height=5, width=50)
        self.create_lobby_button = tk.Button(self.lobby_frame, text="Create New Lobby", command=self.create_lobby)
        self.join_lobby_button = tk.Button(self.lobby_frame, text="Join Lobby", command=self.join_lobby)

        self.status_label = tk.Label(self.root, text="Not connected")

        # Place the initial frame
        self.connect_frame.pack(padx=10, pady=10)
        self.status_label.pack(padx=10, pady=5)

    def connect_to_server(self):
        self.player_name = self.player_name_entry.get().strip()
        if not self.player_name:
            messagebox.showwarning("Input Error", "Please enter a player name.")
            return

        try:
            # Connect to the server
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))

            # Send the player's name
            self.client_socket.sendall(self.player_name.encode())

            self.connect_frame.pack_forget()
            self.status_label.config(text=f"Connected as {self.player_name}")

            # Start a thread to listen for available lobbies
            threading.Thread(target=self.listen_for_lobbies, daemon=True).start()

            # Show lobby frame
            self.lobby_frame.pack(padx=10, pady=10)

        except ConnectionRefusedError:
            messagebox.showerror("Connection Error", "Unable to connect to the server.")
            self.status_label.config(text="Connection failed")

    def listen_for_lobbies(self):
        while True:
            try:
                # Receive list of available lobbies from the server
                available_lobbies = self.client_socket.recv(1024).decode().split(',')
                self.update_lobby_list(available_lobbies)
            except Exception as e:
                print("Error while listening for lobbies:", e)
                break

    def update_lobby_list(self, lobbies):
        # Clear the current list
        self.lobby_listbox.delete(0, tk.END)

        # Add lobbies to the listbox
        for lobby in lobbies:
            if lobby:
                self.lobby_listbox.insert(tk.END, lobby)

    def create_lobby(self):
        new_lobby_name = f"{self.player_name}'s Lobby"
        self.client_socket.sendall(f"create {new_lobby_name}".encode())
        self.lobby_listbox.insert(tk.END, new_lobby_name)

    def join_lobby(self):
        selected_lobby = self.lobby_listbox.curselection()
        if selected_lobby:
            lobby_name = self.lobby_listbox.get(selected_lobby)
            self.client_socket.sendall(f"join {lobby_name}".encode())
        else:
            messagebox.showwarning("Select Lobby", "Please select a lobby to join.")

# Create the main window
root = tk.Tk()
app = ClientApp(root)
root.mainloop()
