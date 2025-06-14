import pygame
from config import CELL_SIZE, PADDING, BLACK

# Cell class
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = [True, True, True, True]  # top, right, bottom, left
        self.visited = False

    # Draws the walls
    def draw(self, surface):
        x = PADDING + self.x * CELL_SIZE
        y = PADDING + self.y * CELL_SIZE
        if self.walls[0]:  # top
            pygame.draw.line(surface, BLACK, (x, y), (x + CELL_SIZE, y), 2)
        if self.walls[1]:  # right
            pygame.draw.line(surface, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls[2]:  # bottom
            pygame.draw.line(surface, BLACK, (x + CELL_SIZE, y + CELL_SIZE), (x, y + CELL_SIZE), 2)
        if self.walls[3]:  # left
            pygame.draw.line(surface, BLACK, (x, y + CELL_SIZE), (x, y), 2)

    # Used to highlight
    def highlight(self, surface, color=(0, 255, 0)):
        x = PADDING + self.x * CELL_SIZE
        y = PADDING + self.y * CELL_SIZE
        pygame.draw.rect(surface, color, (x+2, y+2, CELL_SIZE-4, CELL_SIZE-4))

    # Used to color visited/path cells.
    def fill(self, surface, color):
        x = PADDING + self.x * CELL_SIZE
        y = PADDING + self.y * CELL_SIZE
        pygame.draw.rect(surface, color, (x+4, y+4, CELL_SIZE-8, CELL_SIZE-8))

# Cell Directions
DIRS = {'top': (0, -1), 'right': (1, 0), 'bottom': (0, 1), 'left': (-1, 0)}
DIR_INDEX = ['top', 'right', 'bottom', 'left']
