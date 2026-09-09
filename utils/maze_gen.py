import random
from collections import deque

NORTH = 0b0001
EAST = 0b0010
SOUTH = 0b0100
WEST = 0b1000

#NORTH = 1
#EAST = 2
#SOUTH = 4
#WEST = 8

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

    def get_neighbours(
    self,
    position: tuple[int, int],
    ) -> list[tuple[int, int]]:
        """Return the neighbouring cells. Which cells are connected?"""
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
    
    def generate(self) -> None:
        """Generate a random maze"""
        visited: set[tuple[int, int]] = set()
        stack: list[tuple[int, int]] = []

        current = self.entry
        visited.add(current)
        stack.append(current)

        while stack:
            current = stack[-1]
            
            """Find the unvisited neighbours"""
            neighbours = self.get_neighbours(current)
            unvisited = [
                neighbour
                for neighbour in neighbours
                if neighbour not in visited
            ]
            """Pick one randomly and remove the wall"""
            if unvisited:
                next_cell = self.random.choice(unvisited)

                self.remove_wall(current, next_cell)

                visited.add(next_cell)
                stack.append(next_cell)

            else:
                stack.pop()

    def validate_connectivity(self) -> bool:
        """Can every cell be reached from the first cell?"""
        visited: set[tuple[int, int]] = set()
        stack: list[tuple[int, int]] = [(0, 0)]

        while stack:
            current = stack.pop()

            if current in visited:
                continue

            visited.add(current)

            for neighbour in self.get_open_neighbours(current):
                if neighbour not in visited:
                    stack.append(neighbour)

        total_cells = self.width * self.height

        return len(visited) == total_cells

    def validate_walls(self) -> bool:
        """Do neighbouring cells have matching walls?"""
        for y in range(self.height):
            for x in range(self.width):
                cell = self.maze[y][x]

                """Check East neighbour"""
                if x < self.width - 1:
                    east_cell = self.maze[y][x + 1]

                    east_wall = bool(cell.walls & EAST)
                    west_wall = bool(east_cell.walls & WEST)

                    if east_wall != west_wall:
                        return False

                """Check South neighbour"""
                if y < self.height - 1:
                    south_cell = self.maze[y + 1][x]

                    south_wall = bool(cell.walls & SOUTH)
                    north_wall = bool(south_cell.walls & NORTH)

                    if south_wall != north_wall:
                        return False

        return True

    def validate_borders(self) -> bool:
        """Are the outer borders of the maze closed?"""
        for x in range(self.width):
            if self.maze[0][x].walls & NORTH == 0:
                return False

            if self.maze[self.height - 1][x].walls & SOUTH == 0:
                return False

        for y in range(self.height):
            if self.maze[y][0].walls & WEST == 0:
                return False

            if self.maze[y][self.width - 1].walls & EAST == 0:
                return False

        return True

    #validate_connectivity() - Can I reach every cell?
    #validate_walls() - Do neighboring cells agree?
    #validate_borders() - Is the maze contained within its boundaries?
    #NOW PERFECT OPTION, FOUND OUT BZY COUNTING, CELLS-1"""

    def count_open_connections(self) -> int:
        """Count the connections between maze cells"""
        connections = 0

        for y in range(self.height):
            for x in range(self.width):
                cell = self.maze[y][x]

                if x < self.width - 1:
                    if not (cell.walls & EAST):
                        connections += 1

                if y < self.height - 1:
                    if not (cell.walls & SOUTH):
                        connections += 1

        return connections

    def validate_perfect(self) -> bool:
        """Is the maze a perfect maze?"""
        return (
            self.validate_connectivity()
            and self.count_open_connections()
            == self.width * self.height - 1
        )

    def solve(self) -> list[tuple[int, int]]:
        """Find shortest path from entry to exit."""
        queue: deque[tuple[int, int]] = deque()
        visited: set[tuple[int, int]] = set()
        previous: dict[tuple[int, int], tuple[int, int] | None] = {}

        queue.append(self.entry)
        visited.add(self.entry)
        previous[self.entry] = None

        while queue:
            #BFS: process cells in the order they were discovered
            current = queue.popleft()

            if current == self.exit:
                break

            for neighbour in self.get_open_neighbours(current):
                #avoids walking around the same cells over and over again:    
                if neighbour not in visited:
                    visited.add(neighbour)
                    #records how I got to this spot:
                    previous[neighbour] = current
                    queue.append(neighbour)

        if self.exit not in visited:
            raise ValueError("No path exists between entry and exit.")

        path: list[tuple[int, int]] = []
        current: tuple[int, int] | None = self.exit

        while current is not None:
            path.append(current)
            current = previous[current]

        path.reverse()

        return path

    def to_hex(self) -> list[str]:
        """Maze walls are converted to hexadecimal rows"""
        rows: list[str] = []

        for row in self.maze:
            line = ""

            for cell in row:
                line += format(cell.walls, "X")

            rows.append(line)

        return rows

    def path_to_directions(
        self,
        path: list[tuple[int, int]],
    ) -> str:
        """Convert the coordinate path to directions"""
        directions: list[str] = []

        for current, next_cell in zip(path, path[1:]):
            dx = next_cell[0] - current[0]
            dy = next_cell[1] - current[1]

            if dx == 1 and dy == 0:
                directions.append("EAST")
            elif dx == -1 and dy == 0:
                directions.append("WEST")
            elif dx == 0 and dy == 1:
                directions.append("SOUTH")
            elif dx == 0 and dy == -1:
                directions.append("NORTH")

        return "".join(directions)


def write_maze(
    filename: str,
    generator: MazeGenerator,
) -> None:
    """Write the generated maze to a file."""

    path = generator.solve()
    directions = generator.path_to_directions(path)

    with open(filename, "w") as output_file:
        for row in generator.to_hex():
            output_file.write(row + "\n")

        output_file.write("\n")
        output_file.write(f"{generator.entry[0]},{generator.entry[1]}\n")
        output_file.write(f"{generator.exit[0]},{generator.exit[1]}\n")
        output_file.write(directions + "\n")


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
    
    
if __name__ == "__main__":
    generator = MazeGenerator(
    3,
    3,
    (0, 0),
    (2, 2),
    True,
    42,
)

print("Connected:", generator.validate_connectivity())


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

print("Connected:", generator.validate_connectivity())


if __name__ == "__main__":
    generator = MazeGenerator(
    3,
    3,
    (0, 0),
    (2, 2),
    True,
    42,
)

generator.maze[0][0].walls &= ~EAST
OPTIONAL for true: generator.remove_wall((0, 0), (1, 0))

print("Walls:", generator.validate_walls())


if __name__ == "__main__":
    generator = MazeGenerator(
    3,
    3,
    (0, 0),
    (2, 2),
    True,
    42,
)

generator.maze[0][0].walls &= ~NORTH

print("Borders:", generator.validate_borders())


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

print("Connected:", generator.validate_connectivity())
print("Walls:", generator.validate_walls())
print("Borders:", generator.validate_borders())
print("Connections:", generator.count_open_connections())
print("Perfect:", generator.validate_perfect())


if __name__ == "__main__":
    generator = MazeGenerator(
        3,
        3,
        (0, 0),
        (2, 2),
        True,
        42,
    )

    generator.remove_wall((0, 0), (1, 0))
    generator.remove_wall((1, 0), (1, 1))
    generator.remove_wall((1, 1), (2, 1))
    generator.remove_wall((2, 1), (2, 2))

    path = generator.solve()

    print("Path:", path)

    
#impossible maze:
if __name__ == "__main__":
    generator = MazeGenerator(
    3,
    3,
    (0, 0),
    (2, 2),
    True,
    42,
    )

    path = generator.solve()

    print("Path:", path)


if __name__ == "__main__":
    generator = MazeGenerator(
    10,
    10,
    (0, 0),
    (9, 9),
    True,
    42,
    )

    generator.generate()

    print("Connected:", generator.validate_connectivity())
    print("Perfect:", generator.validate_perfect())

    path = generator.solve()

    print("Path:", path)
    print("Path length:", len(path))
"""

#test hexadecimal conversion
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

    rows = generator.to_hex()

    for row in rows:
        print(row)
