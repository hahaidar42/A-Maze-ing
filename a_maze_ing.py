from maze import Maze
from parser import parse_config
from typing import Any, cast
from solver import solve
from converter import write_maze_file
import os


def main() -> Any:
    """
    Main application loop for the maze generator.

    Reads configuration, generates the maze, and provides an interactive
    terminal menu for controlling the maze display.

    Features:
        - Maze regeneration with optional seed increment
        - Toggle path display
        - Rotate wall colors
        - Graceful exit

    Returns:
        Any: The application exits with no return value.

    Raises:
        KeyboardInterrupt: Handled gracefully with a user message.
        Exception: General exceptions are caught and displayed.
    """
    config = parse_config("config.txt")
    output_file = cast(str, config["OUTPUT_FILE"])
    width: int = cast(int, config["WIDTH"])
    height: int = cast(int, config["HEIGHT"])
    entry: tuple[int, int] = cast(tuple[int, int], config["ENTRY"])
    exit_: tuple[int, int] = cast(tuple[int, int], config["EXIT"])
    perfect: bool = cast(bool, config["PERFECT"])
    algo: str = cast(str, config["ALGO"])
    maze = Maze(
        width,
        height,
        entry,
        exit_,
    )
    os.system("cls" if os.name == "nt" else "clear")
    if config["SEED"] is not None:
        seed = cast(int | None, config["SEED"])
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
    maze.build(seed, True, perfect, algo)  # need to add algo
    colorindex: int = 0
    write_maze_file(maze, output_file)
    maze.print_ascii(colors[colorindex], True)
    patternb: bool = True
    seed = None
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
            os.system("cls" if os.name == "nt" else "clear")
            if seed:
                seed += 1
            maze.build(seed, True, perfect, algo)  # need to add algo
            maze.print_ascii(colors[colorindex], patternb)
            solved = False

        elif choice == 2:
            directions, path = solve(maze)
            if solved:
                solved = False
                os.system("cls" if os.name == "nt" else "clear")
                maze.print_ascii(colors[colorindex], patternb)
            else:
                solved = True
                os.system("cls" if os.name == "nt" else "clear")
                maze.animate_path(path, colors[colorindex],)

        elif choice == 3:
            os.system("cls" if os.name == "nt" else "clear")
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
        print("\ninvalid input")
    except Exception as e:
        print(e)
