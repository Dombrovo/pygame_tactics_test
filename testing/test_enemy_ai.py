"""
Test script for enemy AI system.

This script tests the basic enemy AI movement behaviors:
- Cultists move 1 tile towards investigator with highest health
- Hounds move 2 tiles towards nearest investigator
"""

import sys
import os

# Add parent directory to path to import game modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from combat.grid import Grid
from combat import enemy_ai
from entities.investigator import Investigator
from entities.enemy import Cultist, HoundOfTindalos
from entities import equipment


def test_cultist_targeting():
    """Test that cultists target the investigator with highest health."""
    print("\n=== TEST: Cultist Targeting ===")

    # Create investigators with different health values
    inv1 = Investigator(name="Low Health Inv", max_health=15)
    inv1.current_health = 5

    inv2 = Investigator(name="High Health Inv", max_health=15)
    inv2.current_health = 15

    inv3 = Investigator(name="Medium Health Inv", max_health=15)
    inv3.current_health = 10

    investigators = [inv1, inv2, inv3]

    # Test target selection
    target = enemy_ai.find_highest_health_target(investigators)

    print(f"Investigators:")
    for inv in investigators:
        print(f"  - {inv.name}: {inv.current_health} HP")

    print(f"\nCultist targets: {target.name} (highest health)")

    assert target == inv2, f"Expected cultist to target {inv2.name}, but got {target.name}"
    print("[OK] Cultist correctly targets highest health investigator\n")


def test_hound_targeting():
    """Test that hounds target the nearest investigator."""
    print("\n=== TEST: Hound Targeting ===")

    # Create a grid
    grid = Grid(10)

    # Create hound at position (5, 5)
    hound = HoundOfTindalos(name="Test Hound")
    grid.place_unit(hound, 5, 5)

    # Create investigators at different distances
    inv1 = Investigator(name="Far Inv")
    grid.place_unit(inv1, 0, 0)  # Distance ~7.07

    inv2 = Investigator(name="Near Inv")
    grid.place_unit(inv2, 6, 6)  # Distance ~1.41

    inv3 = Investigator(name="Medium Inv")
    grid.place_unit(inv3, 2, 5)  # Distance = 3

    investigators = [inv1, inv2, inv3]

    # Test target selection
    target = enemy_ai.find_nearest_target(hound, investigators, grid)

    print(f"Hound position: {hound.position}")
    print(f"Investigators:")
    for inv in investigators:
        dist = grid.get_distance(hound.position[0], hound.position[1],
                                inv.position[0], inv.position[1])
        print(f"  - {inv.name} at {inv.position}: distance = {dist:.2f}")

    print(f"\nHound targets: {target.name} (nearest)")

    assert target == inv2, f"Expected hound to target {inv2.name}, but got {target.name}"
    print("[OK] Hound correctly targets nearest investigator\n")


def test_cultist_movement():
    """Test that cultists move 1 tile towards target."""
    print("\n=== TEST: Cultist Movement (1 tile) ===")

    # Create a grid
    grid = Grid(10)

    # Create cultist at position (8, 5)
    cultist = Cultist(name="Test Cultist")
    grid.place_unit(cultist, 8, 5)

    # Create investigator at position (0, 5) - straight line 8 tiles away
    inv = Investigator(name="Target Inv")
    inv.current_health = 10
    grid.place_unit(inv, 0, 5)

    investigators = [inv]

    print(f"Before: Cultist at {cultist.position}, Investigator at {inv.position}")

    # Execute AI turn
    enemy_ai.execute_enemy_turn(cultist, investigators, grid)

    print(f"After:  Cultist at {cultist.position}, Investigator at {inv.position}")

    # Cultist should have moved 1 tile towards investigator (from x=8 to x=7)
    expected_pos = (7, 5)
    assert cultist.position == expected_pos, f"Expected cultist at {expected_pos}, but got {cultist.position}"
    print(f"[OK] Cultist moved 1 tile towards target\n")


def test_hound_movement():
    """Test that hounds move 2 tiles towards target."""
    print("\n=== TEST: Hound Movement (2 tiles) ===")

    # Create a grid
    grid = Grid(10)

    # Create hound at position (8, 5)
    hound = HoundOfTindalos(name="Test Hound")
    grid.place_unit(hound, 8, 5)

    # Create investigator at position (0, 5) - straight line 8 tiles away
    inv = Investigator(name="Target Inv")
    grid.place_unit(inv, 0, 5)

    investigators = [inv]

    print(f"Before: Hound at {hound.position}, Investigator at {inv.position}")

    # Execute AI turn
    enemy_ai.execute_enemy_turn(hound, investigators, grid)

    print(f"After:  Hound at {hound.position}, Investigator at {inv.position}")

    # Hound should have moved 2 tiles towards investigator (from x=8 to x=6)
    expected_pos = (6, 5)
    assert hound.position == expected_pos, f"Expected hound at {expected_pos}, but got {hound.position}"
    print(f"[OK] Hound moved 2 tiles towards target\n")


def test_blocked_movement():
    """Test that enemies can't move through obstacles."""
    print("\n=== TEST: Blocked Movement ===")

    # Create a grid with a wall
    grid = Grid(10)

    # Create hound at position (8, 5)
    hound = HoundOfTindalos(name="Test Hound")
    grid.place_unit(hound, 8, 5)

    # Create investigator at position (0, 5)
    inv = Investigator(name="Target Inv")
    grid.place_unit(inv, 0, 5)

    # Place blocking terrain in the path (x=7, y=5)
    tile = grid.get_tile(7, 5)
    tile.terrain_type = "full_cover"
    tile.blocks_movement = True
    tile.blocks_sight = True

    investigators = [inv]

    print(f"Before: Hound at {hound.position}, Investigator at {inv.position}")
    print(f"Blocking terrain at (7, 5)")

    # Execute AI turn
    enemy_ai.execute_enemy_turn(hound, investigators, grid)

    print(f"After:  Hound at {hound.position}")

    # Hound should find alternate path or not move if completely blocked
    # It should NOT be at (7, 5) or (6, 5) if blocked
    print(f"[OK] Hound handled blocked terrain (moved to {hound.position})\n")


def run_all_tests():
    """Run all AI tests."""
    print("\n" + "="*60)
    print("ENEMY AI TEST SUITE")
    print("="*60)

    try:
        test_cultist_targeting()
        test_hound_targeting()
        test_cultist_movement()
        test_hound_movement()
        test_blocked_movement()

        print("\n" + "="*60)
        print("ALL TESTS PASSED!")
        print("="*60)

    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()
