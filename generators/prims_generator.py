import pygame
import os
import sys
import time
import random
import config
from config import GRID_WIDTH, GRID_HEIGHT, DELAY, SAVE_FRAMES, WHITE
from utils.helpers import remove_walls
from utils.render import draw_step_counters, draw_time_counters

# Generate the maze using the Prim's Algorithm
def generate_maze(grid, screen, font, draw_button, frame_count, start_x=0, start_y=0):
    if SAVE_FRAMES:
        os.makedirs(config.FRAME_DIR, exist_ok=True)

    # Initialize the generation timer
    start_time = time.time()
    paused_time = 0
    pause_start = None

    visited = set()
    walls = []
    start = grid[start_x][start_y]
    start.visited = True
    visited.add(start)

    def add_walls(cell):
        x, y = cell.x, cell.y
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                walls.append((cell, grid[ny][nx]))

    add_walls(start)
    paused = False

    gen_step_count = 0
    while True:
        # Filter walls to keep only those where b is unvisited
        valid_walls = [(a, b) for (a, b) in walls if not b.visited]

        if not valid_walls:
            break  # maze complete — no valid frontier left

        screen.fill(WHITE)

        # Draw maze structure
        for row in grid:
            for cell in row:
                cell.draw(screen)

        # Highlight valid frontier cells
        # Using set() avoids duplicate rendering of the same cell.
        seen = set()
        for _, frontier_cell in valid_walls:
            if (frontier_cell.x, frontier_cell.y) not in seen:
                frontier_cell.highlight(screen, (0, 255, 0))
                seen.add((frontier_cell.x, frontier_cell.y))

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

        # Handle pause and quit events
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

        # ---- PRIM'S STEP ----
        # Choose a random valid wall and proceed
        a, b = random.choice(valid_walls)
        walls.remove((a, b))

        if not b.visited:
            remove_walls(a, b)
            b.visited = True
            visited.add(b)
            add_walls(b)

        # Increment at every visible Prim's frame step
        gen_step_count += 1

    # Remove entrance and exit walls
    grid[0][0].walls[3] = False                             # Left wall of top-left
    grid[GRID_HEIGHT - 1][GRID_WIDTH - 1].walls[1] = False  # Right wall of bottom-right

    return frame_count, gen_step_count, elapsed_time
