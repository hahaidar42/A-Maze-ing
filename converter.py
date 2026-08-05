from maze import Maze, Cell
from solver import solve


def cell_to_hex(cell: Cell) -> str:
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


def grid_to_lines(maze: Maze) -> list[str]:
    lines = []
    for y in range(maze.height):
        row_string = ""
        for x in range(maze.width):
            cell = maze.get_cell(x, y)
            row_string += cell_to_hex(cell)
        lines.append(row_string)
    return lines


def write_maze_file(maze: Maze, filepath: str) -> None:
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
