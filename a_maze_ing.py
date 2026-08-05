from maze import Maze
from parser import parse_config
from typing import Any
from solver import solve
from converter import write_maze_file


def main() -> Any:
    config = parse_config("config.txt")
    output_file = config["OUTPUT_FILE"]
    maze = Maze(
        config["WIDTH"],
        config["HEIGHT"],
        config["ENTRY"],
        config["EXIT"],
    )
    if (config["SEED"] is not None):
        seed = config["SEED"]
    else:
        seed = None

    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    YELLOW = "\033[33m"
    WHITE = "\033[37m"
    PINK = "\033[38;5;217m"

    colors = (RESET, RED, GREEN, BLUE, YELLOW, WHITE, PINK)
    maze.build(seed, True, True)
    colorindex: int = 0
    write_maze_file(maze, output_file)
    maze.print_ascii(colors[colorindex], True)
    patternb: bool = True
    seed: int | None = None
    solved: bool = False
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
            b: bool = True
            while b:
                x = input("Enter a seed or leave it "
                          "empty for a random Maze: ")
                if x == "":
                    seed = None
                    b = False
                else:
                    try:
                        seed = int(x)
                        b = False
                    except ValueError:
                        print("Please enter a valid integer"
                              " or leave it empty.")
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
            maze.build(seed, patternb, perfectb)
            maze.print_ascii(colors[colorindex], patternb)
            solved = False
        elif choice == 2:
            directions, path = solve(maze)
            if solved:
                solved = False
                maze.print_ascii(colors[colorindex], patternb)
            else:
                solved = True
                maze.printsolved(colors[colorindex], patternb, path)

        elif choice == 3:
            if colorindex > 5:
                colorindex = 0
            colorindex += 1
            if solved:
                maze.printsolved(colors[colorindex], patternb, path)
            else:
                maze.print_ascii(colors[colorindex], patternb)

        elif choice == 4:
            break
        else:
            print("You entered an unsupported number choose between 1-4")


if __name__ == "__main__":
    main()
