from src import parser, MazeGenerator, write_maze, tui


def main() -> int:
    """DocStrings"""
    config = parser()
    try:
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
        tui(config.output_file)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
    return 0


if __name__ == "__main__":
    main()
