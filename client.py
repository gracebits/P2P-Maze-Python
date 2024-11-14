import pygame
import socketio
from config import MAZE_WIDTH, MAZE_HEIGHT, CELL_SIZE, WHITE, BLUE, RED, SERVER_URL

# Initialize Pygame
pygame.init()
SCREEN_WIDTH = MAZE_WIDTH * CELL_SIZE
SCREEN_HEIGHT = MAZE_HEIGHT * CELL_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Escape")

# Colors and fonts
font = pygame.font.SysFont('Arial', 20)

# Setup for connecting to the server
sio = socketio.Client()
socket_url = f"{SERVER_URL}/game"  # Use SERVER_URL from config.py

# Game lobby data
current_room = None
player_name = None

# Event handler when joining a room
def join_lobby(room_name, player_name):
    sio.emit('join_lobby', {'player_name': player_name, 'room_name': room_name}, namespace='/game')

# Event handler to create a room
def create_lobby(room_name, player_name):
    sio.emit('create_lobby', {'player_name': player_name, 'room_name': room_name}, namespace='/game')

# Event handler for when the game starts
def on_game_start(data):
    print("Game starting with maze:", data)
    # Start game logic can go here (e.g., generate maze, etc.)

# Event handler for room updates (show available rooms)
def update_rooms(rooms):
    print("Available rooms:", rooms)
    screen.fill(WHITE)  # Clear the screen

    y_offset = 100
    for room in rooms:
        room_text = font.render(f"Room: {room} - {len(rooms[room]['players'])}/4 players", True, (0, 0, 0))
        screen.blit(room_text, (100, y_offset))
        y_offset += 30

    pygame.display.update()

# Event handler for when the player is ready
def on_ready_status(data):
    print(f"{data['player_name']} is ready")

# Event handler for enabling the start button
def enable_start(data):
    if player_name == rooms[0]['players'][0]:  # If this is the creator
        print("You can start the game now!")

# Main loop to interact with the server
def main_game_loop():
    global current_room, player_name
    running = True
    while running:
        screen.fill(WHITE)  # Clear the screen for each loop

        # Handle player input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:  # Create lobby
                    room_name = input("Enter the room name: ")
                    player_name = input("Enter your name: ")
                    create_lobby(room_name, player_name)
                elif event.key == pygame.K_j:  # Join lobby
                    room_name = input("Enter the room name to join: ")
                    player_name = input("Enter your name: ")
                    join_lobby(room_name, player_name)
                elif event.key == pygame.K_r:  # Ready up
                    if player_name and current_room:
                        sio.emit('ready', {'player_name': player_name, 'room_name': current_room})

        pygame.display.update()  # Update the display window

    pygame.quit()

# Connect and start the game client
def start_client():
    sio.connect(socket_url)
    sio.on('update_rooms', update_rooms)
    sio.on('ready_status', on_ready_status)
    sio.on('start_game', on_game_start)
    sio.on('enable_start', enable_start)
    main_game_loop()

# Entry point for the client script
if __name__ == '__main__':
    start_client()
