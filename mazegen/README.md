*This project has been created as part of the 42 curriculum by hahaidar, rmrad*

## Description

A-Maze-Ing is a Python-based maze generator that creates and visualizes random mazes from a configuration file. The project implements a fully functional maze generation system with support for perfect mazes (unique path between entry and exit), hexadecimal wall encoding, and both terminal and graphical visualization using MiniLibX (MLX). The maze generator is designed with reusability in mind, packaged as a standalone Python module that can be imported and used in future projects.

The project combines algorithm design, graph theory concepts (spanning trees), and user interaction to create an engaging tool for maze generation and exploration.

#### Makefile Commands

- `make run` - Execute the main script
- `make debug` - Run the main script in debug mode (pdb)
- `make clean` - Remove temporary files and caches
- `make lint` - Run flake8 and mypy with standard checks
- `make lint-strict` - Run flake8 and mypy with strict checks

### Configuration File Format

The configuration file uses `KEY = VALUE` pairs, one per line. Lines starting with `#` are comments and are ignored.

| Key | Description | Example |
|-----|-------------|---------|
| `WIDTH` | Maze width (number of cells) | `WIDTH=20` |
| `HEIGHT` | Maze height (number of cells) | `HEIGHT=15` |
| `ENTRY` | Entry coordinates (x,y) | `ENTRY=0,0` |
| `EXIT` | Exit coordinates (x,y) | `EXIT=19,14` |
| `OUTPUT_FILE` | Output filename | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Is the maze perfect? (True/False) | `PERFECT=True` |

Additional keys (e.g., `SEED`, `ALGORITHM`) may be added for advanced functionality.

### Output File Format

The maze is written to the output file using hexadecimal digits per cell, where each digit encodes closed walls:

| Bit | Direction |
|-----|-----------|
| 0 (LSB) | North |
| 1 | East |
| 2 | South |
| 3 | West |

A wall being closed sets the bit to 1; open means 0. Example: `3` (binary 0011) means walls are open to the south and west.

The file contains:
1. One line per row of cells (hexadecimal digits)
2. An empty line
3. Entry coordinates (x,y)
4. Exit coordinates (x,y)  
5. The shortest valid path from entry to exit (using N, E, S, W)

### Visual Representation

The program supports two display modes:

 **Terminal ASCII rendering** - Default display in the terminal

## Resources

### Technical Documentation
- [Maze Generation Algorithms - Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Prim's Algorithm](https://en.wikipedia.org/wiki/Prim%27s_algorithm)
- [Kruskal's Algorithm](https://en.wikipedia.org/wiki/Kruskal%27s_algorithm)
- [Recursive Backtracking](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_backtracking)
- [Spanning Trees in Graph Theory](https://en.wikipedia.org/wiki/Spanning_tree)
- [PEP 257 - Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)
- [Python Typing Documentation](https://docs.python.org/3/library/typing.html)
- [MLX Documentation](https://harm-smits.github.io/42docs/libs/minilibx)

### AI Usage

We used AI tools in the following areas:
- **code structure** - used ai to section the project to tasks
- **Documentation** - Help with README structure, docstrings, and technical explanations
- **Debugging** - Assistance in identifying and fixing logic errors, particularly with maze generation algorithms
- **Testing** - Generating initial test cases for edge cases and validation

All AI-generated content was reviewed, tested, and fully understood before integration. We verified code correctness through peer review and manual testing.

## Maze Generation Algorithm

### Chosen Algorithm

We implemented the **Recursive Backtracking** algorithm (also known as Depth-First Search) for maze generation.

### Why This Algorithm

1. **Simplicity and Elegance** - The algorithm is straightforward to implement and understand
2. **Perfect Mazes** - Naturally produces perfect mazes (unique path between any two points) when the `PERFECT` flag is enabled
3. **Efficiency** - O(n) time complexity where n is the number of cells
4. **Visual Appeal** - The recursive nature creates interesting, winding mazes with long corridors
5. **Educational Value** - This algorithm is a classic example of graph traversal and backtracking, fundamental concepts in computer science

### Algorithm Implementation Details

The recursive backtracking works as follows:
1. Start from a random cell
2. Mark it as visited
3. While there are unvisited neighbors:
   a. Choose a random unvisited neighbor
   b. Remove the wall between the current cell and the chosen neighbor
   c. Recursively visit the chosen neighbor
4. Backtrack when no unvisited neighbors remain

This creates a spanning tree of the grid, guaranteeing connectivity and a single path between any two points.

## Code Reusability

### Reusable Module

The maze generation logic is encapsulated in the `MazeGenerator` class within a standalone module, packaged as `mazegen-*` (e.g., `mazegen-1.0.0-py3-none-any.whl`).

## Team and Project Management

### Team Roles

| Member | Responsibilities |
|--------|------------------|
| hahaidar | solver implementation, parsing data, converting data to bits, debugging |
| rmrad | maze generation algorithm, logic implementation, terminal display|
## Bonuses Implemented

-  **Multiple maze generation algorithms** - Recursive Backtracking, Prim's, and Kruskal's algorithms
-  **Animation during maze generation** - Visual feedback showing the maze being built step by step in MLX mode

## Additional Features

- **Seed reproducibility** - Generate the same maze with a given seed
- **Interactive controls** - Regenerate, toggle path, change colors, quit
- **"42" pattern** - Special marker within the maze (automatically handled when space permits)
- **Graceful error handling** - Comprehensive validation with clear error messages

