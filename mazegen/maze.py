import random
import os
import time


class Cell:
    """
    Represents a single cell in the maze grid.

    Each cell maintains its wall states (North, East, South, West) and a
    visited flag for maze generation algorithms.

    Attributes:
        x (int): X-coordinate of the cell in the grid.
        y (int): Y-coordinate of the cell in the grid.
        north_wall (bool): True if the north wall is present (closed).
        east_wall (bool): True if the east wall is present (closed).
        south_wall (bool): True if the south wall is present (closed).
        west_wall (bool): True if the west wall is present (closed).
        visited (bool): Used during maze generation to track visited cells.
    """

    def __init__(self, x: int, y: int):
        """
        Initialize a new Cell with all walls closed and unvisited.

        Args:
            x: X-coordinate of the cell in the grid.
            y: Y-coordinate of the cell in the grid.
        """
        self.x: int = x
        self.y: int = y
        self.north_wall: bool = True
        self.east_wall: bool = True
        self.south_wall: bool = True
        self.west_wall: bool = True
        self.visited: bool = False


class MazeGenerator:
    """
    Represents a maze grid with generation and visualization capabilities.

    This class provides functionality for generating perfect and non-perfect
    mazes using various algorithms, visualizing them in the terminal, and
    managing the required "42" pattern.

    Attributes:
        grid (list[list[Cell]]): 2D grid of Cell objects.
        width (int): Number of cells in the x-direction.
        height (int): Number of cells in the y-direction.
        entry (tuple[int, int]): (x, y) coordinates of the maze entry.
        exit_pos (tuple[int, int]): (x, y) coordinates of the maze exit.

    Class Attributes:
        RESET (str): ANSI reset code for terminal colors.
        RED (str): ANSI red color code.
        GREEN (str): ANSI green color code.
        WHITE (str): ANSI white background color code.
        YELLOW (str): ANSI yellow color code.
    """

    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    WHITE = "\033[47m"
    YELLOW = "\033[33m"

    def __init__(self, width: int, height: int, entry: tuple[int, int],
                 exit_pos: tuple[int, int]):
        """
        Initialize a new empty maze grid.

        Args:
            width: Number of cells in the x-direction.
            height: Number of cells in the y-direction.
            entry: (x, y) coordinates of the maze entry.
            exit_pos: (x, y) coordinates of the maze exit.

        Raises:
            ValueError: If entry and exit are the same.
        """
        self.grid: list[list[Cell]] = []
        self.width: int = width
        self.height: int = height
        self.entry: tuple[int, int] = entry
        self.exit_pos: tuple[int, int] = exit_pos
        for y in range(self.height):
            row: list[Cell] = []
            for x in range(self.width):
                row.append(Cell(x, y))
            self.grid.append(row)

    def is_inside(self, x: int, y: int) -> bool:
        """
        Check if a given coordinate is within the maze bounds.

        Args:
            x: X-coordinate to check.
            y: Y-coordinate to check.

        Returns:
            True if the coordinate is inside the maze, False otherwise.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return True
        return False

    def get_cell(self, x: int, y: int) -> Cell:
        """
        Get the cell at the specified coordinates.

        Args:
            x: X-coordinate of the cell.
            y: Y-coordinate of the cell.

        Returns:
            The Cell object at the specified coordinates.

        Raises:
            ValueError: If the coordinates are out of bounds.
        """
        if not self.is_inside(x, y):
            raise ValueError(f"Cell coordinates ({x}, {y}) are out of bounds.")
        return self.grid[y][x]

    def get_neighbor(self, cell: Cell, direction: str) -> Cell | None:
        """
        Get the neighboring cell in a given direction.

        Args:
            cell: The reference cell.
            direction: One of 'N', 'E', 'S', 'W' (North, East, South, West).

        Returns:
            The neighboring Cell if it exists, None if out of bounds.

        Raises:
            ValueError: If an invalid direction is provided.
        """
        if direction == "N":
            if not self.is_inside(cell.x, cell.y - 1):
                return None
            return self.get_cell(cell.x, cell.y - 1)
        elif direction == "E":
            if not self.is_inside(cell.x + 1, cell.y):
                return None
            return self.get_cell(cell.x + 1, cell.y)
        elif direction == "S":
            if not self.is_inside(cell.x, cell.y + 1):
                return None
            return self.get_cell(cell.x, cell.y + 1)
        elif direction == "W":
            if not self.is_inside(cell.x - 1, cell.y):
                return None
            return self.get_cell(cell.x - 1, cell.y)
        else:
            raise ValueError(f"Invalid direction: {direction}")

    def remove_wall(self, cell1: Cell, direction: str) -> bool:
        """
        Remove the wall between two adjacent cells.

        This method removes the wall in the specified direction from cell1
        and the corresponding wall from the neighboring cell.

        Args:
            cell1: The cell from which to remove a wall.
            direction: The direction of the wall to remove ('N', 'E', 'S', 'W').

        Returns:
            True if the wall was removed, False if it was already open.

        Raises:
            ValueError: If the neighbor is out of bounds.
        """
        cell2 = self.get_neighbor(cell1, direction)
        if cell2 is None:
            raise ValueError(
                f"Cannot remove wall in direction {direction} from "
                f"cell ({cell1.x}, {cell1.y}) - out of bounds.")
        if direction == "N":
            if cell1.north_wall:
                cell1.north_wall = False
                cell2.south_wall = False
                return True
        elif direction == "E":
            if cell1.east_wall:
                cell1.east_wall = False
                cell2.west_wall = False
                return True
        elif direction == "S":
            if cell1.south_wall:
                cell1.south_wall = False
                cell2.north_wall = False
                return True
        elif direction == "W":
            if cell1.west_wall:
                cell1.west_wall = False
                cell2.east_wall = False
                return True
        return False

    def get_unvisited_neighbors(self, cell: Cell) -> list[str]:
        """
        Get directions to unvisited neighboring cells.

        Args:
            cell: The cell to check.

        Returns:
            A list of directions ('N', 'E', 'S', 'W') where the neighbor
            exists and has not been visited.
        """
        unvisited_neighbors = []
        for direction in ["N", "E", "S", "W"]:
            neighbor = self.get_neighbor(cell, direction)
            if neighbor and not neighbor.visited:
                unvisited_neighbors.append(direction)
        return unvisited_neighbors

    def animate_path(self, path: list[tuple[int, int]],
                     color: str = RESET) -> None:
        """
        Animate the display of a path through the maze.

        The path is revealed step by step with a delay between steps.

        Args:
            path: List of (x, y) coordinates representing the path.
            color: ANSI color code for the maze walls.

        Returns:
            None
        """
        self.printsolved(path=[path[0]], color=color)

        for i in range(1, len(path)):
            time.sleep(0.05)

            os.system("cls" if os.name == "nt" else "clear")

            self.printsolved(path=path[:i+1], color=color)

    def get_visited_neighbors(self, cell: Cell) -> list[str]:
        """
        Get directions to visited neighboring cells.

        Args:
            cell: The cell to check.

        Returns:
            A list of directions ('N', 'E', 'S', 'W') where the neighbor
            exists and has been visited.
        """
        visited_neighbors = []
        for direction in ["N", "E", "S", "W"]:
            neighbor = self.get_neighbor(cell, direction)
            if neighbor and neighbor.visited:
                visited_neighbors.append(direction)
        return visited_neighbors

    def primgeneration(self, seed: int | None = None) -> None:
        """
        Generate a maze using Prim's algorithm.

        Prim's algorithm works by maintaining a frontier of cells adjacent to
        the visited set, and randomly adding cells from the frontier.

        Args:
            seed: Optional seed for reproducible random generation.

        Returns:
            None
        """
        if seed is not None:
            random.seed(seed)
        pattern_coords = set(self.pattern42_coords())
        frontier: list[Cell] = []
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            current = self.get_cell(x, y)
            if not current.visited and (x, y) not in pattern_coords:
                break
        current.visited = True
        directions: list[str] = self.get_unvisited_neighbors(current)
        for i in directions:
            neighbor = self.get_neighbor(current, i)
            if (neighbor
                    and not neighbor.visited
                    and (neighbor.x, neighbor.y) not in pattern_coords
                    ):
                frontier.append(neighbor)
        while frontier:
            ranfrontier = random.choice(frontier)
            visited_neighbors = self.get_visited_neighbors(ranfrontier)
            if not visited_neighbors:
                frontier.remove(ranfrontier)
                continue
            valid_neighbors = []
            for direction in visited_neighbors:
                newvisted = self.get_neighbor(ranfrontier, direction)

                if (
                    newvisted
                    and (newvisted.x, newvisted.y) not in pattern_coords
                ):
                    valid_neighbors.append(direction)
            if not valid_neighbors:
                frontier.remove(ranfrontier)
                continue
            direction = random.choice(valid_neighbors)

            self.remove_wall(ranfrontier, direction)

            ranfrontier.visited = True
            frontier.remove(ranfrontier)

            current = ranfrontier
            directions: list[str] = self.get_unvisited_neighbors(current)
            for i in directions:
                neighbor = self.get_neighbor(current, i)
                if (neighbor and not neighbor.visited
                        and neighbor not in frontier
                        and (neighbor.x, neighbor.y) not in pattern_coords):
                    frontier.append(neighbor)


    def generate(self, seed: int | None = None) -> None:
        """
        Generate a perfect maze using recursive backtracking (DFS).

        This is the primary maze generation algorithm. It creates a perfect
        maze (unique path between any two points) by performing a depth-first
        traversal of the grid.

        Args:
            seed: Optional seed for reproducible random generation.

        Returns:
            None
        """
        if seed is not None:
            random.seed(seed)
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            current = self.get_cell(x, y)
            if not current.visited:
                break
        current.visited = True
        stack: list[Cell] = []
        while True:
            neighbors = self.get_unvisited_neighbors(current)
            if neighbors:
                direction = random.choice(neighbors)
                self.remove_wall(current, direction)
                stack.append(current)
                next_cell = self.get_neighbor(current, direction)
                assert next_cell is not None
                current = next_cell
                current.visited = True
            else:
                if not stack:
                    break
                current = stack.pop()

    def print_ascii(self, color: str = RESET, pattern: bool = True) -> None:
        """
        Print the maze in ASCII format to the terminal.

        The maze is displayed with walls represented as +--- and | characters.
        The entry is marked with 'E' in green, the exit with 'X' in red,
        and the "42" pattern cells are highlighted in white.

        Args:
            color: ANSI color code for the maze walls.
            pattern: If True, display the "42" pattern in white.
        """
        for x in range(self.width):
            print(f"{color}+---{self.RESET}", end="")
        print(f"{color}+")
        for y in range(self.height):
            print(f"{color}|{self.RESET}", end="")
            for x in range(self.width):
                cell = self.get_cell(x, y)
                if (x, y) == self.entry:
                    print(f"{self.GREEN} E {self.RESET}", end="")
                elif (x, y) == self.exit_pos:
                    print(f"{self.RED} X {self.RESET}", end="")
                elif (x, y) in self.pattern42_coords():
                    if pattern:
                        print(f"{self.WHITE}   {self.RESET}", end="")
                    else:
                        print("   ", end="")
                else:
                    print("   ", end="")
                if cell.east_wall:
                    print(f"{color}|{self.RESET}", end="")
                else:
                    print(" ", end="")
            print()

            for x in range(self.width):
                cell = self.get_cell(x, y)
                if cell.south_wall:
                    print(f"{color}+---{self.RESET}", end="")
                else:
                    print(f"{color}+{self.RESET}   ", end="")
            print(f"{color}+{self.RESET}")

    def pattern42_coords(self) -> list[tuple[int, int]]:
        """
        Get the coordinates of cells that form the "42" pattern.

        The pattern is centered in the maze and forms the digits "42".
        If the maze is too small (< 8x6), an empty list is returned.

        Returns:
            A list of (x, y) coordinates for the "42" pattern cells.
        """
        if self.width < 8 or self.height < 6:
            return []

        midw = self.width // 2
        midh = self.height // 2

        return [
            (midw - 2, midh - 1),
            (midw - 3, midh - 1),
            (midw - 4, midh - 1),
            (midw - 4, midh - 2),
            (midw - 4, midh - 3),
            (midw - 2, midh),
            (midw - 2, midh + 1),
            (midw,     midh - 1),
            (midw,     midh - 3),
            (midw,     midh),
            (midw,     midh + 1),
            (midw + 1, midh + 1),
            (midw + 2, midh - 2),
            (midw + 2, midh + 1),
            (midw + 1, midh - 3),
            (midw + 2, midh - 3),
            (midw + 2, midh - 1),
            (midw + 1, midh - 1),
        ]

    def has_3x3_open_space(self) -> bool:
        """
        Check if the maze contains a 3x3 open space (no walls).

        This is used for non-perfect maze generation to ensure corridors
        are not wider than 2 cells.

        Returns:
            True if a 3x3 open space exists, False otherwise.
        """
        for row in self.grid:
            for cell in row:
                # center cell must have no walls
                if (cell.north_wall or cell.east_wall or
                        cell.south_wall or cell.west_wall):
                    continue

                north = self.get_cell(cell.x, cell.y - 1) \
                    if cell.y > 0 else None
                south = self.get_cell(cell.x, cell.y + 1) \
                    if cell.y < self.height - 1 else None
                east = self.get_cell(cell.x + 1, cell.y) \
                    if cell.x < self.width - 1 else None
                west = self.get_cell(cell.x - 1, cell.y) \
                    if cell.x > 0 else None

                if north and south and east and west:
                    if (not north.east_wall and not north.west_wall and
                        not south.east_wall and not south.west_wall and
                        not east.north_wall and not east.south_wall and
                            not west.north_wall and not west.south_wall):
                        return True

        return False

    def Pattern42(self) -> None:
        """
        Mark cells that form the "42" pattern as visited.

        This prevents the maze generation algorithm from modifying the walls
        of these cells, ensuring the pattern remains visible.

        The pattern is centered in the maze. If the maze is too small
        (< 8x6), the pattern is skipped.
        """
        if self.width < 8 or self.height < 6:
            return
        midw: int = self.width // 2
        midh: int = self.height // 2
        cell1 = self.get_cell(int(midw) - 2, int(midh) - 1)
        cell1.visited = True
        cell2 = self.get_cell(int(midw) - 3, int(midh) - 1)
        cell2.visited = True
        cell3 = self.get_cell(int(midw) - 4, int(midh) - 1)
        cell3.visited = True
        cell4 = self.get_cell(int(midw) - 4, int(midh) - 2)
        cell4.visited = True
        cell5 = self.get_cell(int(midw) - 4, int(midh) - 3)
        cell5.visited = True
        cell6 = self.get_cell(int(midw) - 2, int(midh))
        cell6.visited = True
        cell7 = self.get_cell(int(midw) - 2, int(midh) + 1)
        cell7.visited = True
        cell8 = self.get_cell(int(midw), int(midh) - 1)
        cell8.visited = True
        cell9 = self.get_cell(int(midw), int(midh) - 3)
        cell9.visited = True
        cell10 = self.get_cell(int(midw), int(midh))
        cell10.visited = True
        cell11 = self.get_cell(int(midw), int(midh) + 1)
        cell11.visited = True
        cell12 = self.get_cell(int(midw + 1), int(midh) + 1)
        cell12.visited = True
        cell13 = self.get_cell(int(midw + 2), int(midh)-2)
        cell13.visited = True
        cell14 = self.get_cell(int(midw + 2), int(midh) + 1)
        cell14.visited = True
        cell15 = self.get_cell(int(midw + 1), int(midh)-3)
        cell15.visited = True
        cell16 = self.get_cell(int(midw + 2), int(midh)-3)
        cell16.visited = True
        cell17 = self.get_cell(int(midw + 2), int(midh)-1)
        cell17.visited = True
        cell18 = self.get_cell(int(midw + 1), int(midh)-1)
        cell18.visited = True

    def reset(self) -> None:
        """
        Reset all cells in the maze to their initial state.

        All walls are closed and all cells are marked as unvisited.
        """
        for row in self.grid:
            for cell in row:
                cell.north_wall = True
                cell.east_wall = True
                cell.south_wall = True
                cell.west_wall = True
                cell.visited = False

    def notperfect(self, seed: int | None = None,
                   pattern42: bool = False) -> None:
        """
        Add extra passages to create a non-perfect maze.

        This method modifies the maze to have multiple paths by adding
        additional openings with a 15% probability during generation.

        Args:
            seed: Optional seed for reproducible random generation.
            pattern42: If True, preserve the "42" pattern cells.
        """
        newseed: int | None = seed
        if self.width == 1 or self.height == 1:
            return
        while True:
            removedw: int = 0
            for row in self.grid:
                for i in row:
                    i.visited = False
            if pattern42:
                self.Pattern42()
            if newseed is not None:
                random.seed(newseed)
                newseed = newseed + 1
            while True:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                current = self.get_cell(x, y)
                if not current.visited:
                    break
            current.visited = True
            stack: list[Cell] = []
            while True:
                neighbors = self.get_unvisited_neighbors(current)

                if neighbors:
                    direction = random.choice(neighbors)

                    if random.random() < 0.15:

                        if self.remove_wall(current, direction):
                            removedw += 1

                    stack.append(current)

                    next_cell = self.get_neighbor(current, direction)
                    assert next_cell is not None

                    current = next_cell
                    current.visited = True
                else:
                    if not stack:
                        break

                    current = stack.pop()
            if removedw > 0 and not self.has_3x3_open_space():
                break

    def build(self, seed: int | None = None,
              pattern42: bool = False,
              perfect: bool = True, algo: str = "DFS") -> None:
        """
        Build the maze with the specified parameters.

        This is the main entry point for maze generation. It resets the maze,
        validates entry and exit positions, optionally applies the "42" pattern,
        generates the maze using the specified algorithm, and handles perfect
        vs non-perfect maze generation.

        Args:
            seed: Optional seed for reproducible random generation.
            pattern42: If True, include the "42" pattern in the maze.
            perfect: If True, generate a perfect maze (unique path).
            algo: The generation algorithm to use ('DFS' or 'PRIM').

        Raises:
            ValueError: If entry or exit is inside the "42" pattern.
        """
        self.reset()
        if self.entry == self.exit_pos:
            raise ValueError(
                f"Entry and exit must be different, both are {self.entry}")
        if self.width < 8 or self.height < 6:
            print(
                "Warning: maze is too small for the 42"
                " pattern. Pattern will be skipped.")
        if pattern42:
            self.Pattern42()
            for row in self.grid:
                for i in row:
                    if i.visited:
                        if (i.x, i.y) == self.entry:
                            raise ValueError(
                                "Entry is in the 42 pattern")
                        if (i.x, i.y) == self.exit_pos:
                            raise ValueError(
                                "Exit is in the 42 pattern")

        if algo == "dfs":
            self.generate(seed)
        else:
            self.primgeneration(seed)
        if not perfect:
            self.notperfect(seed, pattern42)

    def printsolved(self, color: str = RESET, pattern: bool = True,
                    path: list[tuple[int, int]] | None = None) -> None:
        """
        Print the maze with a solution path highlighted.

        The path is marked with '*' in yellow. Entry and exit are shown
        as 'E' (green) and 'X' (red) respectively.

        Args:
            color: ANSI color code for the maze walls.
            pattern: If True, display the "42" pattern in white.
            path: List of (x, y) coordinates representing the solution path.
        """
        if path is None:
            path = []
        for x in range(self.width):
            print(f"{color}+---{self.RESET}", end="")
        print(f"{color}+")
        for y in range(self.height):
            print(f"{color}|{self.RESET}", end="")
            for x in range(self.width):
                cell = self.get_cell(x, y)

                if (x, y) == self.entry:
                    print(f"{self.GREEN} E {self.RESET}", end="")
                elif (x, y) == self.exit_pos:
                    print(f"{self.RED} X {self.RESET}", end="")
                elif (x, y) in path:
                    print(f"{self.YELLOW} * {self.RESET}", end="")
                elif (x, y) in self.pattern42_coords():
                    if pattern:
                        print(f"{self.WHITE}   {self.RESET}", end="")
                    else:
                        print("   ", end="")
                else:
                    print("   ", end="")
                if cell.east_wall:
                    print(f"{color}|{self.RESET}", end="")
                else:
                    print(" ", end="")
            print()

            for x in range(self.width):
                cell = self.get_cell(x, y)
                if cell.south_wall:
                    print(f"{color}+---{self.RESET}", end="")
                else:
                    print(f"{color}+{self.RESET}   ", end="")
            print(f"{color}+{self.RESET}")
