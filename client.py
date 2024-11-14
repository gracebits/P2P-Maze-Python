import pygame
from config import MAZE_WIDTH, MAZE_HEIGHT, CELL_SIZE, WHITE, BLUE, RED
from network import sio, connect_to_server, send_ready, start_game

# Initialize Pygame
pygame.init()
SCREEN_WIDTH = MAZE_WIDTH * CELL_SIZE
SCREEN_HEIGHT = MAZE_HEIGHT * CELL_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Escape")

# Colors and fonts
font = pygame.font.SysFont('Arial', 20)

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
    # Implement game initialization here

# Event handler to show available rooms
def update_rooms(data):
    print("Available rooms:", data)
    # Display available rooms on the screen
    room_list = data
    room_list_text = font.render(f"Available Rooms: {room_list}", True, (0, 0, 0))
    screen.blit(room_list_text, (100, 100))

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
        screen.fill(WHITE)

        # Handle player input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:  # Create lobby example
                    room_name = input("Enter the room name: ")
                    player_name = input("Enter your name: ")
                    create_lobby(room_name, player_name)
                elif event.key == pygame.K_j:  # Join lobby example
                    room_name = input("Enter the room name to join: ")
                    player_name = input("Enter your name: ")
                    join_lobby(room_name, player_name)

        pygame.display.update()

    pygame.quit()

# Connect and start the game client
def start_client():
    connect_to_server()
    main_game_loop()

# Entry point for the client script
if __name__ == '__main__':
    start_client()
