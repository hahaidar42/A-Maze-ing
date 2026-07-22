def solve_maze(maze, entry: Tuple[int, int], exit: Tuple[int, int]) -> Optional[str]:
    """
    Find shortest path from entry to exit using BFS.
    
    Args:
        maze: Maze object with cells and wall information
        entry: (x, y) starting position
        exit: (x, y) target position
        
    Returns:
        String of directions (N/E/S/W) or None if no path exists
    """



def get_neighbors(maze, x: int, y: int) -> List[Tuple[int, int, str]]:
    """
    Return list of (neighbor_x, neighbor_y, direction) for all reachable neighbors.
    A neighbor is reachable if:
    1. It's inside the maze
    2. There's no wall between current cell and neighbor
    """

# How do you check if a neighbor is inside the maze? (Use maze.is_inside())

# How do you get the neighbor cell? (Use maze.get_cell() or maze.get_neighbor())

# How do you check if there's a wall between two cells?



# Put start into queue

# Mark start visited

# while queue is not empty

#     remove front cell

#     if this is exit

#         stop

#     for every neighbor

#         if not visited

#             mark visited

#             add to queue















# pseudocode 


# queue = deque([start])

# visited = {start}

# parent = {}

# while queue:

#     current = queue.popleft()

#     if current == end:
#         break

#     for neighbor in neighbors(current):

#         if neighbor not in visited:

#             visited.add(neighbor)

#             parent[neighbor] = current

#             queue.append(neighbor)



# recovering the path

# path = []

# current = end

# while current != start:
#     path.append(current)
#     current = parent[current]

# path.append(start)

# path.reverse()