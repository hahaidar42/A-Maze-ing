#!/usr/bin/env python3
"""Maze generator configuration parser."""

import sys
from typing import Dict, Tuple, Union, Optional


def parse_bool(value: str) -> bool:
    """Convert string to boolean (case-insensitive).

    Args:
        value: String like 'True', 'False', 'true', 'false', etc.

    Returns:
        Boolean value.

    Raises:
        ValueError: If the string cannot be converted to boolean.
    """
    value_lower = value.strip().lower()
    if value_lower == "true":
        return True
    elif value_lower == "false":
        return False
    else:
        raise ValueError(f"PERFECT must be True or False, got '{value}'")


def parse_int(value: str) -> int:
    """Convert string to integer with error handling.

    Args:
        value: String to convert to integer.

    Returns:
        Integer value.

    Raises:
        ValueError: If the string cannot be converted to integer.
    """
    try:
        return int(value.strip())
    except ValueError as error:
        raise ValueError(f"expected integer, got '{value}'") from error


def parse_coords(value: str) -> Tuple[int, int]:
    """Convert "x,y" string to tuple of integers.

    Args:
        value: Coordinate string like "0,0" or "10, 5".

    Returns:
        Tuple of (x, y) integers.

    Raises:
        ValueError: If the string cannot be parsed as coordinates.
    """
    try:
        value = value.strip()
        x, y = value.split(",", 1)
        return (int(x.strip()), int(y.strip()))
    except ValueError as error:
        raise ValueError(
            f"invalid coordinate format, expected 'x,y' got '{value}'") from error


def parse_config(filepath: str) -> Dict[str, Union[int, str, Tuple[int, int], bool, Optional[int]]]:
    """Parse and validate configuration file.

    Args:
        filepath: Path to the configuration file.

    Returns:
        Validated configuration dictionary with proper types.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        ValueError: If the configuration is invalid.
    """
    config = {}

    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                if '=' not in line:
                    raise ValueError(
                        f"invalid line format (missing '='): {line}")

                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"configuration file '{filepath}' not found")

    # Check required keys (SEED is optional)
    required = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}
    missing = required - config.keys()
    if missing:
        raise ValueError(f"Missing required keys: {missing}")

    # Convert and validate values
    width = parse_int(config["WIDTH"])
    height = parse_int(config["HEIGHT"])
    entry = parse_coords(config["ENTRY"])
    exit_coords = parse_coords(config["EXIT"])
    perfect = parse_bool(config["PERFECT"])
    output_file = config["OUTPUT_FILE"].strip()
    seed = parse_int(config["SEED"]) if "SEED" in config else None

    # Validate ranges
    if width <= 0 or height <= 0:
        raise ValueError(
            f"Width and height must be positive, got {width}x{height}")

    # Check entry bounds
    if not (0 <= entry[0] < width and 0 <= entry[1] < height):
        raise ValueError(
            f"Entry {entry} out of bounds for {width}x{height} maze")

    # Check exit bounds
    if not (0 <= exit_coords[0] < width and 0 <= exit_coords[1] < height):
        raise ValueError(
            f"Exit {exit_coords} out of bounds for {width}x{height} maze")

    # Check entry != exit
    if entry == exit_coords:
        raise ValueError(f"Entry and exit must be different, both are {entry}")

    # Return validated config
    return {
        "WIDTH": width,
        "HEIGHT": height,
        "ENTRY": entry,
        "EXIT": exit_coords,
        "OUTPUT_FILE": output_file,
        "PERFECT": perfect,
        "SEED": seed
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt", file=sys.stderr)
        sys.exit(1)

    try:
        config = parse_config(sys.argv[1])
        print("Configuration loaded successfully:")
        for key, value in config.items():
            print(f"  {key}: {value}")
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
