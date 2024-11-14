# network.py
import socketio
from config import SERVER_URL

# Initialize the Socket.IO client
sio = socketio.Client()

# Use the `/game` namespace
namespace = '/game'

# Event handlers
def on_connect():
    print("Connected to server!")
    sio.emit('join', {'player_name': 'Player1', 'room_name': 'game_room'}, namespace=namespace)

def on_update_players(data):
    print("Players updated:", data)

def on_start_game(data):
    print("Game starting...")
    maze_data = data['maze']
    return maze_data

def connect_to_server():
    try:
        sio.connect(SERVER_URL + namespace)  # Use the correct namespace URL
        print(f"Connecting to {SERVER_URL + namespace}...")
    except Exception as e:
        print(f"Failed to connect to server: {e}")

def emit_ready(room_name, player_name):
    sio.emit('ready', {'room_name': room_name, 'player_name': player_name}, namespace=namespace)

def emit_start_game(room_name):
    sio.emit('start_game', {'room_name': room_name}, namespace=namespace)

# Register event listeners
sio.on('connect', on_connect, namespace=namespace)
sio.on('update_players', on_update_players, namespace=namespace)
sio.on('start_game', on_start_game, namespace=namespace)

# Client-side functions
def join_room(player_name, room_name):
    sio.emit('join', {'player_name': player_name, 'room_name': room_name}, namespace=namespace)

def send_ready(player_name, room_name):
    sio.emit('ready', {'player_name': player_name, 'room_name': room_name}, namespace=namespace)

def start_game(room_name):
    sio.emit('start_game', {'room_name': room_name}, namespace=namespace)
