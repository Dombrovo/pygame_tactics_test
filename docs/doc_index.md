# Eldritch Tactics - Code Documentation

Welcome to the Eldritch Tactics code documentation! This folder contains comprehensive guides explaining how the game works, from Pygame-CE fundamentals to detailed data flow diagrams.

---

## Quick Start

**New to the project?** Start with these files:

- **[CLAUDE.md](../CLAUDE.md)** - **START HERE** - Current project state, completed features, UV usage
- **[PLAN.md](../PLAN.md)** - Future roadmap, planned features (Phases 2-5)
- **[CONTRIBUTING.md](../CONTRIBUTING.md)** - Developer guidelines, code style, how to contribute

**Want to understand the code?** Read the guides below:

---

## Documentation Overview

### For New Python/Pygame Developers

Start here if you're new to Pygame or game development:

1. **[Pygame-CE Fundamentals](01_pygame_fundamentals.md)**
   - What is Pygame-CE and how does it work?
   - The game loop pattern
   - Core Pygame objects (Surface, Rect, Event, Clock)
   - RGB colors, coordinate system, and common patterns

### Understanding the Architecture

Once you understand Pygame basics, learn how Eldritch Tactics is structured:

2. **[Architecture Overview](02_architecture_overview.md)**
   - Project structure and file organization
   - Design principles (separation of concerns, centralized config)
   - Module breakdown (config.py, ui_elements.py, title_screen.py, main.py)
   - How screens work and navigate between each other

### Deep Dives

For detailed understanding of specific systems:

3. **[UI Components Deep Dive](03_ui_components.md)**
   - How the Button class works internally
   - Button lifecycle (creation, update, event handling, drawing)
   - The callback pattern explained
   - MenuButton inheritance example
   - Creating custom components

4. **[Data Flow & Interaction Patterns](04_data_flow.md)**
   - Complete system flow from startup to exit
   - Mouse click flow (frame-by-frame)
   - Event propagation (OS → Pygame → Buttons)
   - Rendering pipeline
   - State transitions and timing breakdown

5. **[Grid and Battle System](05_grid_and_battle_system.md)**
   - Grid system (10x10 battlefield, tiles, cover)
   - Entity system (Units, Investigators, Enemies)
   - Battle screen (rendering, turn management, controls)
   - Coordinate conversion (pixel ↔ grid)
   - Distance calculations and neighbor finding
   - Current limitations and next steps

6. **[Stat System with Modifiers](06_stat_system.md)**
   - Base stats + modifiers pattern
   - Property-based calculated stats
   - Applying modifiers (backgrounds, traits, injuries)
   - Stat clamping rules (min/max enforcement)
   - API reference and usage examples
   - Integration with backgrounds and equipment

7. **[Action Points System](07_action_points_system.md)**
   - 2-action economy design philosophy
   - Unit class integration (consume, check, reset)
   - ActionPointsDisplay UI component
   - Action bar smart enabling/disabling
   - Valid action combinations (Move-Move, Move-Attack, etc.)
   - Usage examples and testing

8. **[Terrain Tooltip System](08_terrain_tooltip_system.md)**
   - Tooltip UI component architecture
   - Tile tooltip data structure
   - Battle screen integration
   - Screen edge avoidance algorithm
   - Testing and bug fix documentation
   - User experience design

9. **[Equipment & Inventory System](09_equipment_system.md)**
   - Equipment framework (Equipment, Weapon, Armor, Accessory classes)
   - Weapon library (12 pre-defined weapons)
   - Unit integration (equipped_weapon, weapon properties)
   - Property-based stat delegation
   - Weapon modifiers and accuracy calculations
   - Automatic weapon assignment
   - Testing and usage examples

10. **[Enemy AI System](10_enemy_ai_system.md)**
   - AI targeting strategies (highest health vs nearest)
   - Movement behaviors (Cultists 1 tile, Hounds 2 tiles)
   - Pathfinding integration (A* to adjacent tiles)
   - Battle screen integration
   - Testing and debugging
   - Future enhancements (attack logic, advanced tactics)

11. **[Combat Deck System](11_combat_deck_system.md)** ⭐ NEW
   - Personal deck-based combat resolution (Gloomhaven-style)
   - Card system (NULL, x2, +2, +1, -1, +0)
   - Standard 20-card deck composition
   - Drawing, reshuffling, and statistics tracking
   - Investigator integration (personal decks)
   - Deck improvement and progression
   - Usage in attack resolution
   - Testing and examples

---

## Quick Reference

### Where to Find Things

| What You Want | Where to Look |
|---------------|---------------|
| Change button width | [config.py](../config.py) line 109 |
| Change screen resolution | [config.py](../config.py) lines 20-21 |
| Change grid/tile size | [config.py](../config.py) lines 94-95 |
| Understand how buttons work | [03_ui_components.md](03_ui_components.md) |
| Understand the game loop | [01_pygame_fundamentals.md](01_pygame_fundamentals.md) |
| Understand the battle system | [05_grid_and_battle_system.md](05_grid_and_battle_system.md) |
| Understand the stat system | [06_stat_system.md](06_stat_system.md) |
| Understand action points | [07_action_points_system.md](07_action_points_system.md) |
| Understand tooltips | [08_terrain_tooltip_system.md](08_terrain_tooltip_system.md) |
| Understand equipment system | [09_equipment_system.md](09_equipment_system.md) |
| Understand enemy AI | [10_enemy_ai_system.md](10_enemy_ai_system.md) |
| Understand combat deck system | [11_combat_deck_system.md](11_combat_deck_system.md) |
| See complete click flow | [04_data_flow.md](04_data_flow.md#mouse-click-flow---detailed) |
| Add a new menu option | [02_architecture_overview.md](02_architecture_overview.md#adding-a-new-screen) |
| Add a new enemy type | [05_grid_and_battle_system.md](05_grid_and_battle_system.md#enemy-classes) |
| Add a new weapon | [09_equipment_system.md](09_equipment_system.md#adding-new-weapons) |
| Apply stat modifiers | [06_stat_system.md](06_stat_system.md#usage-examples) |
| Consume action points | [07_action_points_system.md](07_action_points_system.md#usage-examples) |
| Equip weapons | [09_equipment_system.md](09_equipment_system.md#usage-examples) |
| Create tooltips | [08_terrain_tooltip_system.md](08_terrain_tooltip_system.md#creating-tooltips) |
| Use combat decks | [11_combat_deck_system.md](11_combat_deck_system.md#usage-in-combat-resolution) |
| Improve decks | [11_combat_deck_system.md](11_combat_deck_system.md#deck-progression-system-phase-2) |

### Code Files (with extensive comments)

All code files have been extensively commented:

- **[config.py](../config.py)** - All game constants with explanations
- **[main.py](../main.py)** - Entry point with step-by-step comments
- **[ui/ui_elements.py](../ui/ui_elements.py)** - UI components (Button, MenuButton, TextLabel, InvestigatorTile)
- **[ui/title_screen.py](../ui/title_screen.py)** - Title screen with positioning math explained
- **[ui/settings_screen.py](../ui/settings_screen.py)** - Settings menu
- **[combat/grid.py](../combat/grid.py)** - Grid and Tile system with cover mechanics
- **[combat/battle_screen.py](../combat/battle_screen.py)** - Battle UI, emoji font system, and rendering
- **[combat/enemy_ai.py](../combat/enemy_ai.py)** - Enemy AI targeting and movement behaviors
- **[entities/unit.py](../entities/unit.py)** - Base unit class with stat system + equipment
- **[entities/investigator.py](../entities/investigator.py)** - Player units with random names + weapons + combat decks
- **[entities/enemy.py](../entities/enemy.py)** - Enemy types (Cultist, Hound) + weapons
- **[entities/equipment.py](../entities/equipment.py)** - Equipment system (weapons, armor, accessories)
- **[entities/combat_deck.py](../entities/combat_deck.py)** - Combat deck system (Card, CombatDeck classes)
- **[assets/json/names_data.json](../assets/json/names_data.json)** - Name database (male/female/nicknames)

---

## Learning Path

### Beginner Path (Never used Pygame)

1. Read [Pygame Fundamentals](01_pygame_fundamentals.md) - Learn the basics
2. Run the game and observe: `uv run python main.py`
3. Read [main.py](../main.py) with comments - See initialization
4. Read [Architecture Overview](02_architecture_overview.md) - Understand structure
5. Click "New Game" and explore the battle screen (note random names!)
6. Read [Grid and Battle System](05_grid_and_battle_system.md) - Understand the grid
7. Read [Stat System](06_stat_system.md) - Understand stat modifiers
8. Experiment: Change colors in [config.py](../config.py) or modify unit stats

### Intermediate Path (Some Pygame experience)

1. Skim [Pygame Fundamentals](01_pygame_fundamentals.md) - Refresh concepts
2. Read [Architecture Overview](02_architecture_overview.md) - See our approach
3. Read [UI Components](03_ui_components.md) - Learn our UI system
4. Read [Grid and Battle System](05_grid_and_battle_system.md) - Understand tactical battle
5. Read [Stat System](06_stat_system.md) - Learn modifier pattern
6. Read [battle_screen.py](../combat/battle_screen.py) - See complete implementation
7. Experiment: Apply stat modifiers or create a new enemy type

### Advanced Path (Want to extend the system)

1. Read [Architecture Overview](02_architecture_overview.md#adding-a-new-screen) - Screen pattern
2. Read [Data Flow](04_data_flow.md) - Understand interaction patterns
3. Read [Grid and Battle System](05_grid_and_battle_system.md) - Combat system
4. Read [Stat System](06_stat_system.md) - Modifier implementation
5. Implement backgrounds/traits using stat modifiers
6. Implement movement or attack systems (see Next Session in [CLAUDE.md](../CLAUDE.md))
7. Create a new screen or UI component

---

## Key Concepts Explained

### The Game Loop

Every Pygame game follows this pattern (60 times per second):

```
while running:
    handle_events()  # Process input
    update()         # Update state
    draw()           # Render
    display.flip()   # Show
    clock.tick(60)   # Wait for 60 FPS
```

See: [Pygame Fundamentals - Game Loop](01_pygame_fundamentals.md#the-game-loop-pattern)

### The Callback Pattern

Buttons execute a function when clicked:

```python
def start_game():
    print("Starting!")

button = Button(..., on_click=start_game)
# When clicked, button calls start_game()
```

See: [UI Components - Callback Pattern](03_ui_components.md#the-callback-pattern)

### Centralized Configuration

All magic numbers go in one file:

```python
# config.py
MENU_BUTTON_WIDTH = 400

# Everywhere else:
button = Button(..., width=config.MENU_BUTTON_WIDTH)
```

See: [Architecture - Centralized Configuration](02_architecture_overview.md#2-centralized-configuration)

### Screen Navigation

Each screen has a `run()` method that returns where to go next:

```python
title_screen = TitleScreen(screen)
next_screen = title_screen.run(clock)  # Returns "new_game", "exit", etc.

if next_screen == "new_game":
    # Show battle screen
```

See: [Architecture - How Screens Work](02_architecture_overview.md#how-screens-work)

---

## Common Questions

### How do I add a new button?

1. Create the callback function in the screen class
2. Create a MenuButton with `on_click=your_function`
3. Add it to `self.buttons` list
4. It will automatically be updated and drawn

See: [Architecture - Adding New UI Elements](02_architecture_overview.md#adding-new-ui-elements)

### How do I change colors/sizes?

Edit [config.py](../config.py) - all visual constants are there.

### How do I debug event handling?

Add print statements in `handle_events()`:

```python
for event in pygame.event.get():
    print(f"Event: {pygame.event.event_name(event.type)}")
```

See: [Data Flow - Debugging](04_data_flow.md#debugging-data-flow)

### Why does my button not respond to clicks?

Check:
1. Is `update()` being called every frame?
2. Is `handle_event()` being called for each event?
3. Is the button in the `self.buttons` list?
4. Is `is_hovered` True when clicking?

See: [UI Components - Button Lifecycle](03_ui_components.md#button-lifecycle)

---

## Visual Aids

### System Architecture

```
main.py
  └─ Creates TitleScreen
      ├─ Contains MenuButtons
      │   └─ Each has callback
      └─ Runs game loop
          ├─ handle_events()
          ├─ update()
          ├─ draw()
          └─ flip() + tick()
```

### Click Flow

```
User clicks
  → OS event
    → Pygame captures
      → title_screen.handle_events()
        → button.handle_event()
          → Detects click
            → Calls callback
              → Sets next_screen
                → Loop exits
                  → Returns to main.py
```

See: [Data Flow - Complete diagrams](04_data_flow.md)

---

## Next Steps

### To Learn More

- **Pygame-CE Official Docs**: https://pyga.me/docs/
- **Real Python Pygame Tutorial**: https://realpython.com/pygame-a-primer/
- **UV Package Manager**: https://docs.astral.sh/uv/

### To Contribute

1. Read **[CONTRIBUTING.md](../CONTRIBUTING.md)** for code style and conventions
2. Check **[CLAUDE.md](../CLAUDE.md)** for current state
3. Check **[PLAN.md](../PLAN.md)** for future roadmap
4. Follow established patterns (screens, components, callbacks)
5. Add comments explaining your code

### To Extend

The system is designed to be extended:

- Add new screens (Settings, Battle, Campaign)
- Add new UI components (Slider, Dropdown, Dialog)
- Add new game features (following Phases 1-5 in PLAN.md)

### Development History

- **[session_archive.md](session_archive.md)** - Complete development sessions archive (Sessions 2-10)
  - Comprehensive details on all features implemented
  - Session 10: Enemy AI System
  - Session 9: Equipment & Inventory System
  - Session 8: Terrain Tooltip System
  - Session 7: Movement & Action Points
  - Session 6: Turn Order Tracker Visual
  - Session 5: Turn Order System
  - Session 4: UI Enhancements & Character Portraits
  - Earlier sessions (2-3)

---

## Documentation Maintenance

These docs should be updated when:

- New major features are added
- Architecture patterns change
- New components are created
- Performance characteristics change

Last updated: 2025-12-08 (Enemy AI System added)
Version: 0.1.0 (MVP Phase 1 - 99% Complete)

**Note**: CLAUDE.md has been streamlined. For detailed session histories, see [session_archive.md](session_archive.md).

---

## Feedback

Found something confusing? Have suggestions? These docs are meant to help you understand the code. Let us know what could be clearer!

**Happy coding! 🎲🐙**
