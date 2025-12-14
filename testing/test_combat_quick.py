"""
Quick test of the new combat card system.

Tests that:
1. Misses don't draw cards
2. Hits draw cards
3. NULL cards deal 0 damage but count as hits
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from entities.investigator import create_test_squad
from entities.enemy import create_test_enemies
from entities.combat_deck import create_monster_deck
from combat.grid import Grid
from combat.terrain_generator import generate_terrain
from combat.combat_resolver import resolve_attack, format_attack_result


def main():
    """Run quick combat test."""
    print("=" * 60)
    print("QUICK COMBAT CARD TEST")
    print("=" * 60)

    # Setup
    grid = Grid()
    terrain = generate_terrain("open_field")
    for x, y, cover_type in terrain:
        grid.get_tile(x, y).cover_type = cover_type

    investigators = create_test_squad()
    enemies = create_test_enemies()
    monster_deck = create_monster_deck()

    # Position units
    inv = investigators[0]
    enemy = enemies[0]
    inv.position = (2, 2)
    enemy.position = (4, 2)  # 2 tiles away
    grid.get_tile(2, 2).occupant = inv
    grid.get_tile(4, 2).occupant = enemy

    print(f"\nAttacker: {inv.name} (Deck size: {inv.combat_deck.size()})")
    print(f"Defender: {enemy.name} (HP: {enemy.current_health}/{enemy.max_health})")
    print(f"Distance: 2 tiles, Hit chance: ~55%\n")

    # Run 10 attacks to see the new behavior
    print("Running 10 attack simulations:\n")

    for i in range(10):
        # Reset enemy health
        enemy.current_health = enemy.max_health

        # Resolve attack
        result = resolve_attack(inv, enemy, grid, monster_deck)

        # Format result
        msg = format_attack_result(inv, enemy, result)
        print(f"Attack {i+1}:")
        print(msg)

        # Show if card was drawn
        if result.get("card_drawn"):
            print(f"  [Card drawn from deck: {result['card_drawn']}]")
        else:
            print(f"  [No card drawn - attack missed]")
        print()

    print("=" * 60)
    print("OBSERVATIONS")
    print("=" * 60)
    print("1. Misses should NOT draw cards")
    print("2. Hits should draw cards")
    print("3. NULL cards should show 'NO DAMAGE' but still be hits")
    print("4. No good cards should be wasted on misses")


if __name__ == "__main__":
    main()
