from sys import argv, stderr


def Validator() -> int:
    """DocString"""
    if len(argv) != 2:
        stderr.write("Error: Usage python3 a_maze_ing.py <config.txt>")
        return 1
    with open(argv[1]) as file:
        print(f"{file.read()}")
    return 0
