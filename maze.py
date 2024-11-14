# maze.py
import random
from config import MAZE_WIDTH, MAZE_HEIGHT, CELL_SIZE, WHITE, BLACK

class Maze:
    def __init__(self, width=MAZE_WIDTH, height=MAZE_HEIGHT, cell_size=CELL_SIZE):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = []
        self.generate_maze()

    def generate_maze(self):
        self.grid = [[1 for _ in range(self.width)] for _ in range(self.height)]  # 1 represents walls
        for row in range(1, self.height - 1):
            for col in range(1, self.width - 1):
                self.grid[row][col] = random.choice([0, 1])  # 0 = path, 1 = wall
        # Ensure start and end points are clear
        self.grid[1][1] = 0  # Start
        self.grid[self.height - 2][self.width - 2] = 0  # End

    def is_wall(self, x, y):
        return self.grid[y][x] == 1

    def print_maze(self):
        for row in self.grid:
            print("".join(str(cell) for cell in row))

    def draw_maze(self, screen, font):
        for row in range(self.height):
            for col in range(self.width):
                color = WHITE if self.grid[row][col] == 0 else BLACK
                pygame.draw.rect(screen, color, (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))
                pygame.draw.rect(screen, BLACK, (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size), 1)

        # Draw start and end points
        pygame.draw.rect(screen, GREEN, (1 * self.cell_size, 1 * self.cell_size, self.cell_size, self.cell_size))
        pygame.draw.rect(screen, RED, ((self.width - 2) * self.cell_size, (self.height - 2) * self.cell_size, self.cell_size, self.cell_size))
