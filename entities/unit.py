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

        # --- BASE STATS (Set at creation) ---
        # Health system
        self.base_max_health = max_health
        self.current_health = max_health

        # Sanity system
        self.base_max_sanity = max_sanity
        self.current_sanity = max_sanity

        # Combat stats
        self.base_accuracy = accuracy      # Base hit chance percentage
        self.base_will = will              # Defense against sanity damage
        self.base_movement_range = movement_range

        # --- MODIFIERS (Applied by backgrounds, traits, equipment, status effects) ---
        # These values are ADDED to base stats to get effective stats
        # Example: base_accuracy = 75, accuracy_modifier = +10 → accuracy = 85%
        # Modifiers can be positive (buffs) or negative (debuffs/injuries)
        self.max_health_modifier = 0
        self.max_sanity_modifier = 0
        self.accuracy_modifier = 0
        self.will_modifier = 0
        self.movement_modifier = 0

        # Status flags
        self.is_incapacitated = False

        # Action Points System (2 actions per turn)
        # Each action can be: Move or Attack
        # Allows: Move-Move, Move-Attack, Attack-Move, Attack-Attack
        self.max_action_points = 2
        self.current_action_points = 2

    # --- CALCULATED STATS (Properties: base + modifiers) ---
    # These are Python @property decorators, which make methods act like attributes
    # When you access unit.max_health, it actually calls the max_health() method
    # This auto-calculates effective stats from base + modifiers
    #
    # Benefits:
    # 1. Always up-to-date (recalculated each access)
    # 2. No need to manually update when modifiers change
    # 3. Clean syntax: unit.accuracy instead of unit.get_accuracy()
    #
    # Example usage:
    #   unit.base_accuracy = 75
    #   unit.accuracy_modifier = 10
    #   print(unit.accuracy)  # Prints 85 (auto-calculated)

    @property
    def max_health(self) -> int:
        """
        Effective max health = base + modifiers.

        Clamped to minimum of 1 (unit always has at least 1 max HP).
        Even with severe injuries, a unit can't have 0 max health.
        """
        return max(1, self.base_max_health + self.max_health_modifier)

    @property
    def max_sanity(self) -> int:
        """
        Effective max sanity = base + modifiers.

        Clamped to minimum of 1 (unit always has at least 1 max sanity).
        """
        return max(1, self.base_max_sanity + self.max_sanity_modifier)

    @property
    def accuracy(self) -> int:
        """
        Effective accuracy = base + modifiers.

        Clamped between 5-95%:
        - Minimum 5%: Even terrible shooters have some chance to hit
        - Maximum 95%: Even expert marksmen can miss (no guaranteed hits)

        This range prevents degenerate gameplay (auto-hit or auto-miss).
        """
        return max(5, min(95, self.base_accuracy + self.accuracy_modifier))

    @property
    def will(self) -> int:
        """
        Effective will = base + modifiers.

        Will reduces sanity damage taken (acts as sanity armor).
        Minimum 0 (can't have negative will, but also no minimum positive value).
        """
        return max(0, self.base_will + self.will_modifier)

    @property
    def movement_range(self) -> int:
        """
        Effective movement range = base + modifiers.

        Clamped to minimum of 1 (unit must be able to move at least 1 tile).
        Even with leg injuries, a unit can still crawl/limp 1 tile.
        """
        return max(1, self.base_movement_range + self.movement_modifier)

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

    def apply_stat_modifiers(self, **modifiers):
        """
        Apply stat modifiers from backgrounds, traits, or equipment.

        This is the PRIMARY way to modify unit stats. Use this instead of
        directly changing modifier values.

        Modifiers are ADDITIVE - calling this multiple times stacks the effects:
        - First call: apply_stat_modifiers(accuracy=10) → accuracy_modifier = +10
        - Second call: apply_stat_modifiers(accuracy=5) → accuracy_modifier = +15

        Common use cases:
        - Applying background traits at creation:
          investigator.apply_stat_modifiers(max_health=3, accuracy=-5)

        - Equipping items:
          investigator.apply_stat_modifiers(accuracy=10)  # Scoped rifle

        - Suffering injuries:
          investigator.apply_stat_modifiers(movement=-1)  # Leg wound

        - Temporary buffs/debuffs (Phase 2+):
          investigator.apply_stat_modifiers(will=2)  # Elder Sign protection

        Args:
            **modifiers: Keyword arguments for stat changes.
                        Values can be positive (buff) or negative (debuff).
                        Keys: max_health, max_sanity, accuracy, will, movement

        Example:
            # Apply "Veteran" trait: +10% accuracy, -1 sanity
            unit.apply_stat_modifiers(accuracy=10, max_sanity=-1)
        """
        if "max_health" in modifiers:
            self.max_health_modifier += modifiers["max_health"]
        if "max_sanity" in modifiers:
            self.max_sanity_modifier += modifiers["max_sanity"]
        if "accuracy" in modifiers:
            self.accuracy_modifier += modifiers["accuracy"]
        if "will" in modifiers:
            self.will_modifier += modifiers["will"]
        if "movement" in modifiers or "movement_range" in modifiers:
            # Accept both "movement" and "movement_range" for flexibility
            self.movement_modifier += modifiers.get("movement", modifiers.get("movement_range", 0))

    def has_modifiers(self) -> bool:
        """Check if unit has any active stat modifiers."""
        return (
            self.max_health_modifier != 0 or
            self.max_sanity_modifier != 0 or
            self.accuracy_modifier != 0 or
            self.will_modifier != 0 or
            self.movement_modifier != 0
        )

    def reset_turn_flags(self):
        """
        Reset per-turn action points (called at start of turn).

        Each turn, units get 2 action points.
        Actions cost:
        - Move: 1 action point
        - Attack: 1 action point

        This allows: Move-Move, Move-Attack, Attack-Move, or Attack-Attack.
        """
        self.current_action_points = self.max_action_points

    def can_move(self) -> bool:
        """
        Check if unit can move this turn.

        Action economy (2 action points):
        - Move costs 1 action point
        - Can move if at least 1 action point remains

        Returns:
            True if unit has action points to move
        """
        return self.current_action_points >= 1

    def can_attack(self) -> bool:
        """
        Check if unit can attack this turn.

        Action economy (2 action points):
        - Attack costs 1 action point
        - Can attack if at least 1 action point remains
        - Can attack multiple times if action points available

        Returns:
            True if unit has action points to attack
        """
        return self.current_action_points >= 1

    def consume_action_point(self, amount: int = 1) -> bool:
        """
        Consume action points when performing an action.

        Args:
            amount: Number of action points to consume (default 1)

        Returns:
            True if action points were consumed, False if not enough available
        """
        if self.current_action_points >= amount:
            self.current_action_points -= amount
            return True
        return False

    def has_actions_remaining(self) -> bool:
        """
        Check if unit has any action points remaining.

        Returns:
            True if current_action_points > 0
        """
        return self.current_action_points > 0

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
