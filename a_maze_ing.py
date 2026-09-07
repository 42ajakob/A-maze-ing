from Utils import Validator, Parser, MazeGen, OutFileCreator, TUI


def main() -> int:
    """DocStrings"""
    try:
        Validator()
        ParsedData = Parser()
        Maze = MazeGen(ParsedData)
        OutFile = OutFileCreator(Maze)
        TUI(OutFile)
    except Exception as e:
        print(f"Error: {e}")
        return 2
    return 0


if __name__ == "__main__":
    exit(main())
