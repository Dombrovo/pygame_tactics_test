# Architecture Overview

This document explains the high-level structure of Eldritch Tactics and how all the pieces fit together.

## Project Structure

```
pygame_tactics_test/
├── main.py                    # Entry point - orchestrates everything
├── config.py                  # Centralized configuration constants
├── ui/
│   ├── __init__.py           # Package marker
│   ├── ui_elements.py        # Reusable UI components (Button, Label)
│   └── title_screen.py       # Title screen implementation
├── docs/                      # Documentation (you are here!)
│   ├── 01_pygame_fundamentals.md
│   ├── 02_architecture_overview.md
│   ├── 03_ui_components.md
│   └── 04_data_flow.md
├── pyproject.toml            # Project metadata and dependencies
└── README.md                 # Project introduction
```

---

## Design Principles

### 1. Separation of Concerns

Each file/module has ONE clear responsibility:

| File | Responsibility |
|------|----------------|
| `config.py` | Store all constants (colors, sizes, game rules) |
| `ui_elements.py` | Define reusable UI components |
| `title_screen.py` | Implement the title screen |
| `main.py` | Initialize Pygame and orchestrate screens |

**Why this matters:**
- Easy to find code ("Where do I change button width?" → config.py)
- Easy to test (each module can be tested independently)
- Easy to extend (add new screens without touching existing code)

### 2. Centralized Configuration

ALL magic numbers go in `config.py`:

```python
# ❌ BAD - scattered throughout codebase
button = Button(100, 100, 400, 80)  # What do these numbers mean?
screen.fill((15, 15, 25))           # What color is this?

# ✅ GOOD - centralized in config.py
button = Button(100, 100, config.MENU_BUTTON_WIDTH, config.MENU_BUTTON_HEIGHT)
screen.fill(config.COLOR_BG)
```

**Benefits:**
- Change one value, affects everything
- No hunting through code for hardcoded numbers
- Easy to experiment with different settings

### 3. Composition Over Inheritance

We use **composition** (containing objects) more than inheritance:

```python
# TitleScreen CONTAINS buttons and labels
class TitleScreen:
    def __init__(self):
        self.buttons = [
            MenuButton(...),
            MenuButton(...),
        ]
        self.title = TextLabel(...)
```

**Why composition?**
- More flexible than inheritance
- Easier to understand (just a list of objects)
- Can add/remove components dynamically

### 4. Data-Driven Design

UI elements are **data**, not code:

```python
# Instead of hardcoding UI in code, we could load from JSON:
# {
#   "buttons": [
#     {"text": "New Game", "x": 760, "y": 490},
#     {"text": "Continue", "x": 760, "y": 580}
#   ]
# }
```

This makes it easy to:
- Modify UI without touching code
- Support multiple languages
- Create UI editors

---

## Module Breakdown

### config.py - Configuration Hub

**Purpose:** Store all game constants in one place

**What it contains:**
- Display settings (resolution, FPS, fullscreen)
- Colors (background, buttons, text)
- UI dimensions (button sizes, spacing)
- Game rules (hit chances, squad sizes)

**Usage pattern:**
```python
import config

# Access constants
screen = pygame.display.set_mode(
    (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
)
```

**See:** [Full code with comments](../config.py)

---

### ui/ui_elements.py - Reusable Components

**Purpose:** Define UI widgets that can be used anywhere

**What it contains:**
- `Button` - Base interactive button class
- `MenuButton` - Specialized menu button (extends Button)
- `TextLabel` - Non-interactive text display

**Design pattern: Self-contained components**

Each component knows how to:
- Update itself (check hover state)
- Handle events (detect clicks)
- Draw itself (render to screen)

**Example:**
```python
button = MenuButton(x, y, "Click Me", on_click=my_function)

# In game loop:
button.update(mouse_pos)       # Update hover state
button.handle_event(event)     # Check for clicks
button.draw(screen)            # Render
```

**Key concept: Callback pattern**
```python
def start_game():
    print("Game starting!")

button = Button(..., on_click=start_game)
# When button is clicked, it calls start_game()
```

**See:** [Full code with comments](../ui/ui_elements.py)

---

### ui/title_screen.py - Title Screen

**Purpose:** Implement the main menu

**What it contains:**
- Title screen UI layout
- Button positioning logic
- Game loop for the title screen
- Event handling and navigation

**Structure:**
```python
class TitleScreen:
    def __init__(self, screen):
        # Create all UI elements
        self.buttons = [...]
        self.title = TextLabel(...)

    def handle_events(self):
        # Process input

    def update(self):
        # Update button states

    def draw(self):
        # Render everything

    def run(self, clock):
        # Game loop
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        return self.next_screen
```

**See:** [Full code with comments](../ui/title_screen.py)

---

### main.py - Entry Point & Orchestrator

**Purpose:** Initialize Pygame and coordinate screens

**Responsibilities:**
1. Initialize Pygame (`pygame.init()`)
2. Create display window
3. Create master clock
4. Show title screen
5. Handle navigation between screens
6. Clean up on exit

**Flow:**
```python
def main():
    pygame.init()
    screen = pygame.display.set_mode(...)
    clock = pygame.time.Clock()

    # Show title screen
    title_screen = TitleScreen(screen)
    choice = title_screen.run(clock)

    # Handle user's choice
    if choice == "new_game":
        # TODO: Show battle screen
        pass

    pygame.quit()
    sys.exit(0)
```

**See:** [Full code with comments](../main.py)

---

## How Screens Work

Each screen (title, battle, settings) follows the same pattern:

### 1. Screen Class Template

```python
class SomeScreen:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.running = True
        # Create UI elements

    def handle_events(self) -> None:
        # Process input
        for event in pygame.event.get():
            # Handle events

    def update(self) -> None:
        # Update game state

    def draw(self) -> None:
        # Render everything
        self.screen.fill(config.COLOR_BG)
        # Draw UI elements

    def run(self, clock: pygame.time.Clock) -> str:
        # Main loop
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(config.FPS)

        return self.next_screen  # Where to go next
```

### 2. Adding a New Screen

To add a new screen (e.g., Settings):

1. **Create the screen class** (`ui/settings_screen.py`):
   ```python
   class SettingsScreen:
       # ... follow template above ...
   ```

2. **Import in main.py**:
   ```python
   from ui.settings_screen import SettingsScreen
   ```

3. **Handle navigation**:
   ```python
   if next_screen == "settings":
       settings = SettingsScreen(screen)
       next_screen = settings.run(clock)
   ```

That's it! The screen is integrated.

---

## Object Relationships

### Composition Hierarchy

```
TitleScreen
├── Contains: screen (Surface)
├── Contains: buttons (list of MenuButtons)
│   └── Each MenuButton contains:
│       ├── rect (pygame.Rect)
│       ├── text (str)
│       ├── on_click (callback function)
│       └── colors (tuples)
├── Contains: title (TextLabel)
├── Contains: subtitle (TextLabel)
└── Contains: flavor_text (TextLabel)
```

### Inheritance Hierarchy

```
Button
└── MenuButton (adds enabled/disabled state)
```

**Why minimal inheritance?**
- Easier to understand (shallow hierarchy)
- More flexible (can't inherit from multiple classes)
- Composition is often clearer

---

## Data Flow

### User Input → UI Response

```
1. User clicks mouse
   ↓
2. OS generates event
   ↓
3. Pygame captures event
   ↓
4. title_screen.handle_events() gets event
   ↓
5. Forwards to all buttons
   ↓
6. Button checks if click was on it
   ↓
7. Button calls on_click callback
   ↓
8. Callback sets next_screen and running=False
   ↓
9. Title screen loop exits
   ↓
10. main.py receives next_screen value
   ↓
11. main.py navigates to next screen
```

**See:** [Data Flow Guide](04_data_flow.md) for detailed diagrams

---

## Extension Points

### Adding New UI Elements

To add a new component (e.g., Slider):

1. Add class to `ui_elements.py`:
   ```python
   class Slider:
       def __init__(self, x, y, width, min_val, max_val):
           # ...

       def update(self, mouse_pos):
           # Check if dragging

       def handle_event(self, event):
           # Handle mouse down/up

       def draw(self, screen):
           # Render slider bar and handle
   ```

2. Use it like any other component:
   ```python
   slider = Slider(100, 100, 300, 0, 100)
   slider.update(mouse_pos)
   slider.draw(screen)
   ```

### Adding Game State

For Phase 2+ (campaign, roster), we'll add:

```
game_state.py         # Global game state
campaign/
├── campaign.py       # Campaign screen
├── roster.py         # Investigator management
└── mission_select.py # Mission selection
```

---

## Testing Strategy

### Manual Testing

Run the game and verify:
- Buttons respond to hover (change color)
- Clicks execute correct actions
- Keyboard shortcuts work (ESC, Enter)
- Window closes properly

### Unit Testing (Future)

```python
# tests/test_ui_elements.py
def test_button_hover():
    button = Button(0, 0, 100, 50, "Test")
    button.update((50, 25))  # Mouse in center
    assert button.is_hovered == True

    button.update((200, 200))  # Mouse far away
    assert button.is_hovered == False
```

---

## Performance Considerations

### Current Performance

- 60 FPS easily achieved on modern hardware
- Title screen has minimal rendering (just a few buttons)
- No performance concerns at this stage

### Future Optimizations (when needed)

1. **Dirty Rectangle Rendering**
   - Only redraw changed areas
   - Use `pygame.display.update(rect_list)`

2. **Object Pooling**
   - Reuse objects instead of creating/destroying
   - Important for bullets, particles, etc.

3. **Spatial Partitioning**
   - For collision detection in battle
   - Grid-based or quadtree

---

## Next Steps

- [UI Components Deep Dive](03_ui_components.md) - Learn how buttons work internally
- [Data Flow Diagrams](04_data_flow.md) - Trace event handling step-by-step
- [Pygame Fundamentals](01_pygame_fundamentals.md) - Core Pygame concepts

---

## Summary

Eldritch Tactics uses a **modular, screen-based architecture**:

- **config.py** - All constants in one place
- **ui_elements.py** - Reusable components
- **title_screen.py** - Self-contained screen with its own game loop
- **main.py** - Orchestrates screens and handles navigation

Each screen follows the same pattern:
1. Create UI elements in `__init__()`
2. Handle events, update state, draw
3. Run game loop until user makes choice
4. Return where to go next

This architecture makes it easy to:
- Add new screens
- Modify existing screens
- Test components independently
- Understand code flow
