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

        # Turn order (Session 5)
        all_units = self.player_units + self.enemy_units
        random.shuffle(all_units)
        self.turn_order = all_units
        self.current_turn_index = 0
        self.current_turn_unit = self.turn_order[0]

        # Battle state
        self.selected_unit = None  # Unit being viewed (not necessarily whose turn it is)
        self.round_number = 1  # Round = all units take one turn

        # Turn Order Tracker (Session 6)
        self.turn_order_tracker = TurnOrderTracker(
            x=(SCREEN_WIDTH - 1200) // 2,  # Centered
            y=10,  # Top of screen
            width=1200,
            height=70
        )
        self.turn_order_tracker.update_turn_order(
            self.turn_order,
            self.current_turn_index
        )

        # Adjust grid offset for turn order tracker
        self.grid_offset_y = 95  # Was 100, moved down for tracker
```

### Turn Order Tracker (Session 6)

The turn order tracker displays all units in their turn sequence at the top of the battle screen.

**Visual Layout**:
```
┌────────────────────────────────────────────────────────┐
│ TURN ORDER:                                            │
│ Player: Arthur Blackwood                               │
│ [Label]   [🖼️] [🔫] [🖼️] [🐺] [🖼️] [🔫] [🖼️] [🐺]     │
│  280px      ↑ Current turn (green border, 60×60px)     │
└────────────────────────────────────────────────────────┘
```

**Features**:
- **Unit icons** - Investigators show portrait images, enemies show emoji
- **Current turn highlight** - 4px green border on active unit
- **Turn info display** - "Player: Name" or "Enemy: Name" shown below label
- **Mini health bars** - 4px tall color-coded bars at bottom of each icon
- **Portrait caching** - Images loaded once and reused

**Integration**:
```python
# In update():
self.turn_order_tracker.update(mouse_pos)

# In draw():
self.turn_order_tracker.draw(screen)  # First, at top

# When turn advances:
self.turn_order_tracker.update_turn_order(
    self.turn_order,
    self.current_turn_index
)
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
# Left click on grid (any unit)
→ Selects ANY unit (player or enemy) to view stats
→ Shows unit stats in info panel (right side)
→ Works during both player and enemy turns

# Left click on investigator tile
→ Selects that investigator for commands (player turn only)
→ Updates action bar with available actions

# Left click on action bar buttons
→ Executes selected action (Move, Attack, etc.)
→ Hotkeys 1-0 also work

# Left click on empty tile (Phase 2 - not yet implemented)
→ Move selected unit there
→ Attack enemy there (if in range)
```

**Selection Behavior**:
- **Grid clicks** = View any unit's stats (intelligence gathering)
- **Investigator tiles** = Command player units (player turn only)
- **Action bar** = Only populates for player units (can't control enemies)

**Keyboard Controls**:
- **Tab**: Cycle through player units (command focus, not enemy units)
- **1-0**: Trigger action bar slots (hotkeys for abilities)
- **Space**: End Turn (advance to next unit in turn order)
- **ESC**: Return to main menu

### Turn System (Session 5: Individual Unit Turns)

**Turn Order Structure**:
- All units (players + enemies) shuffled into single queue
- Each unit takes their turn in order
- Round increments when all units have acted

```python
# Turn order initialization
all_units = player_units + enemy_units  # [4 investigators, 4 enemies]
random.shuffle(all_units)               # Random order
turn_order = all_units                  # [Unit1, Unit2, ..., Unit8]

# Example turn order (random):
# 1. Cultist Alpha (Enemy)
# 2. John Carter (Player)
# 3. Hound Beta (Enemy)
# 4. Sarah Mitchell (Player)
# 5. Cultist Beta (Enemy)
# 6. Marcus Stone (Player)
# 7. Hound Alpha (Enemy)
# 8. Elena Ramirez (Player)
# → Round 2 starts, back to Cultist Alpha

# Turn advancement
def _advance_turn():
    # Move to next unit in turn order
    current_turn_index = (current_turn_index + 1) % len(turn_order)
    current_turn_unit = turn_order[current_turn_index]

    # Skip incapacitated units
    while not current_turn_unit.can_act():
        current_turn_index = (current_turn_index + 1) % len(turn_order)
        current_turn_unit = turn_order[current_turn_index]

    # Check for round wrap
    if current_turn_index < previous_index:
        round_number += 1

    # Update action bar for current unit
    if current_turn_unit.team == "player":
        action_bar.update_for_investigator(current_turn_unit)
    else:
        action_bar.clear()
        # TODO: Execute enemy AI
```

**Turn Flow**:
1. Battle starts → Random turn order created → First unit's turn
2. Current turn unit highlighted in **green**
3. Player can view any unit (yellow highlight if different from current turn)
4. Action bar shows current turn unit's actions (if player unit)
5. Player clicks "End Turn" or presses Space
6. Next unit in order takes their turn
7. Enemy turns auto-skip (AI placeholder: immediately advances)
8. When all 8 units acted → Round increments → Wraps to first unit

**Visual Indicators**:
- 🟢 **Green highlight** = Current turn unit (can act now)
- 🟡 **Yellow highlight** = Selected for viewing (if different)
- **Header**: "ROUND X | Player/Enemy Turn: Unit Name"
- **End Turn button**: Right of action bar (150×70px)

### Rendering

The battle screen renders in layers with **emoji font support and color coding**:

**Font System**:
- Automatically detects and loads emoji-capable system fonts:
  - Windows: Segoe UI Emoji
  - macOS: Apple Color Emoji
  - Linux: Noto Color Emoji / Symbola
- Falls back to ASCII symbols if no emoji font available

**Layer 1: Grid**
```python
for y in range(10):
    for x in range(10):
        # Draw tile background (color based on terrain)
        # Draw grid lines
        # Draw cover symbols (⬛ ▪️ or ## ::)
```

**Layer 2: Units (with team color coding)**
```python
for unit in all_units:
    # Choose color: BLUE for player, RED for enemy
    if unit.team == "player":
        color = COLOR_PLAYER  # Blue
    else:
        color = COLOR_ENEMY   # Red

    # Draw unit symbol (👤 🔫 🐺 or [I] [C] [H])
    # Draw health bar (red)
    # Draw sanity bar (blue)
```

**Layer 3: Selection Highlights (Session 5: Dual Highlight System)**
```python
# Green highlight = Current turn unit (can act now)
if current_turn_unit and current_turn_unit.position:
    draw_highlight(current_turn_unit.position, color=COLOR_CURRENT_TURN)  # Green

# Yellow highlight = Selected for viewing (if different from current turn)
if selected_unit and selected_unit.position:
    if selected_unit != current_turn_unit:
        draw_highlight(selected_unit.position, color=COLOR_SELECTED)  # Yellow
```

**Layer 4: UI Overlay**
```python
# Top: Round number and current turn unit name
#      "ROUND 2 | Player Turn: Sarah Mitchell"
# Left: Investigator tiles panel (4 tiles stacked, 510×180px each)
# Right: Unit info panel (stats for selected/current unit)
# Bottom: Action bar (10 slots, centered, 790px wide)
#         End Turn button (right of action bar, 150×70px)
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
- ✅ Grid rendering with cover symbols
- ✅ Unit rendering with emoji font support
- ✅ Team color coding (blue vs red)
- ✅ ASCII fallback for systems without emoji fonts
- ✅ Unit selection (mouse click, Tab cycling)
- ✅ Enemy unit selection (click any unit to view stats for tactical intelligence)
- ✅ **Turn order system** (Session 5: individual unit turns, random order)
- ✅ **Dual highlight system** (Session 5: green=current turn, yellow=viewing)
- ✅ **End Turn button** (Session 5: advance to next unit)
- ✅ **Round tracking** (Session 5: full cycle through all units)
- ✅ Health/sanity bar visualization
- ✅ Investigator tiles panel (left side, 4 stacked tiles)
- ✅ Action bar (bottom center, 10 slots with hotkeys, tied to current turn unit)
- ✅ Synchronized selection (grid ↔ tiles ↔ Tab)
- ✅ Smart UI behavior (action bar shows current turn unit only)

**Implemented (Session 7)**:
- ✅ **Movement system** with A* pathfinding (`combat/pathfinding.py`)
- ✅ **Movement mode activation** (click Move button to show range)
- ✅ **Green tile highlighting** for valid destinations
- ✅ **Click-to-move** functionality
- ✅ **Path validation** with movement range limits
- ✅ **Flood-fill algorithm** for reachable tile calculation
- ✅ **Movement action tracking** (Move + Attack OR Move + Move)
- ✅ **Action bar callback system** (routes button clicks to actions)

**Not yet implemented**:
- ❌ Attacking (line of sight, hit chance, damage)
- ❌ Line of sight calculations (Bresenham's algorithm)
- ❌ Hit chance display
- ❌ Damage resolution
- ❌ Enemy AI

These features will be added in the next development session.

---

## File Locations

- **Grid System**: `combat/grid.py` (305 lines)
- **Pathfinding**: `combat/pathfinding.py` (320 lines) **NEW Session 7**
- **Unit Base**: `entities/unit.py` (240 lines)
- **Investigators**: `entities/investigator.py` (170 lines)
- **Enemies**: `entities/enemy.py` (220 lines)
- **Battle Screen**: `combat/battle_screen.py` (~1050 lines with movement system)
- **Turn Order Tests**: `testing/test_turn_order.py` (Session 5)
- **Movement Tests**: `testing/test_movement.py` (Session 7) **NEW**

---

## Next Steps

See [CLAUDE.md](../CLAUDE.md) for:
1. ✅ ~~Pathfinding (A* algorithm for movement)~~ **COMPLETED Session 7**
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
- **Turn order system** (Session 5: individual unit turns, random order)
- **Dual highlight system** (Session 5: green for current turn, yellow for viewing)
- **Movement system** (Session 7: A* pathfinding, green tile highlights, click-to-move)
- **Movement mode activation** (Session 7: click Move button to show range)
- **Action bar callbacks** (Session 7: routes action clicks to battle screen)
- **Visual feedback** (health bars, highlights, unit info, investigator tiles, action bar)
- **End Turn button** (Session 5: advance through turn order)

The next phase: adding attacks, line of sight, and AI to make the battle fully playable!
