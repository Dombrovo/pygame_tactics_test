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

**Last Updated**: 2025-12-08 (Session 11)
**Current Phase**: Phase 1 - MVP (~99% Complete - Combat Deck System Complete, Line of Sight & Combat Resolution Next)

### ✅ Completed Systems (High-Level Overview)

For detailed information on each system, see the [documentation](#documentation).

#### Core Foundation
- ✅ Project foundation (UV package manager, Pygame-CE 2.5.6, Git repo)
- ✅ Configuration system (centralized constants in config.py)
- ✅ Main entry point (screen navigation, game loop, 60 FPS)

#### UI Framework
- ✅ **Base Components**: Button, MenuButton, TextLabel, Tooltip
- ✅ **Battle UI**: InvestigatorTile, ActionButton, ActionBar, TurnOrderTracker, ActionPointsDisplay
- ✅ **Screens**: Title screen with menu navigation, Battle screen
- ✅ **Callback pattern** for event handling
- 📖 *See [docs/03_ui_components.md](docs/03_ui_components.md) for details*

#### Grid & Battle System
- ✅ **Grid**: 10x10 battlefield with Tile/Grid classes
- ✅ **Cover system**: Empty, half cover (+20% defense), full cover (+40% defense)
- ✅ **Terrain generation**: 6 procedural generators (symmetric, scattered, urban ruins, ritual site, open field, chokepoint)
- ✅ **Coordinate systems**: Pixel ↔ grid conversion, distance calculations
- ✅ **Tooltips**: Hover over terrain to see cover type and bonuses
- 📖 *See [docs/05_grid_and_battle_system.md](docs/05_grid_and_battle_system.md) and [docs/08_terrain_tooltip_system.md](docs/08_terrain_tooltip_system.md) for details*

#### Entity System
- ✅ **Base Unit class**: Health + sanity dual resource, stat modifiers pattern
- ✅ **Investigators**: Random name generation (1920s theme), character portraits (55 unique images), role-based stats
- ✅ **Enemies**: Cultist (ranged), Hound of Tindalos (fast melee)
- ✅ **Enemy spawning**: Random squad selection (4 squad types: balanced, cultist-only, hound-pack, mixed)
- ✅ **Equipment system**: 12 weapons with damage, range, attack type, accuracy modifiers
- ✅ **Combat deck system**: Personal 20-card decks for each investigator (similar to Gloomhaven)
- 📖 *See [docs/06_stat_system.md](docs/06_stat_system.md), [docs/09_equipment_system.md](docs/09_equipment_system.md), and [docs/11_combat_deck_system.md](docs/11_combat_deck_system.md) for details*

#### Combat Mechanics
- ✅ **Turn order**: Individual unit turns (random order, future: initiative-based)
- ✅ **Action points**: 2 actions per turn (Move-Move, Move-Attack, Attack-Attack)
- ✅ **Movement**: A* pathfinding, flood-fill for range calculation, click-to-move
- ✅ **Enemy AI**: Cultists move 1 tile to highest health, Hounds move 2 tiles to nearest
- ✅ **Visual feedback**: Dual highlights (green=current turn, yellow=selected), turn order tracker
- 📖 *See [docs/07_action_points_system.md](docs/07_action_points_system.md) and [docs/10_enemy_ai_system.md](docs/10_enemy_ai_system.md) for details*

#### Visual Rendering
- ✅ **Emoji font system**: Platform-specific emoji fonts with ASCII fallback
- ✅ **Team color coding**: Blue (player), Red (enemy)
- ✅ **Character portraits**: Unique image per investigator, no reuse
- ✅ **UI panels**: Investigator tiles (left), unit info (right), action bar (bottom)

#### Documentation
- ✅ **11 comprehensive guides** covering Pygame basics, architecture, UI, data flow, systems, AI, combat decks
- ✅ **Inline code comments** in all source files
- ✅ **Session archive** documenting development history
- 📖 *See [docs/doc_index.md](docs/doc_index.md) for full documentation index*

### 🚧 In Progress

**Next Task**: Combat Resolution (Attacks, Hit Chance, Line of Sight)

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
- ✅ Enemy AI movement complete (Cultists 1 tile, Hounds 2 tiles)
- ✅ Combat deck system complete (20-card decks, ready for attack resolution integration)
- ⏳ Line of Sight next (Bresenham's algorithm)
- ⏳ Combat resolution next (hit chance, damage application, deck integration)
- ⏳ Enemy AI attacks (after combat resolution)

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
│   ├── enemy_ai.py            # Enemy AI (targeting, movement behaviors)
│   └── battle_screen.py       # Battle UI, rendering, turn system, movement mode
│
├── entities/                  # Entity System
│   ├── unit.py                # Base Unit (with stat modifiers + equipment)
│   ├── investigator.py        # Player units (random names + portraits + weapons + combat decks)
│   ├── enemy.py               # Enemy units (Cultist, Hound + weapons)
│   ├── equipment.py           # Equipment system (weapons, armor, accessories)
│   └── combat_deck.py         # Combat deck system (Card, CombatDeck classes)
│
├── assets/                    # Game assets
│   ├── images/                # Character portraits (55 unique), sprites
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
│   ├── test_equipment.py
│   ├── test_enemy_ai.py
│   └── test_combat_deck.py
│
└── docs/                      # Documentation
    ├── doc_index.md           # Documentation index (START HERE)
    ├── session_archive.md     # Previous development sessions
    ├── 01_pygame_fundamentals.md
    ├── 02_architecture_overview.md
    ├── 03_ui_components.md
    ├── 04_data_flow.md
    ├── 05_grid_and_battle_system.md
    ├── 06_stat_system.md
    ├── 07_action_points_system.md
    ├── 08_terrain_tooltip_system.md
    ├── 09_equipment_system.md
    ├── 10_enemy_ai_system.md
    └── 11_combat_deck_system.md
```

---

## Quick Reference

### Running the Game

```bash
uv run python main.py
```

### Running Tests

```bash
# Run specific test
uv run python testing/test_equipment.py

# Run all tests (if pytest configured)
uv run pytest
```

### Project Documentation

- **Current state** → **CLAUDE.md** (this file)
- **Future plans** → [PLAN.md](PLAN.md)
- **Developer guide** → [CONTRIBUTING.md](CONTRIBUTING.md)
- **Code docs** → [docs/doc_index.md](docs/doc_index.md)
- **Session history** → [docs/session_archive.md](docs/session_archive.md)

### Key Files

- `main.py` - Entry point, screen navigation
- `config.py` - All game constants
- `combat/battle_screen.py` - Main battle UI
- `entities/investigator.py` - Player unit generation
- `ui/ui_elements.py` - Reusable UI components

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

## Documentation

### For New Developers

**Start here**: [docs/doc_index.md](docs/doc_index.md) - Complete documentation index

**Quick guides**:
1. [Pygame Fundamentals](docs/01_pygame_fundamentals.md) - Game loop, surfaces, events
2. [Architecture Overview](docs/02_architecture_overview.md) - Project structure, patterns
3. [UI Components](docs/03_ui_components.md) - Button system, callbacks
4. [Data Flow](docs/04_data_flow.md) - Event handling, rendering pipeline

**System details**:
- [Grid & Battle System](docs/05_grid_and_battle_system.md) - Tactical combat mechanics
- [Stat System](docs/06_stat_system.md) - Modifiers and properties
- [Action Points](docs/07_action_points_system.md) - 2-action economy
- [Tooltips](docs/08_terrain_tooltip_system.md) - Contextual UI
- [Equipment](docs/09_equipment_system.md) - Weapons and loadouts
- [Enemy AI](docs/10_enemy_ai_system.md) - AI targeting and movement

### Development History

**Recent sessions** (Sessions 4-10):
- [Session Archive](docs/session_archive.md) - Detailed development history including:
  - Session 10: Enemy AI System (movement behaviors)
  - Session 9: Equipment & Inventory System
  - Session 8: Terrain Tooltip System
  - Session 7: Movement & Action Points
  - Session 6: Turn Order Tracker Visual
  - Session 5: Turn Order System
  - Session 4: UI Enhancements & Character Portraits
  - Earlier sessions (2-3)

---

## MVP Goal

**Objective**: Get a single tactical battle playable with core mechanics working.

**Status**: ~99% Complete

**Remaining Features**:
- Line of sight calculation (Bresenham's algorithm)
- Combat resolution (hit chance, damage)
- Attack actions (ranged, melee)
- Enemy AI attacks (movement complete)

---

## Links

- **Future Roadmap**: [PLAN.md](PLAN.md) - Phases 2-5, system designs, long-term vision
- **Developer Guide**: [CONTRIBUTING.md](CONTRIBUTING.md) - Code style, architecture, workflows
- **Documentation Index**: [docs/doc_index.md](docs/doc_index.md) - All documentation files
- **Session History**: [docs/session_archive.md](docs/session_archive.md) - Development sessions 2-10

---

**Last Updated**: 2025-12-08 (Session 10.1 - Bug Fixes & Enemy Spawning)
**Version**: 2.4.1 (Random Enemy Squad Generation)
**Target Platform**: Windows/Mac/Linux Desktop
**Engine**: Pygame CE 2.5.x
**Python**: 3.10+
