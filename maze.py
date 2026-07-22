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
    def __init__(self):
        self.grid: list[list[Cell]] = []
        self.width: int = 12
        self.height: int = 12
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

    def generate(self) -> None:
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
                current = self.get_neighbor(current, direction)
                assert current is not None
                current.visited = True
            else:
                if not stack:
                    break
                current = stack.pop()

    def print_ascii(self) -> None:
        for x in range(self.width):
            print("+---", end="")
        print("+")
        for y in range(self.height):
            print("|", end="")
            for x in range(self.width):
                cell = self.get_cell(x, y)
                if cell.east_wall:
                    print("   |", end="")
                else:
                    print("    ", end="")
            print()
            for x in range(self.width):
                cell = self.get_cell(x, y)
                if cell.south_wall:
                    print("+---", end="")
                else:
                    print("+   ", end="")
            print("+")

    def Pattern42(self) -> None:
        if self.width < 9 or self.height < 7:
            raise ValueError(
                "Maze dimensions must be at least 9x7 for Pattern42.")
        midw: int = self.width / 2
        midh: int = self.height / 2
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
        cell18 = self.get_cell(int(midw + 2), int(midh)+-1)
        cell18.visited = True
        cell19 = self.get_cell(int(midw + 1), int(midh)-1)
        cell19.visited = True

