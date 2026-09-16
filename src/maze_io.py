from dataclasses import dataclass
from src import MazeConfig


@dataclass
class Maze:
    """Parsed representation of a maze output file"""
    grid: list[list[int]]      # grid[y][x] -> 4-bit wall mask (bit=closed)
    path: str                  # sequence of N/E/S/W moves from entry to exit


def parse_output_file(config: "MazeConfig") -> Maze:
    """Read maze output file, returning it as a Maze class"""
    with open(config.output_file) as f:
        lines = f.read().splitlines()

    grid_lines: list[str] = []
    idx = 0
    while idx < len(lines) and lines[idx] != "":
        grid_lines.append(lines[idx])
        idx += 1

    if len(grid_lines) != config.height:
        raise ValueError(
            f"{config.output_file}: expected {config.height} grid rows, "
            f"found {len(grid_lines)}"
        )

    grid: list[list[int]] = []
    for row_idx, line in enumerate(grid_lines):
        if len(line) != config.width:
            raise ValueError(
                f"{config.output_file}: row {row_idx} has {len(line)} "
                f"columns, expected {config.width}"
            )
        try:
            row = [int(ch, 16) for ch in line]
        except ValueError:
            raise ValueError(
                f"{config.output_file}: row {row_idx} contains a "
                f"non-hex character: {line}"
            ) from None
        grid.append(row)

    idx += 1
    remaining = lines[idx:]
    if len(remaining) < 3 or len(remaining) > 3:
        raise ValueError(
            f"{config.output_file}: invalid output "
            "format for entry, exit, path"
        )
    path = remaining[2]

    return Maze(grid=grid, path=path)
