# Stat System with Modifiers

**File**: `entities/unit.py`
**Status**: ✅ Complete (Phase 1)
**Last Updated**: 2025-11-27

---

## Overview

The **Stat System** provides a flexible framework for managing unit statistics that can be modified by backgrounds, traits, equipment, and status effects. It uses a **base + modifiers pattern** where stats are calculated dynamically.

### Key Concepts

1. **Base Stats**: Original stat values set at character creation (never change)
2. **Modifiers**: Adjustments from backgrounds, traits, equipment, injuries, etc.
3. **Effective Stats**: Calculated values (base + modifiers) used in gameplay
4. **Properties**: Auto-calculated stats using Python `@property` decorators

---

## Architecture

### Base Stats (Immutable)

Stored as `base_*` attributes on the `Unit` class:

```python
self.base_max_health = 15       # Starting max HP
self.base_max_sanity = 10       # Starting max sanity
self.base_accuracy = 75         # Starting hit chance %
self.base_will = 5              # Starting sanity defense
self.base_movement_range = 4    # Starting movement tiles
```

### Modifiers (Mutable)

Stored as separate `*_modifier` attributes:

```python
self.max_health_modifier = 0    # +/- HP adjustment
self.max_sanity_modifier = 0    # +/- sanity adjustment
self.accuracy_modifier = 0      # +/- accuracy adjustment
self.will_modifier = 0          # +/- will adjustment
self.movement_modifier = 0      # +/- movement adjustment
```

### Effective Stats (Calculated)

Accessed via `@property` decorators that compute `base + modifiers`:

```python
@property
def max_health(self) -> int:
    """Effective max health = base + modifiers"""
    return max(1, self.base_max_health + self.max_health_modifier)

@property
def accuracy(self) -> int:
    """Effective accuracy = base + modifiers (clamped 5-95%)"""
    return max(5, min(95, self.base_accuracy + self.accuracy_modifier))
```

---

## Stat Clamping Rules

All effective stats are automatically clamped to valid ranges:

| Stat | Minimum | Maximum | Notes |
|------|---------|---------|-------|
| `max_health` | 1 | None | Can't have 0 or negative HP |
| `max_sanity` | 1 | None | Can't have 0 or negative sanity |
| `accuracy` | 5% | 95% | Never guaranteed hit/miss |
| `will` | 0 | None | Can be reduced to 0 |
| `movement_range` | 1 | None | Must move at least 1 tile |

**Why clamping?**
- Prevents game-breaking stats (100% accuracy, 0 HP)
- Maintains tactical depth (always 5% miss chance)
- Avoids division by zero errors

---

## Usage Examples

### Creating a Unit with Base Stats

```python
from entities.investigator import Investigator

# Create investigator with base stats
inv = Investigator(
    name="John Carter",
    max_health=15,
    max_sanity=10,
    accuracy=75,
    will=5,
    movement_range=4,
    gender="male"
)

# Access stats (returns base values initially)
print(inv.max_health)    # 15
print(inv.accuracy)      # 75
```

### Applying Modifiers

#### Method 1: Using `apply_stat_modifiers()` (Recommended)

```python
# Apply a "Soldier" background
inv.apply_stat_modifiers(accuracy=10, max_sanity=-1)

# Stats are now modified
print(inv.accuracy)      # 85 (75 base + 10 modifier)
print(inv.max_sanity)    # 9 (10 base - 1 modifier)
```

#### Method 2: Direct Modification

```python
# Manually adjust modifiers
inv.accuracy_modifier += 10
inv.max_sanity_modifier -= 1

# Same result as Method 1
print(inv.accuracy)      # 85
print(inv.max_sanity)    # 9
```

### Stacking Multiple Modifiers

```python
# Apply background
inv.apply_stat_modifiers(accuracy=10, max_sanity=-1)

# Apply trait
inv.apply_stat_modifiers(will=2, movement=1)

# Apply injury
inv.apply_stat_modifiers(max_health=-2, movement=-1)

# All modifiers stack!
print(f"Accuracy: {inv.base_accuracy} + {inv.accuracy_modifier} = {inv.accuracy}")
# Output: "Accuracy: 75 + 10 = 85"

print(f"Movement: {inv.base_movement_range} + {inv.movement_modifier} = {inv.movement_range}")
# Output: "Movement: 4 + 0 = 4" (1 from trait, -1 from injury = 0)
```

### Checking for Modifiers

```python
# Check if unit has any active modifiers
if inv.has_modifiers():
    print("This unit has stat modifications")
```

---

## Implementation in Phase 2+

### Background System

```python
# Define background modifiers
BACKGROUNDS = {
    "Soldier": {
        "accuracy": 10,
        "max_sanity": -1
    },
    "Scholar": {
        "will": 2,
        "max_health": -2
    },
    "Athlete": {
        "movement": 1,
        "max_health": 2
    },
    "Detective": {
        "will": 1,
        "accuracy": 5
    }
}

# Apply to investigator
def apply_background(inv: Investigator, background: str):
    inv.background = background
    inv.apply_stat_modifiers(**BACKGROUNDS[background])
```

### Trait System

```python
# Traits with stat effects
TRAITS = {
    "Veteran": {"accuracy": 5, "will": 1},
    "Alcoholic": {"accuracy": -5, "max_health": 2},
    "Paranoid": {"will": 2, "movement": -1},
    "Brave": {"max_sanity": 2, "accuracy": -5}
}

# Apply trait
def add_trait(inv: Investigator, trait: str):
    inv.traits.append(trait)
    inv.apply_stat_modifiers(**TRAITS[trait])
```

### Injury System

```python
INJURIES = {
    "Leg Wound": {"movement": -1, "max_health": -2},
    "Shell Shocked": {"will": -2, "max_sanity": -2},
    "Broken Arm": {"accuracy": -10},
    "Concussion": {"will": -1, "accuracy": -5}
}

def apply_injury(inv: Investigator, injury: str):
    inv.permanent_injuries.append(injury)
    inv.apply_stat_modifiers(**INJURIES[injury])
```

### Equipment System

```python
# Equipment bonuses
EQUIPMENT = {
    "Body Armor": {"max_health": 3, "movement": -1},
    "Blessed Amulet": {"will": 2},
    "Scoped Rifle": {"accuracy": 10},
    "Lightweight Boots": {"movement": 1}
}

def equip_item(inv: Investigator, item: str):
    inv.equipment.append(item)
    inv.apply_stat_modifiers(**EQUIPMENT[item])
```

---

## API Reference

### Unit Class Methods

#### `apply_stat_modifiers(**modifiers)`

Apply stat modifiers to the unit.

**Parameters:**
- `max_health` (int, optional): HP modifier
- `max_sanity` (int, optional): Sanity modifier
- `accuracy` (int, optional): Accuracy modifier
- `will` (int, optional): Will modifier
- `movement` or `movement_range` (int, optional): Movement modifier

**Returns:** None

**Example:**
```python
unit.apply_stat_modifiers(accuracy=10, max_sanity=-1)
```

#### `has_modifiers()`

Check if unit has any active stat modifiers.

**Returns:** `bool` - True if any modifier is non-zero

**Example:**
```python
if unit.has_modifiers():
    print("Modified stats detected!")
```

### Properties

All stats are accessed as properties (read-only):

```python
unit.max_health       # int: Effective max HP
unit.max_sanity       # int: Effective max sanity
unit.accuracy         # int: Effective accuracy (5-95)
unit.will             # int: Effective will (min 0)
unit.movement_range   # int: Effective movement (min 1)
```

### Base Stats and Modifiers

Access underlying values directly:

```python
# Base stats (read/write)
unit.base_max_health
unit.base_max_sanity
unit.base_accuracy
unit.base_will
unit.base_movement_range

# Modifiers (read/write)
unit.max_health_modifier
unit.max_sanity_modifier
unit.accuracy_modifier
unit.will_modifier
unit.movement_modifier
```

---

## Testing

### Test Script: `testing/test_stat_system.py`

Run comprehensive stat system tests:

```bash
uv run python testing/test_stat_system.py
```

**Tests:**
1. Base stat initialization
2. Modifier application
3. Modifier stacking
4. Negative modifiers (injuries)
5. Stat clamping (min/max enforcement)
6. Property calculations

**Sample Output:**
```
Ernest Sinclair (male)
Initial:     HP 15, SAN 10, ACC 75%, WILL 5, MOVE 4

After Soldier background (+10 acc, -1 san):
             HP 15, SAN 9,  ACC 85%, WILL 5, MOVE 4

After Veteran trait (+2 will, +1 move):
             HP 15, SAN 9,  ACC 85%, WILL 7, MOVE 5

After Leg Wound injury (-2 hp, -1 move):
             HP 13, SAN 9,  ACC 85%, WILL 7, MOVE 4
```

---

## Backwards Compatibility

✅ **All existing code remains functional!**

The stat system uses `@property` decorators, so code that accesses stats like:
- `unit.accuracy`
- `unit.max_health`
- `unit.movement_range`

...will automatically use the calculated effective stats. No changes needed to:
- Battle screen rendering (`combat/battle_screen.py`)
- Combat calculations (future)
- UI displays (`ui/`)

---

## Design Rationale

### Why Properties Instead of Methods?

```python
# ✅ Clean: Looks like attribute access
damage = unit.accuracy * 2

# ❌ Verbose: Requires method calls everywhere
damage = unit.get_accuracy() * 2
```

### Why Separate Base + Modifier?

1. **Transparency**: Always see original vs modified values
2. **Debugging**: Easy to track what changed a stat
3. **Reversibility**: Can remove modifiers (e.g., cure injury)
4. **UI Display**: Show "15 → 13 (-2)" instead of just "13"

### Why Auto-Clamping?

Prevents exploits and maintains game balance:
- Can't get 100% accuracy (always 5% miss chance)
- Can't reduce HP to 0 through modifiers (min 1)
- Can't become immobile (min 1 movement)

---

## Future Enhancements (Phase 2+)

### Temporary Buffs/Debuffs

```python
class TemporaryEffect:
    def __init__(self, modifiers, duration):
        self.modifiers = modifiers
        self.turns_remaining = duration

# Apply temporary buff
unit.temp_effects.append(TemporaryEffect({"accuracy": 20}, duration=3))
```

### Percentage Modifiers

```python
# Multiplicative modifiers (e.g., +10% to all stats)
unit.stat_multiplier = 1.1
```

### Conditional Modifiers

```python
# Accuracy bonus when in cover
@property
def accuracy(self) -> int:
    base = self.base_accuracy + self.accuracy_modifier
    if self.is_in_cover():
        base += 10
    return max(5, min(95, base))
```

---

## Related Documentation

- **[01_pygame_fundamentals.md](01_pygame_fundamentals.md)** - Pygame basics
- **[02_architecture_overview.md](02_architecture_overview.md)** - System structure
- **[05_grid_and_battle_system.md](05_grid_and_battle_system.md)** - Battle mechanics

---

## Summary

The stat system provides a **flexible, transparent, and type-safe** way to manage unit statistics with modifiers. It's ready for backgrounds, traits, equipment, and status effects in Phase 2+, while maintaining backwards compatibility with existing Phase 1 code.

**Key Benefits:**
- ✅ Easy to modify stats from any source
- ✅ Automatic clamping prevents invalid values
- ✅ Transparent (see base + modifiers separately)
- ✅ Backwards compatible with existing code
- ✅ Extensible for future features
