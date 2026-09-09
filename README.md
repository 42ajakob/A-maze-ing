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


## Maze Generation Algorithm

### Depth-First Search (DFS)


## Perfect and imperfect mazes

### Perfect mazes

### Imperfect mazes


## 42 Pattern


## Maze Representation


## Output File Format

## Breadth-First Search (BFS)

## Visual Representation


## Code Reusability

You must provide a short documentation describing how to:
• Instantiate and use your generator, with at least a basic example.
• Pass custom parameters (e.g., size, seed).
• Access the generated structure, and access at least a solution.

## Project Management and Roles

The project was developed by **anjakob** and **zmaurer**. The tasks were distributed evenly:

### anjakob
Responsible for the parsing and visual representation:


### zmaurer
Responsible for the maze generation and ...:


## Planning and Evolution

At the start of the project, the tasks were divived into 4 parts: parsing the config file, maze generation, writing the maze into an output file and visual representation (TUI).

### What worked well

### What could be improved


## Resources

• The complete structure and format of your config file.
• The maze generation algorithm you chose.
• Why you chose this algorithm.
• What part of your code is reusable, and how.
• Your team and project management with:
◦ The roles of each team member.

A-Maze-ing This is the way
◦ Your anticipated planning and how it evolved until the end
◦ What worked well and what could be improved
◦ Have you used any specific tools? Which ones?
