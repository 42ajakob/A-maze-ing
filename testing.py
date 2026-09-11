from utils.maze_gen import MazeGenerator
from utils.out_file_creator import write_maze

generator = MazeGenerator(
        width=20,
        height=15,
        entry=(0, 0),
        exit=(19, 14),
        perfect=True,
        seed=42,
    )

generator.generate()

# print(generator.to_hex())

write_maze("maze.txt.", generator)
