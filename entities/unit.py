"""
Base Unit class for all game entities.

This module defines the base Unit class that both player investigators
and enemy units inherit from.
"""

from typing import Tuple, Optional


class Unit:
    """
    Base class for all units (investigators and enemies).

    Units have:
    - Health and Sanity (dual resource system)
    - Position on the grid
    - Combat stats (accuracy, movement)
    - Team affiliation (player or enemy)
    """

    def __init__(
        self,
        name: str,
        max_health: int,
        max_sanity: int,
        accuracy: int,
        will: int,
        movement_range: int,
        team: str,
        symbol: str = "?"
    ):
        """
        Initialize a unit.

        Args:
            name: Unit's display name
            max_health: Maximum health points
            max_sanity: Maximum sanity points
            accuracy: Base hit chance percentage (0-100)
            will: Sanity defense stat
            movement_range: How many tiles unit can move per turn
            team: "player" or "enemy"
            symbol: Unicode symbol for display (e.g., "👤", "🔫")
        """
        # Identity
        self.name = name
        self.team = team
        self.symbol = symbol

        # Position (will be set when placed on grid)
        self.position: Optional[Tuple[int, int]] = None

        # Health system
        self.max_health = max_health
        self.current_health = max_health

        # Sanity system
        self.max_sanity = max_sanity
        self.current_sanity = max_sanity

        # Combat stats
        self.accuracy = accuracy  # Base hit chance percentage
        self.will = will          # Defense against sanity damage
        self.movement_range = movement_range

        # Status flags
        self.is_incapacitated = False
        self.has_moved = False      # Track if unit moved this turn
        self.has_attacked = False   # Track if unit attacked this turn

    def take_damage(self, amount: int) -> int:
        """
        Apply health damage to the unit.

        Args:
            amount: Damage to apply

        Returns:
            Actual damage dealt (may be capped by current health)
        """
        actual_damage = min(amount, self.current_health)
        self.current_health -= actual_damage

        if self.current_health <= 0:
            self.current_health = 0
            self.is_incapacitated = True

        return actual_damage

    def take_sanity_damage(self, amount: int) -> int:
        """
        Apply sanity damage to the unit.

        Sanity damage is reduced by Will stat.

        Args:
            amount: Base sanity damage

        Returns:
            Actual sanity damage dealt
        """
        # Will reduces sanity damage
        actual_damage = max(0, amount - self.will)
        self.current_sanity -= actual_damage

        if self.current_sanity <= 0:
            self.current_sanity = 0
            self.is_incapacitated = True

        return actual_damage

    def heal(self, amount: int) -> int:
        """
        Restore health points.

        Args:
            amount: Health to restore

        Returns:
            Actual health restored (capped at max)
        """
        old_health = self.current_health
        self.current_health = min(self.max_health, self.current_health + amount)
        return self.current_health - old_health

    def restore_sanity(self, amount: int) -> int:
        """
        Restore sanity points.

        Args:
            amount: Sanity to restore

        Returns:
            Actual sanity restored (capped at max)
        """
        old_sanity = self.current_sanity
        self.current_sanity = min(self.max_sanity, self.current_sanity + amount)
        return self.current_sanity - old_sanity

    def get_health_percentage(self) -> float:
        """Get current health as percentage (0.0 to 1.0)."""
        if self.max_health == 0:
            return 0.0
        return self.current_health / self.max_health

    def get_sanity_percentage(self) -> float:
        """Get current sanity as percentage (0.0 to 1.0)."""
        if self.max_sanity == 0:
            return 0.0
        return self.current_sanity / self.max_sanity

    def can_act(self) -> bool:
        """
        Check if unit can perform actions.

        Returns:
            True if not incapacitated, False otherwise
        """
        return not self.is_incapacitated

    def reset_turn_flags(self):
        """
        Reset per-turn flags (called at start of turn).

        In MVP: Units can Move + Attack OR Move twice per turn.
        """
        self.has_moved = False
        self.has_attacked = False

    def can_move(self) -> bool:
        """
        Check if unit can move this turn.

        Returns:
            True if unit hasn't moved twice yet
        """
        # In MVP: Can move if haven't attacked, or can always move once
        return not self.has_attacked or not self.has_moved

    def can_attack(self) -> bool:
        """
        Check if unit can attack this turn.

        Returns:
            True if unit hasn't attacked and hasn't moved twice
        """
        # Can attack if: (moved 0 or 1 times) AND (haven't attacked)
        return not self.has_attacked

    def get_info_text(self) -> str:
        """
        Get formatted info string for UI display.

        Returns:
            Multi-line string with unit stats
        """
        lines = [
            f"Name: {self.name}",
            f"Team: {self.team}",
            f"HP: {self.current_health}/{self.max_health}",
            f"Sanity: {self.current_sanity}/{self.max_sanity}",
            f"Accuracy: {self.accuracy}%",
            f"Will: {self.will}",
            f"Move: {self.movement_range}",
        ]

        if self.is_incapacitated:
            lines.append("STATUS: INCAPACITATED")

        return "\n".join(lines)

    def __repr__(self) -> str:
        """String representation for debugging."""
        status = " [INCAPACITATED]" if self.is_incapacitated else ""
        return f"{self.name} ({self.team}): {self.current_health}/{self.max_health} HP, {self.current_sanity}/{self.max_sanity} SAN{status}"
