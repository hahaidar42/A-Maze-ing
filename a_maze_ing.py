from maze import Maze
from parser import parse_config
from typing import Any
from solver import solve
from converter import write_maze_file

config = parse_config("config.txt")
maze = Maze(
    config["WIDTH"],
    config["HEIGHT"],
    config["ENTRY"],
    config["EXIT"],
)

RESET = "\033[0m"
RED = "\033[41m"
GREEN = "\033[42m"
BLUE = "\033[44m"
YELLOW = "\033[43m"
WHITE = "\033[47m"
colors = (RED, GREEN, BLUE, YELLOW, WHITE, RESET)
# maze.build(None, True, True)
# maze.print_ascii(YELLOW)


def interface(colors) -> Any:
    maze.build(None, True, True)
    maze.print_ascii(RESET)
    colorindex: int = 0
    write_maze_file(maze, "output.txt")
    while True:
        print("=== A-MAZE-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")
        try:
            choice: int = int(input("choice? (1-4): "))
        except ValueError:
            print("Please enter a number.")
            continue

        if choice == 1:
            try:
                x: int | None = int(input("Enter a seed or leave it "
                                          "empty for a random Maze "
                                          "\n(Any invalid input will generate"
                                          " a random Maze ): "))
            except ValueError:
                x = None
                continue
            perfecto: str = "x"
            patterno: str = "x"
            while perfecto not in ("n", "y"):
                perfecto = input("Do you want your maze to be perfect (y/n): ")
            while patterno != "y" and patterno != "n":
                patterno: str = input("Do you want to add a 42 pattern"
                                      " to your maze (y/n): ")
            if patterno == "y":
                patternb: bool = True
            else:
                patternb: bool = False
            if perfecto == "y":
                perfectb: bool = True
            else:
                perfectb: bool = False
            maze.build(x, patternb, perfectb)
            maze.print_ascii(colors[colorindex - 1])
        elif choice == 2:
            directions, path = solve(maze)
            if colorindex == 0:
                maze.printsolved(colors[5], path)
            else:
                maze.printsolved(colors[colorindex - 1], path)

        elif choice == 3:
            if colorindex > 5:
                colorindex = 0
            colorindex += 1
            maze.print_ascii(colors[colorindex - 1])

        elif choice == 4:
            break
        else:
            print("You entered an unsupported number choose between 1-4")


interface(colors)