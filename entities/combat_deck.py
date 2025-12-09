"""
Combat Deck System for Eldritch Tactics.

This module implements a personal deck-based combat resolution system
similar to Gloomhaven or Arkham Horror LCG. Each investigator has their own
deck that they draw from during attack resolution.

The deck adds:
1. Tactical variability - no guaranteed outcomes
2. Character progression - upgrade decks over time
3. Risk/reward gameplay - push your luck or play safe
4. Memorable moments - critical hits and auto-misses
"""

import random
from typing import List, Optional, Dict
from enum import Enum


class CardType(Enum):
    """
    Types of combat cards.

    Each card type has different effects on combat resolution:
    - NULL: Auto-miss (ignore all modifiers, attack fails)
    - MULTIPLY: Multiply final damage by 2
    - PLUS: Add bonus to damage (+2, +1)
    - MINUS: Subtract from damage (-1, -2)
    - ZERO: No modifier (baseline)
    """
    NULL = "null"       # Auto-miss (skull icon in real card games)
    MULTIPLY = "x2"     # Double damage (critical hit)
    PLUS = "+"          # Positive modifier
    MINUS = "-"         # Negative modifier
    ZERO = "0"          # No modifier


class Card:
    """
    Represents a single combat card.

    Cards modify attack rolls, adding variability to combat.
    """

    def __init__(self, card_type: CardType, modifier: int = 0, name: str = None):
        """
        Initialize a combat card.

        Args:
            card_type: The type of card (NULL, MULTIPLY, PLUS, MINUS, ZERO)
            modifier: Numeric modifier for damage (+2, +1, -1, etc.)
            name: Optional custom name for special cards
        """
        self.card_type = card_type
        self.modifier = modifier
        self.name = name or self._generate_name()

    def _generate_name(self) -> str:
        """Generate display name for the card."""
        if self.card_type == CardType.NULL:
            return "NULL"
        elif self.card_type == CardType.MULTIPLY:
            return "x2"
        elif self.card_type == CardType.ZERO:
            return "+0"
        elif self.card_type == CardType.PLUS:
            return f"+{self.modifier}"
        elif self.card_type == CardType.MINUS:
            return f"{self.modifier}"  # Negative sign already included
        return "???"

    def is_null(self) -> bool:
        """Check if this is a NULL card (auto-miss)."""
        return self.card_type == CardType.NULL

    def is_multiply(self) -> bool:
        """Check if this is a MULTIPLY card (critical hit)."""
        return self.card_type == CardType.MULTIPLY

    def apply_to_damage(self, base_damage: int) -> int:
        """
        Apply this card's modifier to base damage.

        Args:
            base_damage: The base damage before card modifier

        Returns:
            Modified damage after applying card effect

        Examples:
            >>> card = Card(CardType.PLUS, 2)  # +2 card
            >>> card.apply_to_damage(5)
            7

            >>> card = Card(CardType.MULTIPLY, 2)  # x2 card
            >>> card.apply_to_damage(5)
            10

            >>> card = Card(CardType.NULL, 0)  # NULL card
            >>> card.apply_to_damage(5)
            0
        """
        if self.card_type == CardType.NULL:
            # Auto-miss: no damage regardless of base
            return 0
        elif self.card_type == CardType.MULTIPLY:
            # Critical hit: double damage
            return base_damage * 2
        else:
            # Add/subtract modifier (can't go below 0)
            return max(0, base_damage + self.modifier)

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Card({self.name})"

    def __str__(self) -> str:
        """User-friendly string representation."""
        return self.name


class CombatDeck:
    """
    Personal combat deck for an investigator.

    Each investigator has their own deck that persists across battles.
    The deck is drawn from during attack resolution, adding variability
    and excitement to combat.

    Standard deck composition (20 cards):
    - 1x NULL (auto-miss)
    - 1x x2 (double damage)
    - 1x +2
    - 5x +1
    - 5x -1
    - 6x +0
    - 1x +0 (20th card)
    """

    def __init__(self, owner_name: str = "Unknown"):
        """
        Initialize an empty combat deck.

        Args:
            owner_name: Name of the investigator who owns this deck
        """
        self.owner_name = owner_name
        self.draw_pile: List[Card] = []
        self.discard_pile: List[Card] = []

        # Statistics (for progression and UI display)
        self.total_cards_drawn = 0
        self.nulls_drawn = 0
        self.crits_drawn = 0

    def add_card(self, card: Card) -> None:
        """
        Add a card to the deck.

        New cards are added to the draw pile.

        Args:
            card: Card to add to the deck
        """
        self.draw_pile.append(card)

    def remove_card(self, card_name: str) -> bool:
        """
        Remove a card from the deck (deck improvement).

        Searches both draw pile and discard pile.
        Removes the first matching card found.

        Args:
            card_name: Name of card to remove (e.g., "-1", "+0", "NULL")

        Returns:
            True if card was found and removed, False otherwise

        Example:
            >>> deck.remove_card("-1")  # Remove one -1 card (deck improvement)
            True
        """
        # Try to remove from draw pile first
        for i, card in enumerate(self.draw_pile):
            if card.name == card_name:
                self.draw_pile.pop(i)
                return True

        # Try discard pile if not found in draw pile
        for i, card in enumerate(self.discard_pile):
            if card.name == card_name:
                self.discard_pile.pop(i)
                return True

        return False

    def shuffle(self) -> None:
        """
        Shuffle the draw pile.

        Uses random.shuffle for randomization.
        """
        random.shuffle(self.draw_pile)

    def reshuffle_discard(self) -> None:
        """
        Reshuffle discard pile back into draw pile.

        This happens automatically when the draw pile is empty.
        The discard pile is shuffled and becomes the new draw pile.
        """
        self.draw_pile = self.discard_pile
        self.discard_pile = []
        self.shuffle()
        print(f"[{self.owner_name}] Deck reshuffled ({len(self.draw_pile)} cards)")

    def draw(self) -> Optional[Card]:
        """
        Draw a card from the deck.

        The card is moved from draw pile to discard pile.
        If draw pile is empty, automatically reshuffles discard pile.

        Returns:
            The drawn card, or None if deck is completely empty

        Example:
            >>> card = deck.draw()
            >>> print(f"Drew: {card.name}")
            Drew: +1
        """
        # Check if draw pile is empty
        if not self.draw_pile:
            if not self.discard_pile:
                # Both piles empty - deck is exhausted
                print(f"[{self.owner_name}] WARNING: Deck is empty!")
                return None

            # Reshuffle discard pile into draw pile
            self.reshuffle_discard()

        # Draw top card
        card = self.draw_pile.pop(0)
        self.discard_pile.append(card)

        # Update statistics
        self.total_cards_drawn += 1
        if card.is_null():
            self.nulls_drawn += 1
        elif card.is_multiply():
            self.crits_drawn += 1

        return card

    def peek(self, count: int = 1) -> List[Card]:
        """
        Look at the top N cards without drawing them.

        Useful for abilities that let you preview upcoming cards.

        Args:
            count: Number of cards to peek at (default 1)

        Returns:
            List of cards from top of draw pile (not removed)
        """
        return self.draw_pile[:count]

    def size(self) -> int:
        """Get total number of cards in deck (draw + discard)."""
        return len(self.draw_pile) + len(self.discard_pile)

    def cards_remaining(self) -> int:
        """Get number of cards left in draw pile before reshuffle."""
        return len(self.draw_pile)

    def get_deck_composition(self) -> Dict[str, int]:
        """
        Get the composition of the entire deck.

        Returns:
            Dictionary mapping card names to counts

        Example:
            >>> composition = deck.get_deck_composition()
            >>> print(composition)
            {'+2': 1, '+1': 5, '+0': 7, '-1': 5, 'x2': 1, 'NULL': 1}
        """
        composition = {}
        all_cards = self.draw_pile + self.discard_pile

        for card in all_cards:
            composition[card.name] = composition.get(card.name, 0) + 1

        return composition

    def reset(self) -> None:
        """
        Reset the deck for a new battle.

        Moves all cards from discard back to draw pile and shuffles.
        Does NOT reset deck composition (permanent improvements persist).
        """
        self.draw_pile.extend(self.discard_pile)
        self.discard_pile = []
        self.shuffle()

    def get_statistics(self) -> Dict[str, float]:
        """
        Get deck performance statistics.

        Returns:
            Dictionary with statistics (draw rate, crit rate, null rate)
        """
        if self.total_cards_drawn == 0:
            return {
                "total_draws": 0,
                "crit_rate": 0.0,
                "null_rate": 0.0,
            }

        return {
            "total_draws": self.total_cards_drawn,
            "crit_rate": self.crits_drawn / self.total_cards_drawn,
            "null_rate": self.nulls_drawn / self.total_cards_drawn,
        }

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"CombatDeck(owner={self.owner_name}, draw={len(self.draw_pile)}, discard={len(self.discard_pile)})"


# ============================================================================
# FACTORY FUNCTIONS - Create pre-configured decks
# ============================================================================

def create_standard_deck(owner_name: str = "Unknown") -> CombatDeck:
    """
    Create a standard 20-card combat deck.

    Composition:
    - 1x NULL (auto-miss)
    - 1x x2 (double damage)
    - 1x +2
    - 5x +1
    - 5x -1
    - 7x +0

    Total: 20 cards

    This is the default deck that all investigators start with.

    Args:
        owner_name: Name of the investigator who owns this deck

    Returns:
        A shuffled standard deck ready for use

    Example:
        >>> deck = create_standard_deck("John Doe")
        >>> card = deck.draw()
        >>> print(f"Drew: {card.name}")
    """
    deck = CombatDeck(owner_name)

    # Add NULL card (auto-miss)
    deck.add_card(Card(CardType.NULL, 0))

    # Add x2 card (critical hit)
    deck.add_card(Card(CardType.MULTIPLY, 2))

    # Add +2 card
    deck.add_card(Card(CardType.PLUS, 2))

    # Add 5x +1 cards
    for _ in range(5):
        deck.add_card(Card(CardType.PLUS, 1))

    # Add 5x -1 cards
    for _ in range(5):
        deck.add_card(Card(CardType.MINUS, -1))

    # Add 7x +0 cards (6 specified + 1 to reach 20 total)
    for _ in range(7):
        deck.add_card(Card(CardType.ZERO, 0))

    # Shuffle the deck
    deck.shuffle()

    return deck


def create_improved_deck(owner_name: str = "Unknown", remove_negatives: int = 2) -> CombatDeck:
    """
    Create an improved deck with some negative cards removed.

    This represents a veteran investigator who has upgraded their deck.

    Args:
        owner_name: Name of the investigator
        remove_negatives: Number of -1 cards to remove (default 2)

    Returns:
        An improved deck with fewer negative cards
    """
    deck = create_standard_deck(owner_name)

    # Remove some -1 cards
    for _ in range(remove_negatives):
        deck.remove_card("-1")

    return deck


def create_blessed_deck(owner_name: str = "Unknown") -> CombatDeck:
    """
    Create a blessed deck with extra positive cards.

    This could represent a character with divine protection or luck.
    Adds extra +1 cards and an additional x2.

    Args:
        owner_name: Name of the investigator

    Returns:
        A blessed deck with enhanced positive cards
    """
    deck = create_standard_deck(owner_name)

    # Add extra positive cards
    deck.add_card(Card(CardType.PLUS, 1))
    deck.add_card(Card(CardType.PLUS, 1))
    deck.add_card(Card(CardType.MULTIPLY, 2))  # Extra crit

    # Remove one -1
    deck.remove_card("-1")

    deck.shuffle()
    return deck


def create_cursed_deck(owner_name: str = "Unknown") -> CombatDeck:
    """
    Create a cursed deck with extra negative cards.

    This could represent a character suffering from madness or bad luck.
    Adds extra -1 cards and an additional NULL.

    Args:
        owner_name: Name of the investigator

    Returns:
        A cursed deck with more negative cards
    """
    deck = create_standard_deck(owner_name)

    # Add curse cards
    deck.add_card(Card(CardType.MINUS, -1))
    deck.add_card(Card(CardType.MINUS, -1))
    deck.add_card(Card(CardType.NULL, 0))  # Extra auto-miss

    deck.shuffle()
    return deck
