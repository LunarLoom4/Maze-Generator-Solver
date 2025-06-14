import pygame
import sys
import time
import heapq
import config
from config import GRID_WIDTH, GRID_HEIGHT, WHITE, GRAY, GREEN, SAVE_FRAMES, DELAY
from utils.helpers import get_neighbors_for_solver
from utils.render import draw_path_line
from utils.render import draw_step_counters, draw_time_counters

# Solving the maze with the Dijkstra Algorithm
def solve_maze_with_dijkstra(grid, screen, font, draw_button, frame_count, gen_step_count, gen_time):
    start = grid[0][0]
    end = grid[GRID_HEIGHT - 1][GRID_WIDTH - 1]

    dist = {cell: float('inf') for row in grid for cell in row}
    dist[start] = 0
    pq = [(0, (start.y, start.x), start)]
    came_from = {}

    visited_cells = set()
    paused = False

    solve_step_count = 0

    # Initialize the solver timer
    start_time = time.time()
    paused_time = 0
    pause_start = None

    while pq:
        # Draw background and grid walls first
        screen.fill(WHITE)
        for row in grid:
            for cell in row:
                cell.draw(screen)

        # Draw all previously visited cells
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

        # Handle pause/quit events
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

        # Solve step
        current_dist, _, current = heapq.heappop(pq)
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path = path[::-1]
            path = [start] + path + [end]

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

            draw_path_line(screen, path, color=GREEN, width=4)

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

            if SAVE_FRAMES:  # 30 frames
                for _ in range(30):
                    pygame.image.save(screen, f"{config.FRAME_DIR}/frame_{frame_count:04d}.png")
                    frame_count += 1

            # Delay so the final path stays on screen for a moment
            pygame.time.wait(1000)
            return path

        visited_cells.add(current)

        for neighbor in get_neighbors_for_solver(current, grid, GRID_WIDTH, GRID_HEIGHT):
            if dist[current] + 1 < dist[neighbor]:
                dist[neighbor] = dist[current] + 1
                came_from[neighbor] = current
                heapq.heappush(pq, (dist[neighbor], (neighbor.y, neighbor.x), neighbor))

        # Increment step count
        solve_step_count += 1

    return []
