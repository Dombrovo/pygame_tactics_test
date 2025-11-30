# Action Points System

**Version**: 2.2 (Session 7)
**Last Updated**: 2025-11-30

This document explains the action points system used in Eldritch Tactics for managing unit actions during combat.

---

## Table of Contents

1. [Overview](#overview)
2. [Design Philosophy](#design-philosophy)
3. [Implementation](#implementation)
4. [Unit Class Integration](#unit-class-integration)
5. [UI Components](#ui-components)
6. [Action Bar Integration](#action-bar-integration)
7. [Usage Examples](#usage-examples)
8. [Testing](#testing)

---

## Overview

The action points system gives each unit **2 action points per turn** that can be spent on various actions:

- **Move**: Costs 1 action point
- **Attack**: Costs 1 action point (when implemented)
- **Future abilities**: Will cost varying amounts

### Valid Action Combinations

With 2 action points, units can perform any of these combinations per turn:

1. **Move → Move**: Sprint across the battlefield (double movement)
2. **Move → Attack**: Reposition then shoot
3. **Attack → Move**: Shoot then retreat to cover
4. **Attack → Attack**: Double-tap (when implemented)

This flexible system replaced the old boolean flag approach (`has_moved`/`has_attacked`) which was more restrictive.

---

## Design Philosophy

### Why 2 Action Points?

**Tactical Flexibility**: Players can choose between:
- **Aggressive**: Attack twice for maximum damage
- **Mobile**: Move twice to reach distant positions
- **Balanced**: Move and attack in same turn

**Extensibility**: Future abilities can cost different amounts:
- Basic actions (Move, Attack): 1 AP
- Advanced abilities (Overwatch, Aimed Shot): 2 AP
- Quick actions (Reload, Use Item): 0 AP (future)

**Simplicity**: Easy to understand and visualize (2 circles = 2 actions)

### Advantages Over Boolean Flags

**Old System** (boolean flags):
```python
has_moved: bool
has_attacked: bool
# Complex logic: if attacked, can't move again; if moved twice, can't attack
```

**New System** (action points):
```python
current_action_points: int  # Simple: if AP >= cost, can do action
```

**Benefits**:
- ✅ Simpler logic (just check `current_action_points >= 1`)
- ✅ Easier to extend (new actions just consume AP)
- ✅ Clearer to players (see remaining actions at a glance)
- ✅ More flexible (any combination of actions works)

---

## Implementation

### Unit Class (entities/unit.py)

#### Core Attributes

```python
class Unit:
    def __init__(self, ...):
        # Action Points System (2 actions per turn)
        self.max_action_points = 2
        self.current_action_points = 2
```

#### Key Methods

**Consuming Action Points**:
```python
def consume_action_point(self, amount: int = 1) -> bool:
    """
    Consume action points when performing an action.

    Returns:
        True if action points were consumed, False if not enough available
    """
    if self.current_action_points >= amount:
        self.current_action_points -= amount
        return True
    return False
```

**Checking Available Actions**:
```python
def can_move(self) -> bool:
    """Check if unit can move (has at least 1 AP)."""
    return self.current_action_points >= 1

def can_attack(self) -> bool:
    """Check if unit can attack (has at least 1 AP)."""
    return self.current_action_points >= 1

def has_actions_remaining(self) -> bool:
    """Check if unit has any action points remaining."""
    return self.current_action_points > 0
```

**Resetting at Turn Start**:
```python
def reset_turn_flags(self):
    """Reset action points at the start of unit's turn."""
    self.current_action_points = self.max_action_points
```

---

## Unit Class Integration

### Turn Flow

1. **Turn Starts**: `reset_turn_flags()` called → `current_action_points = 2`
2. **Action Performed**: `consume_action_point(1)` called → `current_action_points = 1`
3. **Action Performed**: `consume_action_point(1)` called → `current_action_points = 0`
4. **Turn Ends**: Unit can no longer act (buttons disabled)

### Movement Integration

When a unit moves (in `battle_screen.py`):

```python
def _try_move_to_tile(self, target_x: int, target_y: int) -> bool:
    # Check if unit can still move
    if not self.current_turn_unit.can_move():
        print(f"Cannot move (no action points remaining)")
        return False

    # Execute movement
    if self.grid.move_unit(current_x, current_y, target_x, target_y):
        # Consume 1 action point for movement
        self.current_turn_unit.consume_action_point(1)

        # Update UI to reflect new action state
        self._update_action_bar()
        self._update_action_points_display()

        return True
```

---

## UI Components

### ActionPointsDisplay (ui/ui_elements.py)

A visual display showing remaining action points as circular indicators.

**Size**: 200×100px
**Position**: Bottom-left corner of battle screen

#### Visual Design

```
┌──────────┐
│ ACTIONS  │  ← Label
│  🟡 🟡   │  ← Circles (filled = available, hollow = used)
│   2/2    │  ← Counter
└──────────┘
```

**Color Coding**:
- **Available AP**: Golden filled circles with glow effect
- **Used AP**: Gray hollow circles
- **Text**: White label, golden counter

#### Implementation

```python
class ActionPointsDisplay:
    def __init__(self, x: int, y: int, width: int = 200, height: int = 100):
        self.rect = pygame.Rect(x, y, width, height)
        self.current_unit = None
        self.circle_radius = 18

    def update_for_unit(self, unit) -> None:
        """Update display for given unit (or None to clear)."""
        self.current_unit = unit

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the action points display."""
        # Draw background panel
        # Draw "ACTIONS" label
        # Draw action point circles (filled or hollow)
        # Draw "X/2" counter
```

#### Drawing Logic

For each action point (0 to `max_action_points`):

```python
for i in range(max_ap):
    is_available = i < current_ap

    if is_available:
        # Filled golden circle (available)
        pygame.draw.circle(screen, COLOR_TEXT_HIGHLIGHT, (x, y), radius)
        pygame.draw.circle(screen, LIGHTER_GOLD, (x, y), radius - 4)  # Glow
    else:
        # Hollow gray circle (used)
        pygame.draw.circle(screen, COLOR_TEXT_DIM, (x, y), radius, 3)
```

---

## Action Bar Integration

### Smart Button Enabling/Disabling

The action bar automatically enables/disables buttons based on action points:

```python
class ActionBar:
    def update_for_investigator(self, investigator) -> None:
        if investigator and not investigator.is_incapacitated:
            # Move button enabled only if can move
            self.action_buttons[0].enabled = investigator.can_move()

            # Attack button enabled only if can attack
            self.action_buttons[1].enabled = investigator.can_attack()
```

**Visual Feedback**:
- **Enabled buttons**: Bright colors, clickable
- **Disabled buttons**: Grayed out, not clickable
- Updates automatically after each action

---

## Usage Examples

### Example 1: Move Twice (Sprint)

```python
# Turn starts
unit.reset_turn_flags()  # current_action_points = 2

# First move
if unit.can_move():  # True (2 >= 1)
    unit.consume_action_point(1)  # current_action_points = 1
    # Move unit on grid

# Second move
if unit.can_move():  # True (1 >= 1)
    unit.consume_action_point(1)  # current_action_points = 0
    # Move unit on grid

# Try third action
if unit.can_move():  # False (0 < 1)
    # Action not allowed!
```

### Example 2: Move Then Attack

```python
# Turn starts
unit.reset_turn_flags()  # current_action_points = 2

# Move
if unit.can_move():  # True
    unit.consume_action_point(1)  # current_action_points = 1
    # Move unit

# Attack
if unit.can_attack():  # True (1 >= 1)
    unit.consume_action_point(1)  # current_action_points = 0
    # Execute attack

# No actions remaining
if unit.has_actions_remaining():  # False (0 <= 0)
    # Turn is effectively over
```

### Example 3: Attack Twice (Future)

```python
# Turn starts
unit.reset_turn_flags()  # current_action_points = 2

# First attack
if unit.can_attack():  # True
    unit.consume_action_point(1)  # current_action_points = 1
    # Execute attack

# Second attack
if unit.can_attack():  # True
    unit.consume_action_point(1)  # current_action_points = 0
    # Execute attack
```

---

## Testing

### Test Suite (testing/test_action_points.py)

Comprehensive tests verify all system behaviors:

#### Test 1: Initialization
```python
inv = Investigator(...)
assert inv.max_action_points == 2
assert inv.current_action_points == 2
```

#### Test 2: Can Move/Attack Checks
```python
assert inv.can_move() == True   # 2 AP available
assert inv.can_attack() == True
```

#### Test 3: Consuming Action Points
```python
inv.consume_action_point(1)  # Use 1 AP
assert inv.current_action_points == 1
assert inv.can_move() == True  # Can still move

inv.consume_action_point(1)  # Use 2nd AP
assert inv.current_action_points == 0
assert inv.can_move() == False  # No AP left
```

#### Test 4: Reset Turn Flags
```python
inv.consume_action_point(2)  # Use all AP
assert inv.current_action_points == 0

inv.reset_turn_flags()  # New turn
assert inv.current_action_points == 2
assert inv.can_move() == True
```

#### Test 5: Action Combinations
```python
# Test Move-Move, Move-Attack, Attack-Attack
# Verify all combinations work correctly
```

**All tests passing** with ASCII output for Windows compatibility.

---

## Future Enhancements

### Variable Action Point Costs

Different actions could cost different amounts:

```python
# Basic actions
MOVE_COST = 1
ATTACK_COST = 1

# Advanced abilities
OVERWATCH_COST = 2  # Costs full turn
AIMED_SHOT_COST = 2  # High-accuracy shot

# Quick actions
RELOAD_COST = 0  # Free action
USE_ITEM_COST = 0  # Free action
```

### Action Point Modifiers

Traits/equipment could modify max AP:

```python
class Investigator(Unit):
    def __init__(self):
        super().__init__()
        self.max_action_points = 2

        # Apply "Quick" trait: +1 AP per turn
        if self.has_trait("Quick"):
            self.max_action_points = 3
```

### Action Point Recovery

Special abilities could restore AP mid-turn:

```python
def use_adrenaline_shot(unit):
    """Restore 1 action point (once per battle)."""
    unit.current_action_points = min(
        unit.current_action_points + 1,
        unit.max_action_points
    )
```

---

## See Also

- **[06_stat_system.md](06_stat_system.md)** - Related stat modifier system
- **[05_grid_and_battle_system.md](05_grid_and_battle_system.md)** - How actions integrate with grid
- **[CLAUDE.md](../CLAUDE.md)** - Current project state

---

**Last Updated**: 2025-11-30 (Session 7)
**Status**: Fully implemented and tested
