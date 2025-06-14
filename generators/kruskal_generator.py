import pygame
import os
import sys
import time
import config
from config import GRID_WIDTH, GRID_HEIGHT, WHITE, GREEN, SAVE_FRAMES, DELAY
from utils.helpers import remove_walls
from utils.render import draw_step_counters, draw_time_counters

# Disjoint Set Union (Union-Find) for Kruskal's algorithm
class DisjointSet:
    def __init__(self):
        self.parent = {}

    def find(self, item):
        if self.parent.get(item) != item:
            self.parent[item] = self.find(self.parent.get(item, item))
        return self.parent.get(item, item)

    def union(self, set1, set2):
        root1 = self.find(set1)
        root2 = self.find(set2)
        if root1 != root2:
            self.parent[root2] = root1
            return True
        return False

# Generate the maze using the Kruskal Algorithm
def generate_maze(grid, screen, font, draw_button, frame_count):
    if SAVE_FRAMES:
        os.makedirs(config.FRAME_DIR, exist_ok=True)

    # Initialize the generation timer
    start_time = time.time()
    paused_time = 0
    pause_start = None

    # Initialize DSU with all cells
    dsu = DisjointSet()
    for row in grid:
        for cell in row:
            dsu.parent[cell] = cell

    # List of all potential walls between adjacent cells
    walls = []
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if x < GRID_WIDTH - 1:
                walls.append((grid[y][x], grid[y][x + 1]))
            if y < GRID_HEIGHT - 1:
                walls.append((grid[y][x], grid[y + 1][x]))

    import random
    random.shuffle(walls)
    paused = False
    gen_step_count = 0

    # Loop while there are walls and maze is not fully connected
    while walls:
        # Peek at the next wall pair
        a, b = walls[-1]

        # If they are in different sets, proceed with union and visualization
        if dsu.find(a) != dsu.find(b):
            screen.fill(WHITE)

            # Draw all cells
            for row in grid:
                for cell in row:
                    cell.draw(screen)

            # Highlight current cells being connected
            a.highlight(screen, GREEN)
            b.highlight(screen, GREEN)

            # Draw pause/resume button
            btn_rect = draw_button(screen, font, paused)

            # Draw the step counters
            draw_step_counters(screen, gen_step_count, 0)

            # Draw the time counters
            if paused:
                elapsed_time_display = elapsed_time  # Doesn't change
            else:
                elapsed_time = time.time() - start_time - paused_time
                elapsed_time_display = elapsed_time
            draw_time_counters(screen, elapsed_time_display, 0)

            pygame.display.flip()

            # Save frame
            if SAVE_FRAMES:
                pygame.image.save(screen, f"{config.FRAME_DIR}/frame_{frame_count:04d}.png")
                frame_count += 1

            pygame.time.wait(DELAY)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if btn_rect.collidepoint(event.pos):
                        if not paused:
                            pause_start = time.time()
                        else:
                            paused_time += time.time() - pause_start
                        paused = not paused

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if not paused:
                        pause_start = time.time()
                    else:
                        paused_time += time.time() - pause_start
                    paused = not paused

            if paused:
                continue

            # Finalize wall: pop and connect
            walls.pop()
            dsu.union(a, b)
            remove_walls(a, b)
        else:
            # Already connected — discard wall silently
            walls.pop()

        # Increment at every visible Kruskal frame step
        gen_step_count += 1

    # Remove entrance and exit walls
    grid[0][0].walls[3] = False                             # Left wall of top-left
    grid[GRID_HEIGHT - 1][GRID_WIDTH - 1].walls[1] = False  # Right wall of bottom-right

    return frame_count, gen_step_count, elapsed_time
