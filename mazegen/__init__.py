"""
MazeGen - A reusable maze generation package.

This package provides the core MazeGenerator class with multiple generation algorithms,
pathfinding, and visualization capabilities.

Example:
    >>> from mazegen import MazeGenerator
    >>> maze = MazeGenerator(20, 15, (0, 0), (19, 14))
    >>> maze.build(seed=42, perfect=True)
    >>> print(maze.print_ascii())
"""

from mazegen.maze import MazeGenerator, Cell
from mazegen.solver import solve
from mazegen.converter import cell_to_hex, grid_to_lines, write_maze_file


__version__ = "1.0.0"
__all__ = [
    "MazeGenerator",
    "Cell",
    "solve",
    "cell_to_hex",
    "grid_to_lines",
    "write_maze_file",
    "MazeError",
    "InvalidCoordinateError",
    "InvalidMazeSizeError",
]