import random

def generate_maze(width, height):
    return [[random.choice([0, 1]) for _ in range(width)] for _ in range(height)]
