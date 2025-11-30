"""
Test script for action points system.

Tests the new 2-action system where units have 2 action points per turn
and can spend them on Move and Attack actions.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from entities.investigator import Investigator
from entities.unit import Unit


def test_action_points_initialization():
    """Test that units start with 2 action points."""
    print("=" * 60)
    print("TEST 1: Action Points Initialization")
    print("=" * 60)

    inv = Investigator(name="Test Investigator", gender="male")

    print(f"\nInvestigator created: {inv.name}")
    print(f"  Max action points: {inv.max_action_points}")
    print(f"  Current action points: {inv.current_action_points}")

    assert inv.max_action_points == 2, "Max action points should be 2"
    assert inv.current_action_points == 2, "Current action points should start at 2"

    print("\n[OK] Action points initialized correctly!\n")


def test_can_move_and_attack():
    """Test that units can move and attack when they have action points."""
    print("=" * 60)
    print("TEST 2: Can Move/Attack Checks")
    print("=" * 60)

    inv = Investigator(name="Test Investigator", gender="male")

    print(f"\nInitial state (2/2 action points):")
    print(f"  can_move(): {inv.can_move()}")
    print(f"  can_attack(): {inv.can_attack()}")

    assert inv.can_move() == True, "Should be able to move with 2 action points"
    assert inv.can_attack() == True, "Should be able to attack with 2 action points"

    print("\n[OK] Can move and attack with full action points!\n")


def test_consume_action_points():
    """Test consuming action points."""
    print("=" * 60)
    print("TEST 3: Consuming Action Points")
    print("=" * 60)

    inv = Investigator(name="Test Investigator", gender="male")

    print(f"\nStarting action points: {inv.current_action_points}/2")

    # Consume first action point (e.g., Move)
    result = inv.consume_action_point(1)
    print(f"After consuming 1 AP: {inv.current_action_points}/2")
    print(f"  Consumption successful: {result}")
    print(f"  can_move(): {inv.can_move()}")
    print(f"  can_attack(): {inv.can_attack()}")

    assert result == True, "Should successfully consume action point"
    assert inv.current_action_points == 1, "Should have 1 action point remaining"
    assert inv.can_move() == True, "Should still be able to move with 1 AP"
    assert inv.can_attack() == True, "Should still be able to attack with 1 AP"

    # Consume second action point (e.g., Attack)
    result = inv.consume_action_point(1)
    print(f"\nAfter consuming 2nd AP: {inv.current_action_points}/2")
    print(f"  Consumption successful: {result}")
    print(f"  can_move(): {inv.can_move()}")
    print(f"  can_attack(): {inv.can_attack()}")

    assert result == True, "Should successfully consume second action point"
    assert inv.current_action_points == 0, "Should have 0 action points remaining"
    assert inv.can_move() == False, "Should NOT be able to move with 0 AP"
    assert inv.can_attack() == False, "Should NOT be able to attack with 0 AP"

    # Try to consume when no points remain
    result = inv.consume_action_point(1)
    print(f"\nTrying to consume when empty: {result}")
    assert result == False, "Should fail to consume when no points remain"

    print("\n[OK] Action point consumption works correctly!\n")


def test_reset_turn_flags():
    """Test resetting action points at start of turn."""
    print("=" * 60)
    print("TEST 4: Reset Turn Flags (Action Points)")
    print("=" * 60)

    inv = Investigator(name="Test Investigator", gender="male")

    # Consume all action points
    inv.consume_action_point(1)
    inv.consume_action_point(1)

    print(f"\nAfter using all actions: {inv.current_action_points}/2")
    print(f"  can_move(): {inv.can_move()}")
    print(f"  can_attack(): {inv.can_attack()}")

    assert inv.current_action_points == 0, "Should have 0 AP"
    assert inv.can_move() == False, "Should not be able to move"

    # Reset turn (new turn starts)
    inv.reset_turn_flags()

    print(f"\nAfter reset_turn_flags(): {inv.current_action_points}/2")
    print(f"  can_move(): {inv.can_move()}")
    print(f"  can_attack(): {inv.can_attack()}")

    assert inv.current_action_points == 2, "Should have 2 AP after reset"
    assert inv.can_move() == True, "Should be able to move after reset"
    assert inv.can_attack() == True, "Should be able to attack after reset"

    print("\n[OK] Action points reset correctly on new turn!\n")


def test_action_combinations():
    """Test various action combinations (move-move, move-attack, etc)."""
    print("=" * 60)
    print("TEST 5: Action Combinations")
    print("=" * 60)

    # Test Move -> Move
    print("\n5a. Move -> Move:")
    inv = Investigator(name="Mover", gender="male")
    print(f"  Start: {inv.current_action_points}/2 AP")

    inv.consume_action_point(1)  # First move
    print(f"  After 1st move: {inv.current_action_points}/2 AP, can_move()={inv.can_move()}")

    inv.consume_action_point(1)  # Second move
    print(f"  After 2nd move: {inv.current_action_points}/2 AP, can_move()={inv.can_move()}")

    assert inv.current_action_points == 0, "Should have 0 AP"
    assert inv.can_move() == False, "Should not be able to move again"
    print("  [OK] Move-Move uses both actions")

    # Test Move -> Attack
    print("\n5b. Move -> Attack:")
    inv = Investigator(name="Attacker", gender="male")
    print(f"  Start: {inv.current_action_points}/2 AP")

    inv.consume_action_point(1)  # Move
    print(f"  After move: {inv.current_action_points}/2 AP, can_attack()={inv.can_attack()}")

    inv.consume_action_point(1)  # Attack
    print(f"  After attack: {inv.current_action_points}/2 AP, can_move()={inv.can_move()}")

    assert inv.current_action_points == 0, "Should have 0 AP"
    assert inv.can_move() == False, "Should not be able to move again"
    print("  [OK] Move-Attack uses both actions")

    # Test Attack -> Attack
    print("\n5c. Attack -> Attack:")
    inv = Investigator(name="Shooter", gender="male")
    print(f"  Start: {inv.current_action_points}/2 AP")

    inv.consume_action_point(1)  # First attack
    print(f"  After 1st attack: {inv.current_action_points}/2 AP, can_attack()={inv.can_attack()}")

    inv.consume_action_point(1)  # Second attack
    print(f"  After 2nd attack: {inv.current_action_points}/2 AP, can_attack()={inv.can_attack()}")

    assert inv.current_action_points == 0, "Should have 0 AP"
    assert inv.can_attack() == False, "Should not be able to attack again"
    print("  [OK] Attack-Attack uses both actions")

    print("\n[OK] All action combinations work correctly!\n")


def run_all_tests():
    """Run all action points tests."""
    print("\n")
    print("=" * 60)
    print("          ACTION POINTS SYSTEM TESTS")
    print("=" * 60)
    print()

    try:
        test_action_points_initialization()
        test_can_move_and_attack()
        test_consume_action_points()
        test_reset_turn_flags()
        test_action_combinations()

        print("=" * 60)
        print("[OK] ALL TESTS PASSED!")
        print("=" * 60)
        print("\nAction points system is working correctly.")
        print("Units now have 2 action points per turn.")
        print("Each Move or Attack consumes 1 action point.")
        print("\nValid combinations:")
        print("  - Move + Move")
        print("  - Move + Attack")
        print("  - Attack + Move")
        print("  - Attack + Attack")
        print()

    except AssertionError as e:
        print("\n" + "=" * 60)
        print("[X] TEST FAILED!")
        print("=" * 60)
        print(f"Assertion Error: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print("\n" + "=" * 60)
        print("[X] TEST FAILED!")
        print("=" * 60)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
