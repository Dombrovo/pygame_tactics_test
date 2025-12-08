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

    """

    def __init__(
        self,
        name: str,
        max_health: int,
        max_sanity: int,
        accuracy: int,
        will: int,
        movement_range: int,
        symbol: str
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


    def get_info_text(self) -> str:
        """
        Get formatted info string for UI display.

        Returns:
            Multi-line string with enemy stats
        """
        lines = [
            f"{self.symbol} {self.name}",
            f"HP: {self.current_health}/{self.max_health}",
        ]

        # Show weapon info if equipped
        if self.equipped_weapon:
            lines.append(f"Range: {self.equipped_weapon.weapon_range} tiles")
            lines.append(f"Attack: {self.equipped_weapon.attack_type}")

            if self.equipped_weapon.sanity_damage > 0:
                lines.append(f"[!] Sanity Dmg: {self.equipped_weapon.sanity_damage}")

        if self.is_incapacitated:
            lines.append("[X] DEFEATED")

        return "\n".join(lines)


class Cultist(Enemy):
    """
    Cultist - Ranged human enemy
    Cultists are weak and attack from range with firearms
    Stats:
    - Medium health (10 health) 
    - Ranged attack (3 tile range)
    - No sanity damage (just guns)
    - Moderate accuracy (60 base accuracy)
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
            symbol="🔫"           # Gun symbol
        )

        # Equip weapon (uses equipment system - weapon provides range/attack type/damage)
        self.equip_weapon(equipment.CULTIST_PISTOL)

    def __repr__(self) -> str:
        """String representation for debugging."""
        status = " [DEFEATED]" if self.is_incapacitated else ""
        return f"Cultist '{self.name}': {self.current_health}/{self.max_health} HP{status}"


class HoundOfTindalos(Enemy):
    """
    Hound of Tindalos - Fast melee horror
    Interdimensional predators that hunt through angles of time
    Stats:
    - Low health (7 Health)
    - Very fast movement (6 movement_range)
    - Melee only (1 tile range)
    - Causes sanity damage (5 sanity_damage)
    - High accuracy (75 base accuracy)
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
            symbol="🐺"           # Wolf symbol
        )

        # Equip weapon (uses equipment system - weapon provides range/attack type/sanity damage)
        self.equip_weapon(equipment.HOUND_CLAWS)

    def __repr__(self) -> str:
        """String representation for debugging."""
        status = " [BANISHED]" if self.is_incapacitated else ""
        return f"Hound '{self.name}': {self.current_health}/{self.max_health} HP{status}"


def create_test_enemies() -> List[Enemy]:
    """
    Create a test group of enemies for MVP testing.

    Randomly selects between 4 squad types:
    - Balanced: 2 Cultists + 2 Hounds
    - Cultist squad: 4 Cultists (easier)
    - Hound pack: 3 Hounds (harder)
    - Mixed: 3 Cultists + 1 Hound

    Returns:
        List of enemies (3-4 depending on squad type)
    """
    import random
    # Store function references (not calling them yet)
    enemy_squad_choices = {
        'balanced': create_balanced_squad,
        'cultist': create_cultist_squad,
        'hounds': create_hound_pack,
        'cultists_with_hound': create_cultists_with_hound_pack
    }
    # Pick a random squad type and call the function
    enemy_squad = random.choice(list(enemy_squad_choices.keys()))
    return enemy_squad_choices[enemy_squad]()


def create_balanced_squad() -> List[Enemy]:
    """
    Create a squad of 4 Cultists (easier encounter).

    Returns:
        List of 4 Cultists
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
    enemies = [
        Cultist(name="Cultist Alpha"),
        Cultist(name="Cultist Beta"),
        Cultist(name="Cultist Charlie"),
        Cultist(name="Cultist Delta"),
    ]

    return enemies


def create_hound_pack() -> List[Enemy]:
    """
    Create a pack of 3 Hounds (harder encounter).

    Returns:
        List of 3 Hounds
    """
    enemies = [
        HoundOfTindalos(name="Hound Alpha"),
        HoundOfTindalos(name="Hound Beta"),
        HoundOfTindalos(name="Hound Charlie"),
    ]
    return enemies


def create_cultists_with_hound_pack() -> List[Enemy]:
    """
    Create a pack of 3 Hounds (harder encounter).

    Returns:
        List of 3 Hounds
    """
    enemies = [
        Cultist(name="Cultist Alpha"),
        Cultist(name="Cultist Beta"),
        Cultist(name="Cultist Charlie"),
        HoundOfTindalos(name="Hound Alpha"),
    ]
    return enemies
