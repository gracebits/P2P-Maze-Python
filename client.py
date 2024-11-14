import socket
import tkinter as tk
from tkinter import messagebox
import threading
import config  # Import the configuration from config.py

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lobby Client")
        self.root.geometry("400x400")  # Set a default window size

        # Use values from config.py
        self.server_ip = config.SERVER_IP
        self.server_port = config.SERVER_PORT
        self.client_socket = None
        self.player_name = None
        self.current_lobby = None
        self.ready = False

        # Create widgets for connection frame
        self.connect_frame = tk.Frame(self.root)
        self.connect_label = tk.Label(self.connect_frame, text="Connecting to server...")
        self.connect_label.pack(padx=10, pady=10)

        self.status_label = tk.Label(self.root, text="Not connected")

        # Place the initial frame
        self.connect_frame.pack(padx=10, pady=10)
        self.status_label.pack(padx=10, pady=5)

        # Start automatic connection to the server
        self.connect_to_server()

    def connect_to_server(self):
        try:
            # Connect to the server using the config values
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))

            self.connect_label.config(text="Connected to server. Please enter your name:")

            # Start a thread to listen for available lobbies and room updates
            threading.Thread(target=self.listen_for_updates, daemon=True).start()

            # Ask for player name
            self.ask_player_name()

        except ConnectionRefusedError:
            messagebox.showerror("Connection Error", "Unable to connect to the server.")
            self.status_label.config(text="Connection failed")

    def ask_player_name(self):
        # Once connected, ask for the player name
        self.connect_frame.pack_forget()

        self.name_frame = tk.Frame(self.root)
        self.name_label = tk.Label(self.name_frame, text="Enter your player name:")
        self.player_name_entry = tk.Entry(self.name_frame)
        self.name_button = tk.Button(self.name_frame, text="Submit", command=self.submit_name)

        self.name_label.pack(padx=10, pady=5)
        self.player_name_entry.pack(padx=10, pady=5)
        self.name_button.pack(padx=10, pady=10)

        self.name_frame.pack(padx=10, pady=10)

    def submit_name(self):
        self.player_name = self.player_name_entry.get().strip()
        if not self.player_name:
            messagebox.showwarning("Input Error", "Please enter a player name.")
            return

        # Send the player's name to the server
        self.client_socket.sendall(self.player_name.encode())

        # Proceed to show lobby frame
        self.name_frame.pack_forget()
        self.status_label.config(text=f"Connected as {self.player_name}")

        # Show the lobby frame
        self.show_lobby_frame()

    def show_lobby_frame(self):
        # Create frame to display available lobbies and buttons for actions
        self.lobby_frame = tk.Frame(self.root)
        self.lobby_label = tk.Label(self.lobby_frame, text="Available Lobbies:")
        self.lobby_listbox = tk.Listbox(self.lobby_frame, height=5, width=50)
        self.create_lobby_button = tk.Button(self.lobby_frame, text="Create New Lobby", command=self.create_lobby)
        self.join_lobby_button = tk.Button(self.lobby_frame, text="Join Lobby", command=self.join_lobby)

        # Add widgets to the frame
        self.lobby_label.pack(padx=10, pady=5)
        self.lobby_listbox.pack(padx=10, pady=5)
        self.create_lobby_button.pack(padx=10, pady=5)
        self.join_lobby_button.pack(padx=10, pady=5)

        self.lobby_frame.pack(padx=10, pady=10)

    def listen_for_updates(self):
        while True:
            try:
                # Receive list of available lobbies from the server
                available_lobbies = self.client_socket.recv(1024).decode().split(',')
                self.update_lobby_list(available_lobbies)
            except Exception as e:
                print("Error while listening for updates:", e)
                break

    def update_lobby_list(self, lobbies):
        # Clear the current list
        self.lobby_listbox.delete(0, tk.END)

        # If no lobbies are available, show a message
        if not lobbies or lobbies == ['']:
            self.lobby_listbox.insert(tk.END, "No lobbies available.")
        else:
            # Add lobbies to the listbox
            for lobby in lobbies:
                if lobby:
                    self.lobby_listbox.insert(tk.END, lobby)

    def create_lobby(self):
        new_lobby_name = f"{self.player_name}'s Lobby"
        self.client_socket.sendall(f"create {new_lobby_name}".encode())

        # Change the screen to the lobby/room view
        self.show_lobby_room(new_lobby_name)

    def join_lobby(self):
        selected_lobby = self.lobby_listbox.curselection()
        if selected_lobby:
            lobby_name = self.lobby_listbox.get(selected_lobby)
            self.client_socket.sendall(f"join {lobby_name}".encode())

            # Change the screen to the lobby/room view
            self.show_lobby_room(lobby_name)
        else:
            messagebox.showwarning("Select Lobby", "Please select a lobby to join.")

    def show_lobby_room(self, lobby_name):
        # Remove the previous lobby list view
        self.lobby_frame.pack_forget()

        # Set the current lobby
        self.current_lobby = lobby_name

        # Create a new lobby room frame
        self.room_frame = tk.Frame(self.root)
        self.room_label = tk.Label(self.room_frame, text=f"Lobby: {lobby_name}")
        self.player_listbox = tk.Listbox(self.room_frame, height=5, width=50)
        self.ready_button = tk.Button(self.room_frame, text="Ready", command=self.set_ready)

        # Pack all widgets for the room view
        self.room_label.pack(padx=10, pady=5)
        self.player_listbox.pack(padx=10, pady=5)
        self.ready_button.pack(padx=10, pady=5)

        self.room_frame.pack(padx=10, pady=10)

        # Send a request to the server to update lobby information
        self.client_socket.sendall(f"get_players {lobby_name}".encode())

    def set_ready(self):
        # Mark the player as ready
        self.ready = True
        self.ready_button.config(state="disabled")  # Disable the ready button after clicking

        # Inform the server that the player is ready
        self.client_socket.sendall(f"ready {self.current_lobby} {self.player_name}".encode())

        # Update the room status
        self.update_room_status()

    def update_room_status(self):
        # In this example, we would receive the room status from the server
        pass

# Create the main window
root = tk.Tk()
app = ClientApp(root)
root.mainloop()
