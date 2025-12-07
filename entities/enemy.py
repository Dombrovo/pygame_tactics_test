"""
Enemy unit classes.

This module defines the two MVP enemy types:
- Cultist: Ranged attacker
- Hound of Tindalos: Fast melee horror with sanity damage
"""

from entities.unit import Unit
from entities import equipment  # Import equipment module for weapons
from typing import List


class Enemy(Unit):
    """
    Base enemy class.

    Extends Unit with enemy-specific behaviors.
    Enemy weapons are handled through the equipment system (equipped_weapon).

    Note: The old weapon_range, attack_type, sanity_damage parameters
    have been replaced by the equipment system. Use equip_weapon() instead.
    """

    def __init__(
        self,
        name: str,
        max_health: int,
        max_sanity: int,
        accuracy: int,
        will: int,
        movement_range: int,
        symbol: str,
        # Legacy parameters kept for backward compatibility (not used)
        weapon_range: int = None,
        attack_type: str = None,
        sanity_damage: int = None
    ):
        """
        Initialize an enemy unit.

        Args:
            name: Enemy name
            max_health: Maximum health
            max_sanity: Maximum sanity (enemies have sanity too)
            accuracy: Hit chance percentage
            will: Sanity defense
            movement_range: Tiles per turn
            symbol: Unicode symbol for display
            weapon_range: DEPRECATED - Use equip_weapon() instead
            attack_type: DEPRECATED - Use equip_weapon() instead
            sanity_damage: DEPRECATED - Use equip_weapon() instead
        """
        super().__init__(
            name=name,
            max_health=max_health,
            max_sanity=max_sanity,
            accuracy=accuracy,
            will=will,
            movement_range=movement_range,
            team="enemy",
            symbol=symbol
        )

        # Weapon stats now come from equipped_weapon
        # Subclasses should call self.equip_weapon() to set their weapon

    def get_info_text(self) -> str:
        """
        Get formatted info string for UI display.

        Returns:
            Multi-line string with enemy stats
        """
        lines = [
            f"{self.symbol} {self.name}",
            f"HP: {self.current_health}/{self.max_health}",
            f"Range: {self.weapon_range} tiles",
            f"Attack: {self.attack_type}",
        ]

        if self.weapon_sanity_damage > 0:
            lines.append(f"[!] Sanity Dmg: {self.weapon_sanity_damage}")

        if self.is_incapacitated:
            lines.append("[X] DEFEATED")

        return "\n".join(lines)


class Cultist(Enemy):
    """
    Cultist - Ranged human enemy.

    Cultists are weak but attack from range with firearms.
    Stats:
    - Medium health
    - Ranged attack (3 tile range)
    - No sanity damage (just guns)
    - Moderate accuracy
    """

    def __init__(self, name: str = "Cultist"):
        """
        Initialize a Cultist.

        Args:
            name: Cultist's name (default "Cultist")
        """
        super().__init__(
            name=name,
            max_health=10,
            max_sanity=8,         # Cultists have some sanity
            accuracy=60,          # Lower accuracy than investigators
            will=3,               # Low will
            movement_range=4,     # Standard movement
            symbol="🔫",          # Gun symbol
            weapon_range=3,       # Can shoot 3 tiles away
            attack_type="ranged",
            sanity_damage=0       # Physical damage only
        )

        # Equip weapon (uses equipment system)
        self.equip_weapon(equipment.CULTIST_PISTOL)

    def __repr__(self) -> str:
        """String representation for debugging."""
        status = " [DEFEATED]" if self.is_incapacitated else ""
        return f"Cultist '{self.name}': {self.current_health}/{self.max_health} HP{status}"


class HoundOfTindalos(Enemy):
    """
    Hound of Tindalos - Fast melee horror.

    Interdimensional predators that hunt through angles of time.
    Stats:
    - Low health (glass cannon)
    - Very fast movement
    - Melee only (1 tile range)
    - Causes significant sanity damage
    - High accuracy
    """

    def __init__(self, name: str = "Hound of Tindalos"):
        """
        Initialize a Hound of Tindalos.

        Args:
            name: Hound's name (default "Hound of Tindalos")
        """
        super().__init__(
            name=name,
            max_health=8,         # Low health
            max_sanity=15,        # Eldritch creatures have high sanity
            accuracy=75,          # High accuracy for melee
            will=10,              # Very high will
            movement_range=6,     # FAST - can close distance quickly
            symbol="🐺",          # Wolf symbol
            weapon_range=1,       # Melee only (adjacent tiles)
            attack_type="melee",
            sanity_damage=5       # Seeing it up close causes sanity loss
        )

        # Equip weapon (uses equipment system)
        self.equip_weapon(equipment.HOUND_CLAWS)

    def __repr__(self) -> str:
        """String representation for debugging."""
        status = " [BANISHED]" if self.is_incapacitated else ""
        return f"Hound '{self.name}': {self.current_health}/{self.max_health} HP{status}"


def create_test_enemies() -> List[Enemy]:
    """
    Create a test group of enemies for MVP testing.

    Returns:
        List of 4 enemies (2 Cultists, 2 Hounds)
    """
    enemies = [
        Cultist(name="Cultist Alpha"),
        Cultist(name="Cultist Beta"),
        HoundOfTindalos(name="Hound Alpha"),
        HoundOfTindalos(name="Hound Beta"),
    ]

    return enemies


def create_cultist_squad() -> List[Enemy]:
    """
    Create a squad of 4 Cultists (easier encounter).

    Returns:
        List of 4 Cultists
    """
    return [
        Cultist(name="Cultist 1"),
        Cultist(name="Cultist 2"),
        Cultist(name="Cultist 3"),
        Cultist(name="Cultist 4"),
    ]


def create_hound_pack() -> List[Enemy]:
    """
    Create a pack of 3 Hounds (harder encounter).

    Returns:
        List of 3 Hounds
    """
    return [
        HoundOfTindalos(name="Hound 1"),
        HoundOfTindalos(name="Hound 2"),
        HoundOfTindalos(name="Hound 3"),
    ]
