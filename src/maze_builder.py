from .parser import parser, MazeConfig
from .mazegen.generator import MazeGenerator
from .output_file import write_maze


def create_maze() -> "MazeConfig":
    """parses config, generates a maze,
    creates output file, returns config
    """
    config = parser()
    maze = MazeGenerator(
        width=config.width,
        height=config.height,
        entry=config.maze_entry,
        exit=config.maze_exit,
        perfect=config.perfect,
        seed=config.seed,
    )
    maze.generate()
    write_maze(
        config.output_file, maze
    )
    return config
