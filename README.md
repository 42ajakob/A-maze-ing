*This project has been created as part of the 42 curriculum by anjakob, zmaurer.*

# A-Maze-ing


## Description

A-Maze-ing is a Python project developed as part of the 42 curriculum.

The objective of the project is to generate a valid random maze from a configuration file, write it to an output file using the required hexadecimal wall representation, display it visually to the user, and to prodive a shortest path between entrance and exit.

The project explores concepts like:
* Maze generation algorithms
* Pathfinding
* Random generation and reproducibility through seeds
* File parsing and validation
* Data structures
* Terminal-based visualisation
* Object-oriented programming
* Python type hints and static analysis
* Code reusability and package creation

The generated maze must respect the constraints defined by the subject, including valid borders, coherent walls between neighbouring cells, connectivity, corridor-width limitations, and the optional perfect-maze requirement.

When possible, the maze also contains a visible 42 pattern made from closed cells.


## Instructions

### Requirements

* Python **3.10 or later**
* `pip`
* `flake8`
* `mypy`

### Installation

Install the dependencies with:

```bash
make install
```

### Running the project

To execute the main program, the subject's execution format requires:

```bash
python3 a_maze_ing.py config.txt
```

The configuration filename can be changed, if it is passed as the only argument.

The project includes a `Makefile` for common development tasks:

```bash
make install
make run
make clean
```

To run the program using Python's built-in debugger:

```bash
make debug
```

To run both `flake8` and `mypy` using the required checks:

```bash
make lint
```


## Configuration file

The maze parameters are provided in a plain text configuration file, whose path is passed as the program's only argument.

Example (`config.txt`):

```
# This is a comment
SEED=42

WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14

OUTPUT_FILE=maze.txt
PERFECT=True
```

Each non-empty, non-comment line follows a `KEY=VALUE` format. Blank lines are ignored and lines starting with `#` are treated as comments.

| Key | Description |
|---|---|
| `SEED` | Random seed used for generation, allowing the same maze to be reproduced |
| `WIDTH` | Maze width, in cells |
| `HEIGHT` | Maze height, in cells |
| `ENTRY` | Entry coordinates, as `x,y` |
| `EXIT` | Exit coordinates, as `x,y` |
| `OUTPUT_FILE` | Path of the file the generated maze is written to |
| `PERFECT` | `True` for a perfect maze, `False` for an imperfect maze with loops |

All seven keys are required. The parser exits with an error message if a key is missing or unknown, a line cannot be split into a key and a value, or a value fails validation (for example a negative coordinate, or an entry/exit position outside the maze bounds).

The file is parsed and validated in `src/parser.py`, using `pydantic` to build a `MazeConfig` object that is then passed to the maze generator.


## Maze Generation Algorithm

### Depth-First Search (DFS)

The maze is generated using a randomized Depth-First Search (DFS) algorithm with backtracking.

The generator starts at the configured entry cell and keeps a stack of cells that have been visited. At each step, it looks for neighbouring cells that have not yet been visited and randomly chooses one. The wall between the current cell and the selected neighbour is then removed, creating a passage between the two cells.

If a cell has no unvisited neighbours, the algorithm backtracks using the stack until it finds a cell with an available neighbour.

The generated maze is stored as a two-dimensional structure of `Cell` objects. Each cell stores its four walls as a four-bit integer.

DFS was chosen because it is relatively simple to implement, produces a fully connected maze, and works well with the requirement to generate random mazes.


## Perfect and imperfect mazes

### Perfect mazes

When `PERFECT=True`, the generator creates a maze with exactly one path between any two maze cells. This is achieved by the DFS generation algorithm without adding additional connections.

The generator also validates the result by checking that the maze is connected and that the number of open connections is equal to the number of maze cells minus one.

### Imperfect mazes

When `PERFECT=False`, the maze is first generated using the same DFS algorithm. Additional closed walls are then selected randomly and opened to create loops.

This means that an imperfect maze can contain multiple possible paths between cells, while remaining connected.


## 42 Pattern

The generator creates a visible `42` pattern using cells whose walls remain completely closed.

The pattern is positioned in the centre of sufficiently large mazes. These cells are excluded from the normal maze connectivity calculations because they intentionally represent the visual `42` rather than usable maze cells.

The pattern requires a minimum maze size of 7 columns by 5 rows. If the maze is smaller than this, the maze can still be generated, but the program reports that the `42` pattern cannot be displayed.

The configured entry and exit positions are also validated so that they cannot be placed inside the `42` pattern.


## Maze Representation

Each maze cell stores its four walls as a four-bit integer:

* bit 0: North
* bit 1: East
* bit 2: South
* bit 3: West

A value of `1` means that the corresponding wall is closed, while `0` means that it is open.

For example, a cell with all four walls closed has the value `1111` in binary, which is represented as hexadecimal `F`.

The generator stores the maze as a two-dimensional list of `Cell` objects, allowing other parts of the project to access the generated maze structure.


## Output File Format

The generated maze is converted into hexadecimal wall values, with one row of hexadecimal values per maze row.

After the maze representation, the output file contains an empty line followed by:

* the entry coordinates,
* the exit coordinates,
* the shortest path represented using `N`, `E`, `S`, and `W`.

The output writer uses a context manager to create the file and writes all data using UTF-8 encoding.


## Breadth-First Search (BFS)

The generator uses Breadth-First Search (BFS) to find the shortest path from the entry to the exit.

BFS starts at the entry cell and explores reachable cells level by level. Each visited cell stores its previous cell, which allows the complete path to be reconstructed once the exit is reached.

Because BFS explores paths in increasing order of their length, the first time the exit is reached, the resulting path is a shortest valid path.

The solution is returned as a list of `(x, y)` coordinates and can also be converted into the required `N`, `E`, `S`, and `W` direction format.


## Visual Representation

Once the maze has been generated and written to the output file, it is loaded and displayed in an interactive terminal user interface (TUI) built with the `curses` library.

The output file is parsed back into a `Maze` object, which is then converted into a two-dimensional character grid: each maze cell is drawn as a single character surrounded by its walls, so a maze of width W and height H produces a grid of `2*H+1` rows by `2*W+1` columns.

| Character | Meaning |
|---|---|
| `*` | closed wall |
| ` ` (space) | open passage |
| `.` | solution path |
| `S` | entry |
| `X` | exit |
| `#` | `42` pattern cell |

Each character is styled with its own colour, using bold text for the entry, exit, and `42` pattern cells so they stand out from the rest of the maze.

The TUI supports the following controls:

| Key | Action |
|---|---|
| Arrow keys | Scroll the view |
| `p` | Show or hide the solution path |
| `4` | Show or hide the `42` pattern |
| `c` | Cycle through the available wall colours |
| `r` | Regenerate the maze using the same configuration file |
| `q` / `Esc` | Quit |

A status bar at the bottom of the screen shows the current state of the path and `42` pattern toggles, along with the result of the last action performed.


## Code Reusability

The maze-generation logic was implemented as a reusable Python package called `mazegen`.

The main reusable class is `MazeGenerator`, which can be imported independently of the main application:

```python
from mazegen import MazeGenerator

generator = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    perfect=True,
    seed=42,
)

generator.generate()
```

The generator accepts custom parameters including the maze width and height, entry and exit coordinates, whether the maze should be perfect, and an optional random seed.

Using the same seed with the same parameters produces the same maze, which makes generation reproducible.

A generated maze can be accessed through the `maze` attribute:

```python
maze = generator.maze
```

The structure contains `Cell` objects. Each cell provides its wall configuration through its `walls` attribute.

The shortest solution can be accessed with:

```python
solution = generator.solve()
```

The solution is returned as a list of `(x, y)` coordinates.

The package is defined using `pyproject.toml` and can be built into standard Python distribution formats:

```bash
python3 -m build
```

This produces both a source distribution (`.tar.gz`) and a wheel (`.whl`) that can be installed with `pip`.


## Project Management and Roles

The project was developed by **anjakob** and **zmaurer**. The tasks were distributed evenly:

### anjakob
Responsible for the configuration parsing and the visual representation of the maze:

* Implemented the configuration file parser and validation
* Connected the configuration values to the maze generator
* Created the Makefile
* Implemented the maze visualisation and user interaction
* Displayed the maze, entry, exit, and solution path
* Implemented maze regeneration and path visibility controls
* Integrated the different components into the final application

### zmaurer
Responsible for the maze generation and the output-file generation:

* Implemented the `MazeGenerator` class and DFS maze-generation algorithm
* Implemented perfect and imperfect maze generation
* Implemented the 42 pattern and maze validation
* Implemented the BFS shortest-path solver
* Implemented the hexadecimal maze representation and output file generation
* Added tests for the generator, solver, validation, and output
* Created the reusable `mazegen` Python package.


## Planning and Evolution

At the start of the project, the tasks were divived into 4 parts: parsing the configuration file, maze generation, writing the maze into an output file, and visual representation using the TUI.

The maze generation part was developed as an independent component first. This made it possible to test the generator separately before integrating it with the parser and TUI.

The generator was later moved into the reusable `mazegen` package. Tests were updated to import `MazeGenerator` from the package, and the package was built and tested in a separate virtual environment to verify that it could be installed independently.

### What worked well

* Separating maze generation from parsing and visualisation made development easier because each component could be tested independently.

* Using a random seed made it possible to reproduce specific mazes during development and testing.

* The generator was covered by automated tests for connectivity, wall consistency, perfect and imperfect mazes, the `42` pattern, deterministic generation, pathfinding, and output formatting.


### What could be improved

* The reusable package could have been designed as a separate component from the beginning rather than being extracted from the main implementation later.


## Resources

The project was developed using the following resources:

* Python documentation for language features and standard-library modules
* Documentation for `pytest`, `flake8`, `mypy`, and Python packaging
* The 42 project subject for the maze constraints and required output format
* Git and GitHub for version control and collaboration
* Automated tests for validating the maze generator and output format
* Python `collections.deque` documentation for the BFS queue
* pytest documentation for automated testing
* mypy documentation for static type checking
* flake8 documentation for code style checking
* Python Packaging User Guide for building the reusable `mazegen` package

AI assistance was used during development for:
* understanding DFS maze generation and BFS pathfinding
* debugging Python, mypy and flake8 issues
* discussing the project architecture and separation between maze generation, output writing and visualisation
* improving and checking the Readme file

The final implementation was tested and reviewed by the team.
