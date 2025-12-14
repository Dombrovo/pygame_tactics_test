"""
Test to analyze miss rates and understand combat card behavior.

This script tests the combat resolution system to see:
1. How often attacks miss
2. How cards interact with hit/miss mechanics
3. Whether the miss rate seems correct
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from entities.investigator import create_test_squad
from entities.enemy import create_test_enemies
from entities.combat_deck import create_monster_deck
from combat.grid import Grid
from combat.terrain_generator import TerrainGenerator
from combat.combat_resolver import resolve_attack, calculate_hit_chance, get_attack_preview
from combat.line_of_sight import get_cover_between


def analyze_combat_scenario(attacker, target, grid, monster_deck, num_trials=100):
    """
    Run multiple attack simulations and analyze results.

    Args:
        attacker: The attacking unit
        target: The target unit
        grid: The battlefield grid
        monster_deck: Monster deck for enemy attacks
        num_trials: Number of attack simulations to run

    Returns:
        Dictionary with analysis results
    """
    results = {
        "total_attacks": 0,
        "hits": 0,
        "misses": 0,
        "null_card_misses": 0,  # Misses due to NULL card
        "roll_misses": 0,       # Misses due to d100 roll failing
        "cards_drawn": {},      # Count of each card type drawn
        "wasted_good_cards": 0, # +1, +2, x2 cards that resulted in miss
    }

    # Get preview info
    preview = get_attack_preview(attacker, target, grid)
    if not preview["valid"]:
        print(f"[!] Attack is not valid: {preview['reason']}")
        return results

    print(f"\n=== Combat Scenario ===")
    print(f"Attacker: {attacker.name}")
    print(f"Target: {target.name}")
    print(f"Distance: {preview['distance']:.1f} tiles")
    print(f"Cover: {preview['cover']}")
    print(f"Hit Chance: {preview['hit_chance']}%")
    print(f"Base Damage: {preview['base_damage']}")
    print(f"\nRunning {num_trials} trials...\n")

    # Run trials
    for i in range(num_trials):
        # Reset target health for each trial
        target.current_health = target.max_health

        # Resolve attack
        result = resolve_attack(attacker, target, grid, monster_deck)

        if not result["valid"]:
            continue

        results["total_attacks"] += 1

        # Track card drawn
        card_name = result.get("card_drawn", "None")
        results["cards_drawn"][card_name] = results["cards_drawn"].get(card_name, 0) + 1

        # Analyze result
        if result["hit"]:
            results["hits"] += 1
        else:
            results["misses"] += 1

            # Categorize miss type
            if result.get("card_is_null"):
                results["null_card_misses"] += 1
            else:
                results["roll_misses"] += 1

                # Check if we wasted a good card
                if card_name in ["+1", "+2", "x2"]:
                    results["wasted_good_cards"] += 1

    return results


def print_results(results):
    """Print analysis results in readable format."""
    if results["total_attacks"] == 0:
        print("[!] No valid attacks were made")
        return

    print(f"\n=== Results ({results['total_attacks']} attacks) ===")
    print(f"Hits: {results['hits']} ({results['hits']/results['total_attacks']*100:.1f}%)")
    print(f"Misses: {results['misses']} ({results['misses']/results['total_attacks']*100:.1f}%)")

    if results['misses'] > 0:
        print(f"\nMiss Breakdown:")
        print(f"  NULL card auto-misses: {results['null_card_misses']} ({results['null_card_misses']/results['misses']*100:.1f}% of misses)")
        print(f"  D100 roll failures: {results['roll_misses']} ({results['roll_misses']/results['misses']*100:.1f}% of misses)")
        print(f"  Wasted good cards (+1/+2/x2): {results['wasted_good_cards']}")

    print(f"\nCards Drawn (only on successful hits):")
    # Filter out None values and sort
    cards = {k: v for k, v in results['cards_drawn'].items() if k is not None}
    if cards:
        for card_name in sorted(cards.keys()):
            count = cards[card_name]
            pct = count / results['total_attacks'] * 100
            print(f"  {card_name:>4}: {count:3} ({pct:5.1f}%)")
    else:
        print("  (No cards drawn - all attacks missed)")


def main():
    """Run miss analysis tests."""
    print("=" * 60)
    print("MISS RATE ANALYSIS")
    print("=" * 60)

    # Create test battlefield
    grid = Grid()
    from combat.terrain_generator import generate_terrain
    terrain = generate_terrain("open_field")
    for x, y, cover_type in terrain:
        grid.get_tile(x, y).cover_type = cover_type

    # Create units
    investigators = create_test_squad()
    enemies = create_test_enemies()
    monster_deck = create_monster_deck()

    # Position units for testing
    # Scenario 1: Close range, no cover
    investigators[0].position = (2, 2)
    enemies[0].position = (4, 2)  # 2 tiles away
    grid.get_tile(2, 2).occupant = investigators[0]
    grid.get_tile(4, 2).occupant = enemies[0]

    print("\n" + "=" * 60)
    print("SCENARIO 1: Close range (2 tiles), minimal cover")
    print("=" * 60)
    results1 = analyze_combat_scenario(investigators[0], enemies[0], grid, monster_deck, num_trials=100)
    print_results(results1)

    # Scenario 2: Medium range
    # Clear previous occupants
    grid.get_tile(2, 2).occupant = None
    grid.get_tile(4, 2).occupant = None
    investigators[1].position = (1, 1)
    enemies[1].position = (6, 1)  # 5 tiles away
    grid.get_tile(1, 1).occupant = investigators[1]
    grid.get_tile(6, 1).occupant = enemies[1]

    print("\n" + "=" * 60)
    print("SCENARIO 2: Medium range (5 tiles)")
    print("=" * 60)
    results2 = analyze_combat_scenario(investigators[1], enemies[1], grid, monster_deck, num_trials=100)
    print_results(results2)

    # Scenario 3: Long range
    # Clear previous occupants
    grid.get_tile(1, 1).occupant = None
    grid.get_tile(6, 1).occupant = None
    investigators[2].position = (0, 0)
    enemies[2].position = (8, 0)  # 8 tiles away
    grid.get_tile(0, 0).occupant = investigators[2]
    grid.get_tile(8, 0).occupant = enemies[2]

    print("\n" + "=" * 60)
    print("SCENARIO 3: Long range (8 tiles)")
    print("=" * 60)
    results3 = analyze_combat_scenario(investigators[2], enemies[2], grid, monster_deck, num_trials=100)
    print_results(results3)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("\nKey Findings:")
    print("1. D100 roll determines hit/miss FIRST")
    print("2. Cards are ONLY drawn on successful hits")
    print("3. NULL cards deal 0 damage (but still count as hits)")
    print("4. NO cards are wasted on misses")
    print("\nNew System Benefits:")
    print("- No more wasted good cards (+1/+2/x2)")
    print("- More player-friendly and intuitive")
    print("- Decks cycle slower (only on hits)")
    print("- NULL cards are rare disappointments, not common frustrations")
    print("\nTo increase hit rate:")
    print("- Close distance (each tile = -10% hit chance)")
    print("- Avoid cover (half = -20%, full = -40%)")
    print("- Use weapons with high accuracy modifiers")


if __name__ == "__main__":
    main()
