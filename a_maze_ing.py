from src import parser, MazeGenerator, write_maze, tui

def create_maze() -> "MazeConfig":
    """parses config, generates a maze,
    creates output file, returns config
    """
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
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
    return config

def main() -> int:
    """creates a maze and starts tui"""
    config = create_maze()
    tui(config.output_file, config)

    return 0


if __name__ == "__main__":
    main()
