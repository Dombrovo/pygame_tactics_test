# Eldritch Tactics - Lovecraftian Turn-Based Tactical Game

## Game Overview

A turn-based tactical game inspired by X-COM, featuring squads of flawed investigators fighting against Lovecraftian horrors. Combines grid-based tactical combat with strategic meta-layer management, including permadeath, sanity mechanics, and escalating cosmic threats.

**Core Theme**: Psychological horror meets tactical strategy - fragile humans against incomprehensible eldritch entities.

---

## Technology Stack

- **Engine**: Pygame CE (Community Edition)
- **Language**: Python 3.10+
- **Package Manager**: UV (fast Python package installer and resolver)
- **Installation**: `uv add pygame-ce`

---

## ⚠️ CRITICAL CODING GUIDELINES

### **DO NOT Use Unicode/Emoji in Command-Line Output**

**Platform**: Windows (primary development environment)

**Issue**: Windows console (cmd.exe) uses CP1252 encoding by default, which CANNOT display:
- Emoji symbols (✓, ✗, ✔, ✘, ⚠, etc.)
- Unicode arrows (→, ←, ↑, ↓, ⇒, etc.)
- Box drawing characters (╔, ║, ═, ╗, etc.)

**Result**: `UnicodeEncodeError: 'charmap' codec can't encode character...`

**ALWAYS Use ASCII Alternatives**:
```python
# ❌ WRONG - Will crash on Windows
print(f"✓ Test passed")
print(f"Path: (0,0) → (3,3)")

# ✅ CORRECT - Works everywhere
print(f"[OK] Test passed")
print(f"Path: (0,0) -> (3,3)")
```

**ASCII Alternatives**:
- ✓ → `[OK]` or `PASS`
- ✗ → `[X]` or `FAIL`
- → → `->`
- ⚠ → `[!]` or `WARNING`

**Where This Applies**:
- Test scripts (`testing/*.py`)
- Debug print statements
- Console output
- Any Python `print()` to terminal

**Where Unicode IS Okay**:
- Pygame rendered text (uses font rendering, not console)
- JSON data files
- Markdown documentation

---

## Current Development State

**Last Updated**: 2025-12-08 (Session 9)
**Current Phase**: Phase 1 - MVP (~98% Complete - Equipment System Complete, Line of Sight & Combat Next)

### ✅ Completed Components

#### 00. Documentation
- ✅ Comprehensive inline code comments (all files)
- ✅ docs/01_pygame_fundamentals.md - Pygame-CE basics
- ✅ docs/02_architecture_overview.md - System structure
- ✅ docs/03_ui_components.md - UI deep dive
- ✅ docs/04_data_flow.md - Interaction patterns
- ✅ docs/05_grid_and_battle_system.md - Grid and battle system
- ✅ docs/06_stat_system.md - Stat system with modifiers
- ✅ docs/doc_index.md - Documentation index

#### 1. Project Foundation
- ✅ UV package manager configured with pyproject.toml
- ✅ Virtual environment (.venv) created
- ✅ Pygame-CE installed and tested (2.5.6)
- ✅ Git repository initialized

#### 2. Configuration System
- ✅ Centralized config.py with all constants
- ✅ Screen settings (1920x1080 fullscreen)
- ✅ Color palette for Lovecraftian theme
- ✅ UI dimensions and game balance constants
- ✅ Grid and tile constants (10x10, 80px tiles)

#### 3. UI Framework
- ✅ Button class (interactive, hover/click detection)
- ✅ MenuButton class (extends Button with enabled/disabled state)
- ✅ TextLabel class (non-interactive text display)
- ✅ InvestigatorTile class (status panel component)
- ✅ ActionButton class (action bar slot component)
- ✅ ActionBar class (10-slot ability/action bar)
- ✅ TurnOrderTracker class (visual turn sequence display)
- ✅ ActionPointsDisplay class (visual action points indicator)
- ✅ Tooltip class (contextual information on hover)
- ✅ Callback pattern implementation

#### 4. Title Screen
- ✅ Fullscreen title screen (1920x1080)
- ✅ Menu navigation (New Game, Continue, Settings, Exit)
- ✅ Keyboard shortcuts (ESC, Enter, Space)
- ✅ Visual feedback (hover effects, button states)

#### 5. Main Entry Point
- ✅ Pygame initialization sequence
- ✅ Display/window management
- ✅ Clock for FPS control (60 FPS)
- ✅ Screen navigation orchestration
- ✅ Battle screen integration

#### 6. Grid System
- ✅ Tile class (position, terrain, cover, occupancy)
- ✅ Grid class (10x10 battlefield)
- ✅ Cover system (empty, half cover, full cover)
- ✅ Unit placement and movement tracking
- ✅ Distance calculations (Euclidean, Manhattan)
- ✅ Neighbor finding (orthogonal + diagonal)

#### 7. Entity System
- ✅ Base Unit class (health, sanity, stats, team)
- ✅ Stat System with Modifiers
  - Base stats + modifier pattern
  - Properties auto-calculate effective stats
  - Easy modifier application for backgrounds/traits
  - Auto-clamping (accuracy 5-95%, stats min values)
- ✅ Investigator class (player units)
  - Random name generation with gender
  - 50/50 male/female assignment
  - 30% chance for nicknames
  - Dual resource system (health + sanity)
- ✅ Enemy base class
- ✅ Cultist class (🔫 ranged attacker)
- ✅ Hound of Tindalos class (🐺 fast melee horror)

#### 7.5. Equipment & Inventory System (Session 9)
- ✅ Base Equipment class (for all equippable items)
- ✅ Weapon class with damage, range, attack type, accuracy modifiers
- ✅ Weapon Library - 9 investigator weapons, 3 enemy weapons
  - Investigator: Revolver, Rifle, Shotgun, Tommy Gun, Knife, Axe, Crowbar, Blessed Blade, Elder Sign
  - Enemy: Cultist Pistol, Hound Claws, Tentacle Strike
- ✅ Unit integration with weapon properties
  - `equipped_weapon` attribute
  - `weapon_damage`, `weapon_range`, `attack_type` properties
  - `weapon_sanity_damage` property
  - `equip_weapon()`, `unequip_weapon()`, `has_weapon()` methods
  - Weapon accuracy modifiers integrated into accuracy calculation
- ✅ Automatic weapon assignment
  - Investigators equip role-appropriate weapons (Balanced→Revolver, Sniper→Rifle, Tank→Shotgun)
  - Enemies equip their signature weapons
- ✅ Unarmed combat fallback (2 damage, range 1, melee)
- ✅ Comprehensive test suite (`testing/test_equipment.py`) - All tests passing

#### 8. Battle Screen
- ✅ Grid rendering (10x10 with cover symbols)
- ✅ Unit rendering (emoji symbols + health/sanity bars)
- ✅ Unit selection (mouse click, Tab cycling)
- ✅ Turn-based system (individual unit turns with random order)
- ✅ Dual highlighting (green=current turn, yellow=viewing)
- ✅ Unit info panel (right side display)
- ✅ Turn/round counter and current unit display
- ✅ Action bar (10 slots, bottom center, tied to current turn)
- ✅ End Turn button (right of action bar)
- ✅ Pixel ↔ grid coordinate conversion

#### 9. Name Generation System
- ✅ JSON name database (assets/json/names_data.json)
  - 84 male first names, 84 female first names
  - 90 last names, 113 nicknames
  - 1920s Lovecraftian theme
- ✅ Random generation with 50/50 gender distribution
- ✅ 30% nickname probability

#### 10. Character Portrait System
- ✅ Unique image assignment (25 female, 30 male portraits)
- ✅ No image reuse - Once assigned, images never used again
- ✅ Pool tracking system prevents duplicates
- ✅ Automatic assignment in `create_test_squad()`

#### 11. Visual Rendering System
- ✅ Emoji font support with automatic detection
  - Windows: Segoe UI Emoji
  - macOS: Apple Color Emoji
  - Linux: Noto Color Emoji/Symbola
- ✅ ASCII fallback system ([I], [C], [H] symbols)
- ✅ Team-based color coding (Blue=Player, Red=Enemy)

#### 12. Investigator Tiles Panel (Session 4)
- ✅ InvestigatorTile UI component (510×180px)
- ✅ Character portrait display with image loading
- ✅ Two-line name display (first + nickname / last name)
- ✅ Health and sanity bars with current/max values
- ✅ Compact stat display (accuracy, movement, will)
- ✅ Selection indicator (yellow border)
- ✅ Battle screen integration (left panel, 4 stacked tiles)
- ✅ Synchronized selection (tile clicks ↔ grid clicks ↔ Tab)
- ✅ Enhanced tactical overview

#### 13. Action Bar System (Session 4, Updated Session 5)
- ✅ ActionButton UI component (70×70px square buttons)
  - Icon/emoji display with text labels
  - Hotkey indicators (1-0 in top-left corner)
  - Enabled/disabled states with visual feedback
  - Hover and pressed states
- ✅ ActionBar class (10 action slots)
  - Horizontal layout, centered below grid
  - **Session 5 Update**: Now tied to current turn unit (not selected unit)
  - Mouse click support for all slots
  - Keyboard hotkey support (1-0 keys)
  - Auto-populates Move and Attack placeholders
  - Clears when no player unit's turn or incapacitated
- ✅ Battle screen integration
  - Positioned below grid (centered, 790px wide)
  - **Session 5**: End Turn button positioned to the right (150×70px)
  - Event handling (mouse + keyboard)
  - Disabled controls help text (replaced by action bar)

#### 14. Enemy Unit Selection (Session 4)
- ✅ Enhanced selection system for tactical intelligence
  - Click any unit (player or enemy) to view stats
  - Works during both player and enemy turns
  - Yellow highlight on currently inspected unit
- ✅ Smart UI behavior
  - Action bar clears when enemy selected (can't control)
  - Investigator tiles for player commands (player turn only)
  - Tab cycling limited to player units (command focus)
- ✅ Enemy stats display in right panel
  - Health, sanity, accuracy, will, movement
  - Weapon range and attack type (ranged/melee)
  - Sanity damage for eldritch enemies
- ✅ Tactical benefits
  - Scout enemy capabilities before engagement
  - Identify priority targets (low HP, high threat)
  - Strategic planning based on enemy stats

#### 15. Turn Order System (Session 5)
- ✅ Individual unit turn structure (replaces phase-based system)
  - Random turn order initialization (all units shuffled)
  - Round tracking (round = all units take one turn)
  - Automatic advancement with wrap-around
  - Future-ready for initiative stat implementation
- ✅ End Turn button (150×70px, right of action bar)
  - Click or Space key to advance turn
  - Automatically skips incapacitated units
  - Enemy turns auto-skip (AI placeholder)
- ✅ Dual highlight system
  - Green highlight: Current turn unit (can act now)
  - Yellow highlight: Selected unit for viewing (if different)
  - Both highlights shown simultaneously for clarity
- ✅ Action bar behavior updated
  - Shows actions only for current turn unit
  - Selecting other units doesn't change action bar
  - Enforces proper turn structure
- ✅ Turn order debugging
  - Console output shows full turn order at battle start
  - Turn advancement messages for development
  - Comprehensive test suite (`testing/test_turn_order.py`)

#### 16. Turn Order Tracker (Session 6)
- ✅ TurnOrderTracker UI component (1200×70px, top of screen)
  - Horizontal bar displaying all 8 units in turn sequence
  - Unit icons: Investigators show portrait images, Enemies show emoji symbols
  - Current turn highlight (green border, 4px thick)
  - Hover highlight (golden border, 3px thick)
  - Team color coding (blue background for players, red for enemies)
  - Mini health bars at bottom of each icon (color-coded: green/yellow/red)
  - Portrait image caching for performance
- ✅ Integrated turn display
  - "TURN ORDER:" label at top-left
  - Current turn info below label: "Player: Name" or "Enemy: Name"
  - Golden highlighted text for current turn
  - Replaces redundant battle header (removed)
- ✅ Battle screen integration
  - Positioned at y=10 (top of screen)
  - Grid offset adjusted to y=95 (was 100) to accommodate tracker
  - Updates automatically when turns advance
  - No tooltips needed - info shown in fixed location
- ✅ Visual benefits
  - At-a-glance turn sequence visibility
  - Character recognition via portraits
  - Clean visual hierarchy (portraits vs symbols)
  - Always-visible current turn information

#### 17. Movement System (Session 7)
- ✅ Pathfinding module (`combat/pathfinding.py`)
  - **A* algorithm** for optimal path finding
  - Configurable movement costs (orthogonal: 1.0, diagonal: 1.414)
  - Path validation with max distance limits
  - Obstacle avoidance (units block movement)
  - Cover passable (units can move through cover)
- ✅ Reachable tiles calculation
  - **Flood-fill algorithm** for efficient range finding
  - Returns all tiles within movement range
  - Excludes occupied tiles
  - Used for highlighting valid destinations
- ✅ Battle screen integration
  - **Movement mode activation** - Click Move button to show range
  - Green tile highlighting for valid movement destinations
  - Click-to-move functionality (click green tile to move there)
  - Path length validation before movement
  - Movement action tracking (consumes 1 action point)
  - Auto-updates range after movement
- ✅ Movement mode state machine
  - `movement_mode_active` flag controls highlight visibility
  - `activate_movement_mode()` - Shows green tiles (called by Move button)
  - `deactivate_movement_mode()` - Hides green tiles
  - Auto-deactivates on: movement completion, turn end, unit selection
  - Prevents accidental moves (requires explicit Move button click)
- ✅ Action bar integration
  - Move button (slot 0, hotkey 1) activates movement mode
  - Action bar callback system (`on_action_click`)
  - `_on_action_button_click()` handler routes actions
  - Buttons auto-disable when no action points remain
  - Ready for Attack and future abilities
- ✅ Visual feedback
  - Green tint on reachable tiles (only when mode active)
  - Green border (2px) around reachable tiles
  - No highlights until Move button clicked
  - Console feedback (path length, tiles reachable)
- ✅ Testing
  - Comprehensive test suite (`testing/test_movement.py`)
  - Tests pathfinding, obstacles, range calculation
  - Tests all 4 investigator movement stats
  - Tests unit blocking (no movement through units)
  - **All tests passing** (ASCII output for Windows compatibility)

#### 18. Action Points System (Session 7)
- ✅ **2-Action Economy** - Each unit has 2 action points per turn
  - Move costs 1 action point
  - Attack costs 1 action point (when implemented)
  - Valid combinations: Move-Move, Move-Attack, Attack-Move, Attack-Attack
  - Replaces old boolean flags (has_moved/has_attacked)
- ✅ Unit class updates (`entities/unit.py`)
  - `max_action_points = 2` - Maximum actions per turn
  - `current_action_points` - Remaining actions this turn
  - `consume_action_point(amount)` - Consumes action points when acting
  - `has_actions_remaining()` - Checks if any points remain
  - `can_move()` and `can_attack()` now check action points
  - `reset_turn_flags()` restores action points at turn start
- ✅ ActionPointsDisplay UI component (200×100px, bottom-left)
  - "ACTIONS" label at top
  - Circular indicators for each action point:
    - 🟡 Filled golden circles = available action points
    - ⚪ Hollow gray circles = used action points
  - "X/2" counter showing remaining actions
  - Real-time updates as actions are used
  - Golden glow effect on available actions
- ✅ Battle screen integration
  - Display positioned bottom-left, aligned with action bar
  - Updates on turn advancement and action consumption
  - `_update_action_points_display()` method
  - Draws every frame showing current unit's remaining actions
- ✅ Smart action bar behavior
  - Move button enabled only if `can_move()` returns True
  - Attack button enabled only if `can_attack()` returns True
  - Buttons auto-gray-out when no action points remain
  - Visual feedback for available vs unavailable actions
- ✅ Testing
  - Comprehensive test suite (`testing/test_action_points.py`)
  - Tests initialization, consumption, reset, all combinations
  - Verifies Move-Move, Move-Attack, Attack-Attack work correctly
  - **All tests passing** (ASCII output for Windows compatibility)

#### 19. Procedural Terrain Generation System (Session 8)
- ✅ **Modular Generator Framework** (`combat/terrain_generator.py`)
  - Base `TerrainGenerator` class for extensibility
  - 6 specialized generators with unique tactical characteristics
  - Data-driven design (returns terrain data, doesn't modify grid directly)
  - Automatic spawn zone protection (player: x < 3, enemy: x > 6)
- ✅ **Six Terrain Generators**
  - **SymmetricGenerator**: Mirror-symmetric maps for balanced, competitive combat
  - **ScatteredGenerator**: Random cover placement with configurable density (15%) and full/half ratio (40/60)
  - **UrbanRuinsGenerator**: City ruins with vertical walls (70% probability) and debris piles (50%)
  - **RitualSiteGenerator**: Circular pattern with central 2×2 altar for dramatic eldritch battles
  - **OpenFieldGenerator**: Minimal cover (~4 pieces) favoring ranged combat and mobility
  - **ChokepointGenerator**: Vertical walls with 2-tile gaps, defensive positioning
- ✅ Grid integration (`combat/grid.py`)
  - `setup_generated_terrain(terrain_data)` - Applies procedural terrain to grid
  - `setup_test_cover()` deprecated but kept for backwards compatibility
- ✅ Battle screen integration (`combat/battle_screen.py`)
  - Replaced hardcoded `setup_test_cover()` with `generate_random_terrain()`
  - Each battle uses randomly selected generator for variety
  - Console output shows which generator was used
- ✅ Testing
  - Comprehensive test suite (`testing/test_terrain_generation.py`)
  - ASCII visualization of all generator layouts
  - Validates spawn zone clearance (no cover blocks unit placement)
  - Validates coordinate bounds and cover type correctness
  - **All tests passing** with no spawn zone violations
- ✅ Impact
  - **Replayability**: Every battle has different terrain layout
  - **Tactical depth**: Different generators require different strategies
  - **Thematic atmosphere**: Generators match mission types (urban ruins, ritual sites, etc.)
  - **Future-ready**: Easy to add new generators or mission-specific terrain

#### 20. Terrain Tooltip System (Session 8)
- ✅ **Tooltip UI Component** (`ui/ui_elements.py`)
  - `Tooltip` class (191 lines) for contextual information display
  - Multi-line display: title (golden) + flavor text (dim) + mechanics (normal)
  - Semi-transparent background with border (alpha=230)
  - Automatic screen edge avoidance (adjusts position to stay on-screen)
  - Bold title effect (double-render technique)
  - Configurable padding, colors, and font sizes
- ✅ **Tile Tooltip Data** (`combat/grid.py`)
  - Tooltip fields added to `Tile` class: `tooltip_title`, `tooltip_flavor`, `tooltip_mechanics`
  - **Full Cover**: "Solid terrain that provides complete protection" / "+40% chance for attacks to miss"
  - **Half Cover**: "Low obstacles that provide partial protection" / "+20% chance for attacks to miss"
  - **Empty tiles**: No tooltip (empty strings)
  - `has_tooltip()` method checks if tile has displayable content
  - **Critical fix**: `add_cover()` now updates tooltip data when adding terrain
- ✅ **Battle Screen Integration** (`combat/battle_screen.py`)
  - `terrain_tooltip` instance created in battle screen
  - `hovered_tile` tracking for current mouse position
  - `_update_terrain_tooltip()` method (35 lines) updates every frame
  - Converts mouse position to grid coordinates via `_pixel_to_grid()`
  - Shows tooltip when hovering over terrain with cover
  - Hides tooltip when hovering over empty tiles or off-grid
  - Drawn last (appears on top of all other UI elements)
- ✅ **User Experience**
  - Hover mouse over terrain → Tooltip appears near cursor
  - Tooltip follows mouse with 15px offset
  - Displays terrain type, description, and defense bonus
  - Disappears when leaving terrain tile
  - No lag or flicker (smooth 60 FPS)
- ✅ **Testing**
  - `testing/test_tooltip.py` - Component tests (basic functionality, edge avoidance, visual test)
  - `testing/test_tooltip_integration.py` - Integration tests (tile data, add_cover() updates, terrain generation)
  - **All tests passing** (verified tooltip data updates correctly)
- ✅ **Bug Fix Documentation**
  - `TOOLTIP_FIX_SUMMARY.md` - Complete debugging history and resolution
  - Root cause: `add_cover()` wasn't updating tooltip fields
  - Solution: Update tooltip data when terrain is added to tiles

### 🚧 In Progress

**Next Task**: Combat Resolution (Attacks, Hit Chance, Line of Sight)

---

## File Structure

```
pygame_tactics_test/
├── main.py                    # Entry point
├── config.py                  # Configuration constants
├── pyproject.toml             # Project metadata
├── CLAUDE.md                  # This file (current state)
├── PLAN.md                    # Future roadmap
├── CONTRIBUTING.md            # Developer guidelines
│
├── ui/                        # UI Framework
│   ├── ui_elements.py         # Button, MenuButton, TextLabel, InvestigatorTile, ActionBar, TurnOrderTracker, Tooltip
│   ├── title_screen.py        # Title screen
│   └── settings_screen.py     # Settings menu
│
├── combat/                    # Combat System
│   ├── grid.py                # Grid, Tile classes, cover system
│   ├── pathfinding.py         # A* pathfinding, movement range calculation
│   ├── terrain_generator.py   # Procedural terrain generation (6 generators)
│   └── battle_screen.py       # Battle UI, rendering, turn system, movement mode
│
├── entities/                  # Entity System
│   ├── unit.py                # Base Unit (with stat modifiers + equipment)
│   ├── investigator.py        # Player units (random names + portraits + weapons)
│   ├── enemy.py               # Enemy units (Cultist, Hound + weapons)
│   └── equipment.py           # Equipment system (weapons, armor, accessories)
│
├── assets/                    # Game assets
│   ├── images/                # Character portraits, sprites
│   └── json/                  # Data files (names_data.json)
│
├── testing/                   # Test scripts
│   ├── test_names.py
│   ├── test_stat_system.py
│   ├── test_image_assignment.py
│   ├── test_turn_order.py
│   ├── test_movement.py
│   ├── test_action_points.py
│   ├── test_terrain_generation.py
│   ├── test_tooltip.py
│   ├── test_tooltip_integration.py
│   └── test_equipment.py      # Equipment system tests
│
└── docs/                      # Documentation
    ├── doc_index.md
    ├── session_archive.md     # Old session notes
    ├── 01_pygame_fundamentals.md
    ├── 02_architecture_overview.md
    ├── 03_ui_components.md
    ├── 04_data_flow.md
    ├── 05_grid_and_battle_system.md
    └── 06_stat_system.md
```

---

## Next Session Goals

**Primary Objective**: Implement attack mechanics and combat resolution

**Files to Create**:
1. `combat/line_of_sight.py` - Bresenham's line algorithm for LOS
2. `combat/combat_resolver.py` - Hit chance calculation, damage resolution

**Files to Update**:
3. `combat/battle_screen.py` - Add attack action implementation
4. Update unit info display to show weapon stats

**Current Status**:
- ✅ Movement system complete with A* pathfinding
- ✅ Action points system fully implemented (2 actions per turn)
- ✅ Equipment system complete (weapons, damage, range, modifiers)
- ⏳ Line of Sight next (Bresenham's algorithm)
- ⏳ Combat resolution next (hit chance, damage application)

**Estimated Time**: 3-4 hours

---

## ⚠️ CRITICAL: UV Package Manager Usage

**IMPORTANT**: Always use UV commands, not pip!

### Quick Reference

```bash
# ✅ CORRECT - Use UV commands
uv run python main.py              # Run the game
uv run pytest                      # Run tests
uv add pygame-ce                   # Add dependency
uv add --dev pytest                # Add dev dependency
uv sync                            # Install from lockfile

# ❌ WRONG - Do NOT use these
python main.py                     # Missing UV environment
pip install pygame-ce              # Doesn't update lockfile
source .venv/bin/activate          # Unnecessary with UV
```

### Why UV?

- **10-100x faster** than pip
- Automatic virtual environment management
- Lockfile ensures consistent dependencies
- No need to activate venv manually

### Common Tasks

| Task | Command |
|------|---------|
| Run game | `uv run python main.py` |
| Run tests | `uv run python testing/test_*.py` |
| Add package | `uv add <package-name>` |
| Add dev package | `uv add --dev <package-name>` |
| Install dependencies | `uv sync` |
| Update dependencies | `uv lock --upgrade` |

**See Also**: [UV Documentation](https://docs.astral.sh/uv/) for advanced usage

---

## Recent Development: Session 4

**Completed**: 2025-11-29

### Investigator Tiles Panel Implementation

Successfully implemented a comprehensive investigator status panel for enhanced tactical overview:

**Key Features**:
- Large, information-rich tiles (510×180px, 50% larger than initial design)
- Character portrait display with automatic image loading
- Two-line name display to prevent truncation
- Resource bars (HP red, SAN blue) with current/max values
- Compact stats row (ACC, MOV, WIL)
- Visual states: yellow border (selected), hover effect, grayed out (incapacitated)
- Battle screen integration: left panel with 4 vertically-stacked tiles
- Synchronized multi-way selection (tile clicks ↔ grid clicks ↔ Tab cycling)

**Visual Layout** (1920×1080):
```
┌──────────────────────────────────────────────────────────┐
│  TURN ORDER:                                             │
│  Player: Name    [🖼️] [🔫] [🖼️] [🐺] [🖼️] [🔫] [🖼️] [🐺]     │
│                     ↑ Green border (70px tall)           │
├─────────────────┬──────────────┬─────────────────────────┤
│ [Tile 1: 510px] │              │  SELECTED UNIT INFO     │
│   180px tall    │              │  (Right panel)          │
│ [gap: 25px]     │              │                         │
│ [Tile 2: 510px] │   10×10 GRID │  Detailed stats for     │
│   180px tall    │   (800×800)  │  selected unit          │
│ [gap: 25px]     │              │                         │
│ [Tile 3: 510px] │              │                         │
│   180px tall    │              │                         │
│ [gap: 25px]     │              │                         │
│ [Tile 4: 510px] │              │                         │
│   180px tall    │              │                         │
└─────────────────┴──────────────┴─────────────────────────┘
 ┌──────────┐  ┌────────────────────┬───────────┐
 │ ACTIONS  │  │    ACTION BAR      │ End Turn  │
 │  🟡 🟡   │  │ [1][2][3]...[0]    │  Button   │
 │   2/2    │  │                    │           │
 └──────────┘  └────────────────────┴───────────┘
  ↑ Action Points Display (bottom-left)
```

**Impact**:
- At-a-glance squad status (no need to click each unit)
- Large, easy-to-click targets (510×180px vs 80×80px grid tiles)
- Better screen space utilization (left panel fills vertical space)
- Immediate visual feedback for incapacitated units

### Action Bar System Implementation

Successfully implemented a 10-slot action bar for displaying investigator abilities and actions:

**Key Features**:
- 10 action slots (70×70px square buttons) with hotkey indicators (1-0)
- Icon/emoji display (↗ for Move, ⚔ for Attack) with text labels
- Visual states: enabled/disabled, hover, pressed
- Mouse click support for all slots
- Keyboard hotkey support (press 1-0 to trigger actions)
- Auto-updates based on selected investigator
- Clears when no unit selected or incapacitated

**Battle Screen Layout** (Updated):
```
┌────────────────────────────────────────────────────┐
│              TURN 1 | PLAYER PHASE                 │
├─────────────┬──────────────────┬────────────────────┤
│ Inv Tile 1  │                  │ Selected Unit Info │
│ (510×180)   │                  │ (Right panel)      │
├─────────────┤                  │                    │
│ Inv Tile 2  │   10×10 GRID     │                    │
├─────────────┤   (800×800)      │                    │
│ Inv Tile 3  │                  │                    │
├─────────────┤                  │                    │
│ Inv Tile 4  │                  │                    │
└─────────────┴──────────────────┴────────────────────┘
             ┌────────────────────┐
             │    ACTION BAR      │ (10 slots, 790px)
             │ [1][2][3][4]...[0] │ (centered below)
             └────────────────────┘
```

**Integration**:
- Positioned below grid, centered (790px wide total)
- Synchronized with selection system (updates on click/Tab)
- Event handling integrated (mouse + keyboard before grid clicks)
- Replaced controls help text (action bar is more intuitive)

**Current Placeholders**:
- Slot 1 (hotkey 1): Move action ↗
- Slot 2 (hotkey 2): Attack action ⚔
- Slots 3-10: Empty (ready for future abilities)

**Impact**:
- Quick access to abilities via mouse or keyboard
- Visual feedback for available/unavailable actions
- Extensible system ready for Phase 2 abilities
- Improved UX compared to text-based controls

### Enemy Unit Selection (Intelligence Gathering)

Successfully enhanced the selection system to allow viewing enemy unit stats for tactical intelligence:

**Key Features**:
- Click ANY unit (player or enemy) to view stats in right panel
- Selection works during both player and enemy turns
- Yellow highlight shows currently inspected unit
- Action bar automatically clears when enemy selected (can't control enemies)
- Investigator tiles remain for commanding player units (player turn only)
- Tab cycling still limited to player units for quick command access

**Selection Behavior**:
- **Grid clicks** → Select any unit to view stats (intelligence gathering)
- **Investigator tiles** → Select player units for commands (player turn only)
- **Tab key** → Cycle through player units (command cycling)
- **Action bar** → Only populates for player units (command interface)

**Enemy Stats Displayed**:
When selecting enemies, the right panel shows:
- Name, team, position
- Current/max health and sanity
- Accuracy, will, movement range
- Weapon range, attack type (ranged/melee)
- Sanity damage (for eldritch enemies)

**Impact**:
- **Tactical intelligence** - Scout enemy stats before engaging
- **Threat assessment** - Identify priority targets (low HP, high damage)
- **Strategic planning** - Plan attacks based on enemy capabilities
- **Clean interface** - Viewing doesn't interfere with command controls

**For detailed session history, see**: [docs/session_archive.md](docs/session_archive.md)

---

## Recent Development: Session 5

**Completed**: 2025-11-29

### Turn Order System Implementation

Successfully replaced phase-based turns (all players → all enemies) with individual unit turn order system:

**Key Features**:
- **Random turn order** - All 8 units (4 players + 4 enemies) shuffled into single queue
- **Round tracking** - Round increments when all units have taken one turn
- **Auto-skip** - Incapacitated units automatically skipped
- **Enemy AI placeholder** - Enemy turns immediately advance (AI not yet implemented)

**Visual Enhancements**:
- **Dual highlight system**:
  - 🟢 Green border = Current turn unit (can act now)
  - 🟡 Yellow border = Selected for viewing (if different from current turn)
- **Updated header**: "ROUND X | Player/Enemy Turn: Unit Name"
- **End Turn button**: 150×70px button positioned right of action bar

**Behavioral Changes**:
- **Action bar** now tied to current turn unit (not selected unit)
  - Clicking other units shows their stats but doesn't change action bar
  - Enforces proper turn structure
- **Selection** still works for all units (intelligence gathering)
  - Grid clicks select any unit to view stats
  - Investigator tiles for quick player unit access
  - Tab cycling through player units unchanged

**Battle Screen Layout** (Updated with End Turn):
```
┌────────────────────────────────────────────────────────┐
│         ROUND 1 | Player Turn: John Carter            │
├─────────────┬──────────────────┬────────────────────────┤
│ Inv Tile 1  │                  │ Selected Unit Info    │
│   (green)   │    🟢 = Current  │ (Right panel)         │
├─────────────┤    🟡 = Viewing  │                       │
│ Inv Tile 2  │   10×10 GRID     │ Name, HP, SAN         │
├─────────────┤   (800×800)      │ Stats, weapon info    │
│ Inv Tile 3  │                  │                       │
├─────────────┤                  │                       │
│ Inv Tile 4  │                  │                       │
└─────────────┴──────────────────┴────────────────────────┘
         ┌────────────────────┬───────────┐
         │    ACTION BAR      │ End Turn  │
         │ [1][2][3]...[0]    │  Button   │
         └────────────────────┴───────────┘
```

**Turn Advancement Flow**:
1. Battle starts → Random turn order created → First unit's turn
2. Player sees green highlight on current turn unit
3. Action bar shows current unit's actions (if player unit)
4. Click "End Turn" or press Space
5. Next unit in order takes their turn
6. Enemy turns auto-skip with "[AI not yet implemented]" message
7. When all 8 units acted → Round increments, wraps to first unit

**Implementation Details**:
- `turn_order[]` - List of all units in shuffled order
- `current_turn_index` - Index in turn order (0-7)
- `current_turn_unit` - Unit whose turn it is
- `round_number` - Tracks full cycles through turn order
- `_advance_turn()` - Handles turn progression with wrap-around

**Testing**:
Created comprehensive test suite (`testing/test_turn_order.py`):
- ✅ Turn order initialization (random shuffle)
- ✅ Turn advancement with wrap-around
- ✅ Skipping incapacitated units
- ✅ Round incrementing
- ✅ Team mixing (random order, not phase-based)

**Configuration**:
Added to `config.py`:
- `COLOR_CURRENT_TURN = (100, 255, 100)` - Green highlight for active unit

**Impact**:
- More tactical depth - Must plan around turn order
- X-COM-like feel - Unit-based instead of phase-based
- Ready for initiative stat (replace random with stat-based order)
- Clearer visual language (green=act, yellow=view)
- Foundation for complex AI behaviors (each unit acts independently)

---

## Recent Development: Session 6

**Completed**: 2025-11-29

### Turn Order Tracker Visual Implementation

Successfully added visual turn order display at the top of the battle screen:

**Key Features**:
- **Horizontal tracker bar** (1200×70px) showing all 8 units in sequence
- **Portrait integration** - Investigators show character portraits, enemies show emoji
- **Current turn highlight** - Green border (4px) around active unit's icon
- **Hover feedback** - Golden border (3px) on mouse hover
- **Mini health bars** - Color-coded health indicators at bottom of each icon
- **Team color coding** - Blue background for players, red for enemies

**Visual Design**:
- Fixed position at top of screen (y=10)
- "TURN ORDER:" label at top-left
- Current turn info below label: "Player: Name" or "Enemy: Name"
- Golden highlighted text for active unit
- Always visible - no tooltips needed

**Technical Implementation**:
- Portrait image caching for performance
- Automatic fallback to emoji symbols if image load fails
- Updates on turn advancement via `update_turn_order()` method
- Integrated with battle screen's turn system

**Impact**:
- At-a-glance turn sequence visibility
- Enhanced character recognition via portraits vs symbols
- Clean visual hierarchy
- Always-visible current turn information
- Reduced cognitive load (no need to remember turn order)

---

## Recent Development: Session 7

**Completed**: 2025-11-30

### Action Points System and Movement Implementation

Successfully implemented a comprehensive 2-action points system and completed the movement mechanics:

#### Movement System (A* Pathfinding)
**Pathfinding Module** (`combat/pathfinding.py`):
- **A* algorithm** for optimal path calculation
- Configurable movement costs (orthogonal: 1.0, diagonal: 1.414)
- Path validation with max distance limits
- **Flood-fill algorithm** for reachable tiles calculation
- Obstacle avoidance (units block movement, cover is passable)

**Battle Screen Integration**:
- Movement mode activation via Move button (hotkey 1)
- Green tile highlighting for valid destinations
- Click-to-move functionality
- Movement range updates after each move
- State machine prevents accidental moves (requires Move button click)

**Testing**:
- Comprehensive test suite (`testing/test_movement.py`)
- All tests passing with ASCII output for Windows compatibility

#### Action Points System
**2-Action Economy**:
- Each unit has 2 action points per turn
- Move costs 1 AP, Attack costs 1 AP (when implemented)
- Valid combinations: Move-Move, Move-Attack, Attack-Move, Attack-Attack
- Replaces old boolean flags (`has_moved`/`has_attacked`)

**Unit Class Updates** (`entities/unit.py`):
- `max_action_points = 2` - Maximum actions per turn
- `current_action_points` - Remaining actions this turn
- `consume_action_point(amount)` - Consumes AP when acting
- `has_actions_remaining()` - Checks if any points remain
- `can_move()` and `can_attack()` now check action points
- `reset_turn_flags()` restores action points at turn start

**ActionPointsDisplay UI Component**:
- Size: 200×100px, positioned bottom-left corner
- "ACTIONS" label at top
- Circular indicators for each action point:
  - 🟡 Filled golden circles = available action points
  - ⚪ Hollow gray circles = used action points
- "X/2" counter showing remaining actions
- Real-time updates as actions are consumed
- Golden glow effect on available actions

**Smart Action Bar Behavior**:
- Move button enabled only if `can_move()` returns True
- Attack button enabled only if `can_attack()` returns True
- Buttons auto-gray-out when no action points remain
- Visual feedback for available vs unavailable actions

**Battle Screen Layout** (Updated):
```
┌────────────────────────────────────────────────────────┐
│  TURN ORDER: Player: Name  [🖼️] [🔫] [🖼️] [🐺] [🖼️] [🔫]  │
├─────────────┬──────────────────┬──────────────────────┤
│ Inv Tile 1  │                  │ Selected Unit Info  │
├─────────────┤   10×10 GRID     ├──────────────────────┤
│ Inv Tile 2  │   (800×800)      │ Detailed stats      │
├─────────────┤                  │                     │
│ Inv Tile 3  │                  │                     │
├─────────────┤                  │                     │
│ Inv Tile 4  │                  │                     │
└─────────────┴──────────────────┴──────────────────────┘
 ┌──────────┐  ┌────────────────────┬───────────┐
 │ ACTIONS  │  │    ACTION BAR      │ End Turn  │
 │  🟡 🟡   │  │ [1][2][3]...[0]    │  Button   │
 │   2/2    │  │                    │           │
 └──────────┘  └────────────────────┴───────────┘
```

**Testing**:
- Comprehensive test suite (`testing/test_action_points.py`)
- Tests all action combinations (Move-Move, Move-Attack, Attack-Attack)
- Verifies action point consumption, reset, and boundary conditions
- All tests passing with ASCII output

**Impact**:
- Flexible action economy supports varied tactical approaches
- Clear visual feedback on remaining actions
- Foundation ready for attack implementation
- Prevents action overflow bugs with smart button disabling
- Enhanced player agency (multiple action combinations per turn)

---

## Recent Development: Session 9

**Completed**: 2025-12-08

### Equipment & Inventory System Implementation

Successfully implemented a comprehensive equipment system for weapons, armor, and accessories:

**Key Features**:
- **Modular equipment framework** - Base `Equipment` class, `Weapon`/`Armor`/`Accessory` subclasses
- **12 pre-defined weapons** - 9 for investigators, 3 for enemies
- **Property-based stat delegation** - Unit stats automatically pull from equipped weapon
- **Weapon modifiers** - Accuracy bonuses/penalties (Rifle +10%, Shotgun -10%)
- **Dual damage types** - Health damage + sanity damage (for eldritch weapons)
- **Automatic weapon assignment** - Investigators and enemies auto-equip appropriate weapons
- **Unarmed combat fallback** - Units without weapons default to 2 damage, range 1, melee

**Equipment Module** (`entities/equipment.py` - 434 lines):
- `Equipment` base class (name, description, slot, icon)
- `Weapon` class (damage, range, attack_type, accuracy_modifier, sanity_damage)
- `Armor` class (Phase 2+ placeholder)
- `Accessory` class (Phase 2+ placeholder)
- Weapon library with 12 pre-defined weapons
- Helper functions (`get_weapon_by_name()`, `get_all_investigator_weapons()`)

**Investigator Weapons**:
- **Revolver** - 5 dmg, range 3, balanced (standard issue)
- **Rifle** - 6 dmg, range 5, +10% accuracy (sniper weapon)
- **Shotgun** - 8 dmg, range 2, -10% accuracy (tank weapon)
- **Tommy Gun** - 4 dmg, range 3, -5% accuracy (spray weapon)
- **Combat Knife** - 4 dmg, range 1, melee, +5% accuracy
- **Fire Axe** - 7 dmg, range 1, melee, -5% accuracy (heavy)
- **Crowbar** - 3 dmg, range 1, melee (improvised)
- **Blessed Blade** - 5 dmg, range 1, melee, 3 sanity dmg (anti-eldritch)
- **Elder Sign Amulet** - 3 dmg, range 4, ranged, 5 sanity dmg, -10% accuracy (cursed artifact)

**Enemy Weapons**:
- **Cultist Pistol** - 4 dmg, range 3, -5% accuracy (cheap handgun)
- **Hound Claws** - 6 dmg, range 1, melee, +10% accuracy, 5 sanity dmg (terrifying)
- **Tentacle Strike** - 5 dmg, range 2, melee reach, 4 sanity dmg

**Unit Class Updates** (`entities/unit.py`):
- Added `equipped_weapon: Optional[Weapon]` attribute
- New weapon properties: `weapon_damage`, `weapon_range`, `attack_type`, `weapon_sanity_damage`
- Updated `accuracy` property to include weapon accuracy modifiers
- Added equipment methods: `equip_weapon()`, `unequip_weapon()`, `has_weapon()`

**Investigator Updates** (`entities/investigator.py`):
- `create_test_squad()` now auto-equips role-appropriate weapons:
  - Balanced -> Revolver
  - Sniper -> Rifle (+10% accuracy boost!)
  - Tank -> Shotgun (high damage, close range)
  - Scout -> Revolver

**Enemy Updates** (`entities/enemy.py`):
- Refactored `Enemy` base class to use equipment system
- `Cultist` auto-equips Cultist Pistol
- `HoundOfTindalos` auto-equips Eldritch Claws
- Updated `get_info_text()` to use weapon properties

**Testing** (`testing/test_equipment.py` - 293 lines):
- 7 comprehensive test functions covering all equipment features
- Tests weapon creation, equipping, stat delegation, modifiers
- Tests investigator/enemy weapon assignment
- Tests sanity damage weapons, weapon library functions
- **All tests passing** with ASCII-only output

**Impact**:
- **Attack system ready** - Damage, range, and modifiers now available
- **Extensible design** - Easy to add new weapons in future
- **Phase 2 prepared** - Armor and accessories framework in place
- **Tactical variety** - Different weapons encourage different playstyles
- **Clean architecture** - Property delegation keeps code DRY

---

## Quick Reference

### Running the Game

```bash
uv run python main.py
```

### Project Structure
- Current state documentation → **CLAUDE.md** (this file)
- Future plans & roadmap → **PLAN.md**
- Developer guidelines → **CONTRIBUTING.md**
- Code documentation → **docs/** directory

### Key Files
- `main.py` - Entry point, screen navigation
- `config.py` - All game constants
- `combat/battle_screen.py` - Main battle UI
- `entities/investigator.py` - Player unit generation
- `ui/ui_elements.py` - Reusable UI components

---

## MVP Goal

**Objective**: Get a single tactical battle playable with core mechanics working.

**Status**: ~75% Complete

**Remaining Features**:
- Movement system (A* pathfinding)
- Line of sight calculation (Bresenham's algorithm)
- Combat resolution (hit chance, damage)
- Attack actions (ranged, melee)
- Basic enemy AI

---

## Links

- **Future Roadmap**: [PLAN.md](PLAN.md) - Phases 2-5, system designs, long-term vision
- **Developer Guide**: [CONTRIBUTING.md](CONTRIBUTING.md) - Code style, architecture, workflows
- **Documentation Index**: [docs/doc_index.md](docs/doc_index.md) - All documentation files
- **Session History**: [docs/session_archive.md](docs/session_archive.md) - Previous development sessions

---

**Last Updated**: 2025-11-30 (Session 7)
**Version**: 2.2 (Action Points System + Movement)
**Target Platform**: Windows/Mac/Linux Desktop
**Engine**: Pygame CE 2.5.x
**Python**: 3.10+
