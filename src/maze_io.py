from dataclasses import dataclass

N, E, S, W = 0b0001, 0b0010, 0b0100, 0b1000

_STEP_DELTA = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}


@dataclass
class Maze:
    """Parsed representation of a maze output file."""
    grid: list[list[int]]      # grid[y][x] -> 4-bit wall mask (bit=closed)
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    path: str                  # sequence of N/E/S/W moves from entry to exit


def parse_output_file(path: str) -> Maze:
    """Read and validate a maze output file, returning it as a Maze."""
    with open(path) as f:
        lines = f.read().splitlines()

    # 1. grid lines: everything up to the first blank line
    grid_lines: list[str] = []
    idx = 0
    while idx < len(lines) and lines[idx].strip() != "":
        grid_lines.append(lines[idx].strip())
        idx += 1

    if not grid_lines:
        raise ValueError("No maze data found in output file")

    height = len(grid_lines)
    width = len(grid_lines[0])
    for i, ln in enumerate(grid_lines):
        if len(ln) != width:
            raise ValueError(
                f"Row {i} has length {len(ln)}, expected {width} "
                f"(ragged maze grid)"
            )

    grid: list[list[int]] = []
    for ln in grid_lines:
        row = [int(ch, 16) for ch in ln]
        grid.append(row)

    # 2. skip blank line(s)
    while idx < len(lines) and lines[idx].strip() == "":
        idx += 1

    remaining = lines[idx:]
    if len(remaining) < 3:
        raise ValueError(
            "Expected entry, exit and path lines after the maze grid"
        )

    entry_str, exit_str, path = (
        remaining[0].strip(), remaining[1].strip(), remaining[2].strip()
    )

    def parse_coord(s: str, label: str) -> tuple[int, int]:
        """Parse an "x,y" string into a coordinate, checked to be in bounds."""
        x_str, y_str = s.split(",")
        x, y = int(x_str), int(y_str)
        if not (0 <= x < width and 0 <= y < height):
            raise ValueError(
                f"{label} {(x, y)} is out of bounds for "
                f"width={width}, height={height}"
            )
        return x, y

    entry = parse_coord(entry_str, "entry")
    exit_ = parse_coord(exit_str, "exit")

    path = "".join(ch for ch in path if ch in "NESW")

    x, y = entry
    for step in path:
        dx, dy = _STEP_DELTA[step]
        x, y = x + dx, y + dy
        if not (0 <= x < width and 0 <= y < height):
            raise ValueError(
                f"Path walks outside the maze bounds at step {step!r} "
                f"(would reach {(x, y)})"
            )
    if (x, y) != exit_:
        raise ValueError(
            f"Path does not end at the exit: ends at {(x, y)}, "
            f"expected {exit_}"
        )

    return Maze(grid=grid, width=width, height=height,
                entry=entry, exit=exit_, path=path)
