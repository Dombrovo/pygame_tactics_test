"""
Test script for combat deck system.

This script tests the deck-based combat resolution system:
- Card creation and modifiers
- Deck drawing and reshuffling
- Deck improvements (adding/removing cards)
- Integration with investigators
"""

import sys
import os

# Add parent directory to path to import game modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from entities.combat_deck import (
    Card, CardType, CombatDeck,
    create_standard_deck, create_improved_deck, create_blessed_deck, create_cursed_deck
)
from entities.investigator import Investigator


def test_card_modifiers():
    """Test that cards correctly modify damage."""
    print("\n=== TEST: Card Modifiers ===")

    base_damage = 5

    # Test +2 card
    plus_two = Card(CardType.PLUS, 2)
    assert plus_two.apply_to_damage(base_damage) == 7, "Failed: +2 card"
    print(f"[OK] +2 card: {base_damage} -> {plus_two.apply_to_damage(base_damage)}")

    # Test +1 card
    plus_one = Card(CardType.PLUS, 1)
    assert plus_one.apply_to_damage(base_damage) == 6, "Failed: +1 card"
    print(f"[OK] +1 card: {base_damage} -> {plus_one.apply_to_damage(base_damage)}")

    # Test -1 card
    minus_one = Card(CardType.MINUS, -1)
    assert minus_one.apply_to_damage(base_damage) == 4, "Failed: -1 card"
    print(f"[OK] -1 card: {base_damage} -> {minus_one.apply_to_damage(base_damage)}")

    # Test +0 card
    zero = Card(CardType.ZERO, 0)
    assert zero.apply_to_damage(base_damage) == 5, "Failed: +0 card"
    print(f"[OK] +0 card: {base_damage} -> {zero.apply_to_damage(base_damage)}")

    # Test x2 card (critical hit)
    multiply = Card(CardType.MULTIPLY, 2)
    assert multiply.apply_to_damage(base_damage) == 10, "Failed: x2 card"
    print(f"[OK] x2 card: {base_damage} -> {multiply.apply_to_damage(base_damage)}")

    # Test NULL card (auto-miss)
    null = Card(CardType.NULL, 0)
    assert null.apply_to_damage(base_damage) == 0, "Failed: NULL card"
    print(f"[OK] NULL card: {base_damage} -> {null.apply_to_damage(base_damage)}")

    # Test that damage can't go below 0
    minus_ten = Card(CardType.MINUS, -10)
    assert minus_ten.apply_to_damage(5) == 0, "Failed: Damage should not go negative"
    print(f"[OK] Negative modifier clamped: 5 + (-10) -> {minus_ten.apply_to_damage(5)}")


def test_standard_deck_composition():
    """Test that standard deck has correct card composition."""
    print("\n=== TEST: Standard Deck Composition ===")

    deck = create_standard_deck("Test")

    # Get deck composition
    composition = deck.get_deck_composition()

    print("Deck composition:")
    for card_name, count in sorted(composition.items()):
        print(f"  {card_name}: {count}x")

    # Verify standard deck (20 cards total)
    assert deck.size() == 20, f"Expected 20 cards, got {deck.size()}"
    assert composition.get("NULL", 0) == 1, "Expected 1 NULL card"
    assert composition.get("x2", 0) == 1, "Expected 1 x2 card"
    assert composition.get("+2", 0) == 1, "Expected 1 +2 card"
    assert composition.get("+1", 0) == 5, "Expected 5 +1 cards"
    assert composition.get("-1", 0) == 5, "Expected 5 -1 cards"
    assert composition.get("+0", 0) == 7, "Expected 7 +0 cards"

    print("[OK] Standard deck has correct composition (20 cards)")


def test_deck_drawing():
    """Test drawing cards from the deck."""
    print("\n=== TEST: Deck Drawing ===")

    deck = create_standard_deck("Test")

    # Draw 5 cards
    drawn_cards = []
    for i in range(5):
        card = deck.draw()
        drawn_cards.append(card.name)
        print(f"  Draw {i+1}: {card.name}")

    assert len(drawn_cards) == 5, "Should have drawn 5 cards"
    assert deck.cards_remaining() == 15, f"Expected 15 cards remaining, got {deck.cards_remaining()}"
    assert len(deck.discard_pile) == 5, "Should have 5 cards in discard"

    print(f"[OK] Drew 5 cards, {deck.cards_remaining()} remaining in draw pile")


def test_deck_reshuffle():
    """Test that deck reshuffles when draw pile is empty."""
    print("\n=== TEST: Deck Reshuffle ===")

    deck = create_standard_deck("Test")
    initial_size = deck.size()

    print(f"Initial deck size: {initial_size}")

    # Draw all 20 cards
    for i in range(20):
        card = deck.draw()

    print(f"After drawing 20 cards: {deck.cards_remaining()} in draw pile, {len(deck.discard_pile)} in discard")

    # Next draw should trigger reshuffle
    print("Drawing 21st card (should trigger reshuffle)...")
    card = deck.draw()

    assert card is not None, "Should have drawn a card after reshuffle"
    assert deck.cards_remaining() == 19, f"Expected 19 cards after reshuffle, got {deck.cards_remaining()}"
    assert len(deck.discard_pile) == 1, f"Expected 1 card in discard, got {len(deck.discard_pile)}"

    print(f"[OK] Deck reshuffled automatically, drew: {card.name}")


def test_deck_improvement():
    """Test removing negative cards from deck."""
    print("\n=== TEST: Deck Improvement (Remove -1 cards) ===")

    deck = create_standard_deck("Test")
    composition_before = deck.get_deck_composition()

    print(f"Before: {composition_before.get('-1', 0)}x -1 cards")

    # Remove 2x -1 cards
    removed1 = deck.remove_card("-1")
    removed2 = deck.remove_card("-1")

    composition_after = deck.get_deck_composition()

    print(f"After: {composition_after.get('-1', 0)}x -1 cards")

    assert removed1 and removed2, "Should have successfully removed 2 cards"
    assert composition_after.get("-1", 0) == 3, f"Expected 3 -1 cards, got {composition_after.get('-1', 0)}"
    assert deck.size() == 18, f"Expected 18 total cards, got {deck.size()}"

    print("[OK] Successfully removed 2x -1 cards (deck improved)")


def test_deck_statistics():
    """Test deck statistics tracking."""
    print("\n=== TEST: Deck Statistics ===")

    deck = create_standard_deck("Test")

    # Manually set up a scenario by drawing specific cards
    # (In real game, this would happen naturally during combat)

    # Draw 10 cards to generate some stats
    for _ in range(10):
        deck.draw()

    stats = deck.get_statistics()

    print(f"Total draws: {stats['total_draws']}")
    print(f"Crit rate: {stats['crit_rate']:.1%}")
    print(f"Null rate: {stats['null_rate']:.1%}")

    assert stats['total_draws'] == 10, "Should have 10 total draws"
    assert 0 <= stats['crit_rate'] <= 1, "Crit rate should be between 0 and 1"
    assert 0 <= stats['null_rate'] <= 1, "Null rate should be between 0 and 1"

    print("[OK] Statistics tracked correctly")


def test_investigator_integration():
    """Test that investigators have combat decks."""
    print("\n=== TEST: Investigator Integration ===")

    # Create investigator
    inv = Investigator(name="Test Investigator", gender="male")

    # Check that deck was created
    assert hasattr(inv, 'combat_deck'), "Investigator should have combat_deck attribute"
    assert inv.combat_deck is not None, "Combat deck should be initialized"
    assert inv.combat_deck.size() == 20, "Investigator should start with 20-card deck"

    print(f"Investigator: {inv.name}")
    print(f"Deck size: {inv.combat_deck.size()}")
    print(f"Deck composition: {inv.combat_deck.get_deck_composition()}")

    # Test drawing a card through investigator
    card = inv.draw_combat_card()
    assert card is not None, "Should be able to draw a card"
    print(f"Drew card through investigator: {card.name}")

    # Test reset
    inv.reset_combat_deck()
    assert inv.combat_deck.cards_remaining() == 20, "Deck should reset to full draw pile"
    print(f"After reset: {inv.combat_deck.cards_remaining()} cards in draw pile")

    print("[OK] Investigator combat deck integration works")


def test_special_decks():
    """Test special deck variants (blessed, cursed, improved)."""
    print("\n=== TEST: Special Deck Variants ===")

    # Test improved deck
    improved = create_improved_deck("Veteran")
    comp_improved = improved.get_deck_composition()
    print(f"Improved deck: {comp_improved.get('-1', 0)}x -1 cards (should be 3)")
    assert comp_improved.get("-1", 0) == 3, "Improved deck should have 3 -1 cards"

    # Test blessed deck
    blessed = create_blessed_deck("Lucky")
    comp_blessed = blessed.get_deck_composition()
    print(f"Blessed deck: {comp_blessed.get('x2', 0)}x x2 cards (should be 2)")
    assert comp_blessed.get("x2", 0) == 2, "Blessed deck should have 2 x2 cards"

    # Test cursed deck
    cursed = create_cursed_deck("Unlucky")
    comp_cursed = cursed.get_deck_composition()
    print(f"Cursed deck: {comp_cursed.get('NULL', 0)}x NULL cards (should be 2)")
    assert comp_cursed.get("NULL", 0) == 2, "Cursed deck should have 2 NULL cards"

    print("[OK] Special deck variants work correctly")


def test_combat_simulation():
    """Simulate a series of attacks using the deck."""
    print("\n=== TEST: Combat Simulation ===")

    inv = Investigator(name="Combat Test", gender="male")
    base_damage = 5

    print(f"Simulating 25 attacks with base damage = {base_damage}")
    print("-" * 50)

    total_damage = 0
    nulls = 0
    crits = 0

    for i in range(25):
        card = inv.draw_combat_card()
        modified_damage = card.apply_to_damage(base_damage)
        total_damage += modified_damage

        if card.is_null():
            nulls += 1
            result = "MISS"
        elif card.is_multiply():
            crits += 1
            result = "CRIT"
        else:
            result = ""

        # Only print first 10 and last 5 to keep output manageable
        if i < 10 or i >= 20:
            print(f"  Attack {i+1:2d}: Drew {card.name:>4s} -> {modified_damage} damage {result}")
        elif i == 10:
            print("  ...")

    print("-" * 50)
    print(f"Total damage dealt: {total_damage}")
    print(f"Average damage per attack: {total_damage / 25:.2f}")
    print(f"Nulls drawn: {nulls}")
    print(f"Crits drawn: {crits}")
    print(f"Deck reshuffled: {'Yes' if inv.combat_deck.total_cards_drawn > 20 else 'No'}")

    # Verify stats
    stats = inv.combat_deck.get_statistics()
    assert stats['total_draws'] == 25, "Should have 25 draws"

    print("[OK] Combat simulation completed successfully")


def run_all_tests():
    """Run all combat deck tests."""
    print("\n" + "="*60)
    print("COMBAT DECK TEST SUITE")
    print("="*60)

    try:
        test_card_modifiers()
        test_standard_deck_composition()
        test_deck_drawing()
        test_deck_reshuffle()
        test_deck_improvement()
        test_deck_statistics()
        test_investigator_integration()
        test_special_decks()
        test_combat_simulation()

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
