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

## Current Development State

**Last Updated**: 2025-11-29 (Session 5)
**Current Phase**: Phase 1 - MVP (~80% Complete - Turn Order Complete, Combat Mechanics Next)

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
- ✅ Enhanced header display
  - Shows: "ROUND X | Player/Enemy Turn: Unit Name"
  - Clear visual indicator of whose turn it is
- ✅ Turn order debugging
  - Console output shows full turn order at battle start
  - Turn advancement messages for development
  - Comprehensive test suite (`testing/test_turn_order.py`)

### 🚧 In Progress

**Next Task**: Combat Mechanics (Movement, Attacks, Line of Sight)

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
│   ├── ui_elements.py         # Button, MenuButton, TextLabel, InvestigatorTile
│   ├── title_screen.py        # Title screen
│   └── settings_screen.py     # Settings menu
│
├── combat/                    # Combat System
│   ├── grid.py                # Grid, Tile classes, cover system
│   └── battle_screen.py       # Battle UI, rendering, turn system
│
├── entities/                  # Entity System
│   ├── unit.py                # Base Unit (with stat modifiers)
│   ├── investigator.py        # Player units (random names + portraits)
│   └── enemy.py               # Enemy units (Cultist, Hound)
│
├── assets/                    # Game assets
│   ├── images/                # Character portraits, sprites
│   └── json/                  # Data files (names_data.json)
│
├── testing/                   # Test scripts
│   ├── test_names.py
│   ├── test_stat_system.py
│   └── test_image_assignment.py
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

**Primary Objective**: Implement combat mechanics

**Files to Create**:
1. `combat/pathfinding.py` - A* pathfinding for movement
2. `combat/line_of_sight.py` - Bresenham's line algorithm for LOS
3. `combat/combat_resolver.py` - Hit chance calculation, damage resolution

**Files to Update**:
4. `combat/battle_screen.py` - Add movement and attack actions

**Estimated Time**: 2-3 hours

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
┌─────────────────┬──────────────┬─────────────────────────┐
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

**Last Updated**: 2025-11-29 (Session 5)
**Version**: 2.1 (Turn Order System)
**Target Platform**: Windows/Mac/Linux Desktop
**Engine**: Pygame CE 2.5.x
**Python**: 3.10+
