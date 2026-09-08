from sys import argv


def parser() -> int:
    """DocStrings"""
    with open(argv[1]) as file:
        print(f"{file.read()}")
    return 0
