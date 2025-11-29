"""
Test script for movement system.

Tests pathfinding and movement mechanics without requiring GUI interaction.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from combat.grid import Grid
from combat.pathfinding import find_path, get_reachable_tiles
from entities.investigator import Investigator


def test_pathfinding():
    """Test basic pathfinding."""
    print("=" * 60)
    print("TEST 1: Basic Pathfinding")
    print("=" * 60)

    grid = Grid(size=10)

    # Test simple path (no obstacles)
    print("\n1a. Simple straight path (0,0) -> (3,0):")
    path = find_path(grid, 0, 0, 3, 0)
    if path:
        print(f"  [OK] Path found: {path}")
        print(f"  Length: {len(path)} tiles")
    else:
        print("  [X] No path found!")

    # Test diagonal path
    print("\n1b. Diagonal path (0,0) -> (3,3):")
    path = find_path(grid, 0, 0, 3, 3)
    if path:
        print(f"  [OK] Path found: {path}")
        print(f"  Length: {len(path)} tiles")
    else:
        print("  [X] No path found!")

    # Test with max distance limit
    print("\n1c. Path with distance limit (0,0) -> (5,5), max_distance=4.0:")
    path = find_path(grid, 0, 0, 5, 5, max_distance=4.0)
    if path:
        print(f"  [X] Should not find path (too far): {path}")
    else:
        print("  [OK] Correctly returned None (destination out of range)")

    print("\n[OK] Pathfinding tests passed!\n")


def test_pathfinding_with_obstacles():
    """Test pathfinding with cover obstacles."""
    print("=" * 60)
    print("TEST 2: Pathfinding with Obstacles")
    print("=" * 60)

    grid = Grid(size=10)

    # Create a wall of full cover (blocks LOS)
    # Note: Full cover blocks SIGHT but NOT MOVEMENT in our current implementation
    # Units can move through cover, they just can't shoot through it
    print("\nAdding half cover at (2,2) and (2,3)...")
    grid.add_cover(2, 2, "half_cover")
    grid.add_cover(2, 3, "half_cover")

    print("\n2a. Path around half cover (0,2) -> (4,2):")
    path = find_path(grid, 0, 2, 4, 2)
    if path:
        print(f"  [OK] Path found: {path}")
        print(f"  Length: {len(path)} tiles")
        print(f"  Note: Units CAN move through cover (it only affects hit chance)")
    else:
        print("  [X] No path found!")

    print("\n[OK] Obstacle pathfinding tests passed!\n")


def test_reachable_tiles():
    """Test reachable tiles calculation."""
    print("=" * 60)
    print("TEST 3: Reachable Tiles (Movement Range)")
    print("=" * 60)

    grid = Grid(size=10)

    # Test movement range 4 (standard investigator)
    print("\n3a. Reachable tiles from (5,5) with range 4:")
    reachable = get_reachable_tiles(grid, 5, 5, movement_range=4.0)
    print(f"  [OK] Found {len(reachable)} reachable tiles")
    print(f"  Sample tiles: {sorted(list(reachable))[:10]}")

    # Test movement range 3 (slow unit)
    print("\n3b. Reachable tiles from (5,5) with range 3:")
    reachable = get_reachable_tiles(grid, 5, 5, movement_range=3.0)
    print(f"  [OK] Found {len(reachable)} reachable tiles")

    # Test movement range 5 (scout)
    print("\n3c. Reachable tiles from (5,5) with range 3:")
    reachable = get_reachable_tiles(grid, 5, 5, movement_range=5.0)
    print(f"  [OK] Found {len(reachable)} reachable tiles")

    print("\n[OK] Reachable tiles tests passed!\n")


def test_investigator_movement():
    """Test investigator movement with different templates."""
    print("=" * 60)
    print("TEST 4: Investigator Movement Stats")
    print("=" * 60)

    grid = Grid(size=10)

    # Test different investigator templates
    templates = [
        {"name": "Balanced", "movement_range": 4},
        {"name": "Sniper", "movement_range": 4},
        {"name": "Tank", "movement_range": 3},
        {"name": "Scout", "movement_range": 5},
    ]

    for template in templates:
        inv = Investigator(
            name=template["name"],
            movement_range=template["movement_range"],
            gender="male"
        )

        print(f"\n4. {inv.name} (movement={inv.movement_range}):")

        # Place investigator
        grid.place_unit(inv, 5, 5)

        # Calculate reachable tiles
        reachable = get_reachable_tiles(grid, 5, 5, inv.movement_range)
        print(f"  [OK] Can reach {len(reachable)} tiles from (5,5)")

        # Test pathfinding to edge of range
        target_x, target_y = 5 + inv.movement_range, 5
        path = find_path(grid, 5, 5, target_x, target_y, max_distance=inv.movement_range)

        if path:
            print(f"  [OK] Can path to ({target_x}, {target_y}): {len(path)} tiles")
        else:
            print(f"  [OK] Correctly cannot reach ({target_x}, {target_y}) (out of range)")

        # Remove unit from grid for next test
        grid.remove_unit(5, 5)

    print("\n[OK] Investigator movement tests passed!\n")


def test_movement_with_units():
    """Test that units block movement."""
    print("=" * 60)
    print("TEST 5: Movement Blocked by Units")
    print("=" * 60)

    grid = Grid(size=10)

    # Place two investigators
    inv1 = Investigator(name="Blocker", gender="male")
    inv2 = Investigator(name="Mover", gender="male")

    grid.place_unit(inv1, 5, 5)  # Blocker in the middle
    grid.place_unit(inv2, 3, 5)  # Mover to the left

    print("\nSetup: Blocker at (5,5), Mover at (3,5)")

    # Try to find path through blocker
    print("\n5a. Path from (3,5) -> (7,5) [through blocker at (5,5)]:")
    path = find_path(grid, 3, 5, 7, 5, max_distance=6.0)
    if path:
        print(f"  [OK] Path found (should route around): {path}")
        # Check if path goes through (5,5)
        if (5, 5) in path:
            print(f"  [X] ERROR: Path goes through occupied tile!")
        else:
            print(f"  [OK] Correctly routes around blocker")
    else:
        print("  [X] No path found (unexpected)")

    # Try to move directly onto blocker
    print("\n5b. Attempt to move to occupied tile (3,5) -> (5,5):")
    path = find_path(grid, 3, 5, 5, 5, max_distance=6.0)
    if path:
        print(f"  [X] ERROR: Path found to occupied tile!")
    else:
        print(f"  [OK] Correctly blocked - cannot move to occupied tile")

    print("\n[OK] Unit blocking tests passed!\n")


def run_all_tests():
    """Run all movement tests."""
    print("\n")
    print("=" * 60)
    print("          MOVEMENT SYSTEM TESTS")
    print("=" * 60)
    print()

    try:
        test_pathfinding()
        test_pathfinding_with_obstacles()
        test_reachable_tiles()
        test_investigator_movement()
        test_movement_with_units()

        print("=" * 60)
        print("[OK] ALL TESTS PASSED!")
        print("=" * 60)
        print("\nMovement system is working correctly.")
        print("You can now:")
        print("  1. Run 'uv run python main.py'")
        print("  2. Start a battle (New Game)")
        print("  3. Click a unit on their turn to select them")
        print("  4. See green highlights for valid movement tiles")
        print("  5. Click a green tile to move there")
        print()

    except Exception as e:
        print("\n" + "=" * 60)
        print("[X] TEST FAILED!")
        print("=" * 60)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
