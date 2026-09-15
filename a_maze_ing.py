import sys

from src.maze_builder import create_maze
from src.tui import tui


def main() -> int:
    """creates a maze and starts tui"""
    try:
        config = create_maze()
    except Exception as e:
        print(f"Error: {e}")
        return 1

    tui(config.output_file, config)
    return 0


if __name__ == "__main__":
    sys.exit(main())
