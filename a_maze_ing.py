from maze import Maze
from parser import parse_config
from typing import Any
from solver import solve
from converter import write_maze_file


def main() -> Any:
    config = parse_config("config.txt")
    output_file = config["OUTPUT_FILE"]
    width: int = config["WIDTH"]
    height: int = config["HEIGHT"]
    entry: tuple[int, int] = config["ENTRY"]
    exit_: tuple[int, int] = config["EXIT"]
    perfect: bool = config["PERFECT"]
    maze = Maze(
        width,
        height,
        entry,
        exit_,
    )
    if (config["SEED"] is not None):
        seed: int | None = config["SEED"]
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
    maze.build(seed, True, perfect)
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
            if seed:
                seed += 1
            print("\033[H\033[J", end="")
            maze.build(seed, True, perfect)
            maze.print_ascii(colors[colorindex], patternb)
            solved = False
        elif choice == 2:
            directions, path = solve(maze)
            if solved:
                solved = False
                print("\033[H\033[J", end="")
                maze.print_ascii(colors[colorindex], patternb)
            else:
                solved = True
                maze.animate_path(path, colors[colorindex],)

        elif choice == 3:
            print("\033[H\033[J", end="")
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
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
