from maze import Maze
from parser import parse_config

config = parse_config("config.txt")
maze = Maze(
    config["WIDTH"],
    config["HEIGHT"],
    config["ENTRY"],
    config["EXIT"],
)
maze.build(config["SEED"], True)
maze.print_ascii()
