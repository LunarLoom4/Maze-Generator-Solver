import pygame
import os
import sys
import time
import random
import config
from config import GRID_WIDTH, GRID_HEIGHT, WHITE, GREEN, SAVE_FRAMES, DELAY
from utils.helpers import remove_walls, get_unvisited_neighbors
from utils.render import draw_step_counters, draw_time_counters

# Generate the maze using the Hunt and Kill Algorithm
def generate_maze(grid, screen, font, draw_button, frame_count):
    if SAVE_FRAMES:
        os.makedirs(config.FRAME_DIR, exist_ok=True)

    # Initialize the generation timer
    start_time = time.time()
    paused_time = 0
    pause_start = None

    current = grid[0][0]
    current.visited = True
    paused = False

    running = True
    gen_step_count = 0
    while running:
        screen.fill(WHITE)

        # Draw all cells
        for row in grid:
            for cell in row:
                cell.draw(screen)

        # Highlights the currently involved cells
        if current:
            current.highlight(screen, GREEN)

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

        # KILL PHASE: Random walk
        neighbors = get_unvisited_neighbors(current, grid, GRID_WIDTH, GRID_HEIGHT)
        if neighbors:
            next_cell = random.choice(neighbors)
            remove_walls(current, next_cell)
            next_cell.visited = True
            current = next_cell
            if not paused:
                gen_step_count += 1
            continue

        # HUNT PHASE: Finds next start cell
        found = False
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                cell = grid[y][x]

                # Visualize the hunt scan on current cell
                screen.fill(WHITE)
                for row in grid:
                    for c in row:
                        c.draw(screen)
                cell.highlight(screen, (0, 255, 255))

                # Draw pause/resume button
                btn_rect = draw_button(screen, font, paused)

                # Draw the step counters
                draw_step_counters(screen, gen_step_count, 0)
                if not paused:
                    gen_step_count += 1

                # Draw the time counters
                elapsed_time = time.time() - start_time - paused_time
                draw_time_counters(screen, elapsed_time, 0)

                pygame.display.flip()

                if SAVE_FRAMES:
                    pygame.image.save(screen, f"{config.FRAME_DIR}/frame_{frame_count:04d}.png")
                    frame_count += 1

                pygame.time.wait(DELAY)

                # Check for pause/quit events during scan
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

                # Freeze the scan animation until 'resumed'
                if paused:
                    while paused:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            elif event.type == pygame.MOUSEBUTTONDOWN and btn_rect.collidepoint(event.pos):
                                paused_time += time.time() - pause_start
                                paused = False
                            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                                paused_time += time.time() - pause_start
                                paused = False

                # Only hunt from unvisited cells
                if cell.visited:
                    continue

                # Gathers the adjacent 4 neighbors of a given cell (grid[y][x])
                # regardless of whether they're visited or unvisited.
                neighbors = []
                if y > 0: neighbors.append(grid[y - 1][x])
                if x < GRID_WIDTH - 1: neighbors.append(grid[y][x + 1])
                if y < GRID_HEIGHT - 1: neighbors.append(grid[y + 1][x])
                if x > 0: neighbors.append(grid[y][x - 1])

                visited_neighbors = [nb for nb in neighbors if nb.visited]

                # If this cell is valid for resuming the walk
                if visited_neighbors:
                    neighbor = random.choice(visited_neighbors)
                    remove_walls(cell, neighbor)
                    cell.visited = True
                    current = cell  # THIS IS THE KEY: 'kill' restarts from here
                    found = True
                    break
            if found:
                break

        if not found:
            running = False  # Maze is fully generated

    # Remove entrance and exit walls
    grid[0][0].walls[3] = False                             # Left wall of top-left
    grid[GRID_HEIGHT - 1][GRID_WIDTH - 1].walls[1] = False  # Right wall of bottom-right

    return frame_count, gen_step_count, elapsed_time
