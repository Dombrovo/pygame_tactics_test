# Equipment & Inventory System

**Last Updated**: 2025-12-08 (Session 9)
**Status**: Implemented in Phase 1 MVP

---

## Table of Contents

1. [Overview](#overview)
2. [Equipment Framework](#equipment-framework)
3. [Weapon System](#weapon-system)
4. [Unit Integration](#unit-integration)
5. [Property Delegation](#property-delegation)
6. [Weapon Library](#weapon-library)
7. [Usage Examples](#usage-examples)
8. [Adding New Weapons](#adding-new-weapons)
9. [Testing](#testing)
10. [Future Expansion](#future-expansion)

---

## Overview

The equipment system provides a modular, extensible framework for equippable items including weapons, armor, and accessories. In Phase 1 MVP, the focus is on **weapons**, which determine unit attack capabilities.

### Key Features

- **Modular design** - Base `Equipment` class with specialized subclasses
- **Property delegation** - Unit stats automatically pull from equipped items
- **Weapon modifiers** - Accuracy bonuses/penalties based on weapon type
- **Dual damage types** - Health damage + sanity damage (for eldritch weapons)
- **Automatic assignment** - Units auto-equip appropriate weapons on creation
- **Unarmed fallback** - Units function without weapons (fists/improvised)

### File Location

**`entities/equipment.py`** (434 lines)

---

## Equipment Framework

### Base Equipment Class

All equippable items inherit from the `Equipment` base class:

```python
class Equipment:
    """Base class for all equippable items."""

    def __init__(
        self,
        name: str,
        description: str,
        slot: str,  # "weapon", "armor", "accessory"
        icon: str = "?"
    ):
        self.name = name
        self.description = description
        self.slot = slot
        self.icon = icon
```

**Purpose**: Provides common attributes for all equipment types.

**Attributes**:
- `name` - Display name (e.g., "Revolver", "Kevlar Vest")
- `description` - Flavor text
- `slot` - Equipment slot type
- `icon` - Unicode symbol for UI display

---

## Weapon System

### Weapon Class

Weapons extend `Equipment` with combat-specific attributes:

```python
class Weapon(Equipment):
    """Weapon equipment - determines attack capabilities."""

    def __init__(
        self,
        name: str,
        description: str,
        damage: int,                    # Health damage dealt
        weapon_range: int,              # Attack range in tiles
        attack_type: str,               # "melee" or "ranged"
        accuracy_modifier: int = 0,     # Bonus/penalty to hit chance
        sanity_damage: int = 0,         # Sanity damage (eldritch weapons)
        icon: str = "🔫"
    ):
        super().__init__(name, description, slot="weapon", icon=icon)
        self.damage = damage
        self.weapon_range = weapon_range
        self.attack_type = attack_type
        self.accuracy_modifier = accuracy_modifier
        self.sanity_damage = sanity_damage
```

### Weapon Attributes Explained

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `damage` | int | Health damage on hit | Revolver: 5, Shotgun: 8 |
| `weapon_range` | int | Attack range in tiles | Rifle: 5, Knife: 1 |
| `attack_type` | str | "melee" or "ranged" | Pistol: ranged, Axe: melee |
| `accuracy_modifier` | int | Accuracy bonus/penalty | Rifle: +10, Shotgun: -10 |
| `sanity_damage` | int | Sanity damage on hit | Hound Claws: 5, Revolver: 0 |

---

## Unit Integration

### Unit Class Updates

The `Unit` class has been updated to support equipment:

```python
class Unit:
    def __init__(self, ...):
        # ... existing attributes ...

        # Equipment system
        self.equipped_weapon: Optional[Weapon] = None
```

### Weapon Properties

Unit stats are calculated dynamically from equipped weapons using `@property` decorators:

```python
@property
def weapon_damage(self) -> int:
    """Damage dealt by attacks."""
    if self.equipped_weapon:
        return self.equipped_weapon.damage
    return 2  # Unarmed damage

@property
def weapon_range(self) -> int:
    """Attack range in tiles."""
    if self.equipped_weapon:
        return self.equipped_weapon.weapon_range
    return 1  # Unarmed range (melee only)

@property
def attack_type(self) -> str:
    """Attack type: 'melee' or 'ranged'."""
    if self.equipped_weapon:
        return self.equipped_weapon.attack_type
    return "melee"  # Unarmed is melee

@property
def weapon_sanity_damage(self) -> int:
    """Sanity damage dealt by attacks."""
    if self.equipped_weapon:
        return self.equipped_weapon.sanity_damage
    return 0  # Unarmed doesn't cause sanity damage
```

### Equipment Methods

```python
def equip_weapon(self, weapon: Weapon) -> None:
    """Equip a weapon (replaces current weapon)."""
    self.equipped_weapon = weapon

def unequip_weapon(self) -> Optional[Weapon]:
    """Remove current weapon (returns removed weapon)."""
    old_weapon = self.equipped_weapon
    self.equipped_weapon = None
    return old_weapon

def has_weapon(self) -> bool:
    """Check if unit has a weapon equipped."""
    return self.equipped_weapon is not None
```

---

## Property Delegation

### How It Works

The equipment system uses Python's `@property` decorator to create **computed attributes** that automatically pull values from equipped items.

**Without Weapon**:
```python
unit = Unit(name="Test", ...)
print(unit.weapon_damage)   # 2 (unarmed)
print(unit.weapon_range)    # 1 (melee only)
print(unit.attack_type)     # "melee"
```

**With Weapon**:
```python
unit.equip_weapon(RIFLE)
print(unit.weapon_damage)   # 6 (rifle damage)
print(unit.weapon_range)    # 5 (rifle range)
print(unit.attack_type)     # "ranged"
```

### Accuracy Integration

Weapon accuracy modifiers are **automatically applied** to the unit's total accuracy:

```python
@property
def accuracy(self) -> int:
    """Effective accuracy = base + modifiers + weapon modifier."""
    weapon_modifier = 0
    if self.equipped_weapon:
        weapon_modifier = self.equipped_weapon.accuracy_modifier

    total_accuracy = self.base_accuracy + self.accuracy_modifier + weapon_modifier
    return max(5, min(95, total_accuracy))  # Clamped 5-95%
```

**Example**:
```python
investigator.base_accuracy = 75
investigator.equip_weapon(RIFLE)  # +10% accuracy
print(investigator.accuracy)      # 85% (75 + 10)

investigator.equip_weapon(SHOTGUN)  # -10% accuracy
print(investigator.accuracy)        # 65% (75 - 10)
```

---

## Weapon Library

### Investigator Weapons (9 Total)

#### Ranged Weapons

| Weapon | Damage | Range | Accuracy | Description |
|--------|--------|-------|----------|-------------|
| **Revolver** | 5 | 3 | 0% | Standard .38 sidearm, reliable |
| **Rifle** | 6 | 5 | +10% | Long-range with scope, accurate |
| **Shotgun** | 8 | 2 | -10% | Devastating close-range, inaccurate |
| **Tommy Gun** | 4 | 3 | -5% | Submachine gun, spray and pray |

#### Melee Weapons

| Weapon | Damage | Range | Accuracy | Description |
|--------|--------|-------|----------|-------------|
| **Combat Knife** | 4 | 1 | +5% | Military blade, precise |
| **Fire Axe** | 7 | 1 | -5% | Heavy axe, slow but powerful |
| **Crowbar** | 3 | 1 | 0% | Improvised weapon |

#### Eldritch Weapons

| Weapon | Damage | Range | Accuracy | Sanity Dmg | Description |
|--------|--------|-------|----------|------------|-------------|
| **Blessed Blade** | 5 | 1 | 0% | 3 | Silver dagger with wards |
| **Elder Sign Amulet** | 3 | 4 | -10% | 5 | Cursed artifact, eldritch power |

### Enemy Weapons (3 Total)

| Weapon | Damage | Range | Accuracy | Sanity Dmg | User |
|--------|--------|-------|----------|------------|------|
| **Cultist Pistol** | 4 | 3 | -5% | 0 | Cultists |
| **Hound Claws** | 6 | 1 | +10% | 5 | Hound of Tindalos |
| **Tentacle Strike** | 5 | 2 | 0% | 4 | Future eldritch enemies |

### Accessing Weapons

```python
from entities import equipment

# Direct access
weapon = equipment.REVOLVER
weapon = equipment.SHOTGUN

# By name lookup (case-insensitive)
weapon = equipment.get_weapon_by_name("Rifle")
weapon = equipment.get_weapon_by_name("COMBAT KNIFE")

# Get all weapons
investigator_weapons = equipment.get_all_investigator_weapons()  # 9 weapons
enemy_weapons = equipment.get_all_enemy_weapons()  # 3 weapons
```

---

## Usage Examples

### Basic Weapon Equipping

```python
from entities.investigator import Investigator
from entities import equipment

# Create investigator
inv = Investigator(name="John Carter", accuracy=75)

# Equip rifle
inv.equip_weapon(equipment.RIFLE)
print(f"Damage: {inv.weapon_damage}")     # 6
print(f"Range: {inv.weapon_range}")       # 5
print(f"Accuracy: {inv.accuracy}%")       # 85% (75 + 10 rifle bonus)

# Switch to shotgun
inv.equip_weapon(equipment.SHOTGUN)
print(f"Damage: {inv.weapon_damage}")     # 8
print(f"Range: {inv.weapon_range}")       # 2
print(f"Accuracy: {inv.accuracy}%")       # 65% (75 - 10 shotgun penalty)

# Go unarmed
old_weapon = inv.unequip_weapon()
print(f"Removed: {old_weapon.name}")      # Shotgun
print(f"Damage: {inv.weapon_damage}")     # 2 (unarmed)
print(f"Has weapon: {inv.has_weapon()}")  # False
```

### Automatic Weapon Assignment

Investigators automatically equip weapons based on their role:

```python
from entities.investigator import create_test_squad

squad = create_test_squad()

# Squad composition:
# [0] Balanced -> Revolver (5 dmg, range 3)
# [1] Sniper   -> Rifle (6 dmg, range 5, +10% accuracy)
# [2] Tank     -> Shotgun (8 dmg, range 2, -10% accuracy)
# [3] Scout    -> Revolver (5 dmg, range 3)

sniper = squad[1]
print(sniper.equipped_weapon.name)  # "Hunting Rifle"
print(sniper.weapon_damage)         # 6
print(sniper.accuracy)              # 85% (75 base + 10 rifle)
```

### Enemy Weapons

```python
from entities.enemy import Cultist, HoundOfTindalos

cultist = Cultist()
print(cultist.equipped_weapon.name)      # "Cultist Pistol"
print(cultist.weapon_damage)             # 4
print(cultist.weapon_range)              # 3
print(cultist.attack_type)               # "ranged"

hound = HoundOfTindalos()
print(hound.equipped_weapon.name)        # "Eldritch Claws"
print(hound.weapon_damage)               # 6
print(hound.weapon_sanity_damage)        # 5 (terrifying!)
print(hound.attack_type)                 # "melee"
```

### Using in Combat Resolution (Future)

```python
def resolve_attack(attacker, target):
    # Get weapon stats from equipped weapon
    damage = attacker.weapon_damage
    range_limit = attacker.weapon_range
    attack_type = attacker.attack_type
    sanity_dmg = attacker.weapon_sanity_damage
    hit_chance = attacker.accuracy  # Includes weapon modifier

    # Calculate hit
    if is_hit(hit_chance):
        target.take_damage(damage)
        target.take_sanity_damage(sanity_dmg)
```

---

## Adding New Weapons

### Step 1: Define the Weapon

Add to `entities/equipment.py`:

```python
# In weapon library section

PLASMA_RIFLE = Weapon(
    name="Plasma Rifle",
    description="Experimental energy weapon from beyond.",
    damage=10,
    weapon_range=4,
    attack_type="ranged",
    accuracy_modifier=-15,  # Hard to control
    sanity_damage=2,        # Unnatural technology
    icon="⚡"
)
```

### Step 2: Add to Weapon Library Functions

```python
def get_weapon_by_name(name: str) -> Optional[Weapon]:
    weapon_library = {
        # ... existing weapons ...
        "plasma rifle": PLASMA_RIFLE,
    }
    return weapon_library.get(name.lower())

def get_all_investigator_weapons() -> list[Weapon]:
    return [
        # ... existing weapons ...
        PLASMA_RIFLE,
    ]
```

### Step 3: Use the New Weapon

```python
from entities import equipment

investigator.equip_weapon(equipment.PLASMA_RIFLE)
print(f"Damage: {investigator.weapon_damage}")  # 10
print(f"Sanity damage: {investigator.weapon_sanity_damage}")  # 2
```

---

## Testing

### Test Suite

**File**: `testing/test_equipment.py` (293 lines)

**Tests**:
1. Equipment creation and properties
2. Weapon equipping/unequipping
3. Weapon accuracy modifiers
4. Investigator default weapons
5. Enemy weapons
6. Sanity damage weapons
7. Weapon library functions

### Running Tests

```bash
uv run python testing/test_equipment.py
```

**Expected Output**:
```
============================================================
EQUIPMENT SYSTEM TEST SUITE
============================================================

=== Test: Equipment Creation ===
[OK] Equipment creation test passed

=== Test: Weapon Equipping ===
[OK] Weapon equipping test passed

... (all 7 tests)

============================================================
[OK] ALL EQUIPMENT TESTS PASSED
============================================================
```

---

## Future Expansion

### Phase 2+: Armor System

```python
class Armor(Equipment):
    """Armor equipment - protective gear."""

    def __init__(
        self,
        name: str,
        description: str,
        health_bonus: int = 0,
        damage_reduction: int = 0,
        movement_penalty: int = 0,
        icon: str = "🛡️"
    ):
        super().__init__(name, description, slot="armor", icon=icon)
        self.health_bonus = health_bonus
        self.damage_reduction = damage_reduction
        self.movement_penalty = movement_penalty
```

**Example Armor**:
- **Kevlar Vest** - +2 max HP, 1 damage reduction
- **Warded Coat** - +1 will, protects against sanity damage
- **Heavy Armor** - +5 max HP, 2 damage reduction, -1 movement

### Phase 2+: Accessories

```python
class Accessory(Equipment):
    """Accessory equipment - utility items."""

    def __init__(
        self,
        name: str,
        description: str,
        stat_modifiers: dict = None,
        icon: str = "📿"
    ):
        super().__init__(name, description, slot="accessory", icon=icon)
        self.stat_modifiers = stat_modifiers or {}
```

**Example Accessories**:
- **First Aid Kit** - Enables heal action
- **Elder Sign** - One-time sanity protection
- **Night Vision Goggles** - See in darkness
- **Lucky Charm** - +5% accuracy

### Equipment Slots

```python
class Unit:
    def __init__(self, ...):
        self.equipped_weapon: Optional[Weapon] = None      # ✅ IMPLEMENTED
        self.equipped_armor: Optional[Armor] = None        # Phase 2+
        self.equipped_accessories: list[Accessory] = []    # Phase 2+ (max 2)
```

---

## Design Philosophy

### Why Property Delegation?

**Advantages**:
1. **DRY** (Don't Repeat Yourself) - Stats defined once in weapon, used everywhere
2. **Automatic updates** - Change weapon, stats update immediately
3. **Type safety** - Properties enforce return types
4. **Extensibility** - Easy to add new weapon types

**Alternative (Not Used)**:
```python
# ❌ BAD - Manual stat copying
unit.damage = weapon.damage
unit.range = weapon.range
# Problem: Must manually update when weapon changes
```

### Unarmed Fallback

Units without weapons can still fight:
- **Damage**: 2 (fists, improvised weapons)
- **Range**: 1 (melee only)
- **Attack Type**: Melee

This ensures units are never completely helpless, even if disarmed.

---

**Version**: 1.0
**Status**: Complete
**Phase**: 1 MVP
**Created**: 2025-12-08
