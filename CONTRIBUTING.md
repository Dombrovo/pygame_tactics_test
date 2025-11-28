# Contributing to Eldritch Tactics

Thank you for your interest in contributing to Eldritch Tactics! This document provides guidelines for developers working on the project.

---

## Table of Contents

1. [Architecture Principles](#architecture-principles)
2. [Code Style & Conventions](#code-style--conventions)
3. [Project Structure](#project-structure)
4. [Adding New Features](#adding-new-features)
5. [Testing Guidelines](#testing-guidelines)
6. [Git Workflow](#git-workflow)
7. [Common Patterns](#common-patterns)

---

## Architecture Principles

### 1. Modularity
Every system should be self-contained and extensible:
- Add new enemies by extending the `Enemy` class
- Add new abilities by implementing the `Ability` interface
- Add new UI components without touching existing ones
- Keep dependencies minimal and explicit

### 2. Data-Driven Design
Store configuration in separate files, not hardcoded in logic:
- Unit stats → `entities/*.py` class definitions
- Game constants → `config.py`
- Name data → `assets/json/names_data.json`
- Future: Map layouts, enemy spawns, item definitions in JSON/YAML

### 3. Clear Separation of Concerns
- **`entities/`**: Game logic, stat calculations, unit behaviors
- **`combat/`**: Grid management, battle state, pathfinding
- **`ui/`**: Rendering, input handling, visual components
- **`config.py`**: All constants, no logic
- **`main.py`**: Orchestration only, minimal logic

### 4. Prefer Composition Over Inheritance
- Units have abilities (composition), rather than inheriting from AbilityUnit
- Use mixins for shared behaviors when inheritance is necessary
- Favor dependency injection for testability

---

## Code Style & Conventions

### Python Style

**Follow PEP 8** with these specifics:

```python
# Imports: stdlib → third-party → local
import random
from typing import Optional, List, Tuple

import pygame

from combat.grid import Grid
from entities.unit import Unit

# Constants: UPPER_SNAKE_CASE
MAX_HEALTH = 100
DEFAULT_ACCURACY = 75

# Classes: PascalCase
class Investigator(Unit):
    pass

# Functions/methods: snake_case
def calculate_hit_chance(attacker, target):
    pass

# Variables: snake_case
current_health = 15
movement_range = 4

# Type hints on all function signatures
def move_unit(grid: Grid, unit: Unit, x: int, y: int) -> bool:
    """Move a unit to a new position."""
    pass
```

### Docstrings

Use Google-style docstrings:

```python
def calculate_damage(attacker: Unit, target: Unit, is_critical: bool = False) -> int:
    """
    Calculate damage dealt from attacker to target.

    Args:
        attacker: The attacking unit
        target: The target being attacked
        is_critical: Whether this is a critical hit (default: False)

    Returns:
        Integer damage amount (before applying target's armor)

    Raises:
        ValueError: If attacker or target is None
    """
    pass
```

### Comments

- **Why over what**: Explain intent, not obvious code
- **TODO comments**: Use `TODO(name):` format
- **Complex logic**: Break down with inline comments

```python
# ✅ Good - explains why
# Clamp accuracy between 5-95% to prevent guaranteed hits/misses
final_accuracy = max(5, min(95, base_accuracy + modifiers))

# ❌ Bad - states the obvious
# Set final accuracy to max of 5 and min of 95
final_accuracy = max(5, min(95, base_accuracy + modifiers))

# TODO(claude): Add sanity damage resistance based on Will stat
```

---

## Project Structure

### Current Organization

```
pygame_tactics_test/
├── main.py               # Entry point, screen navigation
├── config.py             # All game constants
│
├── ui/                   # User interface components
│   ├── ui_elements.py    # Reusable components (Button, Tile, etc.)
│   ├── title_screen.py   # Title screen
│   └── settings_screen.py# Settings menu
│
├── combat/               # Battle systems
│   ├── grid.py           # Grid and Tile classes
│   └── battle_screen.py  # Battle UI and game loop
│
├── entities/             # Game entities
│   ├── unit.py           # Base Unit class
│   ├── investigator.py   # Player units
│   └── enemy.py          # Enemy units
│
├── assets/               # Game assets
│   ├── images/           # Sprites, portraits
│   └── json/             # Data files
│
├── testing/              # Test scripts
└── docs/                 # Documentation
```

### File Naming
- Python modules: `snake_case.py`
- Classes: `PascalCase`
- Test files: `test_feature_name.py`
- Documentation: `numbered_descriptive_name.md` (e.g., `01_pygame_fundamentals.md`)

---

## Adding New Features

### 1. UI Components

All UI components should:
- Extend a base pattern (see `ui_elements.py`)
- Implement `update(mouse_pos)`, `handle_event(event)`, `draw(screen)`
- Use callbacks for click handling
- Support hover states

**Example**:
```python
class MyComponent:
    def __init__(self, x, y, on_click=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.on_click = on_click
        self.is_hovered = False

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered:
            if self.on_click:
                self.on_click()
            return True
        return False

    def draw(self, screen):
        color = HOVER_COLOR if self.is_hovered else NORMAL_COLOR
        pygame.draw.rect(screen, color, self.rect)
```

### 2. Entities (Units, Enemies)

- Extend `Unit` base class
- Override `get_info_text()` for UI display
- Use properties for calculated stats (see stat system in `unit.py`)
- Add to appropriate generator function (`create_test_squad()`, etc.)

**Example**:
```python
class NewEnemy(Enemy):
    def __init__(self, name: str = "New Enemy"):
        super().__init__(
            name=name,
            max_health=12,
            max_sanity=10,
            accuracy=65,
            will=4,
            movement_range=5,
            symbol="👾",  # Or use ASCII fallback
            weapon_range=2,
            attack_type="ranged",
            sanity_damage=2
        )
```

### 3. Game Systems

- Create new module in appropriate directory
- Keep public API minimal
- Document all public functions/classes
- Add tests in `testing/` directory

---

## Testing Guidelines

### Manual Testing

**Before committing**:
1. Run the game: `uv run python main.py`
2. Test the feature you modified
3. Test basic navigation (title → battle → title)
4. Check for console errors

### Unit Tests

Create test files in `testing/`:

```python
# testing/test_my_feature.py

def test_feature():
    """Test description."""
    result = my_function(input)
    assert result == expected_output

if __name__ == "__main__":
    test_feature()
    print("✓ All tests passed")
```

Run tests:
```bash
uv run python testing/test_my_feature.py
```

### Integration Tests

For battle system tests, create scenarios:

```python
# testing/test_combat_scenario.py
from combat.grid import Grid
from entities.investigator import create_test_squad
from entities.enemy import create_test_enemies

def test_basic_combat():
    """Test a basic combat scenario."""
    grid = Grid(size=10)
    investigators = create_test_squad()
    enemies = create_test_enemies()

    # Place units
    grid.place_unit(investigators[0], 0, 0)
    grid.place_unit(enemies[0], 9, 9)

    # Test combat logic
    # ...
```

---

## Git Workflow

### Branches

- `main`: Stable, working code
- Feature branches: `feature/combat-mechanics`, `feature/roster-system`
- Bug fixes: `fix/selection-bug`, `fix/memory-leak`

### Commits

Write clear, descriptive commit messages:

```bash
# ✅ Good
git commit -m "Add pathfinding system using A* algorithm"
git commit -m "Fix investigator tile selection not updating on Tab press"
git commit -m "Update battle screen to show action points"

# ❌ Bad
git commit -m "stuff"
git commit -m "fixes"
git commit -m "WIP"
```

**Format**:
```
<verb> <what> [optional context]

- Bullet points for details if needed
- Keep first line under 72 characters
```

### Before Pushing

1. Test locally
2. Check for debug print statements
3. Update documentation if needed
4. Run any relevant test files

---

## Common Patterns

### 1. Callback Pattern (UI Events)

```python
def on_button_click():
    print("Button clicked!")

button = Button(x=100, y=100, text="Click Me", on_click=on_button_click)
```

### 2. Screen Navigation

```python
class MyScreen:
    def run(self, clock):
        """
        Main game loop for this screen.

        Returns:
            str: Name of next screen ("title", "battle", "quit", etc.)
        """
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                # ...

            # Update
            # ...

            # Draw
            # ...

            # FPS control
            clock.tick(60)

        return self.next_screen  # Return where to go next
```

### 3. Stat Modifiers

Use the base + modifier pattern (see `entities/unit.py`):

```python
class Unit:
    def __init__(self):
        # Base stats (immutable)
        self.base_accuracy = 75

        # Modifiers (mutable)
        self.accuracy_modifier = 0

    @property
    def accuracy(self) -> int:
        """Effective accuracy = base + modifiers."""
        return max(5, min(95, self.base_accuracy + self.accuracy_modifier))

# Usage
investigator.accuracy_modifier += 10  # Bonus from trait
print(investigator.accuracy)  # Automatically calculates
```

### 4. Grid Operations

```python
# Get tile
tile = grid.get_tile(x, y)

# Place unit
grid.place_unit(unit, x, y)

# Move unit
grid.move_unit(from_x, from_y, to_x, to_y)

# Distance
distance = grid.get_distance(x1, y1, x2, y2)

# Neighbors
neighbors = grid.get_neighbors(x, y, diagonal=True)
```

---

## Questions?

- **Project State**: See [CLAUDE.md](CLAUDE.md)
- **Future Plans**: See [PLAN.md](PLAN.md)
- **Documentation**: See [docs/doc_index.md](docs/doc_index.md)
- **Architecture**: See [docs/02_architecture_overview.md](docs/02_architecture_overview.md)

---

**Last Updated**: 2025-11-29
