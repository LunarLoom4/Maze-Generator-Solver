import pygame
import os
import sys
import time
import random
import config
from config import GRID_WIDTH, GRID_HEIGHT, DELAY, SAVE_FRAMES, WHITE
from utils.helpers import remove_walls, get_unvisited_neighbors
from utils.render import draw_step_counters, draw_time_counters

# Generate the maze using the DFS Algorithm
def generate_maze(grid, screen, font, draw_button, frame_count, start_x=0, start_y=0):
    if SAVE_FRAMES:
        os.makedirs(config.FRAME_DIR, exist_ok=True)

    # Initialize the generation timer
    start_time = time.time()
    paused_time = 0
    pause_start = None

    stack = []
    current = grid[start_y][start_x]
    current.visited = True
    stack.append(current)
    paused = False

    running = True
    gen_step_count = 0
    while running:
        screen.fill(WHITE)

        # Draw all cells
        for row in grid:
            for cell in row:
                cell.draw(screen)
        current.highlight(screen, (0, 255, 0))

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

        # Handles Quit/Pause events
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

        # Maze generation step
        neighbors = get_unvisited_neighbors(current, grid, GRID_WIDTH, GRID_HEIGHT)
        if neighbors:
            next_cell = random.choice(neighbors)
            remove_walls(current, next_cell)
            next_cell.visited = True
            stack.append(current)
            current = next_cell
        elif stack:
            current = stack.pop()
        else:
            running = False

        # Increment at every visible DFS frame step
        gen_step_count += 1

    # Remove entrance and exit walls
    grid[0][0].walls[3] = False                             # Left wall of top-left
    grid[GRID_HEIGHT - 1][GRID_WIDTH - 1].walls[1] = False  # Right wall of bottom-right

    return frame_count, gen_step_count, elapsed_time
