from utils import validator, parser, maze_gen, out_file_creator, tui


def main() -> int:
    """DocStrings"""
    try:
        validator()
        parsed_data = parser()
        maze = maze_gen(parsed_data)
        out_file = out_file_creator(maze)
        tui(out_file)
    except Exception as e:
        print(f"Error: {e}")
        return 2
    return 0


if __name__ == "__main__":
    exit(main())
