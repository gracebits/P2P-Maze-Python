from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
import logging

app = Flask(__name__)
app.secret_key = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# Enable logging
logging.basicConfig(level=logging.DEBUG)

# Store rooms and player data
rooms = {}  # Room name -> players data (list of players)
max_players = 4  # Maximum players per lobby

@app.route('/')
def index():
    return render_template('index.html')

# Event when a client connects
@socketio.on('connect', namespace='/game')
def on_connect():
    print("Client connected")
    emit('update_rooms', rooms, namespace='/game')

# Event for creating a new lobby
@socketio.on('create_lobby', namespace='/game')
def create_lobby(data):
    player_name = data['player_name']
    room_name = data['room_name']

    # If the room doesn't exist, create it
    if room_name not in rooms:
        rooms[room_name] = {'players': [player_name], 'ready_players': []}
        print(f"Lobby '{room_name}' created by {player_name}")
        join_room(room_name)
        emit('update_rooms', rooms, namespace='/game')
        emit('join_lobby', {'room_name': room_name, 'players': rooms[room_name]['players']}, room=room_name, namespace='/game')
    else:
        emit('error', {'message': 'Room already exists!'}, namespace='/game')

# Event for joining a lobby
@socketio.on('join_lobby', namespace='/game')
def join_lobby(data):
    player_name = data['player_name']
    room_name = data['room_name']

    if room_name in rooms and len(rooms[room_name]['players']) < max_players:
        rooms[room_name]['players'].append(player_name)
        join_room(room_name)
        emit('update_rooms', rooms, namespace='/game')
        emit('join_lobby', {'room_name': room_name, 'players': rooms[room_name]['players']}, room=room_name, namespace='/game')
    else:
        emit('error', {'message': 'Room is full or does not exist!'}, namespace='/game')

# Event for a player to mark themselves as ready
@socketio.on('ready', namespace='/game')
def on_ready(data):
    player_name = data['player_name']
    room_name = data['room_name']

    if player_name not in rooms[room_name]['ready_players']:
        rooms[room_name]['ready_players'].append(player_name)
    
    emit('ready_status', {'player_name': player_name, 'status': 'ready'}, room=room_name, namespace='/game')

    # Check if all players are ready, and allow the room creator to start the game
    if len(rooms[room_name]['ready_players']) == len(rooms[room_name]['players']):
        emit('enable_start', {'room_name': room_name}, room=room_name, namespace='/game')

# Event to start the game when the creator clicks start
@socketio.on('start_game', namespace='/game')
def start_game(data):
    room_name = data['room_name']
    if room_name in rooms and len(rooms[room_name]['players']) >= 2:
        # Game starting logic (e.g., generating maze data)
        maze_data = {'maze': [[0, 1, 1], [0, 0, 1], [1, 0, 0]]}  # Sample maze
        emit('start_game', maze_data, room=room_name, namespace='/game')
    else:
        emit('error', {'message': 'Not enough players to start the game!'}, namespace='/game')

@socketio.on('disconnect', namespace='/game')
def on_disconnect():
    print("Client disconnected")
    for room_name in rooms:
        for player in rooms[room_name]['players']:
            if player == request.sid:
                rooms[room_name]['players'].remove(player)
                rooms[room_name]['ready_players'].remove(player)
                break
    emit('update_rooms', rooms, namespace='/game')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
