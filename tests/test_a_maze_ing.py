import pytest
from pathlib import Path

from mazegen import MazeGenerator
from utils.out_file_creator import write_maze


def test_write_maze(tmp_path: Path) -> None:
    """Test that a maze is written in required format."""
    generator = MazeGenerator(
        width=2,
        height=2,
        entry=(0, 0),
        exit=(1, 1),
        perfect=True,
        seed=42,
    )

    generator.generate()

    output_file = tmp_path / "test_maze.txt"

    write_maze(str(output_file), generator)

    content = output_file.read_text()

    lines = content.splitlines()

    assert len(lines) == 6
    assert lines[2] == ""
    assert lines[3] == "0,0"
    assert lines[4] == "1,1"
    assert lines[5] == generator.path_to_directions(generator.solve())


def test_path_to_directions() -> None:
    """Test converting a coordinate path into directions."""
    generator = MazeGenerator(
        width=3,
        height=3,
        entry=(0, 0),
        exit=(2, 2),
        perfect=True,
        seed=42,
    )

    path = [
        (0, 0),
        (1, 0),
        (1, 1),
        (2, 1),
        (2, 2),
    ]

    directions = generator.path_to_directions(path)

    assert directions == "ESES"


def test_solve() -> None:
    """Test that the solver finds a valid path."""
    generator = MazeGenerator(
        width=3,
        height=3,
        entry=(0, 0),
        exit=(2, 2),
        perfect=True,
        seed=42,
    )

    generator.generate()

    path = generator.solve()

    assert path[0] == (0, 0)
    assert path[-1] == (2, 2)


def test_connection_open_walls() -> None:
    """Test that every pair of cells is connected by an open wall."""
    generator = MazeGenerator(
        width=3,
        height=3,
        entry=(0, 0),
        exit=(2, 2),
        perfect=True,
        seed=42,
    )

    generator.generate()
    path = generator.solve()

    for current, next_cell in zip(path, path[1:]):
        assert next_cell in generator.get_open_neighbours(current)


def test_perfect_maze() -> None:
    """Test that a perfect maze has one path only."""
    generator = MazeGenerator(
        width=10,
        height=10,
        entry=(0, 0),
        exit=(9, 9),
        perfect=True,
        seed=42,
    )

    generator.generate()

    assert generator.validate_perfect()


def test_closed_walls() -> None:
    """Test that closed walls within the maze can be found."""
    generator = MazeGenerator(
        width=2,
        height=2,
        entry=(0, 0),
        exit=(1, 1),
        perfect=True,
        seed=42,
    )

    closed_walls = generator.find_closed_walls()

    assert len(closed_walls) == 4


def test_not_perfect_maze() -> None:
    """Test that a not perfect maze can have additional connections."""
    generator = MazeGenerator(
        width=10,
        height=10,
        entry=(0, 0),
        exit=(9, 9),
        perfect=False,
        seed=42,
    )

    generator.generate()

    assert generator.validate_connectivity()
    assert (
        generator.count_open_connections()
        > generator.count_maze_cells() - 1
    )


def test_42_pattern() -> None:
    """Test that the 42 pattern contains fully closed cells."""
    generator = MazeGenerator(
        width=10,
        height=10,
        entry=(0, 0),
        exit=(9, 9),
        perfect=True,
        seed=42,
    )

    pattern = generator.get_42_pattern()

    assert len(pattern) == 18

    for x, y in pattern:
        assert generator.maze[y][x].walls == 0b1111


def test_42_cell() -> None:
    """Test that identifies cells that are part of the 42 pattern."""
    generator = MazeGenerator(
        width=10,
        height=10,
        entry=(0, 0),
        exit=(9, 9),
        perfect=True,
        seed=42,
    )

    assert generator.is_42_cell((2, 2))
    assert generator.is_42_cell((7, 6))
    assert not generator.is_42_cell((4, 4))


def test_42_pattern_is_centered() -> None:
    """Test that the 42 pattern is centered."""
    generator = MazeGenerator(
        width=20,
        height=15,
        entry=(0, 0),
        exit=(19, 14),
        perfect=True,
        seed=42,
    )

    pattern = generator.get_42_pattern()

    assert (7, 5) in pattern
    assert (12, 9) in pattern
    assert len(pattern) == 18


def test_is_maze_cell() -> None:
    """Test identifying normal maze cells."""
    generator = MazeGenerator(
        width=10,
        height=10,
        entry=(0, 0),
        exit=(9, 9),
        perfect=True,
        seed=42,
    )

    assert not generator.is_maze_cell((2, 2))
    assert generator.is_maze_cell((4, 4))


def test_count_maze_cell() -> None:
    """Test counting cells that belong to maze."""
    generator = MazeGenerator(
        width=10,
        height=10,
        entry=(0, 0),
        exit=(9, 9),
        perfect=True,
        seed=42,
    )

    assert generator.count_maze_cells() == 82


def test_42_cells_are_closed() -> None:
    """Test that all 42 cells have all walls closed."""
    generator = MazeGenerator(
        width=20,
        height=15,
        entry=(0, 0),
        exit=(19, 14),
        perfect=True,
        seed=42,
    )

    generator.generate()

    for position in generator.get_42_pattern():
        x, y = position
        assert generator.maze[y][x].walls == 0b1111


def test_42_pattern_not_used_when_maze_is_too_small() -> None:
    """Test that small mazes do not reserve 42 cells."""
    generator = MazeGenerator(
        width=6,
        height=5,
        entry=(0, 0),
        exit=(5, 4),
        perfect=True,
        seed=42,
    )

    assert generator.get_42_pattern() == set()


def test_entry_exit_not_42() -> None:
    """Test that entry and exit cannot be 42 cells."""
    generator = MazeGenerator(
        width=10,
        height=10,
        entry=(2, 2),
        exit=(9, 9),
        perfect=True,
        seed=42,
    )

    assert not generator.validate_entry_exit()


def test_entry_exit_are_valid() -> None:
    """Test valid entry and exit cells."""
    generator = MazeGenerator(
        width=10,
        height=10,
        entry=(0, 0),
        exit=(9, 9),
        perfect=True,
        seed=42,
    )

    assert generator.validate_entry_exit()


def test_generation_rejects_42_entry() -> None:
    """Test that generation rejects an entry inside the 42 pattern."""
    generator = MazeGenerator(
        width=10,
        height=10,
        entry=(2, 2),
        exit=(9, 9),
        perfect=True,
        seed=42,
    )

    with pytest.raises(ValueError):
        generator.generate()


def test_generation_rejects_42_exit() -> None:
    """Test that generation rejects an exit inside the 42 pattern."""
    generator = MazeGenerator(
        width=10,
        height=10,
        entry=(0, 0),
        exit=(2, 2),
        perfect=True,
        seed=42,
    )

    with pytest.raises(ValueError):
        generator.generate()


def test_same_seed_produces_same_maze() -> None:
    """Test that the same seed produces the same maze."""
    generator1 = MazeGenerator(
        width=20,
        height=15,
        entry=(0, 0),
        exit=(19, 14),
        perfect=True,
        seed=42,
    )

    generator2 = MazeGenerator(
        width=20,
        height=15,
        entry=(0, 0),
        exit=(19, 14),
        perfect=True,
        seed=42,
    )

    generator1.generate()
    generator2.generate()

    assert generator1.to_hex() == generator2.to_hex()


def test_hex_dimensions() -> None:
    """Test that hex output matches maze dimensions."""
    generator = MazeGenerator(
        width=20,
        height=15,
        entry=(0, 0),
        exit=(19, 14),
        perfect=True,
        seed=42,
    )

    generator.generate()
    rows = generator.to_hex()

    assert len(rows) == 15
    assert all(len(row) == 20 for row in rows)


def test_write_maze_contains_solution(tmp_path: Path) -> None:
    """Test that the maze file contains the shortest path."""
    generator = MazeGenerator(
        width=3,
        height=3,
        entry=(0, 0),
        exit=(2, 2),
        perfect=True,
        seed=42,
    )

    generator.generate()

    output_file = tmp_path / "maze.txt"
    write_maze(str(output_file), generator)

    lines = output_file.read_text().splitlines()

    assert len(lines) == 7
    assert lines[3] == ""
    assert lines[4] == "0,0"
    assert lines[5] == "2,2"
    assert lines[6] == generator.path_to_directions(generator.solve())


def test_42_size_is_valid() -> None:
    """Test that a large enough maze can display 42."""
    generator = MazeGenerator(
        width=20,
        height=15,
        entry=(0, 0),
        exit=(19, 14),
        perfect=True,
        seed=42,
    )

    assert generator.validate_42_size()


def test_42_size_is_too_small() -> None:
    """Test that a small maze cannot display 42."""
    generator = MazeGenerator(
        width=6,
        height=5,
        entry=(0, 0),
        exit=(5, 4),
        perfect=True,
        seed=42,
    )

    assert not generator.validate_42_size()


def test_corridor_width_validation() -> None:
    """Reject a completely open 3x3 area."""
    generator = MazeGenerator(
        width=5,
        height=5,
        entry=(0, 0),
        exit=(4, 4),
        perfect=False,
    )

    for y in range(3):
        for x in range(3):
            if x < 2:
                generator.remove_wall((x, y), (x + 1, y))
            if y < 2:
                generator.remove_wall((x, y), (x, y + 1))

    assert not generator.validate_corridor_width()


def test_two_by_three_corridor_is_allowed() -> None:
    """Allow an open area that is only two cells wide."""
    generator = MazeGenerator(
        width=5,
        height=5,
        entry=(0, 0),
        exit=(4, 4),
        perfect=False,
    )

    for y in range(3):
        generator.remove_wall((0, y), (1, y))

        if y < 2:
            generator.remove_wall((0, y), (0, y + 1))
            generator.remove_wall((1, y), (1, y + 1))

    assert generator.validate_corridor_width()


def test_open_area_three_by_two_is_valid() -> None:
    """A completely open area two cells wide is allowed."""
    generator = MazeGenerator(
        width=5,
        height=5,
        entry=(0, 0),
        exit=(4, 4),
        perfect=False,
    )

    for x in range(3):
        generator.remove_wall((x, 0), (x, 1))

        if x < 2:
            generator.remove_wall((x, 0), (x + 1, 0))
            generator.remove_wall((x, 1), (x + 1, 1))

    assert generator.validate_corridor_width()


def test_generated_maze_has_valid_corridor_width() -> None:
    """Generated mazes must not contain 3x3 open areas."""
    generator = MazeGenerator(
        width=20,
        height=15,
        entry=(0, 0),
        exit=(19, 14),
        perfect=False,
        seed=42,
    )

    generator.generate()

    assert generator.validate_corridor_width()
