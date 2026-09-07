from sys import argv


def Parser() -> int:
    """DocStrings"""
    with open(argv[1]) as file:
        print(f"{file.read()}")
    return 0
