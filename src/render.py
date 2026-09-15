from .maze_io import Maze, N, E, S, W
from .mazegen.generator import get_42_pattern

WALL_CH = "*"
OPEN_CH = " "
PATH_CH = "."
ENTRY_CH = "S"
EXIT_CH = "X"
PATTERN_CH = "#"

TAG_WALL = "wall"
TAG_OPEN = "open"
TAG_PATH = "path"
TAG_ENTRY = "entry"
TAG_EXIT = "exit"
TAG_PATTERN = "pattern"

DELTA = {
    "N": (0, -1),
    "S": (0, 1),
    "E": (1, 0),
    "W": (-1, 0),
}


def cell_center(x: int, y: int) -> tuple[int, int]:
    """Row, col of the centre of cell (x, y) in the character grid."""
    return 2 * y + 1, 2 * x + 1


def build_char_grid(maze: Maze) -> tuple[list[list[str]], list[list[str]]]:
    """
    Returns (chars, tags): two grids of identical shape
    (2*height+1 rows x 2*width+1 cols).
    """
    rows = 2 * maze.height + 1
    cols = 2 * maze.width + 1
    chars = [[WALL_CH for _ in range(cols)] for _ in range(rows)]
    tags = [[TAG_WALL for _ in range(cols)] for _ in range(rows)]

    for y in range(maze.height):
        for x in range(maze.width):
            mask = maze.grid[y][x]
            r, c = cell_center(x, y)
            chars[r][c] = OPEN_CH
            tags[r][c] = TAG_OPEN

            if not (mask & N):
                chars[r - 1][c] = OPEN_CH
                tags[r - 1][c] = TAG_OPEN
            if not (mask & S):
                chars[r + 1][c] = OPEN_CH
                tags[r + 1][c] = TAG_OPEN
            if not (mask & E):
                chars[r][c + 1] = OPEN_CH
                tags[r][c + 1] = TAG_OPEN
            if not (mask & W):
                chars[r][c - 1] = OPEN_CH
                tags[r][c - 1] = TAG_OPEN

    return chars, tags


def path_cells(maze: Maze) -> list[tuple[int, int]]:
    """list of (x, y) cell coordinates visited along the solution path,
    in order, including entry and exit."""
    x, y = maze.entry
    cells = [(x, y)]
    for step in maze.path:
        dx, dy = DELTA[step]
        x, y = x + dx, y + dy
        cells.append((x, y))
    return cells


def path_char_positions(maze: Maze) -> set[tuple[int, int]]:
    """Character-grid (row, col) positions to highlight for the path,
    including the corridor cell between each pair of maze cells."""
    cells = path_cells(maze)
    positions: set[tuple[int, int]] = set()
    prev = cell_center(*cells[0])
    positions.add(prev)
    for x, y in cells[1:]:
        r, c = cell_center(x, y)
        mid = ((prev[0] + r) // 2, (prev[1] + c) // 2)
        positions.add(mid)
        positions.add((r, c))
        prev = (r, c)
    return positions


def apply_entry_exit_and_path(
    chars: list[list[str]],
    tags: list[list[str]],
    maze: Maze,
    show_path: bool,
) -> None:
    """Mark entry, exit and, if enabled, the solution path on the char grid."""
    if show_path:
        for r, c in path_char_positions(maze):
            if tags[r][c] == TAG_OPEN:
                chars[r][c] = PATH_CH
                tags[r][c] = TAG_PATH

    er, ec = cell_center(*maze.entry)
    chars[er][ec] = ENTRY_CH
    tags[er][ec] = TAG_ENTRY

    xr, xc = cell_center(*maze.exit)
    chars[xr][xc] = EXIT_CH
    tags[xr][xc] = TAG_EXIT


def apply_42_pattern(
    chars: list[list[str]],
    tags: list[list[str]],
    maze: Maze,
    show_42: bool,
) -> None:
    """Mark the 42 pattern cells on the char grid, if enabled."""
    if not show_42:
        return

    for x, y in get_42_pattern(maze.width, maze.height):
        r, c = cell_center(x, y)
        if tags[r][c] == TAG_OPEN:
            chars[r][c] = PATTERN_CH
            tags[r][c] = TAG_PATTERN
