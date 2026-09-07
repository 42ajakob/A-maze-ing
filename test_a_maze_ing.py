from a_maze_ing import main


def test_a_maze_ing() -> int:
    """Pytest for MazeGenerator or any function"""
    result = main()
    if result:
        return 0
    return 1
