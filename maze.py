import random

def generate_maze(width, height):
    maze = [[1 if random.random() > 0.2 else 0 for _ in range(width)] for _ in range(height)]
    maze[0][0] = 0  # Start point
    maze[-1][-1] = 0  # End point
    return maze
