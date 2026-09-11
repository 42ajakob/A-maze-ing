import random
from collections import deque

N = 0b0001
E = 0b0010
S = 0b0100
W = 0b1000


class Cell:
    """Represent a single cell in the maze."""

    def __init__(self) -> None:
        """Initialize a cell with all walls closed."""
        self.walls: int = 0b1111


class MazeGenerator:
    """Generate a maze."""

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        perfect: bool,
        seed: int | None = None,
    ) -> None:
        """Initialize the maze generator."""
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

    def get_42_pattern(self) -> set[tuple[int, int]]:
        """Return the centered cells used to draw the 42 pattern."""
        pattern = {
            (1, 0),
            (1, 1),
            (0, 1),
            (1, 2),
            (2, 2),
            (1, 3),
            (1, 4),

            (4, 0),
            (5, 0),
            (6, 0),
            (6, 1),
            (4, 2),
            (5, 2),
            (6, 2),
            (6, 3),
            (4, 4),
            (5, 4),
            (6, 4),
        }

        if self.width < 7 or self.height < 5:
            return set()

        pattern_width = 7
        pattern_height = 5

        offset_x = (self.width - pattern_width) // 2
        offset_y = (self.height - pattern_height) // 2

        return {
            (x + offset_x, y + offset_y)
            for x, y in pattern
        }

    def is_42_cell(self, position: tuple[int, int]) -> bool:
        """Return if a cell belongs to the 42 pattern."""
        return position in self.get_42_pattern()

    def is_maze_cell(self, position: tuple[int, int]) -> bool:
        """Return if a cell is part of the actual maze."""
        return position not in self.get_42_pattern()

    def count_maze_cells(self) -> int:
        """Count cells that belong to the maze."""
        count = 0

        for y in range(self.height):
            for x in range(self.width):
                if self.is_maze_cell((x, y)):
                    count += 1

        return count

    def validate_entry_exit(self) -> bool:
        """Check that entry and exit are valid maze cells."""
        return (
            self.is_maze_cell(self.entry)
            and self.is_maze_cell(self.exit)
        )

    def validate_42_size(self) -> bool:
        """Check if the maze is large enough for the 42 pattern."""
        return self.width >= 7 and self.height >= 5

    def get_neighbours(
        self,
        position: tuple[int, int],
    ) -> list[tuple[int, int]]:
        """Return the neighbouring cells."""
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
        """Return the neighbouring cells connected by an open wall."""
        x, y = position
        cell = self.maze[y][x]

        open_neighbours = []

        for neighbour in self.get_neighbours(position):
            nx, ny = neighbour

            # In which direction lays the neighbour?
            if nx == x + 1:
                direction = E
            elif nx == x - 1:
                direction = W
            elif ny == y + 1:
                direction = S
            else:
                direction = N

            # Check if the wall is open
            if not (cell.walls & direction):
                open_neighbours.append(neighbour)

        return open_neighbours

    def remove_wall(
        self,
        first: tuple[int, int],
        second: tuple[int, int],
    ) -> None:
        """Open the wall between two neighbouring cells."""
        x1, y1 = first
        x2, y2 = second

        if not (0 <= x1 < self.width and 0 <= y1 < self.height):
            raise ValueError("First cell is outside of the maze")

        if not (0 <= x2 < self.width and 0 <= y2 < self.height):
            raise ValueError("Second cell is outside of the maze")

        cell1 = self.maze[y1][x1]
        cell2 = self.maze[y2][x2]

        if x2 == x1 + 1:
            cell1.walls &= ~E
            cell2.walls &= ~W

        elif x2 == x1 - 1:
            cell1.walls &= ~W
            cell2.walls &= ~E

        elif y2 == y1 + 1:
            cell1.walls &= ~S
            cell2.walls &= ~N

        elif y2 == y1 - 1:
            cell1.walls &= ~N
            cell2.walls &= ~S

        else:
            raise ValueError("Cells are not neighbouring cells")

    def restore_wall(
        self,
        first: tuple[int, int],
        second: tuple[int, int],
    ) -> None:
        """Close the wall between two neighbouring cells."""
        x1, y1 = first
        x2, y2 = second

        if not (0 <= x1 < self.width and 0 <= y1 < self.height):
            raise ValueError("First cell is outside of the maze")

        if not (0 <= x2 < self.width and 0 <= y2 < self.height):
            raise ValueError("Second cell is outside of the maze")

        cell1 = self.maze[y1][x1]
        cell2 = self.maze[y2][x2]

        if x2 == x1 + 1:
            cell1.walls |= E
            cell2.walls |= W

        elif x2 == x1 - 1:
            cell1.walls |= W
            cell2.walls |= E

        elif y2 == y1 + 1:
            cell1.walls |= S
            cell2.walls |= N

        elif y2 == y1 - 1:
            cell1.walls |= N
            cell2.walls |= S

        else:
            raise ValueError("Cells are not neighbouring cells")

    def generate(self) -> None:
        """Generate a random maze."""

        if not self.validate_entry_exit():
            raise ValueError(
                "Entry and exit must not be part of the 42 pattern."
                )

        visited: set[tuple[int, int]] = set()
        stack: list[tuple[int, int]] = []

        current = self.entry
        visited.add(current)
        stack.append(current)

        while stack:
            # DFS - using stack, last cell in, first cell out
            current = stack[-1]

            # Find the unvisited neighbours
            neighbours = self.get_neighbours(current)
            unvisited = [
                neighbour
                for neighbour in neighbours
                if neighbour not in visited and self.is_maze_cell(neighbour)
            ]
            # Pick one randomly and remove the wall
            if unvisited:
                next_cell = self.random.choice(unvisited)
                self.remove_wall(current, next_cell)
                visited.add(next_cell)
                stack.append(next_cell)

            else:
                # no unvisited neighbour - backtracking by popping stack
                stack.pop()

        if not self.perfect:
            self.add_loops()

        if not self.validate_corridor_width():
            raise ValueError(
                "Generated maze contains an area wider than two cells."
            )

        if not self.validate_connectivity():
            raise ValueError("Generated maze is not fully connected.")

        if not self.validate_walls():
            raise ValueError("Generated maze contains inconsistent walls.")

        if not self.validate_borders():
            raise ValueError("Generated maze has an open outer border.")

        if self.perfect and not self.validate_perfect():
            raise ValueError("Generated maze is not perfect.")

    def find_closed_walls(
        self,
    ) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        """Return closed walls between neighbouring cells."""
        closed_walls: list[tuple[tuple[int, int], tuple[int, int]]] = []

        for y in range(self.height):
            for x in range(self.width):
                cell = self.maze[y][x]

                # cell to the East:
                if (
                    x < self.width - 1
                    and self.is_maze_cell((x, y))
                    and self.is_maze_cell((x + 1, y))
                    and cell.walls & E
                ):
                    closed_walls.append(((x, y), (x + 1, y)))

                # cell to the South:
                if (
                    y < self.height - 1
                    and self.is_maze_cell((x, y))
                    and self.is_maze_cell((x, y + 1))
                    and cell.walls & S
                ):
                    closed_walls.append(((x, y), (x, y + 1)))

        return closed_walls

    def add_loops(self) -> None:
        """Open additional walls to create loops for an imperfect maze."""
        closed_walls = self.find_closed_walls()

        if not closed_walls:
            return

        number_of_walls = max(1, len(closed_walls) // 10)

        self.random.shuffle(closed_walls)

        added = 0

        for wall in closed_walls:
            if added >= number_of_walls:
                break

            self.remove_wall(wall[0], wall[1])

            if self.validate_corridor_width():
                added += 1
            else:
                # if wall created a 3x3 open area, re-close it
                self.restore_wall(wall[0], wall[1])

    def validate_connectivity(self) -> bool:
        """Check if every cell can be reached from the first cell."""
        visited: set[tuple[int, int]] = set()
        stack: list[tuple[int, int]] = [self.entry]

        while stack:
            current = stack.pop()

            if current in visited:
                continue

            visited.add(current)

            for neighbour in self.get_open_neighbours(current):
                if neighbour not in visited and self.is_maze_cell(neighbour):
                    stack.append(neighbour)

        maze_cells = {
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if self.is_maze_cell((x, y))
        }

        return visited == maze_cells

    def validate_walls(self) -> bool:
        """Check if neighbouring cells have matching walls."""
        for y in range(self.height):
            for x in range(self.width):
                cell = self.maze[y][x]

                # Check East neighbour
                if x < self.width - 1:
                    east_cell = self.maze[y][x + 1]

                    east_wall = bool(cell.walls & E)
                    west_wall = bool(east_cell.walls & W)

                    if east_wall != west_wall:
                        return False

                # Check South neighbour
                if y < self.height - 1:
                    south_cell = self.maze[y + 1][x]

                    south_wall = bool(cell.walls & S)
                    north_wall = bool(south_cell.walls & N)

                    if south_wall != north_wall:
                        return False

        return True

    def validate_borders(self) -> bool:
        """Check if the outer borders of the maze are closed."""
        for x in range(self.width):
            if self.maze[0][x].walls & N == 0:
                return False

            if self.maze[self.height - 1][x].walls & S == 0:
                return False

        for y in range(self.height):
            if self.maze[y][0].walls & W == 0:
                return False

            if self.maze[y][self.width - 1].walls & E == 0:
                return False

        return True

    def is_open_3x3(self, x: int, y: int) -> bool:
        """Check whether a 3x3 area is completely open."""
        for row in range(y, y + 3):
            for col in range(x, x + 2):
                if self.maze[row][col].walls & E:
                    return False

        for row in range(y, y + 2):
            for col in range(x, x + 3):
                if self.maze[row][col].walls & S:
                    return False

        return True

    def validate_corridor_width(self) -> bool:
        """Check that no open area is wider than two cells."""
        for y in range(self.height - 2):
            for x in range(self.width - 2):
                if self.is_open_3x3(x, y):
                    return False

        return True

    # validate_connectivity() - Can I reach every cell?
    # validate_walls() - Do neighboring cells agree?
    # validate_borders() - Is the maze contained within its boundaries?
    # NOW PERFECT OPTION, FOUND OUT BY COUNTING, CELLS-1

    def count_open_connections(self) -> int:
        """Count the connections between maze cells."""
        connections = 0

        for y in range(self.height):
            for x in range(self.width):
                cell = self.maze[y][x]

                if (
                    x < self.width - 1
                    and self.is_maze_cell((x, y))
                    and self.is_maze_cell((x + 1, y))
                    and not (cell.walls & E)
                ):
                    connections += 1

                if (
                    y < self.height - 1
                    and self.is_maze_cell((x, y))
                    and self.is_maze_cell((x, y + 1))
                    and not (cell.walls & S)
                ):
                    connections += 1

        return connections

    def validate_perfect(self) -> bool:
        """Check if the maze is a perfect maze."""
        return (
            self.validate_connectivity()
            and self.count_open_connections()
            == self.count_maze_cells() - 1
        )

    def solve(self) -> list[tuple[int, int]]:
        """Find the shortest path from entry to exit."""
        queue: deque[tuple[int, int]] = deque()
        visited: set[tuple[int, int]] = set()
        previous: dict[tuple[int, int], tuple[int, int] | None] = {}

        queue.append(self.entry)
        visited.add(self.entry)
        previous[self.entry] = None

        while queue:
            # BFS: process cells in the order they were discovered
            current = queue.popleft()

            if current == self.exit:
                break

            for neighbour in self.get_open_neighbours(current):
                # avoids walking around the same cells over and over again:
                if (
                    self.is_maze_cell(neighbour)
                    and neighbour not in visited
                ):
                    visited.add(neighbour)
                    # records how I got to this spot:
                    previous[neighbour] = current
                    queue.append(neighbour)

        if self.exit not in visited:
            raise ValueError("No path exists between entry and exit.")

        path: list[tuple[int, int]] = []
        position: tuple[int, int] | None = self.exit

        while position is not None:
            path.append(position)
            position = previous[position]

        path.reverse()

        return path

    def path_to_directions(
        self,
        path: list[tuple[int, int]],
    ) -> str:
        """Convert the coordinate path to directions."""
        directions: list[str] = []

        for current, next_cell in zip(path, path[1:]):
            dx = next_cell[0] - current[0]
            dy = next_cell[1] - current[1]

            if dx == 1 and dy == 0:
                directions.append("E")
            elif dx == -1 and dy == 0:
                directions.append("W")
            elif dx == 0 and dy == 1:
                directions.append("S")
            elif dx == 0 and dy == -1:
                directions.append("N")

        return "".join(directions)

    def to_hex(self) -> list[str]:
        """Maze walls are converted to hexadecimal rows."""
        rows: list[str] = []

        for row in self.maze:
            line = ""

            for cell in row:
                line += format(cell.walls, "X")

            rows.append(line)

        return rows
