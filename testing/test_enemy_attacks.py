"""
Test enemy attack system.

Tests that enemies can:
1. Move toward targets
2. Attack targets after moving (if in range)
3. Properly use combat resolver for damage
"""

from combat.grid import Grid
from combat.terrain_generator import generate_terrain
from entities.investigator import Investigator
from entities.enemy import Cultist, HoundOfTindalos
from combat import enemy_ai
import config


def test_cultist_attack():
    """Test that Cultist moves and attacks if in range."""
    print("\n[TEST] Cultist Move + Attack")
    print("=" * 50)

    # Create grid (empty, no terrain)
    grid = Grid(size=10)

    # Create investigator at (5, 5) with high health
    investigator = Investigator.create_random()
    investigator.current_health = 20  # Highest health
    grid.place_unit(investigator, 5, 5)

    # Create cultist at (4, 4) - 1.41 tiles away (diagonal)
    cultist = Cultist()
    grid.place_unit(cultist, 4, 4)

    print(f"Setup:")
    print(f"  Cultist at (4, 4) - HP: {cultist.current_health}/{cultist.max_health}")
    print(f"  {investigator.name} at (5, 5) - HP: {investigator.current_health}/{investigator.max_health}")
    print(f"  Cultist weapon: {cultist.weapon.name} (Range: {cultist.weapon_range})")
    print(f"  Distance: {grid.get_distance(4, 4, 5, 5):.2f} tiles")

    # Execute enemy turn
    print(f"\nExecuting Cultist turn...")
    result = enemy_ai.execute_enemy_turn(cultist, [investigator], grid)

    # Check result
    if result:
        print(f"\n[RESULT] Attack executed!")
        print(f"  Hit: {result.get('hit', False)}")
        print(f"  Hit chance: {result.get('hit_chance', 0)}%")
        print(f"  Roll: {result.get('roll', 0)}")

        if result.get('hit'):
            damage = result.get('damage_dealt', 0)
            print(f"  Damage dealt: {damage}")
            print(f"  {investigator.name} HP: {investigator.current_health}/{investigator.max_health}")

            if result.get('target_killed'):
                print(f"  [!] {investigator.name} INCAPACITATED!")
        else:
            print(f"  Attack missed")

        print(f"\n[OK] Cultist successfully attacked after moving")
    else:
        print(f"\n[!] No attack result - likely out of range or no LOS")
        print(f"  Cultist position: {cultist.position}")
        print(f"  Target position: {investigator.position}")

    print("=" * 50)


def test_hound_attack():
    """Test that Hound moves and attacks if in range."""
    print("\n[TEST] Hound of Tindalos Move + Attack")
    print("=" * 50)

    # Create grid (empty, no terrain)
    grid = Grid(size=10)

    # Create investigator at (5, 5)
    investigator = Investigator.create_random()
    investigator.current_health = 15
    grid.place_unit(investigator, 5, 5)

    # Create hound at (2, 2) - farther away, needs to move 2 tiles
    hound = HoundOfTindalos()
    grid.place_unit(hound, 2, 2)

    print(f"Setup:")
    print(f"  Hound at (2, 2) - HP: {hound.current_health}/{hound.max_health}")
    print(f"  {investigator.name} at (5, 5) - HP: {investigator.current_health}/{investigator.max_health}")
    print(f"  Hound weapon: {hound.weapon.name} (Range: {hound.weapon_range})")
    print(f"  Initial distance: {grid.get_distance(2, 2, 5, 5):.2f} tiles")
    print(f"  Hound movement: 2 tiles")

    # Execute enemy turn
    print(f"\nExecuting Hound turn...")
    result = enemy_ai.execute_enemy_turn(hound, [investigator], grid)

    # Check result
    print(f"\nFinal hound position: {hound.position}")
    print(f"Final distance: {grid.get_distance(hound.position[0], hound.position[1], 5, 5):.2f} tiles")

    if result:
        print(f"\n[RESULT] Attack executed!")
        print(f"  Hit: {result.get('hit', False)}")
        print(f"  Hit chance: {result.get('hit_chance', 0)}%")

        if result.get('hit'):
            damage = result.get('damage_dealt', 0)
            print(f"  Damage dealt: {damage}")
            print(f"  {investigator.name} HP: {investigator.current_health}/{investigator.max_health}")

        print(f"\n[OK] Hound successfully attacked after moving")
    else:
        print(f"\n[INFO] No attack (likely still out of range after moving)")
        print(f"  This is expected if hound couldn't close to melee range in 2 tiles")

    print("=" * 50)


def test_out_of_range():
    """Test that enemies don't attack when out of range."""
    print("\n[TEST] Out of Range - No Attack")
    print("=" * 50)

    # Create grid (empty, no terrain)
    grid = Grid(size=10)

    # Create investigator at (9, 9) - far corner
    investigator = Investigator.create_random()
    grid.place_unit(investigator, 9, 9)

    # Create cultist at (0, 0) - opposite corner
    cultist = Cultist()
    grid.place_unit(cultist, 0, 0)

    print(f"Setup:")
    print(f"  Cultist at (0, 0)")
    print(f"  {investigator.name} at (9, 9)")
    print(f"  Distance: {grid.get_distance(0, 0, 9, 9):.2f} tiles")
    print(f"  Cultist weapon range: {cultist.weapon_range}")

    # Execute enemy turn
    print(f"\nExecuting Cultist turn...")
    result = enemy_ai.execute_enemy_turn(cultist, [investigator], grid)

    # Should move but not attack (too far)
    print(f"\nCultist moved to: {cultist.position}")
    print(f"New distance: {grid.get_distance(cultist.position[0], cultist.position[1], 9, 9):.2f} tiles")

    if result is None:
        print(f"\n[OK] No attack executed (as expected - out of range)")
    else:
        print(f"\n[!] UNEXPECTED: Attack executed when out of range!")

    print("=" * 50)


def main():
    """Run all enemy attack tests."""
    print("\n" + "=" * 50)
    print("ENEMY ATTACK SYSTEM TESTS")
    print("=" * 50)

    # Run tests
    test_cultist_attack()
    test_hound_attack()
    test_out_of_range()

    print("\n" + "=" * 50)
    print("ALL TESTS COMPLETE")
    print("=" * 50)

    print("\nNote: Attack results are randomized (hit chance, damage cards)")
    print("Run multiple times to see different outcomes")


if __name__ == "__main__":
    main()
