import pygame
from maze import Maze
from network import sio, connect_to_server, join_room, send_ready, start_game
from config import MAZE_WIDTH, MAZE_HEIGHT, CELL_SIZE, WHITE, BLUE, RED

# Initialize Pygame
pygame.init()
SCREEN_WIDTH = MAZE_WIDTH * CELL_SIZE
SCREEN_HEIGHT = MAZE_HEIGHT * CELL_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Escape")

# Colors and fonts
font = pygame.font.SysFont('Arial', 20)

# Initialize the Maze
maze = Maze()

# Player data (with example positions)
players = {'Player1': (1, 1), 'Player2': (3, 3)}  # Example player positions
current_player = 'Player1'

# Draw player names above characters
def draw_player(player_name, position):
    x, y = position
    name_surface = font.render(player_name, True, (255, 255, 255))  # White text
    screen.blit(name_surface, (x * CELL_SIZE + CELL_SIZE // 4, y * CELL_SIZE - 20))  # Adjust position
    color = BLUE if player_name == current_player else RED
    pygame.draw.circle(screen, color, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

# Main game loop
def main_game_loop():
    running = True
    while running:
        screen.fill(WHITE)

        # Draw the maze
        maze.draw_maze(screen, font)

        # Draw players
        for player_name, position in players.items():
            draw_player(player_name, position)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Example: "R" to send ready signal
                    send_ready('game_room', current_player)
                elif event.key == pygame.K_s:  # Example: "S" to start game
                    start_game('game_room')

        # Update the display
        pygame.display.update()

    pygame.quit()

# Run the connection to the server
def start_client():
    connect_to_server()
    join_room('Player1', 'game_room')
    pygame.time.delay(1000)  # Wait for connection

    # Start the game
    main_game_loop()

# Entry point for the client script
if __name__ == '__main__':
    start_client()
