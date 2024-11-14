# server.py
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS

# Initialize Flask and Socket.IO
app = Flask(__name__)
app.secret_key = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# Define the game namespace
namespace = '/game'

# Define a room and players
players = {}

@app.route('/')
def index():
    return render_template('index.html')

# SocketIO event handlers for the `/game` namespace
@socketio.on('connect', namespace=namespace)
def on_connect():
    print("Client connected")
    emit('update_players', players, namespace=namespace)

@socketio.on('join', namespace=namespace)
def on_join(data):
    player_name = data['player_name']
    room_name = data['room_name']
    players[player_name] = (0, 0)  # Example player position
    join_room(room_name)
    emit('update_players', players, room=room_name, namespace=namespace)

@socketio.on('ready', namespace=namespace)
def on_ready(data):
    player_name = data['player_name']
    room_name = data['room_name']
    emit('update_players', players, room=room_name, namespace=namespace)

@socketio.on('start_game', namespace=namespace)
def on_start_game(data):
    room_name = data['room_name']
    # Generate maze data here
    maze_data = {'maze': [[0, 1, 1], [0, 0, 1], [1, 0, 0]]}  # Example maze
    emit('start_game', maze_data, room=room_name, namespace=namespace)

@socketio.on('disconnect', namespace=namespace)
def on_disconnect():
    print("Client disconnected")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
