import pytest

from .mazegen import MazeGenerator
from .output_file import write_maze
from .parser import write_maze

# test Generator

def test_perfect_maze():
    generator = MazeGenerator(
        width=20,
        height=15,
        entry=(0, 0),
        exit=(19, 14),
        perfect=True,
        seed=42,
    )

    generator.generate()

    assert generator.perfect is True
    assert generator.validate_connectivity()
    assert generator.validate_perfect()

    assert (
        generator.count_open_connections()
        == generator.count_maze_cells() - 1
    )


def test_imperfect_maze():
    generator = MazeGenerator(
        width=20,
        height=15,
        entry=(0, 0),
        exit=(19, 14),
        perfect=False,
        seed=42,
    )

    generator.generate()

    assert generator.perfect is False
    assert generator.validate_connectivity()

    assert (
        generator.count_open_connections()
        > generator.count_maze_cells() - 1
    )


# test parser

def test_parser_perfect_true(monkeypatch, tmp_path):
    config_file = tmp_path / "config.txt"

    config_file.write_text(
        """SEED=42
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
"""
    )

    monkeypatch.setattr(
        "sys.argv",
        ["a_maze_ing.py", str(config_file)],
    )

    config = parser()

    assert config.perfect is True
    assert isinstance(config.perfect, bool)


def test_parser_perfect_false(monkeypatch, tmp_path):
    config_file = tmp_path / "config.txt"

    config_file.write_text(
        """SEED=42
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=False
"""
    )

    monkeypatch.setattr(
        "sys.argv",
        ["a_maze_ing.py", str(config_file)],
    )

    config = parser()

    assert config.perfect is False
    assert isinstance(config.perfect, bool)


# test config and complete chain

def test_config_to_perfect_maze(monkeypatch, tmp_path):
    config_file = tmp_path / "config.txt"

    config_file.write_text(
        """SEED=42
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
"""
    )

    monkeypatch.setattr(
        "sys.argv",
        ["a_maze_ing.py", str(config_file)],
    )

    config = parser()

    assert config.perfect is True

    generator = MazeGenerator(
        width=config.width,
        height=config.height,
        entry=config.maze_entry,
        exit=config.maze_exit,
        perfect=config.perfect,
        seed=config.seed,
    )

    generator.generate()

    assert generator.perfect is True
    assert generator.validate_perfect()
    assert (
        generator.count_open_connections()
        == generator.count_maze_cells() - 1
    )


# does same seed give perfect maze?

def test_perfect_maze_is_reproducible():
    maze1 = MazeGenerator(
        width=20,
        height=15,
        entry=(0, 0),
        exit=(19, 14),
        perfect=True,
        seed=42,
    )

    maze2 = MazeGenerator(
        width=20,
        height=15,
        entry=(0, 0),
        exit=(19, 14),
        perfect=True,
        seed=42,
    )

    maze1.generate()
    maze2.generate()

    assert maze1.to_hex() == maze2.to_hex()


# does perfect = TRUE accidentally add loops?

def test_perfect_maze_has_no_extra_connections():
    generator = MazeGenerator(
        width=20,
        height=15,
        entry=(0, 0),
        exit=(19, 14),
        perfect=True,
        seed=42,
    )

    generator.generate()

    cells = generator.count_maze_cells()
    connections = generator.count_open_connections()

    assert connections == cells - 1

                       