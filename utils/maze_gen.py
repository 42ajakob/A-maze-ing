import random

NORTH = 0b0001
EAST = 0b0010
SOUTH = 0b0100
WEST = 0b1000

class Cell:
    """Single cell in the maze"""

    def __init__(self) -> None:
        """Initialize a cell with all walls closed"""
        self.walls: int = 0b1111

class MazeGenerator:
    """Generate a maze"""

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        perfect: bool,
        seed: int | None = None,
    ) -> None:
        """Initialize the maze generator"""
        self.width: int = width
        self.height: int = height
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit
        self.perfect: bool = perfect
        self.seed: int | None = seed
        self.random = random.Random(seed)

        self.maze: list[list[Cell]] = [
            [Cell() for _ in range(width)]
            for _ in range(height)
        ]

    def remove_wall(
    	self,
    	first: tuple[int, int],
    	second: tuple[int, int],
    ) -> None:
        """Open the wall between two neighbouring cells"""
        x1, y1 = first
        x2, y2 = second

        if not (0 <= x1 < self.width and 0 <= y1 < self.height):
            raise ValueError("First cell is outside of the maze")

        if not (0 <= x2 < self.width and 0 <= y2 < self.height):
            raise ValueError("Second cell is outside of the maze")

        cell1 = self.maze[y1][x1]
        cell2 = self.maze[y2][x2]

        if x2 == x1 + 1:
            cell1.walls &= ~EAST
            cell2.walls &= ~WEST

        elif x2 == x1 - 1:
            cell1.walls &= ~WEST
            cell2.walls &= ~EAST

        elif y2 == y1 + 1:
            cell1.walls &= ~SOUTH
            cell2.walls &= ~NORTH

        elif y2 == y1 - 1:
            cell1.walls &= ~NORTH
            cell2.walls &= ~SOUTH

        else:
            raise ValueError("Cells are not neighbouring cells")

    def get_neighbours(
    self,
    position: tuple[int, int],
    ) -> list[tuple[int, int]]:
        """Return the neighboring cells. Which cells are connected?"""
        x, y = position

        neighbours = []

        if y > 0:
            neighbours.append((x, y - 1))

        if x < self.width - 1:
            neighbours.append((x + 1, y))

        if y < self.height - 1:
            neighbours.append((x, y + 1))

        if x > 0:
            neighbours.append((x - 1, y))

        return neighbours

    def get_open_neighbours(
        self,
        position: tuple[int, int],
    ) -> list[tuple[int, int]]:
        """Return the neighbouring cells connected by an open wall. Which cells can be walked to?"""
        x, y = position
        cell = self.maze[y][x]

        open_neighbours = []

        for neighbour in self.get_neighbours(position):
            nx, ny = neighbour

            """In which direction lays the neighbour?"""
            if nx == x + 1:
                direction = EAST
            elif nx == x - 1:
                direction = WEST
            elif ny == y + 1:
                direction = SOUTH
            else:
                direction = NORTH

            """Check if the wall is open"""
            if not (cell.walls & direction):
                open_neighbours.append(neighbour)

        return open_neighbours
    
    def generate(self) -> None:
        """Generate a random maze"""
        visited: set[tuple[int, int]] = set()
        stack: list[tuple[int, int]] = []

        current = (0, 0)
        visited.add(current)
        stack.append(current)

        while stack:
            current = stack[-1]
            
            """Find the unvisited neighbours"""
            neighbors = self.get_neighbours(current)
            unvisited = [
                neighbor
                for neighbor in neighbors
                if neighbor not in visited
            ]
            """Pick one randomly and remove the wall"""
            if unvisited:
                next_cell = self.random.choice(unvisited)

                self.remove_wall(current, next_cell)

                visited.add(next_cell)
                stack.append(next_cell)

            else:
                stack.pop()

"""
TESTING FOLLOWS:


if __name__ == "__main__":
    generator = MazeGenerator(
        width=3,
        height=3,
        entry=(0, 0),
        exit=(2, 2),
        perfect=True,
        seed=42,
    )

    print("Maze size:", generator.width, "x", generator.height)
    print("Entry:", generator.entry)
    print("Exit:", generator.exit)
    print("Perfect:", generator.perfect)
    print("Seed:", generator.seed)

    print("\nWalls:")
    for row in generator.maze:
        for cell in row:
            print(bin(cell.walls), end=" ")
        print()
        
        
if __name__ == "__main__":
    generator = MazeGenerator(
        2,
        1,
        (0, 0),
        (1, 0),
        True,
        42,
    )

    generator.remove_wall((0, 0), (1, 0))

    print(bin(generator.maze[0][0].walls))
    print(bin(generator.maze[0][1].walls))

    
if __name__ == "__main__":
    generator = MazeGenerator(
        3,
        3,
        (0, 0),
        (2, 2),
        True,
        42,
    )

    print("Center:", generator.get_neighbors((1, 1)))
    print("Top-left:", generator.get_neighbors((0, 0)))
    print("Bottom-right:", generator.get_neighbors((2, 2)))

if __name__ == "__main__":
    generator = MazeGenerator(
        3,
        3,
        (0, 0),
        (2, 2),
        True,
        42,
    )

    generator.generate()

    for row in generator.maze:
        for cell in row:
            print(bin(cell.walls), end=" ")
        print()
"""

if __name__ == "__main__":
    generator = MazeGenerator(
        2,
        1,
        (0, 0),
        (1, 0),
        True,
        42,
    )

    print("Before:", generator.get_open_neighbours((0, 0)))

    generator.remove_wall((0, 0), (1, 0))

    print("After:", generator.get_open_neighbours((0, 0)))