#!/usr/bin/env python3
"""Test script for convert.py functionality."""

import os
from maze import Maze, Cell
from converter import cell_to_hex, grid_to_lines, write_maze_file


def test_cell_to_hex() -> None:
    """Test hex encoding for various wall configurations."""
    print("Testing cell_to_hex()...")
    
    # Test 1: all walls open
    c1 = Cell(0, 0)
    c1.north_wall = False
    c1.east_wall = False
    c1.south_wall = False
    c1.west_wall = False
    result = cell_to_hex(c1)
    assert result == "0", f"All open: expected '0', got '{result}'"
    print("  ✓ All walls open → '0'")
    
    # Test 2: all walls closed
    c2 = Cell(0, 0)
    c2.north_wall = True
    c2.east_wall = True
    c2.south_wall = True
    c2.west_wall = True
    result = cell_to_hex(c2)
    assert result == "f", f"All closed: expected 'f', got '{result}'"
    print("  ✓ All walls closed → 'f'")
    
    # Test 3: north + east (binary 0011 = 3)
    c3 = Cell(0, 0)
    c3.north_wall = True
    c3.east_wall = True
    c3.south_wall = False
    c3.west_wall = False
    result = cell_to_hex(c3)
    assert result == "3", f"North+East: expected '3', got '{result}'"
    print("  ✓ North + East walls → '3'")
    
    # Test 4: east + west (binary 1010 = 10 = a)
    c4 = Cell(0, 0)
    c4.north_wall = False
    c4.east_wall = True
    c4.south_wall = False
    c4.west_wall = True
    result = cell_to_hex(c4)
    assert result == "a", f"East+West: expected 'a', got '{result}'"
    print("  ✓ East + West walls → 'a'")
    
    # Test 5: single wall variants
    c5 = Cell(0, 0)
    c5.north_wall = True
    result = cell_to_hex(c5)
    assert result == "1", f"North only: expected '1', got '{result}'"
    print("  ✓ North only → '1'")
    
    c6 = Cell(0, 0)
    c6.east_wall = True
    result = cell_to_hex(c6)
    assert result == "2", f"East only: expected '2', got '{result}'"
    print("  ✓ East only → '2'")
    
    c7 = Cell(0, 0)
    c7.south_wall = True
    result = cell_to_hex(c7)
    assert result == "4", f"South only: expected '4', got '{result}'"
    print("  ✓ South only → '4'")
    
    c8 = Cell(0, 0)
    c8.west_wall = True
    result = cell_to_hex(c8)
    assert result == "8", f"West only: expected '8', got '{result}'"
    print("  ✓ West only → '8'")


def test_grid_to_lines() -> None:
    """Test grid conversion to hex lines."""
    print("\nTesting grid_to_lines()...")
    
    maze = Maze(3, 3, (0, 0), (2, 2))
    maze.build(seed=42)
    
    lines = grid_to_lines(maze)
    
    # Check number of lines
    assert len(lines) == 3, f"Expected 3 lines, got {len(lines)}"
    print(f"  ✓ Correct line count: {len(lines)}")
    
    # Check each line length
    for i, line in enumerate(lines):
        assert len(line) == 3, f"Line {i}: expected length 3, got {len(line)}"
        # Check all characters are valid hex
        for j, char in enumerate(line):
            assert char in "0123456789abcdef", \
                f"Line {i}, char {j}: '{char}' is not valid hex"
    print("  ✓ All lines correct length and valid hex digits")
    
    # Print for visual inspection
    print("  Grid output:")
    for line in lines:
        print(f"    {line}")


def test_write_maze_file() -> None:
    """Test full file output format."""
    print("\nTesting write_maze_file()...")
    
    test_file = "test_output.txt"
    
    # Clean up if exists
    if os.path.exists(test_file):
        os.remove(test_file)
    
    maze = Maze(5, 5, (0, 0), (4, 4))
    maze.build(seed=42)
    
    write_maze_file(maze, test_file)
    
    # Read back and verify
    with open(test_file, 'r') as f:
        lines = f.read().splitlines()
    
    # Should have: 5 grid + 1 blank + 1 entry + 1 exit + 1 path = 9 lines
    assert len(lines) == 9, f"Expected 9 lines, got {len(lines)}"
    print(f"  ✓ Correct total line count: {len(lines)}")
    
    # Check grid lines (first 5)
    for i in range(5):
        assert len(lines[i]) == 5, f"Grid line {i}: expected length 5"
    print("  ✓ Grid lines correct length")
    
    # Check blank line (line 5)
    assert lines[5] == "", f"Expected blank line at position 5, got '{lines[5]}'"
    print("  ✓ Blank line present")
    
    # Check entry line
    assert lines[6] == "0,0", f"Expected entry '0,0', got '{lines[6]}'"
    print(f"  ✓ Entry: {lines[6]}")
    
    # Check exit line
    assert lines[7] == "4,4", f"Expected exit '4,4', got '{lines[7]}'"
    print(f"  ✓ Exit: {lines[7]}")
    
    # Check path exists and is valid directions
    path = lines[8]
    assert len(path) > 0, "Path should not be empty"
    assert all(c in "NESW" for c in path), f"Invalid characters in path: {path}"
    print(f"  ✓ Path: {path} (length: {len(path)})")
    
    # Print full file for inspection
    print("\n  Full file content:")
    with open(test_file, 'r') as f:
        print(f.read())
    
    # Cleanup
    os.remove(test_file)
    print("  ✓ Cleanup complete")


def test_coherence() -> None:
    """Test wall coherence between adjacent cells."""
    print("\nTesting wall coherence...")
    
    maze = Maze(4, 4, (0, 0), (3, 3))
    maze.build(seed=123)
    
    # Check that shared walls match
    issues = []
    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.get_cell(x, y)
            
            # Check east-west coherence
            if x + 1 < maze.width:
                neighbor = maze.get_cell(x + 1, y)
                if cell.east_wall != neighbor.west_wall:
                    issues.append(f"({x},{y}) east vs ({x+1},{y}) west mismatch")
            
            # Check north-south coherence
            if y + 1 < maze.height:
                neighbor = maze.get_cell(x, y + 1)
                if cell.south_wall != neighbor.north_wall:
                    issues.append(f"({x},{y}) south vs ({x},{y+1}) north mismatch")
    
    if issues:
        for issue in issues:
            print(f"  ✗ {issue}")
        raise AssertionError(f"Found {len(issues)} coherence issues")
    else:
        print("  ✓ All adjacent walls coherent")


if __name__ == "__main__":
    test_cell_to_hex()
    test_grid_to_lines()
    test_write_maze_file()
    test_coherence()
    print("\n" + "=" * 40)
    print("ALL TESTS PASSED!")
    print("=" * 40)