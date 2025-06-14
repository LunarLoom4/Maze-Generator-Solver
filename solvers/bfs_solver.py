import pygame
import time
import config
from collections import deque
from config import GRID_WIDTH, GRID_HEIGHT, DELAY, SAVE_FRAMES, WHITE, GREEN, GRAY
from utils.helpers import get_neighbors_for_solver
from utils.render import draw_path_line
from utils.render import draw_step_counters, draw_time_counters

# Solving the maze with the BFS Algorithm
def solve_maze_with_bfs(grid, screen, font, draw_button, frame_count, gen_step_count, gen_time):
    start = grid[0][0]
    end = grid[GRID_HEIGHT - 1][GRID_WIDTH - 1]
    visited = set()
    queue = deque([(start, [start])])
    paused = False
    visited_cells = []

    solve_step_count = 0

    # Initialize the solver timer
    start_time = time.time()
    paused_time = 0
    pause_start = None

    while queue:
        # Draw background and grid walls first
        screen.fill(WHITE)
        for row in grid:
            for cell in row:
                cell.draw(screen)

        # Draw all previously visited cells (on top of walls)
        for cell in visited_cells:
            if cell != start and cell != end:
                cell.fill(screen, GRAY)
        
        start.fill(screen, (0, 0, 255))   # Blue start
        end.fill(screen, (255, 0, 0))     # Red end

        # Draw pause/resume button
        btn_rect = draw_button(screen, font, paused)

        # Draw the step counters
        draw_step_counters(screen, gen_step_count, solve_step_count)

        # Draw the time counters
        if paused:
            elapsed_time_display = elapsed_time  # Doesn't change
        else:
            elapsed_time = time.time() - start_time - paused_time
            elapsed_time_display = elapsed_time
        draw_time_counters(screen, gen_time, elapsed_time_display)

        pygame.display.flip()

        if SAVE_FRAMES:
            pygame.image.save(screen, f"{config.FRAME_DIR}/frame_{frame_count:04d}.png")
            frame_count += 1
        
        pygame.time.wait(DELAY)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
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

        # Solve step
        current, path = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        visited_cells.append(current)

        if current != start and current != end:
            current.fill(screen, GRAY)

        if current == end:
            # Step 1: Draw final path using green-filled cells
            for cell in path:
                if cell != start and cell != end:
                    cell.fill(screen, GREEN)

            start.fill(screen, (0, 0, 255))   # Blue start
            end.fill(screen, (255, 0, 0))     # Red end

            # Draw the step counters
            draw_step_counters(screen, gen_step_count, solve_step_count)

            # Draw the time counters
            if paused:
                elapsed_time_display = elapsed_time  # Doesn't change
            else:
                elapsed_time = time.time() - start_time - paused_time
                elapsed_time_display = elapsed_time
            draw_time_counters(screen, gen_time, elapsed_time_display)

            pygame.display.flip()

            if SAVE_FRAMES:
                for _ in range(5):  # 5 frames
                    pygame.image.save(screen, f"{config.FRAME_DIR}/frame_{frame_count:04d}.png")
                    frame_count += 1

            # Step 2: Draw same screen, now with connected path line
            screen.fill(WHITE)
            for row in grid:
                for cell in row:
                    cell.draw(screen)

            start.fill(screen, (0, 0, 255))   # Blue start
            end.fill(screen, (255, 0, 0))     # Red end

            draw_path_line(screen, path, GREEN, width=4)

            # Draw the step counters
            draw_step_counters(screen, gen_step_count, solve_step_count)

            # Draw the time counters
            if paused:
                elapsed_time_display = elapsed_time  # Doesn't change
            else:
                elapsed_time = time.time() - start_time - paused_time
                elapsed_time_display = elapsed_time
            draw_time_counters(screen, gen_time, elapsed_time_display)

            pygame.display.flip()

            if SAVE_FRAMES:
                for _ in range(30):  # 30 frames
                    pygame.image.save(screen, f"{config.FRAME_DIR}/frame_{frame_count:04d}.png")
                    frame_count += 1

            # Delay so the final path stays on screen for a moment
            pygame.time.wait(1000)
            return path

        for neighbor in get_neighbors_for_solver(current, grid, GRID_WIDTH, GRID_HEIGHT):
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))

        # Increment step count
        solve_step_count += 1
