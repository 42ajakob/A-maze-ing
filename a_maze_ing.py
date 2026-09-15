from src import parser, MazeGenerator, write_maze, tui


def main() -> int:
    """DocStrings"""
    config = parser()
    try:
        maze = MazeGenerator(config)
        output_file = write_maze(maze)
        tui(output_file)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
    return 0


if __name__ == "__main__":
    main()
