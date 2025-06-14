from core.cell import DIRS

# Removes the wall between the cells
def remove_walls(a, b):
    dx = b.x - a.x
    dy = b.y - a.y
    if dx == 1:     # b is right of a
        a.walls[1] = False
        b.walls[3] = False
    elif dx == -1:  # b is left of a
        a.walls[3] = False
        b.walls[1] = False
    elif dy ==  1:  # b is below a
        a.walls[2] = False
        b.walls[0] = False
    elif dy == -1:  # b is above a
        a.walls[0] = False
        b.walls[2] = False

# Gets the unvisited neighbours of a cell
def get_unvisited_neighbors(cell, grid, width, height):
    neighbors = []
    for dx, dy in DIRS.values():
        nx, ny = cell.x + dx, cell.y + dy
        if 0 <= nx < width and 0 <= ny < height:
            neighbor = grid[ny][nx]
            if not neighbor.visited:
                neighbors.append(neighbor)
    return neighbors

# Gets neighbors of a cell
def get_neighbors_for_solver(cell, grid, width, height):
    neighbors = []
    x, y = cell.x, cell.y

    if not cell.walls[0] and y > 0:
        neighbors.append(grid[y - 1][x])  # top
    if not cell.walls[1] and x < width - 1:
        neighbors.append(grid[y][x + 1])  # right
    if not cell.walls[2] and y < height - 1:
        neighbors.append(grid[y + 1][x])  # bottom
    if not cell.walls[3] and x > 0:
        neighbors.append(grid[y][x - 1])  # left

    return neighbors
