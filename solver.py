from collections import deque
from maze import Maze


def _can_move(maze: Maze, x: int, y: int, direction: str) -> bool:
    cell = maze.get_cell(x, y)
    neighbor = maze.get_neighbor(cell, direction)
    if neighbor is None:
        return False

    if direction == "N":
        return not cell.north_wall
    elif direction == "E":
        return not cell.east_wall
    elif direction == "S":
        return not cell.south_wall
    elif direction == "W":
        return not cell.west_wall
    else:
        raise ValueError(f"Invalid direction: {direction}")


def get_reachable_neighbors(
    maze: Maze,
    x: int,
    y: int
) -> list[tuple[int, int]]:
    """Return all reachable neighbor coordinates from (x,y)."""
    coords: list[tuple[int, int]] = []

    cell = maze.get_cell(x, y)

    for direction in ("N", "E", "S", "W"):
        if _can_move(maze, x, y, direction):
            neighbor = maze.get_neighbor(cell, direction)

            if neighbor is not None:
                coords.append((neighbor.x, neighbor.y))

    return coords


def _coords_to_direction(
    from_pos: tuple[int, int],
    to_pos: tuple[int, int]
) -> str:
    """Convert coordinate step to N/E/S/W."""
    dx = to_pos[0] - from_pos[0]
    dy = to_pos[1] - from_pos[1]

    if dx == 0:
        if dy == -1:
            return "N"
        if dy == 1:
            return "S"
    elif dy == 0:
        if dx == 1:
            return "E"
        if dx == -1:
            return "W"

    raise ValueError("Invalid direction")


def solve(maze: Maze) -> tuple[str, list[tuple[int, int]]]:
    """Find shortest path using BFS.

    Returns:
        Tuple of (direction_string, coordinate_path)
    """
    start = maze.entry
    goal = maze.exit_pos

    queue = deque([start])
    visited = {start}
    came_from: dict[
        tuple[int, int],
        tuple[int, int] | None
    ] = {start: None}

    while queue:
        current = queue.popleft()

        if current == goal:
            break
        for neighbor in get_reachable_neighbors(
            maze,
            current[0],
            current[1],
        ):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)
    else:
        raise ValueError("No path found")

    path: list[tuple[int, int]] = []

    node: tuple[int, int] | None = goal

    while node is not None:
        path.append(node)
        node = came_from[node]

    path.reverse()

    directions = []
    for i in range(len(path) - 1):
        direction = _coords_to_direction(path[i], path[i + 1])
        directions.append(direction)

    return "".join(directions), path


def main() -> None:
    maze = Maze(5, 5, (0, 0), (4, 4))
    maze.build(seed=42)
    maze.print_ascii()

    directions, path = solve(maze)
    print(f"\nPath: {path}")
    print(f"Directions: {directions}")
    print(f"Steps: {len(path) - 1}")


if __name__ == "__main__":
    main()
