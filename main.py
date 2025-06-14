import pygame
import sys
from utils.setup_dependencies import install_dependencies; install_dependencies()

from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, FONT_SIZE
from config import GRID_WIDTH, GRID_HEIGHT
from config import set_frame_dir
from core.cell import Cell
from core.ui import draw_button
from core.select_ui import select_algorithm
from generators import dfs_generator, prims_generator, kruskal_generator, hunt_and_kill_generator
from solvers import dfs_solver, bfs_solver, a_star_solver, dijkstra_solver
from utils.generate_video import generate_video_from_frames

def reset_grid():
    return [[Cell(col, row) for col in range(GRID_WIDTH)] for row in range(GRID_HEIGHT)]

def reset_visited(grid):
    for row in grid:
        for cell in row:
            cell.visited = False

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze Generator & Solver - Modular")
    font = pygame.font.SysFont("Arial", FONT_SIZE)
    clock = pygame.time.Clock()

    gen_algo, solve_algo = select_algorithm(screen)

    # Set frame output path
    set_frame_dir(gen_algo, solve_algo)

    grid = reset_grid()
    frame_count = 0

    # --- GENERATION ---
    if gen_algo == 'dfs':
        frame_count, gen_steps, gen_time = dfs_generator.generate_maze(grid, screen, font, draw_button, frame_count)
    elif gen_algo == "prim's":
        frame_count, gen_steps, gen_time = prims_generator.generate_maze(grid, screen, font, draw_button, frame_count)
    elif gen_algo == 'kruskal':
        frame_count, gen_steps, gen_time = kruskal_generator.generate_maze(grid, screen, font, draw_button, frame_count)
    elif gen_algo == 'hunt-and-kill':
        frame_count, gen_steps, gen_time = hunt_and_kill_generator.generate_maze(grid, screen, font, draw_button, frame_count)

    reset_visited(grid)
    pygame.time.wait(1000)

    # --- SOLVING ---
    if solve_algo == 'dfs':
        final_path = dfs_solver.solve_maze_with_dfs(grid, screen, font, draw_button, frame_count, gen_steps, gen_time)
    elif solve_algo == 'bfs':
        final_path = bfs_solver.solve_maze_with_bfs(grid, screen, font, draw_button, frame_count, gen_steps, gen_time)
    elif solve_algo == 'a-star':
        final_path = a_star_solver.solve_maze_with_aStar(grid, screen, font, draw_button, frame_count, gen_steps, gen_time)
    elif solve_algo == 'dijkstra':
        final_path = dijkstra_solver.solve_maze_with_dijkstra(grid, screen, font, draw_button, frame_count, gen_steps, gen_time)
    else:
        final_path = []

    # --- Final Display Loop ---
    running = True
    while running:
        screen.fill(WHITE)
        for row in grid:
            for cell in row:
                cell.draw(screen)
        
        if final_path:
            from utils.render import draw_path_line
            draw_path_line(screen, final_path, color=(0, 200, 0), width=4)
        
        grid[0][0].fill(screen, (0, 0, 255))
        grid[GRID_HEIGHT - 1][GRID_WIDTH - 1].fill(screen, (255, 0, 0))

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    generate_video_from_frames(gen_algo, solve_algo)
    sys.exit()

if __name__ == "__main__":
    main()
