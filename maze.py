import random


class Cell:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y
        self.north_wall: bool = True
        self.east_wall: bool = True
        self.south_wall: bool = True
        self.west_wall: bool = True
        self.visited: bool = False


class Maze:

    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    WHITE = "\033[47m"
    YELLOW = "\033[33m"

    def __init__(self, width: int, height: int, entry: tuple[int, int],
                 exit_pos: tuple[int, int]):
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
        if 0 <= x < self.width and 0 <= y < self.height:
            return True
        return False

    def get_cell(self, x: int, y: int) -> Cell:
        if not self.is_inside(x, y):
            raise ValueError(f"Cell coordinates ({x}, {y}) are out of bounds.")
        return self.grid[y][x]

    def get_neighbor(self, cell: Cell, direction: str) -> Cell | None:
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

    def remove_wall(self, cell1: Cell, direction: str) -> None:
        cell2 = self.get_neighbor(cell1, direction)
        if cell2 is None:
            raise ValueError(
                f"Cannot remove wall in direction {direction} from cell ({cell1.x}, {cell1.y}) - out of bounds.")
        if direction == "N":
            cell1.north_wall = False
            cell2.south_wall = False
        elif direction == "E":
            cell1.east_wall = False
            cell2.west_wall = False
        elif direction == "S":
            cell1.south_wall = False
            cell2.north_wall = False
        elif direction == "W":
            cell1.west_wall = False
            cell2.east_wall = False

    def get_unvisited_neighbors(self, cell: Cell) -> list[str]:
        unvisited_neighbors = []
        for direction in ["N", "E", "S", "W"]:
            neighbor = self.get_neighbor(cell, direction)
            if neighbor and not neighbor.visited:
                unvisited_neighbors.append(direction)
        return unvisited_neighbors

    def generate(self, seed: int | None = None) -> None:
        if seed is not None:
            random.seed(seed)
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        current = self.get_cell(x, y)
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

    def Pattern42(self) -> None:
        if self.width < 8 or self.height < 6:
            print("Warning: maze is too small for the 42 pattern. Pattern will be skipped.")
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
        for row in self.grid:
            for cell in row:
                cell.north_wall = True
                cell.east_wall = True
                cell.south_wall = True
                cell.west_wall = True
                cell.visited = False

    def notperfect(self, seed: int | None = None, pattern42: bool = False) -> None:
        for row in self.grid:
            for i in row:
                i.visited = False
        if pattern42:
            self.Pattern42()
        if seed is not None:
            random.seed(seed)
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        current = self.get_cell(x, y)
        current.visited = True
        stack: list[Cell] = []
        while True:
            neighbors = self.get_unvisited_neighbors(current)

            if neighbors:
                direction = random.choice(neighbors)

                if random.random() < 0.15:
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

    def build(self, seed: int | None = None, pattern42: bool = False, perfect: bool = True) -> None:
        self.reset()
        if self.entry == self.exit_pos:
            raise ValueError(
                f"Entry and exit must be different, both are {self.entry}")
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

        self.generate(seed)
        if not perfect:
            self.notperfect(seed, pattern42)

    def printsolved(self, color: str = RESET, pattern: bool = True, path: list[tuple[int, int]] | None = None) -> None:
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
