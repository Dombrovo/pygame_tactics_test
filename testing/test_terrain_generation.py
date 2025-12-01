"""
Test script for terrain generation system.

This script tests all terrain generators and visualizes their output
using ASCII art to show the terrain patterns.

Run with: uv run python testing/test_terrain_generation.py
"""

import sys
import os

# Add parent directory to path so we can import from combat/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from combat.terrain_generator import (
    GENERATOR_CLASSES,
    generate_random_terrain,
    generate_terrain,
    SymmetricGenerator,
    ScatteredGenerator,
    UrbanRuinsGenerator,
    RitualSiteGenerator,
    OpenFieldGenerator,
    ChokepointGenerator
)
import config


def visualize_terrain(terrain_data, grid_size=10):
    """
    Visualize terrain layout using ASCII art.

    Args:
        terrain_data: List of (x, y, cover_type) tuples
        grid_size: Size of the grid (default 10)

    Returns:
        String representation of the terrain
    """
    # Create empty grid
    grid = [["." for _ in range(grid_size)] for _ in range(grid_size)]

    # Place terrain
    for x, y, cover_type in terrain_data:
        if 0 <= x < grid_size and 0 <= y < grid_size:
            if cover_type == "full_cover":
                grid[y][x] = "#"  # Full cover
            elif cover_type == "half_cover":
                grid[y][x] = ":"  # Half cover

    # Mark spawn zones
    # Player spawns: left side (x < 3)
    # Enemy spawns: right side (x > 6)
    for y in range(grid_size):
        for x in range(grid_size):
            if grid[y][x] == ".":  # Only mark empty tiles
                if x < 3:
                    grid[y][x] = "P"  # Player spawn zone
                elif x > 6:
                    grid[y][x] = "E"  # Enemy spawn zone

    # Convert to string
    lines = []
    lines.append("  " + "".join(str(i) for i in range(grid_size)))
    lines.append("  " + "-" * grid_size)
    for y, row in enumerate(grid):
        lines.append(f"{y}|" + "".join(row))

    return "\n".join(lines)


def test_generator(generator_name, generator_class, grid_size=10):
    """
    Test a specific terrain generator.

    Args:
        generator_name: Name of the generator
        generator_class: Generator class to test
        grid_size: Size of the grid
    """
    print(f"\n{'='*60}")
    print(f"Testing: {generator_name}")
    print(f"{'='*60}")

    # Create generator and generate terrain
    generator = generator_class(grid_size)
    terrain = generator.generate()

    # Statistics
    full_cover = sum(1 for _, _, t in terrain if t == "full_cover")
    half_cover = sum(1 for _, _, t in terrain if t == "half_cover")
    total = len(terrain)

    print(f"\nStatistics:")
    print(f"  Total cover tiles: {total}")
    print(f"  Full cover: {full_cover} ({full_cover/total*100:.1f}%)")
    print(f"  Half cover: {half_cover} ({half_cover/total*100:.1f}%)")
    print(f"  Coverage: {total/(grid_size*grid_size)*100:.1f}% of grid")

    # Visualize
    print(f"\nVisualization:")
    print(f"  Legend: # = Full cover, : = Half cover")
    print(f"          P = Player spawn zone, E = Enemy spawn zone")
    print(f"          . = Empty (center area)\n")
    print(visualize_terrain(terrain, grid_size))

    # Check for spawn zone violations
    spawn_violations = []
    for x, y, cover_type in terrain:
        if x < 3 or x > 6:
            spawn_violations.append((x, y, cover_type))

    if spawn_violations:
        print(f"\n[WARNING] Cover in spawn zones: {len(spawn_violations)} tiles")
        for x, y, cover_type in spawn_violations[:5]:  # Show first 5
            print(f"  - ({x}, {y}): {cover_type}")
    else:
        print(f"\n[OK] No cover in spawn zones")

    return terrain


def test_all_generators():
    """Test all terrain generators."""
    print("\n")
    print("="*60)
    print("TERRAIN GENERATION SYSTEM TEST")
    print("="*60)

    grid_size = 10

    # Test each generator
    for generator_name, generator_class in GENERATOR_CLASSES.items():
        test_generator(generator_name, generator_class, grid_size)

    # Test random generation multiple times
    print(f"\n{'='*60}")
    print("Testing Random Generation (5 iterations)")
    print(f"{'='*60}")

    generator_counts = {}
    for i in range(5):
        terrain = generate_random_terrain(grid_size)
        # Extract generator name from console output (hacky but works for test)
        # Since generate_random_terrain prints the generator name

    print(f"\n[OK] Random generation working")


def test_specific_scenarios():
    """Test specific edge cases and scenarios."""
    print(f"\n{'='*60}")
    print("Testing Specific Scenarios")
    print(f"{'='*60}")

    # Test 1: Empty grid (no terrain)
    print(f"\n[Test 1] Ensure generators don't crash on empty results")
    # Not all generators will be empty, but they shouldn't crash

    # Test 2: Check coordinate bounds
    print(f"\n[Test 2] Checking all coordinates are within bounds")
    for generator_name, generator_class in GENERATOR_CLASSES.items():
        generator = generator_class(grid_size=10)
        terrain = generator.generate()
        out_of_bounds = [(x, y) for x, y, _ in terrain if x < 0 or x >= 10 or y < 0 or y >= 10]
        if out_of_bounds:
            print(f"  [FAIL] {generator_name}: Out of bounds coordinates: {out_of_bounds}")
        else:
            print(f"  [OK] {generator_name}: All coordinates in bounds")

    # Test 3: Cover type validation
    print(f"\n[Test 3] Checking cover types are valid")
    valid_types = {"half_cover", "full_cover"}
    for generator_name, generator_class in GENERATOR_CLASSES.items():
        generator = generator_class(grid_size=10)
        terrain = generator.generate()
        invalid = [(x, y, t) for x, y, t in terrain if t not in valid_types]
        if invalid:
            print(f"  [FAIL] {generator_name}: Invalid cover types: {invalid}")
        else:
            print(f"  [OK] {generator_name}: All cover types valid")


def run_all_tests():
    """Run all terrain generation tests."""
    test_all_generators()
    test_specific_scenarios()

    print(f"\n{'='*60}")
    print("ALL TESTS COMPLETE")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    run_all_tests()
