from collections import deque
from maze import Maze
from solver import solve

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


def get_reachable_neighbors(maze: Maze, x: int, y: int) -> list[tuple[int, int]]:
    """Return all reachable neighbor coordinates from (x,y)."""
    coords = []
    for direction in ("N", "E", "S", "W"):
        if _can_move(maze, x, y, direction):
            cell = maze.get_cell(x, y)
            neighbor = maze.get_neighbor(cell, direction)
            coords.append((neighbor.x, neighbor.y))
    return coords


def _coords_to_direction(from_pos: tuple[int, int], to_pos: tuple[int, int]) -> str:
    """Convert coordinate step to N/E/S/W."""
    if (to_pos[0] - from_pos[0]) == 0:
        if (to_pos[1] - from_pos[1]) == -1:
             return "N"
        elif (to_pos[1] - from_pos[1]) == 1:
             return "S"
    elif (to_pos[1] - from_pos[1]) == 0:
            if (to_pos[0] - from_pos[0]) == 1:
                return "E"
            elif (to_pos[0] - from_pos[0]) == -1:
                return "W"
    else:  
        raise ValueError(f"Invalid direction")


def solve(maze: Maze) -> tuple[str, list[tuple[int, int]]]:
    """Find shortest path using BFS.
    
    Returns:
        Tuple of (direction_string, coordinate_path)
    """
    start = maze.entry
    goal = maze.exit_pos
    
    queue = deque([start])
    visited = {start}
    came_from = {start: None}
    
    while queue:
        current = queue.popleft()
        
        if current == goal:
            break
        
        for neighbor in get_reachable_neighbors(maze, current[0], current[1]):  # ← Your function here
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)
    else:
        raise ValueError("No path found")
    
    path = []
    node = goal
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


#cell (x,y) north (x,y-1) east (x+1,y) south (x,y+1) west (x-1,y)   
 