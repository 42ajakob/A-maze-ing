from .mazegen import MazeGenerator


def write_maze(
    filename: str,
    generator: MazeGenerator,
) -> None:
    """Write the generated maze to a file."""

    path = generator.solve()
    directions = generator.path_to_directions(path)

    with open(filename, "w", encoding="utf-8") as output_file:
        for row in generator.to_hex():
            output_file.write(row + "\n")

        output_file.write("\n")
        output_file.write(f"{generator.entry[0]},{generator.entry[1]}\n")
        output_file.write(f"{generator.exit[0]},{generator.exit[1]}\n")
        output_file.write(directions + "\n")
