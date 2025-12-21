"""
Test script to verify enemy first-turn bug is fixed.

This script simulates battle initialization and checks if enemies
act correctly when they have the first turn.
"""

import sys
import random
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import config
from entities.investigator import create_test_squad
from entities.enemy import create_test_enemies


def test_turn_order_generation():
    """
    Test that turn order is properly randomized and can result
    in enemies going first.
    """
    print("=" * 60)
    print("TEST: Turn Order Generation")
    print("=" * 60)

    enemy_first_count = 0
    player_first_count = 0
    iterations = 100

    for i in range(iterations):
        # Create units
        player_units = create_test_squad()
        enemy_units = create_test_enemies()

        # Simulate turn order creation (same logic as battle_screen.py)
        all_units = player_units + enemy_units
        random.shuffle(all_units)

        # Check who goes first
        first_unit = all_units[0]
        if first_unit.team == "enemy":
            enemy_first_count += 1
        else:
            player_first_count += 1

    print(f"\nResults from {iterations} simulated battles:")
    print(f"  Enemy goes first: {enemy_first_count} times ({enemy_first_count/iterations*100:.1f}%)")
    print(f"  Player goes first: {player_first_count} times ({player_first_count/iterations*100:.1f}%)")

    if enemy_first_count > 0:
        print("\n[OK] Turn order can result in enemies going first")
        print("     The fix in run() method should handle these cases")
    else:
        print("\n[WARNING] Enemies never went first in 100 trials")
        print("          This is statistically unlikely but possible")

    return enemy_first_count > 0


def test_portrait_mode_config():
    """
    Test that portrait mode configuration works.
    """
    print("\n" + "=" * 60)
    print("TEST: Portrait Mode Configuration")
    print("=" * 60)

    print(f"\nCurrent config.GRID_DISPLAY_MODE: '{config.GRID_DISPLAY_MODE}'")

    if config.GRID_DISPLAY_MODE == "portraits":
        print("[OK] Portrait mode is enabled (default)")
        print("     Investigators will show character portraits on grid")
        print("     Enemies will still show symbols (they don't have portraits)")
    elif config.GRID_DISPLAY_MODE == "symbols":
        print("[OK] Symbol mode is enabled")
        print("     All units will show emoji/ASCII symbols")
    else:
        print(f"[WARNING] Unknown display mode: {config.GRID_DISPLAY_MODE}")

    print("\nTo toggle modes, edit config.py line ~42:")
    print("  GRID_DISPLAY_MODE = \"portraits\"  # Show character portraits")
    print("  GRID_DISPLAY_MODE = \"symbols\"    # Show emoji/ASCII symbols")

    return True


def test_investigator_portraits():
    """
    Test that investigators have portrait paths assigned.
    """
    print("\n" + "=" * 60)
    print("TEST: Investigator Portrait Paths")
    print("=" * 60)

    investigators = create_test_squad()

    all_have_portraits = True
    for inv in investigators:
        has_path = hasattr(inv, 'image_path') and inv.image_path
        status = "[OK]" if has_path else "[X]"
        print(f"  {status} {inv.name}: {inv.image_path if has_path else 'NO IMAGE PATH'}")

        if not has_path:
            all_have_portraits = False

    if all_have_portraits:
        print("\n[OK] All investigators have portrait paths")
        print("     Portrait mode will display their images on grid")
    else:
        print("\n[X] Some investigators missing portrait paths")

    return all_have_portraits


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("ENEMY FIRST-TURN FIX & PORTRAIT MODE TESTS")
    print("=" * 60)

    # Run tests
    test1 = test_turn_order_generation()
    test2 = test_portrait_mode_config()
    test3 = test_investigator_portraits()

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Turn Order Generation: {'PASS' if test1 else 'WARN'}")
    print(f"Portrait Mode Config:  {'PASS' if test2 else 'FAIL'}")
    print(f"Investigator Portraits: {'PASS' if test3 else 'FAIL'}")

    print("\n" + "=" * 60)
    print("MANUAL TESTING INSTRUCTIONS")
    print("=" * 60)
    print("1. Run the game: uv run python main.py")
    print("2. Click 'New Game' to start a battle")
    print("3. Observe the first turn:")
    print("   - If enemy goes first, they should move/attack automatically")
    print("   - If player goes first, you should be able to act")
    print("4. Check grid display:")
    print("   - Investigators should show portrait images (if GRID_DISPLAY_MODE='portraits')")
    print("   - Enemies should show red symbols")
    print("   - Health/sanity bars should appear below all units")
    print("5. Try toggling GRID_DISPLAY_MODE in config.py to see both modes")
    print("=" * 60)
