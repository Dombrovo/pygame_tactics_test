"""
Equipment system for investigators and enemies.

This module defines the equipment system including:
- Base Equipment class (for all equippable items)
- Weapon class (with damage, range, accuracy modifiers)
- Armor class (Phase 2+ - for protective gear)
- Accessory class (Phase 2+ - for utility items)

Phase 1 MVP focuses on weapons only.
Phase 2+ will add armor, accessories, and equipment crafting.
"""

from typing import Optional, Literal


class Equipment:
    """
    Base class for all equippable items.

    This is the parent class for Weapon, Armor, and Accessory.
    Provides common attributes like name, description, and slot type.
    """

    def __init__(
        self,
        name: str,
        description: str,
        slot: Literal["weapon", "armor", "accessory"],
        icon: str = "?"
    ):
        """
        Initialize equipment item.

        Args:
            name: Item name (e.g., "Revolver", "Kevlar Vest")
            description: Flavor text describing the item
            slot: Equipment slot type ("weapon", "armor", "accessory")
            icon: Unicode symbol for UI display (optional)
        """
        self.name = name
        self.description = description
        self.slot = slot
        self.icon = icon

    def get_info_text(self) -> str:
        """
        Get formatted info string for UI display.

        Returns:
            Multi-line string with equipment stats
        """
        return f"{self.icon} {self.name}\n{self.description}"

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"{self.__class__.__name__}('{self.name}')"


class Weapon(Equipment):
    """
    Weapon equipment - guns, melee weapons, eldritch artifacts.

    Weapons determine:
    - Attack damage (health damage dealt)
    - Attack range (tiles)
    - Attack type (melee vs ranged)
    - Accuracy modifier (bonus/penalty to hit chance)
    - Sanity damage (for eldritch weapons)

    Examples:
    - Revolver: 5 damage, 3 range, ranged
    - Shotgun: 7 damage, 2 range, ranged, -10% accuracy
    - Combat Knife: 4 damage, 1 range, melee
    - Blessed Blade: 6 damage, 1 range, melee, 3 sanity damage vs eldritch
    """

    def __init__(
        self,
        name: str,
        description: str,
        damage: int,
        weapon_range: int,
        attack_type: Literal["melee", "ranged"],
        accuracy_modifier: int = 0,
        sanity_damage: int = 0,
        icon: str = "🔫"
    ):
        """
        Initialize a weapon.

        Args:
            name: Weapon name (e.g., "Revolver", "Tommy Gun")
            description: Flavor text
            damage: Health damage dealt on hit
            weapon_range: Attack range in tiles
            attack_type: "melee" or "ranged"
            accuracy_modifier: Bonus/penalty to hit chance (default 0)
            sanity_damage: Sanity damage on hit (default 0, for eldritch weapons)
            icon: Unicode symbol (default gun emoji)
        """
        super().__init__(name, description, slot="weapon", icon=icon)

        self.damage = damage
        self.weapon_range = weapon_range
        self.attack_type = attack_type
        self.accuracy_modifier = accuracy_modifier
        self.sanity_damage = sanity_damage

    def get_info_text(self) -> str:
        """
        Get formatted info string for UI display.

        Returns:
            Multi-line string with weapon stats
        """
        lines = [
            f"{self.icon} {self.name}",
            f"Damage: {self.damage}",
            f"Range: {self.weapon_range} tiles",
            f"Type: {self.attack_type.capitalize()}",
        ]

        if self.accuracy_modifier != 0:
            sign = "+" if self.accuracy_modifier > 0 else ""
            lines.append(f"Accuracy: {sign}{self.accuracy_modifier}%")

        if self.sanity_damage > 0:
            lines.append(f"Sanity Damage: {self.sanity_damage}")

        return "\n".join(lines)


class Armor(Equipment):
    """
    Armor equipment - protective gear (Phase 2+).

    NOT IMPLEMENTED IN MVP - Placeholder for Phase 2.

    Will provide:
    - Health bonus
    - Damage reduction
    - Movement penalty (heavy armor)
    """

    def __init__(
        self,
        name: str,
        description: str,
        health_bonus: int = 0,
        damage_reduction: int = 0,
        movement_penalty: int = 0,
        icon: str = "🛡️"
    ):
        """Initialize armor (Phase 2+ feature)."""
        super().__init__(name, description, slot="armor", icon=icon)
        self.health_bonus = health_bonus
        self.damage_reduction = damage_reduction
        self.movement_penalty = movement_penalty


class Accessory(Equipment):
    """
    Accessory equipment - utility items (Phase 2+).

    NOT IMPLEMENTED IN MVP - Placeholder for Phase 2.

    Examples:
    - First Aid Kit (heal action)
    - Elder Sign (sanity protection)
    - Night Vision Goggles (see in darkness)
    """

    def __init__(
        self,
        name: str,
        description: str,
        stat_modifiers: dict = None,
        icon: str = "📿"
    ):
        """Initialize accessory (Phase 2+ feature)."""
        super().__init__(name, description, slot="accessory", icon=icon)
        self.stat_modifiers = stat_modifiers or {}


# ============================================================================
# WEAPON LIBRARY - Pre-defined weapons for MVP
# ============================================================================

# --- INVESTIGATOR WEAPONS (Player Equipment) ---

# Ranged Weapons

REVOLVER = Weapon(
    name="Revolver",
    description="Standard .38 caliber sidearm. Reliable and accurate.",
    damage=5,
    weapon_range=3,
    attack_type="ranged",
    accuracy_modifier=0,
    icon="🔫"
)

RIFLE = Weapon(
    name="Hunting Rifle",
    description="Long-range rifle with excellent accuracy.",
    damage=6,
    weapon_range=5,
    attack_type="ranged",
    accuracy_modifier=10,  # +10% accuracy (scoped)
    icon="🔫"
)

SHOTGUN = Weapon(
    name="Shotgun",
    description="Devastating at close range, inaccurate at distance.",
    damage=8,
    weapon_range=2,
    attack_type="ranged",
    accuracy_modifier=-10,  # -10% accuracy (spread)
    icon="🔫"
)

TOMMY_GUN = Weapon(
    name="Tommy Gun",
    description="Submachine gun with high fire rate. Spray and pray.",
    damage=4,
    weapon_range=3,
    attack_type="ranged",
    accuracy_modifier=-5,  # -5% accuracy (recoil)
    icon="🔫"
)

# Melee Weapons

COMBAT_KNIFE = Weapon(
    name="Combat Knife",
    description="Military-grade blade for close quarters.",
    damage=4,
    weapon_range=1,
    attack_type="melee",
    accuracy_modifier=5,  # +5% accuracy (easy to hit in melee)
    icon="🔪"
)

FIRE_AXE = Weapon(
    name="Fire Axe",
    description="Heavy axe. Slow but devastating.",
    damage=7,
    weapon_range=1,
    attack_type="melee",
    accuracy_modifier=-5,  # -5% accuracy (unwieldy)
    icon="🪓"
)

CROWBAR = Weapon(
    name="Crowbar",
    description="Improvised weapon. Better than nothing.",
    damage=3,
    weapon_range=1,
    attack_type="melee",
    accuracy_modifier=0,
    icon="🔧"
)

# Eldritch Weapons (Phase 2+ - blessed or cursed)

BLESSED_BLADE = Weapon(
    name="Blessed Blade",
    description="Silver dagger inscribed with protective wards.",
    damage=5,
    weapon_range=1,
    attack_type="melee",
    accuracy_modifier=0,
    sanity_damage=3,  # Extra damage vs eldritch enemies
    icon="🗡️"
)

ELDER_SIGN_AMULET = Weapon(
    name="Elder Sign Amulet",
    description="Cursed artifact that channels eldritch power.",
    damage=3,
    weapon_range=4,
    attack_type="ranged",
    accuracy_modifier=-10,  # Hard to control
    sanity_damage=5,  # High sanity damage
    icon="📿"
)

# --- ENEMY WEAPONS (NPC Equipment) ---

CULTIST_PISTOL = Weapon(
    name="Cultist Pistol",
    description="Cheap handgun used by cultists.",
    damage=4,
    weapon_range=3,
    attack_type="ranged",
    accuracy_modifier=-5,  # Poor quality
    icon="🔫"
)

HOUND_CLAWS = Weapon(
    name="Eldritch Claws",
    description="Razor-sharp claws that tear through reality.",
    damage=6,
    weapon_range=1,
    attack_type="melee",
    accuracy_modifier=10,  # Very accurate in melee
    sanity_damage=5,  # Terrifying up close
    icon="🐺"
)

TENTACLE_STRIKE = Weapon(
    name="Tentacle Strike",
    description="Writhing appendage from beyond.",
    damage=5,
    weapon_range=2,  # Reach weapon
    attack_type="melee",
    accuracy_modifier=0,
    sanity_damage=4,
    icon="🦑"
)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_default_investigator_weapon() -> Weapon:
    """
    Get the default starting weapon for investigators.

    MVP uses Revolver as standard issue.
    Phase 2+ will allow choosing starting equipment.

    Returns:
        Weapon object (Revolver)
    """
    return REVOLVER


def get_weapon_by_name(name: str) -> Optional[Weapon]:
    """
    Get weapon by name from the weapon library.

    Args:
        name: Weapon name (case-insensitive)

    Returns:
        Weapon object or None if not found

    Example:
        >>> weapon = get_weapon_by_name("Shotgun")
        >>> print(weapon.damage)  # 8
    """
    # Dictionary of all available weapons
    weapon_library = {
        "revolver": REVOLVER,
        "rifle": RIFLE,
        "hunting rifle": RIFLE,
        "shotgun": SHOTGUN,
        "tommy gun": TOMMY_GUN,
        "combat knife": COMBAT_KNIFE,
        "knife": COMBAT_KNIFE,
        "fire axe": FIRE_AXE,
        "axe": FIRE_AXE,
        "crowbar": CROWBAR,
        "blessed blade": BLESSED_BLADE,
        "elder sign amulet": ELDER_SIGN_AMULET,
        "cultist pistol": CULTIST_PISTOL,
        "hound claws": HOUND_CLAWS,
        "eldritch claws": HOUND_CLAWS,
        "tentacle strike": TENTACLE_STRIKE,
    }

    return weapon_library.get(name.lower())


def get_all_investigator_weapons() -> list[Weapon]:
    """
    Get list of all weapons available to investigators.

    Returns:
        List of Weapon objects
    """
    return [
        REVOLVER,
        RIFLE,
        SHOTGUN,
        TOMMY_GUN,
        COMBAT_KNIFE,
        FIRE_AXE,
        CROWBAR,
        BLESSED_BLADE,
        ELDER_SIGN_AMULET,
    ]


def get_all_enemy_weapons() -> list[Weapon]:
    """
    Get list of all weapons used by enemies.

    Returns:
        List of Weapon objects
    """
    return [
        CULTIST_PISTOL,
        HOUND_CLAWS,
        TENTACLE_STRIKE,
    ]
