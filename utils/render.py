import pygame
from config import CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, PADDING, GREEN

# Draws the path line
def draw_path_line(screen, path, color=GREEN, width=4):
    points = [
        (
            PADDING + cell.x * CELL_SIZE + CELL_SIZE // 2,
            PADDING + cell.y * CELL_SIZE + CELL_SIZE // 2
        )
        for cell in path
    ]
    if len(points) > 1:
        pygame.draw.lines(screen, color, False, points, width)

# Displays the counter
def draw_step_counters(screen, gen_steps, solve_steps, phase=None):
    font = pygame.font.SysFont("Arial", 15)
    y_pos = SCREEN_HEIGHT - 85  # Just above the pause button

    # Left: Generation Steps
    gen_label = font.render(f"Generation Steps = {gen_steps}", True, (0, 0, 0))
    gen_rect = gen_label.get_rect()
    gen_rect.left = 50
    gen_rect.top = y_pos
    screen.blit(gen_label, gen_rect)

    # Right: Solver Steps
    solve_label = font.render(f"Solver Steps = {solve_steps}", True, (0, 0, 0))
    solve_rect = solve_label.get_rect()
    solve_rect.right = SCREEN_WIDTH - 50
    solve_rect.top = y_pos
    screen.blit(solve_label, solve_rect)

def format_time(seconds):
    mins = int(seconds) // 60
    secs = seconds % 60
    return f"{mins:02}:{secs:04.1f}"

def draw_time_counters(screen, gen_time, solve_time):
    font = pygame.font.SysFont("Arial", 15)
    y_pos = 22

    # Left: Generation Time
    gen_time_label = font.render(f"Generation Time = {format_time(gen_time)}", True, (0, 0, 0))
    gen_time_rect = gen_time_label.get_rect()
    gen_time_rect.left = 50
    gen_time_rect.top = y_pos
    screen.blit(gen_time_label, gen_time_rect)

    # Right: Solver Time
    solve_time_label = font.render(f"Solver Time = {format_time(solve_time)}", True, (0, 0, 0))
    solve_time_rect = solve_time_label.get_rect()
    solve_time_rect.right = SCREEN_WIDTH - 50
    solve_time_rect.top = y_pos
    screen.blit(solve_time_label, solve_time_rect)
