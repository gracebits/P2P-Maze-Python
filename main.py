import pygame
import threading
from network import Network
from maze import generate_maze

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
PORT = 5000

class MazeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("P2P Maze Game")
        self.clock = pygame.time.Clock()
        self.running = True

        # Networking
        self.network = Network(PORT)
        self.network.start_listener()

        # Player
        self.player_name = None
        self.players = {}  # {addr: {"name": str, "ready": bool}}
        self.local_ready = False

        # Maze
        self.maze = generate_maze(SCREEN_WIDTH // TILE_SIZE, SCREEN_HEIGHT // TILE_SIZE)

    def draw_waiting_screen(self):
        font = pygame.font.Font(None, 36)
        self.screen.fill((0, 0, 0))

        # Display players
        waiting_text = font.render("Waiting for players...", True, (255, 255, 255))
        self.screen.blit(waiting_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))

        # Show players in lobby
        y_offset = 0
        for player in self.network.players.values():
            player_text = font.render(f"{player['name']} - {'Ready' if player['ready'] else 'Not Ready'}", True, (255, 255, 255))
            self.screen.blit(player_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + y_offset))
            y_offset += 30

        # Ready button
        ready_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 100, 100, 40)
        pygame.draw.rect(self.screen, (0, 255, 0), ready_button)
        button_text = font.render("Ready", True, (0, 0, 0))
        self.screen.blit(button_text, (ready_button.x + 20, ready_button.y + 5))

        pygame.display.flip()
        return ready_button

    def main_menu(self):
        font = pygame.font.Font(None, 36)
        input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20, 200, 40)
        start_button = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 40, 100, 40)

        input_text = ""
        while not self.player_name:
            self.screen.fill((0, 0, 0))
            pygame.draw.rect(self.screen, (255, 255, 255), input_box, 2)
            pygame.draw.rect(self.screen, (0, 255, 0), start_button)

            # Render text
            text_surface = font.render(input_text, True, (255, 255, 255))
            self.screen.blit(text_surface, (input_box.x + 10, input_box.y + 5))

            button_text = font.render("Start", True, (0, 0, 0))
            self.screen.blit(button_text, (start_button.x + 20, start_button.y + 10))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        self.player_name = input_text.strip()
                        self.network.broadcast({"type": "join", "name": self.player_name})

    def wait_for_players(self):
        while not (len(self.network.players) >= 2 and self.network.all_ready()):
            ready_button = self.draw_waiting_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if ready_button.collidepoint(event.pos) and not self.local_ready:
                        self.local_ready = True
                        self.network.broadcast({"type": "ready", "name": self.player_name})
            self.clock.tick(30)

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Draw everything
            self.screen.fill((0, 0, 0))
            self.draw_maze()
            pygame.display.flip()
            self.clock.tick(30)

        self.network.stop()

if __name__ == "__main__":
    game = MazeGame()
    game.main_menu()
    game.wait_for_players()
    game.game_loop()
