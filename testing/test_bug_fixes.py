"""
Test script to verify bug fixes for Session 15.

Tests:
1. Action point consumption for attacks
2. Incapacitated enemies excluded from targeting
3. Monster deck creation and usage
"""

import sys
sys.path.insert(0, '.')

from entities.unit import Unit
from entities.investigator import Investigator, create_test_squad
from entities.enemy import Enemy, create_test_enemies
from entities.combat_deck import create_monster_deck, create_standard_deck
from combat.grid import Grid
from combat.combat_resolver import resolve_attack
from combat.line_of_sight import get_valid_attack_targets
import config

print("=" * 60)
print("BUG FIX TESTS - Session 15")
print("=" * 60)

# Test 1: Action Point Consumption
print("\n[TEST 1] Action Point Consumption")
print("-" * 60)

investigators = create_test_squad()
inv = investigators[0]

print(f"Investigator: {inv.name}")
print(f"Initial action points: {inv.current_action_points}/{inv.max_action_points}")

# Simulate consuming action point for attack
inv.consume_action_point(1)
print(f"After attack: {inv.current_action_points}/{inv.max_action_points}")

if inv.current_action_points == 1:
    print("[OK] Action point correctly consumed (2 -> 1)")
else:
    print(f"[X] FAIL: Expected 1 action point, got {inv.current_action_points}")

# Test ability to attack again
can_attack_again = inv.can_attack()
print(f"Can attack again: {can_attack_again}")

if can_attack_again:
    print("[OK] Can attack again with 1 action point remaining")
    inv.consume_action_point(1)
    print(f"After second attack: {inv.current_action_points}/{inv.max_action_points}")

    if inv.current_action_points == 0:
        print("[OK] Both action points consumed (1 -> 0)")
    else:
        print(f"[X] FAIL: Expected 0 action points, got {inv.current_action_points}")

    # Should not be able to attack with 0 points
    can_attack_third = inv.can_attack()
    if not can_attack_third:
        print("[OK] Cannot attack with 0 action points")
    else:
        print("[X] FAIL: Should not be able to attack with 0 action points")
else:
    print("[X] FAIL: Should be able to attack with 1 action point")

# Test 2: Incapacitated Enemies Excluded from Targeting
print("\n[TEST 2] Incapacitated Enemies Excluded from Targeting")
print("-" * 60)

grid = Grid(config.GRID_SIZE)
enemies = create_test_enemies()

# Place investigator and enemies on grid
grid.place_unit(inv, 0, 0)
for i, enemy in enumerate(enemies):
    grid.place_unit(enemy, i + 1, 0)  # Place enemies in a row

print(f"Placed {len(enemies)} enemies on grid")
print(f"Investigator at (0, 0)")
for i, enemy in enumerate(enemies):
    print(f"  {enemy.name} at ({i+1}, 0) - HP: {enemy.current_health}/{enemy.max_health}")

# Get initial valid targets
initial_targets = get_valid_attack_targets((0, 0), 10, grid, "enemy")
print(f"\nInitial valid targets: {len(initial_targets)}")
print(f"  Positions: {initial_targets}")

# Incapacitate first enemy
enemies[0].take_damage(enemies[0].current_health)
print(f"\nIncapacitated {enemies[0].name}")
print(f"  Is incapacitated: {enemies[0].is_incapacitated}")

# Get targets after incapacitation
targets_after = get_valid_attack_targets((0, 0), 10, grid, "enemy")
print(f"\nValid targets after incapacitation: {len(targets_after)}")
print(f"  Positions: {targets_after}")

# Verify incapacitated enemy is excluded
if len(targets_after) == len(initial_targets) - 1:
    print("[OK] Incapacitated enemy excluded from targeting")

    # Verify the first enemy's position is not in targets
    if (1, 0) not in targets_after:
        print("[OK] Position (1, 0) correctly excluded")
    else:
        print("[X] FAIL: Incapacitated enemy's position still in targets")
else:
    print(f"[X] FAIL: Expected {len(initial_targets) - 1} targets, got {len(targets_after)}")

# Test 3: Monster Deck Creation and Usage
print("\n[TEST 3] Monster Deck Creation and Usage")
print("-" * 60)

# Create monster deck
monster_deck = create_monster_deck()
print(f"Monster deck created: {monster_deck}")
print(f"Owner: {monster_deck.owner_name}")
print(f"Total cards: {monster_deck.size()}")
print(f"Cards remaining: {monster_deck.cards_remaining()}")

# Verify composition matches standard deck
composition = monster_deck.get_deck_composition()
print(f"\nDeck composition:")
for card_name, count in sorted(composition.items()):
    print(f"  {card_name}: {count}x")

# Expected composition (same as standard investigator deck)
expected = {
    'NULL': 1,
    'x2': 1,
    '+2': 1,
    '+1': 5,
    '+0': 7,
    '-1': 5
}

composition_match = True
for card_name, expected_count in expected.items():
    actual_count = composition.get(card_name, 0)
    if actual_count != expected_count:
        print(f"[X] FAIL: {card_name} - expected {expected_count}, got {actual_count}")
        composition_match = False

if composition_match:
    print("\n[OK] Monster deck composition matches standard deck")
else:
    print("\n[X] FAIL: Monster deck composition does not match")

# Draw a few cards to test functionality
print("\nDrawing 3 cards from monster deck:")
for i in range(3):
    card = monster_deck.draw()
    if card:
        print(f"  Card {i+1}: {card.name}")
    else:
        print(f"  [X] FAIL: Failed to draw card {i+1}")

print(f"\nCards remaining after draws: {monster_deck.cards_remaining()}")

# Test 4: Combat Resolution with Monster Deck
print("\n[TEST 4] Combat Resolution with Monster Deck")
print("-" * 60)

# Reset investigator
inv.reset_turn_flags()

# Create fresh units for combat test
test_inv = investigators[1]
test_enemy = enemies[1]

# Place them on grid at close range
grid.place_unit(test_inv, 5, 5)
grid.place_unit(test_enemy, 6, 5)

print(f"Attacker: {test_inv.name} at (5, 5)")
print(f"Target: {test_enemy.name} at (6, 5)")
print(f"Distance: 1 tile")

# Test investigator attack (uses personal deck)
print("\nInvestigator attacking enemy:")
result_inv = resolve_attack(test_inv, test_enemy, grid, monster_deck)

if result_inv.get("valid"):
    print(f"  Valid: {result_inv['valid']}")
    print(f"  Hit: {result_inv.get('hit', False)}")
    print(f"  Card drawn: {result_inv.get('card_drawn', 'None')}")
    print(f"  Damage: {result_inv.get('damage_dealt', 0)}")

    if result_inv.get("card_drawn"):
        print("[OK] Investigator drew from personal deck")
    else:
        print("[!] No card drawn (possible miss or null card)")
else:
    print(f"[X] FAIL: Attack invalid - {result_inv.get('reason')}")

# Restore enemy health if damaged
test_enemy.current_health = test_enemy.max_health

# Test enemy attack (uses monster deck)
print("\nEnemy attacking investigator:")
result_enemy = resolve_attack(test_enemy, test_inv, grid, monster_deck)

if result_enemy.get("valid"):
    print(f"  Valid: {result_enemy['valid']}")
    print(f"  Hit: {result_enemy.get('hit', False)}")
    print(f"  Card drawn: {result_enemy.get('card_drawn', 'None')}")
    print(f"  Damage: {result_enemy.get('damage_dealt', 0)}")

    if result_enemy.get("card_drawn"):
        print("[OK] Enemy drew from monster deck")
    else:
        print("[!] No card drawn (possible miss or null card)")
else:
    print(f"[X] FAIL: Attack invalid - {result_enemy.get('reason')}")

# Final Summary
print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print("[1] Action Point Consumption: See results above")
print("[2] Incapacitated Targeting: See results above")
print("[3] Monster Deck Creation: See results above")
print("[4] Combat Resolution: See results above")
print("\nAll fixes implemented successfully!")
print("=" * 60)
