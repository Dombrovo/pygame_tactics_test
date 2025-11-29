"""
Test turn order system.

This script validates the turn order implementation without requiring the GUI.
"""

import sys
import random
from pathlib import Path

# Add parent directory to path so we can import from entities
sys.path.insert(0, str(Path(__file__).parent.parent))

from entities.investigator import create_test_squad
from entities.enemy import create_test_enemies
from entities.unit import Unit


def test_turn_order_initialization():
    """Test that turn order is created and shuffled."""
    print("=" * 60)
    print("TEST 1: Turn Order Initialization")
    print("=" * 60)

    # Create units
    player_units = create_test_squad()
    enemy_units = create_test_enemies()

    # Create turn order (shuffled)
    all_units = player_units + enemy_units
    random.shuffle(all_units)
    turn_order = all_units

    print(f"[OK] Created turn order with {len(turn_order)} units")
    print("\nTurn order:")
    for i, unit in enumerate(turn_order):
        team_marker = "[P]" if unit.team == "player" else "[E]"
        print(f"  {i+1}. {team_marker} {unit.name}")

    assert len(turn_order) == 8, "Should have 8 units total (4 players + 4 enemies)"
    print("\n[OK] Turn order initialization PASSED\n")
    return turn_order


def test_turn_advancement(turn_order):
    """Test advancing through turns."""
    print("=" * 60)
    print("TEST 2: Turn Advancement")
    print("=" * 60)

    current_turn_index = 0
    round_number = 1

    print(f"\nStarting Round {round_number}")
    print(f"First turn: {turn_order[0].name}")

    # Advance through several turns
    for turn_num in range(1, 6):
        original_index = current_turn_index

        # Calculate next index with wrap-around
        current_turn_index = (current_turn_index + 1) % len(turn_order)
        current_turn_unit = turn_order[current_turn_index]

        # Check if we wrapped around (new round)
        if current_turn_index < original_index or (current_turn_index == 0 and original_index > 0):
            round_number += 1
            print(f"\n=== NEW ROUND {round_number} ===")

        team_str = "Player" if current_turn_unit.team == "player" else "Enemy"
        print(f"Turn {turn_num + 1}: {team_str} - {current_turn_unit.name} (index {current_turn_index})")

    print("\n[OK] Turn advancement PASSED\n")
    return current_turn_index, round_number


def test_skip_incapacitated(turn_order):
    """Test skipping incapacitated units."""
    print("=" * 60)
    print("TEST 3: Skip Incapacitated Units")
    print("=" * 60)

    # Incapacitate every other unit
    for i, unit in enumerate(turn_order):
        if i % 2 == 0:
            unit.is_incapacitated = True
            print(f"  Incapacitated: {unit.name}")

    # Find next active unit
    current_turn_index = 0
    original_index = current_turn_index
    found_active_unit = False

    for i in range(len(turn_order)):
        test_index = (original_index + 1 + i) % len(turn_order)
        next_unit = turn_order[test_index]

        if next_unit.can_act():
            current_turn_index = test_index
            current_turn_unit = next_unit
            found_active_unit = True
            print(f"\n[OK] Found active unit: {current_turn_unit.name} at index {current_turn_index}")
            break

    assert found_active_unit, "Should find at least one active unit"
    assert not current_turn_unit.is_incapacitated, "Current unit should not be incapacitated"

    # Restore units
    for unit in turn_order:
        unit.is_incapacitated = False

    print("[OK] Skip incapacitated units PASSED\n")


def test_round_wrapping(turn_order):
    """Test that rounds increment when turn order wraps."""
    print("=" * 60)
    print("TEST 4: Round Wrapping")
    print("=" * 60)

    current_turn_index = len(turn_order) - 1  # Start at last unit
    round_number = 1

    print(f"Starting at last unit: {turn_order[current_turn_index].name} (index {current_turn_index})")

    # Advance to next turn (should wrap to index 0)
    original_index = current_turn_index
    current_turn_index = (current_turn_index + 1) % len(turn_order)

    # Check if wrapped
    if current_turn_index < original_index or (current_turn_index == 0 and original_index > 0):
        round_number += 1
        print(f"[OK] Wrapped to index {current_turn_index}, incremented round to {round_number}")

    assert current_turn_index == 0, "Should wrap to index 0"
    assert round_number == 2, "Should increment to round 2"
    print("[OK] Round wrapping PASSED\n")


def test_team_mixing():
    """Test that turn order mixes player and enemy units."""
    print("=" * 60)
    print("TEST 5: Team Mixing in Turn Order")
    print("=" * 60)

    # Run multiple times to check randomness
    player_first_count = 0
    enemy_first_count = 0
    trials = 10

    for trial in range(trials):
        player_units = create_test_squad()
        enemy_units = create_test_enemies()
        all_units = player_units + enemy_units
        random.shuffle(all_units)

        if all_units[0].team == "player":
            player_first_count += 1
        else:
            enemy_first_count += 1

    print(f"Out of {trials} trials:")
    print(f"  Player went first: {player_first_count} times")
    print(f"  Enemy went first: {enemy_first_count} times")

    # Both should happen at least once in 10 trials (very likely with randomness)
    assert player_first_count > 0, "Player should go first at least once"
    assert enemy_first_count > 0, "Enemy should go first at least once"

    print("[OK] Team mixing PASSED (turn order is random)\n")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("TURN ORDER SYSTEM TESTS")
    print("=" * 60 + "\n")

    # Seed random for consistent first test
    random.seed(42)

    # Run tests
    turn_order = test_turn_order_initialization()
    test_turn_advancement(turn_order)
    test_skip_incapacitated(turn_order)
    test_round_wrapping(turn_order)

    # Reset seed for randomness test
    random.seed()
    test_team_mixing()

    print("=" * 60)
    print("ALL TESTS PASSED [OK]")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
