# Grid Size Parametres
CELL_SIZE = 25
GRID_WIDTH = 15
GRID_HEIGHT = 15
PADDING = 50

# Ensure even dimensions for ffmpeg (H.264 requires it)
def make_even(x):
    return x if x % 2 == 0 else x + 1

SCREEN_WIDTH = make_even(CELL_SIZE * GRID_WIDTH + 2 * PADDING)
SCREEN_HEIGHT = make_even(CELL_SIZE * GRID_HEIGHT + 2 * PADDING + 50)

# Colors used in the animation
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED   = (200, 0, 0)
GRAY  = (200, 200, 200)
FONT_SIZE = 24

# Video saving
SAVE_FRAMES = True
DELAY = 100  # in ms

# Dynamic frame directory, default fallback
FRAME_DIR = "frames"

def set_frame_dir(gen_algo, solve_algo):
    global FRAME_DIR
    FRAME_DIR = f"frames_{gen_algo.upper()}_{solve_algo.upper()}"
