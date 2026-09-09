"""from a_maze_ing import main


def test_a_maze_ing() -> None:
    #Pytest for MazeGenerator or any function
    main()
    return"""


from utils.maze_gen import MazeGenerator
from utils.out_file_creator import write_maze


def test_write_maze(tmp_path):
    """Test that a maze is written in required format"""
    generator = MazeGenerator(
        width=2,
        height=2,
        entry=(0, 0),
        exit=(1, 1),
        perfect=True,
        seed=42,
    )

    generator.generate()

    output_file = tmp_path / "test_maze.txt"

    write_maze(str(output_file), generator)

    content = output_file.read_text()

    lines = content.splitlines()

    assert len(lines) == 6
    assert lines[2] == ""
    assert lines[3] == "0,0"
    assert lines[4] == "1,1"
    assert lines[5] == generator.path_to_directions(generator.solve())

def test_path_to_directions():
    """Test converting a coordinate path into directions"""
    generator = MazeGenerator(
        width=3,
        height=3,
        entry=(0, 0),
        exit=(2, 2),
        perfect=True,
        seed=42,
	)
    
    path = [
        (0, 0),
        (1, 0),
        (1, 1),
        (2, 1),
        (2, 2),
	]
    
    directions = generator.path_to_directions(path)
    
    assert directions == "ESES"

def test_solve():
    """Testing that the solver finds a valid path"""
    generator = MazeGenerator(
			width=3,
			height=3,
			entry=(0, 0),
			exit=(2, 2),
			perfect=True,
			seed=42,
		)
    
    generator.generate()
    
    path = generator.solve()
    
    assert path[0] == (0, 0)
    assert path[-1] == (2, 2)

def test_connection_open_walls():
    """Testing that every pair of cells is connected by an open wall"""
    generator = MazeGenerator(
			width=3,
			height=3,
			entry=(0, 0),
			exit=(2, 2),
			perfect=True,
			seed=42,
		)
    
    generator.generate()
    path = generator.solve()
    
    for current, next_cell in zip(path, path[1:]):
        assert next_cell in generator.get_open_neighbours(current)

def test_perfect_maze():
    """Testing that a perfect maze has one path only"""
    generator = MazeGenerator(
			width=10,
			height=10,
			entry=(0, 0),
			exit=(9, 9),
			perfect=True,
			seed=42,
		)
    
    generator.generate()
    
    assert generator.validate_perfect()

def test_closed_walls():
    """Testing that closed walls within the maze can be found"""
    generator = MazeGenerator(
			width=2,
			height=2,
			entry=(0, 0),
			exit=(1, 1),
			perfect=True,
			seed=42,
		)
    
    closed_walls = generator.find_closed_walls()
    
    assert len(closed_walls) == 4

def test_not_perfect_maze():
    """Testing that a not perfect maze can have additional connections"""
    generator = MazeGenerator(
			width=10,
			height=10,
			entry=(0, 0),
			exit=(9, 9),
			perfect=False,
			seed=42,
		)

    generator.generate()

    assert generator.validate_connectivity()
    assert generator.count_open_connections() > 10 * 10 - 1