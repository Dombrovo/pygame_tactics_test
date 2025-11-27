# Grid and Battle System Deep Dive

This guide explains the tactical battle system, including the grid, entities, and battle screen.

## Overview

The battle system consists of three main components:

1. **Grid System** (`combat/grid.py`) - The 10x10 battlefield
2. **Entity System** (`entities/`) - Units, investigators, and enemies
3. **Battle Screen** (`combat/battle_screen.py`) - Battle UI and game loop

---

## Grid System

### Tile Class

Each tile on the 10x10 grid represents a single battlefield position.

```python
class Tile:
    def __init__(self, x: int, y: int, terrain_type: str = "empty"):
        self.x = x  # Grid X coordinate (0-9)
        self.y = y  # Grid Y coordinate (0-9)
        self.terrain_type = terrain_type  # "empty", "half_cover", "full_cover"
        self.occupied_by = None  # Unit on this tile (or None)
```

**Terrain Types**:
- **empty**: No cover, no bonuses
- **half_cover** (▪️): -20% hit chance for attackers, doesn't block line of sight
- **full_cover** (⬛): -40% hit chance for attackers, blocks line of sight

**Key Methods**:
- `is_occupied()` - Check if tile has a unit
- `can_move_through()` - Check if units can pass through
- `get_position()` - Get (x, y) coordinates as tuple

### Grid Class

The Grid manages all 100 tiles and provides battlefield operations.

```python
class Grid:
    def __init__(self, size: int = 10):
        self.size = size
        self.tiles = []  # 2D array: tiles[y][x]

        # Create 10x10 grid of empty tiles
        for y in range(size):
            row = []
            for x in range(size):
                row.append(Tile(x, y, "empty"))
            self.tiles.append(row)
```

**Accessing Tiles**:
```python
# Get tile at position (x, y)
tile = grid.get_tile(3, 5)

# Check if position is valid
if grid.is_valid_position(x, y):
    # Position is within 0-9 range
```

**Unit Placement**:
```python
# Place a unit on the grid
grid.place_unit(investigator, x=2, y=4)

# Move a unit
grid.move_unit(from_x=2, from_y=4, to_x=3, to_y=4)

# Remove a unit
grid.remove_unit(x=3, y=4)
```

**Distance Calculations**:
```python
# Euclidean distance (allows diagonal movement)
distance = grid.get_distance(x1, y1, x2, y2)
# Examples:
#   Adjacent orthogonal: 1.0
#   Adjacent diagonal: 1.414 (~√2)
#   3 tiles horizontally: 3.0

# Manhattan distance (only orthogonal)
distance = grid.get_manhattan_distance(x1, y1, x2, y2)
# Examples:
#   Adjacent orthogonal: 1
#   Adjacent diagonal: 2
#   3 tiles horizontally: 3
```

**Finding Neighbors**:
```python
# Get all adjacent tiles (including diagonal)
neighbors = grid.get_neighbors(x=5, y=5, diagonal=True)
# Returns: [(4,5), (6,5), (5,4), (5,6), (4,4), (4,6), (6,4), (6,6)]

# Get only orthogonal neighbors
neighbors = grid.get_neighbors(x=5, y=5, diagonal=False)
# Returns: [(4,5), (6,5), (5,4), (5,6)]
```

---

## Entity System

### Base Unit Class

All units (investigators and enemies) inherit from the Unit class.

```python
class Unit:
    def __init__(self, name, max_health, max_sanity, accuracy,
                 will, movement_range, team, symbol):
        # Identity
        self.name = "John Carter"
        self.team = "player"  # or "enemy"
        self.symbol = "👤"

        # Position
        self.position = (2, 4)  # (x, y) or None

        # Resources
        self.max_health = 15
        self.current_health = 15
        self.max_sanity = 10
        self.current_sanity = 10

        # Stats
        self.accuracy = 75      # Base hit chance %
        self.will = 5           # Sanity defense
        self.movement_range = 4 # Tiles per turn

        # Status
        self.is_incapacitated = False
        self.has_moved = False
        self.has_attacked = False
```

**Damage System**:
```python
# Apply health damage
actual_damage = unit.take_damage(5)
# If unit has 10/15 HP, takes 5 damage → 5/15 HP
# If unit has 3/15 HP, takes 5 damage → 0/15 HP (incapacitated)

# Apply sanity damage (reduced by Will)
actual_damage = unit.take_sanity_damage(8)
# With will=5: 8 - 5 = 3 sanity damage
# Unit loses 3 sanity points
```

**Turn Management**:
```python
# At start of turn
unit.reset_turn_flags()
# Sets has_moved = False, has_attacked = False

# Check if unit can act
if unit.can_act():
    # Unit is not incapacitated

if unit.can_move():
    # Unit hasn't moved twice or attacked

if unit.can_attack():
    # Unit hasn't attacked yet
```

### Investigator Class

Player-controlled units with additional attributes for progression.

```python
class Investigator(Unit):
    def __init__(self, name, max_health=15, max_sanity=10,
                 accuracy=75, will=5, movement_range=4):
        super().__init__(name, max_health, max_sanity, accuracy,
                        will, movement_range, team="player", symbol="👤")

        # Progression (Phase 2+)
        self.experience = 0
        self.kills = 0
        self.missions_survived = 0

        # Traits (Phase 2+)
        self.traits = []
        self.permanent_injuries = []
        self.permanent_madness = []
```

**Test Squad**:
```python
from entities.investigator import create_test_squad

squad = create_test_squad()
# Returns list of 4 investigators:
# - John Carter (15 HP, 10 SAN, 75% acc)
# - Sarah Mitchell (12 HP, 12 SAN, 80% acc)
# - Marcus Stone (18 HP, 8 SAN, 70% acc)
# - Elena Ramirez (14 HP, 11 SAN, 75% acc)
```

### Enemy Classes

#### Cultist

Ranged human enemy with firearms.

```python
class Cultist(Enemy):
    # Stats:
    max_health = 10
    max_sanity = 8
    accuracy = 60
    movement_range = 4
    weapon_range = 3     # Can shoot 3 tiles away
    attack_type = "ranged"
    sanity_damage = 0    # Physical damage only
    symbol = "🔫"
```

#### Hound of Tindalos

Fast melee horror that causes sanity damage.

```python
class HoundOfTindalos(Enemy):
    # Stats:
    max_health = 8       # Low health (glass cannon)
    max_sanity = 15      # High sanity (eldritch)
    accuracy = 75        # High accuracy
    movement_range = 6   # VERY FAST
    weapon_range = 1     # Melee only (adjacent)
    attack_type = "melee"
    sanity_damage = 5    # Causes sanity loss!
    symbol = "🐺"
```

**Test Enemies**:
```python
from entities.enemy import create_test_enemies

enemies = create_test_enemies()
# Returns: [2 Cultists, 2 Hounds]

# Alternative generators:
cultist_squad = create_cultist_squad()  # 4 Cultists
hound_pack = create_hound_pack()        # 3 Hounds
```

---

## Battle Screen

The BattleScreen manages the tactical combat interface and game loop.

### Initialization

```python
class BattleScreen:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.running = True

        # Create grid
        self.grid = Grid(10)
        self.grid.setup_test_cover()

        # Create units
        self.player_units = create_test_squad()
        self.enemy_units = create_test_enemies()

        # Place units on grid
        self._setup_unit_positions()

        # Battle state
        self.current_phase = "player_turn"
        self.selected_unit = None
        self.turn_number = 1
```

### Unit Positioning

Units are placed automatically at battle start:

```python
# Investigators on left side (x=0-1)
Positions: (0,2), (1,2), (0,7), (1,7)

# Enemies on right side (x=8-9)
Positions: (9,2), (8,2), (9,7), (8,7)

# Example battlefield layout:
# 👤 .  .  .  ⬛ ⬛ .  .  🔫
# .  .  ▪️ .  .  .  .  ▪️ .
# 👤 .  .  .  .  .  .  .  🔫
# .  .  .  .  ⬛ ⬛ .  .  .
# .  .  .  .  .  .  .  .  .
# 👤 .  .  .  .  .  .  .  🐺
# .  .  ▪️ .  .  .  .  ▪️ .
# 👤 .  .  .  .  .  .  .  🐺
```

### Coordinate Conversion

The battle screen converts between pixel coordinates (mouse clicks) and grid coordinates.

```python
# Convert pixel position to grid coordinates
def _pixel_to_grid(self, pixel_pos):
    # Mouse clicked at (850, 300)
    # Grid is centered on screen
    # Returns (4, 2) if click was on tile at grid position 4,2

# Convert grid coordinates to pixel position
def _grid_to_pixel(self, grid_x, grid_y):
    # Grid position (5, 5)
    # Returns (940, 500) - top-left corner of that tile
```

### Input Handling

**Mouse Controls**:
```python
# Left click on grid
→ Selects player unit at that position
→ Shows unit stats in info panel

# Left click on empty tile (Phase 2)
→ Move selected unit there
→ Attack enemy there (if in range)
```

**Keyboard Controls**:
- **Tab**: Cycle through player units
- **Space**: End turn (switch player ↔ enemy phase)
- **ESC**: Return to main menu

### Turn System

```python
# Player turn
current_phase = "player_turn"
- Player selects units
- Player performs actions (future: move, attack)
- Player presses Space to end turn

# Enemy turn
current_phase = "enemy_turn"
- AI controls enemy units (future)
- Enemies move and attack (future)
- Automatically switches back to player turn

# Turn counter increments each cycle
turn_number += 1
```

### Rendering

The battle screen renders in layers:

**Layer 1: Grid**
```python
for y in range(10):
    for x in range(10):
        # Draw tile background (color based on terrain)
        # Draw grid lines
        # Draw cover symbols (⬛ ▪️)
```

**Layer 2: Units**
```python
for unit in all_units:
    # Draw unit symbol (👤 🔫 🐺)
    # Draw health bar (red)
    # Draw sanity bar (blue)
```

**Layer 3: Selection Highlight**
```python
if selected_unit:
    # Draw yellow border around selected unit's tile
```

**Layer 4: UI Overlay**
```python
# Top: Turn number and phase
# Right: Unit info panel
# Bottom: Controls help
```

### Win/Lose Conditions

Checked every frame in `update()`:

```python
def _check_win_lose(self):
    active_investigators = count_active(player_units)
    active_enemies = count_active(enemy_units)

    if active_enemies == 0:
        # VICTORY
        next_screen = "victory"

    elif active_investigators == 0:
        # DEFEAT
        next_screen = "defeat"
```

---

## Game Loop Flow

```
1. User clicks "New Game" on title screen
   ↓
2. main.py creates BattleScreen
   ↓
3. BattleScreen.__init__():
   - Creates grid with cover
   - Spawns 4 investigators
   - Spawns 4 enemies
   - Places units on grid
   ↓
4. BattleScreen.run(clock):
   while running:
       handle_events()  # Mouse clicks, keyboard
       update()         # Check win/lose
       draw()           # Render everything
       display.flip()   # Show frame
       clock.tick(60)   # 60 FPS
   ↓
5. Return to main.py with result ("victory", "defeat", "title")
```

---

## Current Limitations (To Be Implemented)

The battle system currently supports:
- ✅ Grid rendering
- ✅ Unit rendering and visualization
- ✅ Unit selection
- ✅ Turn tracking

**Not yet implemented**:
- ❌ Movement (clicking tile to move)
- ❌ Attacking (clicking enemy to attack)
- ❌ Line of sight calculations
- ❌ Hit chance display
- ❌ Damage resolution
- ❌ Enemy AI

These features will be added in the next development session.

---

## File Locations

- **Grid System**: `combat/grid.py` (370 lines)
- **Unit Base**: `entities/unit.py` (240 lines)
- **Investigators**: `entities/investigator.py` (170 lines)
- **Enemies**: `entities/enemy.py` (220 lines)
- **Battle Screen**: `combat/battle_screen.py` (500 lines)

---

## Next Steps

See [Next Session: Combat Mechanics](../Claude.md#next-session-combat-mechanics) for:
1. Pathfinding (A* algorithm for movement)
2. Line of sight (Bresenham's line algorithm)
3. Combat resolution (hit chance, damage)
4. Attack actions (ranged and melee)
5. Enemy AI (basic behavior)

---

## Summary

The battle system provides:
- **10x10 grid** with cover system
- **Dual resource units** (health + sanity)
- **Two enemy types** with different behaviors
- **Turn-based gameplay** (player/enemy phases)
- **Visual feedback** (health bars, selection, unit info)

This foundation enables the next phase: adding movement, attacks, and AI to make the battle fully playable!
