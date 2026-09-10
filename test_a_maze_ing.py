"""from a_maze_ing import main


def test_a_maze_ing() -> None:
    #Pytest for MazeGenerator or any function
    main()
    return"""
import pytest

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
    
    print("pattern:", generator.get_42_pattern())
    print("connected:", generator.validate_connectivity())
    print("connections:", generator.count_open_connections())

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
    assert (
        generator.count_open_connections()
        > generator.count_maze_cells() - 1
	)
    
def test_42_pattern():
    """Test that the 42 pattern contains fully closed cells."""
    generator = MazeGenerator(
        width=10,
        height=10,
        entry=(0, 0),
        exit=(9, 9),
        perfect=True,
        seed=42,
    )

    pattern = generator.get_42_pattern()

    assert len(pattern) == 18

    for x, y in pattern:
        assert generator.maze[y][x].walls == 0b1111
        
"""def test_42_pattern_remains_closed():
    #Test that the 42 pattern cells remain closed after generating.
    generator = MazeGenerator(
        width=10,
        height=10,
        entry=(0, 0),
        exit=(9, 9),
        perfect=True,
        seed=42,
    )

    generator.generate()

    pattern = generator.get_42_pattern()

    #for x, y in pattern:
        #assert generator.maze[y][x].walls == 0b1111  
        
    for y in range(generator.height):
        line = ""
        
        for x in range(generator.width):
            if generator.maze[y][x].walls == 0b1111:
                line += "#"
            else:
                line += "."
                
        print(line)        """

def test_42_cell():
    """Test that identifies cells that are part of the 42 pattern"""
    generator = MazeGenerator(
        width=10,
        height=10,
        entry=(0, 0),
        exit=(9, 9),
        perfect=True,
        seed=42,
    )

    assert generator.is_42_cell((2, 2))
    assert generator.is_42_cell((7, 6))
    assert not generator.is_42_cell((4, 4))
    
def test_42_pattern_is_centered():
    """Test that the 42 pattern is centered."""
    generator = MazeGenerator(
        width=20,
        height=15,
        entry=(0, 0),
        exit=(19, 14),
        perfect=True,
        seed=42,
    )

    pattern = generator.get_42_pattern()

    assert (7, 5) in pattern
    assert (12, 9) in pattern
    assert len(pattern) == 18   
     
def test_is_maze_cell():
    """Test identifying normal maze cells"""
    generator = MazeGenerator(
        width=10,
        height=10,
        entry=(0, 0),
        exit=(9, 9),
        perfect=True,
        seed=42,
    )

    assert not generator.is_maze_cell((2, 2))
    assert generator.is_maze_cell((4, 4))    
    
def test_count_maze_cell():
    """Test counting cells that belong to maze"""
    generator = MazeGenerator(
        width=10,
        height=10,
        entry=(0, 0),
        exit=(9, 9),
        perfect=True,
        seed=42,
    )

    assert generator.count_maze_cells() == 82   
    
def test_42_cells_are_closed():
    """Test that all 42 cells have all walls closed"""
    generator = MazeGenerator(
        width=20,
        height=15,
        entry=(0, 0),
        exit=(19, 14),
        perfect=True,
        seed=42,
    )

    generator.generate()

    for position in generator.get_42_pattern():
        x, y = position
        assert generator.maze[y][x].walls == 0b1111      
        
def test_42_pattern_not_used_when_maze_is_too_small():
    """Test that small mazes do not reserve 42 cells"""
    generator = MazeGenerator(
        width=6,
        height=5,
        entry=(0, 0),
        exit=(5, 4),
        perfect=True,
        seed=42,
    )

    assert generator.get_42_pattern() == set()    
    
def test_entry_exit_not_42():
    """Test that entry and exit cannot be 42 cells"""
    generator = MazeGenerator(
        width=10,
        height=10,
        entry=(2, 2),
        exit=(9, 9),
        perfect=True,
        seed=42,
    )

    assert not generator.validate_entry_exit()

def test_entry_exit_are_valid():
    """Test valid entry and exit cells"""
    generator = MazeGenerator(
        width=10,
        height=10,
        entry=(0, 0),
        exit=(9, 9),
        perfect=True,
        seed=42,
    )

    assert generator.validate_entry_exit()   
    
def test_generation_rejects_42_entry():
    """Test that generation rejects an entry inside the 42 pattern"""
    generator = MazeGenerator(
        width=10,
        height=10,
        entry=(2, 2),
        exit=(9, 9),
        perfect=True,
        seed=42,
    )

    with pytest.raises(ValueError):
        generator.generate()    
        
def test_same_seed_produces_same_maze():
    """Test that the same seed produces the same maze."""
    generator1 = MazeGenerator(
        width=20,
        height=15,
        entry=(0, 0),
        exit=(19, 14),
        perfect=True,
        seed=42,
    )

    generator2 = MazeGenerator(
        width=20,
        height=15,
        entry=(0, 0),
        exit=(19, 14),
        perfect=True,
        seed=42,
    )

    generator1.generate()
    generator2.generate()

    assert generator1.to_hex() == generator2.to_hex()     
          
def test_hex_dimensions():
    """Test that hex output matches maze dimensions"""
    generator = MazeGenerator(
        width=20,
        height=15,
        entry=(0, 0),
        exit=(19, 14),
        perfect=True,
        seed=42,
    )

    generator.generate()
    rows = generator.to_hex()
    
    assert len(rows) == 15
    assert all(len(row) == 20 for row in rows)
    
def test_write_maze_contains_solution(tmp_path):
    """Test that the maze file contains the shortest path."""
    generator = MazeGenerator(
        width=3,
        height=3,
        entry=(0, 0),
        exit=(2, 2),
        perfect=True,
        seed=42,
    )
    generator.generate()

    output_file = tmp_path / "maze.txt"
    write_maze(str(output_file), generator)

    lines = output_file.read_text().splitlines()

    assert len(lines) == 7
    assert lines[3] == ""
    assert lines[4] == "0,0"
    assert lines[5] == "2,2"
    assert lines[6] == generator.path_to_directions(generator.solve())    