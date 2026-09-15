from src.maze_builder import create_maze
from src.tui import tui


def main() -> int:
    """creates a maze and starts tui"""
    config = create_maze()
    tui(config.output_file, config)

    return 0


if __name__ == "__main__":
    main()
