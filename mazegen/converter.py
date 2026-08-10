from mazegen.maze import MazeGenerator, Cell
from mazegen.solver import solve


def cell_to_hex(cell: Cell) -> str:
    """
    Convert a cell's wall configuration to a hexadecimal digit.

    Each wall direction corresponds to a bit in the hexadecimal value:
        - North: bit 0 (value 1)
        - East: bit 1 (value 2)
        - South: bit 2 (value 4)
        - West: bit 3 (value 8)

    A wall being closed sets the bit to 1, open means 0.

    Args:
        cell: The cell whose walls need to be encoded.

    Returns:
        A single hexadecimal digit (0-F) representing the wall configuration.

    Example:
        >>> cell = Cell(0, 0)
        >>> cell.north_wall = True
        >>> cell.east_wall = True
        >>> cell_to_hex(cell)  # Binary: 0011 -> 3
        '3'
    """
    value = 0
    if cell.north_wall:
        value += 1
    if cell.east_wall:
        value += 2
    if cell.south_wall:
        value += 4
    if cell.west_wall:
        value += 8

    return format(value, 'x')


def grid_to_lines(maze: MazeGenerator) -> list[str]:
    """
    Convert the entire maze grid to a list of hexadecimal strings.

    Each row in the maze is converted to a string of hexadecimal digits,
    with each digit representing the wall configuration of a cell.

    Args:
        maze: The Maze object to convert.

    Returns:
        A list of strings, where each string is a row of hexadecimal digits.
    """
    lines = []
    for y in range(maze.height):
        row_string = ""
        for x in range(maze.width):
            cell = maze.get_cell(x, y)
            row_string += cell_to_hex(cell)
        lines.append(row_string)
    return lines


def write_maze_file(maze: MazeGenerator, filepath: str) -> None:
    """
    Write the maze to a file in the required output format.

    The output file contains:
        1. One line per row of cells (hexadecimal digits)
        2. An empty line
        3. Entry coordinates (x,y)
        4. Exit coordinates (x,y)
        5. The shortest valid path from entry to exit (using N, E, S, W)

    Args:
        maze: The Maze object to write to file.
        filepath: The path where the output file will be created.

    Returns:
        None

    Raises:
        OSError: If the file cannot be written.
    """
    grid_lines = grid_to_lines(maze)

    directions, path = solve(maze)

    lines = grid_lines
    lines.append("")
    lines.append(f"{maze.entry[0]},{maze.entry[1]}")
    lines.append(f"{maze.exit_pos[0]},{maze.exit_pos[1]}")
    lines.append(directions)

    with open(filepath, 'w') as f:
        for line in lines:
            f.write(line + "\n")
