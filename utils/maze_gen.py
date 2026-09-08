class Cell:
    """Single cell in the maze"""

    def __init__(self) -> None:
        """Initialize cell with all walls closed"""
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
        """Initialize maze generator"""
        self.width: int = width
        self.height: int = height
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit
        self.perfect: bool = perfect
        self.seed: int | None = seed

        self.maze: list[list[Cell]] = [
            [Cell() for _ in range(width)]
            for _ in range(height)
        ]

    def remove_wall(
        self,
        first: tuple[int, int],
        second: tuple[int, int],
    ) -> None:
        """Open wall between two neighboring cells"""
        x1, y1 = first
        x2, y2 = second

        cell1 = self.maze[y1][x1]
        cell2 = self.maze[y2][x2]

        if x2 == x1 + 1:
            cell1.walls &= ~0b0010
            cell2.walls &= ~0b1000

        elif x2 == x1 - 1:
            cell1.walls &= ~0b1000
            cell2.walls &= ~0b0010

        elif y2 == y1 + 1:
            cell1.walls &= ~0b0100
            cell2.walls &= ~0b0001

        elif y2 == y1 - 1:
            cell1.walls &= ~0b0001
            cell2.walls &= ~0b0100

        else:
            raise ValueError("Cells are not neighboring cells.")


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

    print("Left:", bin(generator.maze[0][0].walls))
    print("Right:", bin(generator.maze[0][1].walls))

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

    generator.remove_wall((0, 0), (1, 0))

    print(bin(generator.maze[0][0].walls))
    print(bin(generator.maze[0][1].walls))