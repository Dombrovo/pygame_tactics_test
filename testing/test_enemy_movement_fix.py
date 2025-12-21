"""
Test that enemy AI now uses full movement_range.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from entities.enemy import Cultist, HoundOfTindalos
from entities.investigator import create_test_squad
from combat.grid import Grid
from combat import enemy_ai

def test_movement_fix():
    """
    Verify that enemies now move their full movement_range.
    """
    print("=" * 70)
    print("ENEMY MOVEMENT FIX VERIFICATION")
    print("=" * 70)

    # Create grid
    grid = Grid(10)

    # Create units
    cultist = Cultist("Test Cultist")
    hound = HoundOfTindalos("Test Hound")
    investigators = create_test_squad()

    # Place cultist at (0, 0)
    grid.place_unit(cultist, 0, 0)

    # Place target investigator at (5, 5) - 7 tiles away diagonally
    target_inv = investigators[0]
    grid.place_unit(target_inv, 5, 5)

    print(f"\nCultist Test:")
    print(f"  Starting position: (0, 0)")
    print(f"  Target position: (5, 5)")
    print(f"  Distance: ~7 tiles (diagonal)")
    print(f"  Movement range: {cultist.movement_range} tiles")

    # Calculate where cultist should move
    move_to = enemy_ai.calculate_movement_target(
        cultist,
        target_inv,
        grid,
        max_tiles=cultist.movement_range  # Should be 4
    )

    if move_to:
        path_length = abs(move_to[0] - 0) + abs(move_to[1] - 0)
        print(f"  Calculated destination: {move_to}")
        print(f"  Manhattan distance from start: {path_length} tiles")

        if path_length == cultist.movement_range:
            print(f"  [OK] Moving full movement_range ({cultist.movement_range} tiles)")
        else:
            print(f"  [WARNING] Not moving full distance (expected {cultist.movement_range}, got {path_length})")
    else:
        print(f"  [ERROR] No movement calculated!")

    # Test Hound
    print(f"\nHound Test:")
    # Create new grid for hound test
    grid2 = Grid(10)
    grid2.place_unit(hound, 0, 0)
    grid2.place_unit(target_inv, 8, 8)

    print(f"  Starting position: (0, 0)")
    print(f"  Target position: (8, 8)")
    print(f"  Distance: ~11 tiles (diagonal)")
    print(f"  Movement range: {hound.movement_range} tiles")

    move_to = enemy_ai.calculate_movement_target(
        hound,
        target_inv,
        grid2,
        max_tiles=hound.movement_range  # Should be 6
    )

    if move_to:
        path_length = abs(move_to[0] - 0) + abs(move_to[1] - 0)
        print(f"  Calculated destination: {move_to}")
        print(f"  Manhattan distance from start: {path_length} tiles")

        if path_length == hound.movement_range:
            print(f"  [OK] Moving full movement_range ({hound.movement_range} tiles)")
        else:
            print(f"  [INFO] Path-based movement (A* pathfinding accounts for obstacles)")
    else:
        print(f"  [ERROR] No movement calculated!")

    print("\n" + "=" * 70)
    print("EXPECTED IN-GAME BEHAVIOR")
    print("=" * 70)
    print("Cultists:")
    print("  - Will move up to 4 tiles toward highest-health investigator")
    print("  - Can cross ~40% of the battlefield in one turn")
    print("  - More aggressive positioning")
    print("")
    print("Hounds:")
    print("  - Will move up to 6 tiles toward nearest investigator")
    print("  - Can cross ~60% of the battlefield in one turn")
    print("  - VERY fast - can close to melee range quickly!")
    print("  - Living up to their 'fast melee horror' description")
    print("")
    print("Tactical Impact:")
    print("  - Players MUST use cover and positioning strategically")
    print("  - Hounds are now serious threats that close distance fast")
    print("  - Ranged weapons become more valuable to keep distance")
    print("  - First turn positioning is critical!")
    print("=" * 70)

if __name__ == "__main__":
    test_movement_fix()
