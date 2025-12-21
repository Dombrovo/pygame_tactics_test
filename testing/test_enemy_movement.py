"""
Test enemy movement distances to verify they're using correct movement_range.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from entities.enemy import Cultist, HoundOfTindalos

def test_enemy_stats():
    """
    Test that enemy units have correct movement_range stats.
    """
    print("=" * 60)
    print("ENEMY MOVEMENT STATS TEST")
    print("=" * 60)

    cultist = Cultist()
    hound = HoundOfTindalos()

    print(f"\nCultist Stats:")
    print(f"  Name: {cultist.name}")
    print(f"  Movement Range: {cultist.movement_range} tiles")
    print(f"  Weapon Range: {cultist.weapon_range} tiles")
    print(f"  Health: {cultist.max_health} HP")

    print(f"\nHound of Tindalos Stats:")
    print(f"  Name: {hound.name}")
    print(f"  Movement Range: {hound.movement_range} tiles")
    print(f"  Weapon Range: {hound.weapon_range} tiles")
    print(f"  Health: {hound.max_health} HP")

    print("\n" + "=" * 60)
    print("CURRENT AI BEHAVIOR (HARDCODED)")
    print("=" * 60)
    print(f"Cultists move: 1 tile (should be {cultist.movement_range})")
    print(f"Hounds move: 2 tiles (should be {hound.movement_range})")

    print("\n" + "=" * 60)
    print("IMPACT OF USING FULL MOVEMENT_RANGE")
    print("=" * 60)
    print(f"\nCultists (4 tiles):")
    print(f"  - Can cross ~40% of 10x10 grid in one turn")
    print(f"  - More aggressive positioning")
    print(f"  - Can close distance faster")

    print(f"\nHounds (6 tiles):")
    print(f"  - Can cross ~60% of 10x10 grid in one turn")
    print(f"  - VERY fast - can reach most positions quickly")
    print(f"  - Lives up to 'fast melee horror' description")

    print("\n" + "=" * 60)
    print("RECOMMENDATION")
    print("=" * 60)
    print("Change AI to use enemy.movement_range instead of hardcoded values")
    print("This makes stats meaningful and enemies more threatening")
    print("=" * 60)

if __name__ == "__main__":
    test_enemy_stats()
