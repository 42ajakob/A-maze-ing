from dataclasses import dataclass
from typing import List, Tuple

N, E, S, W = 0b0001, 0b0010, 0b0100, 0b1000


@dataclass
class Maze:
    grid: List[List[int]]      # grid[y][x] -> 4-bit wall mask (bit=closed)
    width: int
    height: int
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    path: str                  # sequence of N/E/S/W moves from entry to exit


def parse_output_file(path: str) -> Maze:
    with open(path) as f:
        lines = f.read().splitlines()

    # 1. grid lines: everything up to the first blank line
    grid_lines: List[str] = []
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

    grid: List[List[int]] = []
    for ln in grid_lines:
        row = [int(ch, 16) for ch in ln]
        grid.append(row)

    # 2. skip blank line(s)
    while idx < len(lines) and lines[idx].strip() == "":
        idx += 1

    remaining = [ln.strip() for ln in lines[idx:] if ln.strip() != ""]
    if len(remaining) < 3:
        raise ValueError(
            "Expected entry, exit and path lines after the maze grid"
        )

    entry_str, exit_str, path = remaining[0], remaining[1], remaining[2]

    def parse_coord(s: str) -> Tuple[int, int]:
        x_str, y_str = s.split(",")
        return int(x_str), int(y_str)

    entry = parse_coord(entry_str)
    exit_ = parse_coord(exit_str)

    path = "".join(ch for ch in path if ch in "NESW")

    return Maze(grid=grid, width=width, height=height,
                entry=entry, exit=exit_, path=path)
