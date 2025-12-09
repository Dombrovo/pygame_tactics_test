"""
Test script for combat resolution system.

This script tests:
- Line of sight calculations (Bresenham's algorithm)
- Hit chance calculations
- Attack resolution (with combat deck integration)
- Damage application
"""

import sys
import os

# Add parent directory to path to import game modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from combat.grid import Grid
from combat import line_of_sight
from combat import combat_resolver
from entities.investigator import Investigator
from entities.enemy import Cultist, HoundOfTindalos
from entities import equipment


def test_bresenham_line():
    """Test Bresenham's line algorithm."""
    print("\n=== TEST: Bresenham's Line Algorithm ===")

    # Test straight horizontal line
    line = line_of_sight.bresenham_line((0, 0), (5, 0))
    expected = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)]
    assert line == expected, f"Horizontal line failed: {line}"
    print(f"[OK] Horizontal line: {line}")

    # Test straight vertical line
    line = line_of_sight.bresenham_line((0, 0), (0, 5))
    expected = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5)]
    assert line == expected, f"Vertical line failed: {line}"
    print(f"[OK] Vertical line: {line}")

    # Test diagonal line
    line = line_of_sight.bresenham_line((0, 0), (3, 3))
    expected = [(0, 0), (1, 1), (2, 2), (3, 3)]
    assert line == expected, f"Diagonal line failed: {line}"
    print(f"[OK] Diagonal line: {line}")

    # Test angled line
    line = line_of_sight.bresenham_line((0, 0), (4, 2))
    print(f"[OK] Angled line (0,0) -> (4,2): {line}")


def test_line_of_sight_clear():
    """Test line of sight with no obstacles."""
    print("\n=== TEST: Line of Sight (Clear) ===")

    grid = Grid(10)

    # Clear LOS across grid
    has_los = line_of_sight.has_line_of_sight((0, 0), (5, 5), grid)
    assert has_los, "Should have LOS with no obstacles"
    print("[OK] Clear LOS from (0,0) to (5,5)")

    # Clear LOS straight line
    has_los = line_of_sight.has_line_of_sight((0, 0), (9, 0), grid)
    assert has_los, "Should have LOS straight horizontal"
    print("[OK] Clear LOS from (0,0) to (9,0)")


def test_line_of_sight_blocked():
    """Test line of sight with obstacles."""
    print("\n=== TEST: Line of Sight (Blocked) ===")

    grid = Grid(10)

    # Place full cover blocking the path
    tile = grid.get_tile(3, 3)
    tile.terrain_type = "full_cover"
    tile.blocks_sight = True

    # Test that LOS is blocked
    has_los = line_of_sight.has_line_of_sight((0, 0), (5, 5), grid)
    assert not has_los, "LOS should be blocked by full cover at (3,3)"
    print("[OK] LOS blocked by full cover at (3,3)")

    # Test that LOS from another angle works
    has_los = line_of_sight.has_line_of_sight((0, 0), (0, 5), grid)
    assert has_los, "LOS should be clear from (0,0) to (0,5)"
    print("[OK] LOS clear from different angle")


def test_line_of_sight_half_cover():
    """Test that half cover doesn't block LOS."""
    print("\n=== TEST: Line of Sight (Half Cover) ===")

    grid = Grid(10)

    # Place half cover (doesn't block sight)
    tile = grid.get_tile(3, 3)
    tile.terrain_type = "half_cover"
    tile.blocks_sight = False

    # Test that LOS is NOT blocked
    has_los = line_of_sight.has_line_of_sight((0, 0), (5, 5), grid)
    assert has_los, "Half cover should not block LOS"
    print("[OK] Half cover does not block LOS")


def test_hit_chance_calculation():
    """Test hit chance calculations."""
    print("\n=== TEST: Hit Chance Calculation ===")

    # Create investigator with 75% base accuracy
    inv = Investigator(name="Test", gender="male")
    inv.equip_weapon(equipment.REVOLVER)  # No accuracy modifier

    # Create target
    cultist = Cultist(name="Target")

    # Test 1: Close range, no cover
    hit_chance = combat_resolver.calculate_hit_chance(inv, cultist, distance=1, cover_type="empty")
    expected = 75 - 10  # 75% base - 10% distance
    assert hit_chance == expected, f"Expected {expected}%, got {hit_chance}%"
    print(f"[OK] Close range, no cover: {hit_chance}%")

    # Test 2: Medium range, half cover
    hit_chance = combat_resolver.calculate_hit_chance(inv, cultist, distance=3, cover_type="half_cover")
    expected = 75 - 30 - 20  # 75% base - 30% distance - 20% cover = 25%
    assert hit_chance == expected, f"Expected {expected}%, got {hit_chance}%"
    print(f"[OK] Medium range, half cover: {hit_chance}%")

    # Test 3: Long range (should clamp to minimum 5%)
    hit_chance = combat_resolver.calculate_hit_chance(inv, cultist, distance=10, cover_type="full_cover")
    expected = 5  # Should clamp to minimum
    assert hit_chance == expected, f"Expected {expected}% (clamped), got {hit_chance}%"
    print(f"[OK] Long range with cover (clamped to minimum): {hit_chance}%")

    # Test 4: Point blank (should clamp to maximum 95%)
    inv.accuracy_modifier = 50  # Artificially boost accuracy
    hit_chance = combat_resolver.calculate_hit_chance(inv, cultist, distance=0, cover_type="empty")
    expected = 95  # Should clamp to maximum
    assert hit_chance == expected, f"Expected {expected}% (clamped), got {hit_chance}%"
    print(f"[OK] Point blank with bonus (clamped to maximum): {hit_chance}%")


def test_attack_resolution():
    """Test complete attack resolution."""
    print("\n=== TEST: Attack Resolution ===")

    grid = Grid(10)

    # Create attacker and target
    inv = Investigator(name="Attacker", gender="male")
    inv.equip_weapon(equipment.REVOLVER)  # 5 damage, range 4
    grid.place_unit(inv, 0, 0)

    cultist = Cultist(name="Target")
    grid.place_unit(cultist, 3, 0)  # 3 tiles away, straight line

    print(f"Setup: {inv.name} at (0,0), {cultist.name} at (3,0)")
    print(f"Weapon: {inv.equipped_weapon.name} ({inv.weapon_damage} damage, range {inv.weapon_range})")
    print(f"Target HP: {cultist.current_health}/{cultist.max_health}")

    # Resolve attack
    result = combat_resolver.resolve_attack(inv, cultist, grid)

    # Verify attack was valid
    assert result["valid"], f"Attack should be valid, reason: {result.get('reason')}"
    print(f"[OK] Attack is valid")

    # Check calculated values
    print(f"  Hit chance: {result['hit_chance']}%")
    print(f"  Distance: {result['distance']:.1f} tiles")
    print(f"  Cover: {result['cover']}")

    if result.get("card_drawn"):
        print(f"  Card drawn: {result['card_drawn']}")

    if result["hit"]:
        print(f"  [OK] HIT (roll {result['roll']} <= {result['hit_chance']}%)")
        print(f"  Damage: {result['damage_dealt']}")
        print(f"  Target HP: {cultist.current_health}/{cultist.max_health}")
    else:
        print(f"  MISS (roll {result['roll']} > {result['hit_chance']}%)")

    # Verify damage was applied if hit
    if result["hit"]:
        assert cultist.current_health < cultist.max_health, "Target should have taken damage"


def test_attack_out_of_range():
    """Test attack that's out of range."""
    print("\n=== TEST: Attack Out of Range ===")

    grid = Grid(10)

    inv = Investigator(name="Attacker", gender="male")
    inv.equip_weapon(equipment.REVOLVER)  # Range 4
    grid.place_unit(inv, 0, 0)

    cultist = Cultist(name="Target")
    grid.place_unit(cultist, 9, 0)  # 9 tiles away

    result = combat_resolver.resolve_attack(inv, cultist, grid)

    assert not result["valid"], "Attack should be invalid"
    assert result["reason"] == "out_of_range", f"Expected out_of_range, got {result['reason']}"
    print(f"[OK] Attack correctly rejected (out of range: {result.get('distance'):.1f} > {result.get('weapon_range')})")


def test_attack_no_los():
    """Test attack with no line of sight."""
    print("\n=== TEST: Attack No Line of Sight ===")

    grid = Grid(10)

    inv = Investigator(name="Attacker", gender="male")
    inv.equip_weapon(equipment.REVOLVER)  # Range 4
    grid.place_unit(inv, 0, 0)

    cultist = Cultist(name="Target")
    grid.place_unit(cultist, 3, 0)  # 3 tiles away (within range)

    # Block LOS with wall at (2, 0)
    tile = grid.get_tile(2, 0)
    tile.terrain_type = "full_cover"
    tile.blocks_sight = True

    result = combat_resolver.resolve_attack(inv, cultist, grid)

    assert not result["valid"], "Attack should be invalid"
    assert result["reason"] == "no_line_of_sight", f"Expected no_line_of_sight, got {result['reason']}"
    print("[OK] Attack correctly rejected (no line of sight)")


def test_combat_deck_integration():
    """Test that combat deck is used in attack resolution."""
    print("\n=== TEST: Combat Deck Integration ===")

    grid = Grid(10)

    inv = Investigator(name="Attacker", gender="male")
    inv.equip_weapon(equipment.REVOLVER)
    grid.place_unit(inv, 0, 0)

    cultist = Cultist(name="Target")
    grid.place_unit(cultist, 2, 0)

    print(f"Initial deck: {inv.combat_deck.cards_remaining()} cards")

    # Resolve attack
    result = combat_resolver.resolve_attack(inv, cultist, grid)

    # Verify card was drawn
    assert result["card_drawn"] is not None, "Card should have been drawn"
    print(f"[OK] Card drawn: {result['card_drawn']}")

    # Verify deck has one less card
    assert inv.combat_deck.cards_remaining() == 19 or inv.combat_deck.cards_remaining() == 20, \
        "Deck should have 19 cards remaining (or 20 if reshuffled)"
    print(f"[OK] Deck updated: {inv.combat_deck.cards_remaining()} cards remaining")

    # Check if damage was modified by card
    if result["hit"] and not result["card_is_null"]:
        base_damage = result["base_damage"]
        final_damage = result["final_damage"]
        modifier = final_damage - base_damage if not result["card_is_crit"] else "x2"
        print(f"[OK] Damage: {base_damage} base -> {final_damage} final (modifier: {modifier})")


def test_attack_preview():
    """Test attack preview (no actual attack)."""
    print("\n=== TEST: Attack Preview ===")

    grid = Grid(10)

    inv = Investigator(name="Attacker", gender="male")
    inv.equip_weapon(equipment.RIFLE)  # +10% accuracy
    grid.place_unit(inv, 0, 0)

    cultist = Cultist(name="Target")
    grid.place_unit(cultist, 3, 0)

    # Get preview
    preview = combat_resolver.get_attack_preview(inv, cultist, grid)

    assert preview["valid"], "Preview should be valid"
    print(f"[OK] Attack preview:")
    print(f"  Hit chance: {preview['hit_chance']}%")
    print(f"  Distance: {preview['distance']:.1f} tiles")
    print(f"  Base damage: {preview['base_damage']}")
    print(f"  Damage range: {preview['min_damage']}-{preview['max_damage']}")

    # Verify no deck card was drawn
    initial_cards = inv.combat_deck.cards_remaining()
    # Preview again
    combat_resolver.get_attack_preview(inv, cultist, grid)
    assert inv.combat_deck.cards_remaining() == initial_cards, "Preview should not draw cards"
    print(f"[OK] Preview did not consume deck cards")


def test_sanity_damage():
    """Test sanity damage from eldritch weapons."""
    print("\n=== TEST: Sanity Damage ===")

    grid = Grid(10)

    # Create hound with sanity damage
    hound = HoundOfTindalos(name="Terror")
    grid.place_unit(hound, 0, 0)

    inv = Investigator(name="Target", gender="male")
    grid.place_unit(inv, 1, 0)  # Adjacent

    print(f"Hound weapon: {hound.equipped_weapon.name}")
    print(f"Sanity damage: {hound.weapon_sanity_damage}")
    print(f"Target sanity: {inv.current_sanity}/{inv.max_sanity}")

    # Attack
    result = combat_resolver.resolve_attack(hound, inv, grid)

    if result["hit"]:
        print(f"[OK] Hit - dealt {result['damage_dealt']} HP damage")
        if result.get("sanity_damage", 0) > 0:
            print(f"[OK] Dealt {result['sanity_damage']} sanity damage")
            print(f"  Target sanity: {inv.current_sanity}/{inv.max_sanity}")
        else:
            print(f"  (Sanity damage negated by Will: {inv.will})")


def run_all_tests():
    """Run all combat resolution tests."""
    print("\n" + "="*60)
    print("COMBAT RESOLUTION TEST SUITE")
    print("="*60)

    try:
        test_bresenham_line()
        test_line_of_sight_clear()
        test_line_of_sight_blocked()
        test_line_of_sight_half_cover()
        test_hit_chance_calculation()
        test_attack_resolution()
        test_attack_out_of_range()
        test_attack_no_los()
        test_combat_deck_integration()
        test_attack_preview()
        test_sanity_damage()

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
