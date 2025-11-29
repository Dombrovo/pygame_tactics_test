# UI Components Deep Dive

This guide explains how the reusable UI components work internally, with focus on the Button class.

## Overview

The `ui/ui_elements.py` module provides reusable UI components:

1. **Button** - Base interactive button with hover/click detection
2. **MenuButton** - Menu-specific button with enabled/disabled state
3. **TextLabel** - Simple non-interactive text display
4. **InvestigatorTile** - Battle screen status tile for investigators
5. **ActionButton** - Action bar slot button with hotkey support
6. **ActionBar** - 10-slot ability/action bar for battle screen

---

## Button Class

### Purpose

The Button class is a **self-contained interactive element** that:
- Manages its own visual state (normal, hovered, pressed)
- Detects mouse hover and clicks
- Executes a callback function when clicked
- Integrates seamlessly with the game loop

### Anatomy of a Button

```python
button = Button(
    x=100,           # Left edge position
    y=50,            # Top edge position
    width=200,       # Width in pixels
    height=80,       # Height in pixels
    text="Click Me", # Button label
    font_size=48,    # Text size
    on_click=my_function  # Callback when clicked
)
```

### Internal State

```python
class Button:
    # Position and size
    self.rect = pygame.Rect(x, y, width, height)

    # Visual properties
    self.text = "Click Me"
    self.font_size = 48

    # State flags (change every frame)
    self.is_hovered = False  # Mouse over button?
    self.is_pressed = False  # Button being clicked?

    # Callback
    self.on_click = my_function  # Function to call on click

    # Colors for each state
    self.color_normal = (40, 40, 60)
    self.color_hover = (60, 60, 90)
    self.color_active = (80, 80, 120)
```

---

## Button Lifecycle

### 1. Creation (`__init__`)

```python
button = Button(100, 50, 200, 80, "Start Game", on_click=start_game)
```

**What happens:**
1. Creates a `pygame.Rect` at (100, 50) with size 200x80
2. Stores the text "Start Game"
3. Stores the callback function `start_game`
4. Initializes state flags to False
5. Loads colors from config

**Memory allocated:** ~500 bytes per button

### 2. Update Loop (`update`)

Called **every frame** (60 times per second) in the game loop:

```python
# In title_screen.py update():
mouse_pos = pygame.mouse.get_pos()  # e.g., (450, 320)
button.update(mouse_pos)
```

**Button.update() internal logic:**
```python
def update(self, mouse_pos: Tuple[int, int]) -> None:
    # Check if mouse is inside button rectangle
    self.is_hovered = self.rect.collidepoint(mouse_pos)
```

**collidepoint() explained:**
```python
# pygame.Rect.collidepoint() checks if point is inside rectangle
rect = pygame.Rect(100, 50, 200, 80)
# Rectangle spans: x=100 to 300, y=50 to 130

rect.collidepoint((150, 100))  # True - inside
rect.collidepoint((50, 100))   # False - left of rectangle
rect.collidepoint((150, 200))  # False - below rectangle
```

### 3. Event Handling (`handle_event`)

Called **for each input event** from pygame.event.get():

```python
# In title_screen.py handle_events():
for event in pygame.event.get():
    button.handle_event(event)
```

**Click Detection: Two-Step Process**

```
User clicks button:
    Step 1: MOUSEBUTTONDOWN
        ├─ Is mouse over button? → YES
        ├─ Set is_pressed = True
        └─ Return False (not complete yet)

    User holds button down...

    Step 2: MOUSEBUTTONUP
        ├─ Is mouse still over button? → YES
        ├─ Was button pressed earlier? → YES
        ├─ EXECUTE CALLBACK: on_click()
        ├─ Set is_pressed = False
        └─ Return True (complete click!)
```

**Why two steps?**
Allows user to change their mind:
1. Press down on button
2. Drag mouse away (no longer hovering)
3. Release mouse
4. Does NOT count as click!

**Code:**
```python
def handle_event(self, event: pygame.event.Event) -> bool:
    # Step 1: Mouse pressed down
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if self.is_hovered:
            self.is_pressed = True
            return False  # Incomplete

    # Step 2: Mouse released
    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        if self.is_hovered and self.is_pressed:
            self.is_pressed = False
            if self.on_click:
                self.on_click()  # EXECUTE CALLBACK
            return True  # Complete click!
        self.is_pressed = False

    return False
```

### 4. Drawing (`draw`)

Called **every frame** (60 times per second):

```python
# In title_screen.py draw():
button.draw(screen)
```

**Rendering order (layers):**

```python
def draw(self, screen: pygame.Surface) -> None:
    # 1. Choose color based on state
    if self.is_pressed:
        color = self.color_active    # Brightest
    elif self.is_hovered:
        color = self.color_hover     # Medium
    else:
        color = self.color_normal    # Darkest

    # 2. Draw filled rectangle (background)
    pygame.draw.rect(screen, color, self.rect)

    # 3. Draw border (outline)
    border_width = 3 if self.is_hovered else 2
    pygame.draw.rect(screen, self.color_border, self.rect, border_width)

    # 4. Render text to a surface
    font = pygame.font.Font(None, self.font_size)
    text_surface = font.render(self.text, True, text_color)

    # 5. Center text on button
    text_rect = text_surface.get_rect(center=self.rect.center)

    # 6. Draw text surface onto button
    screen.blit(text_surface, text_rect)
```

**Visual result:**
```
┌─────────────────────┐
│                     │  ← Border (2px normally, 3px when hovered)
│    Click Me         │  ← Text centered
│                     │
└─────────────────────┘
     ↑
  Background color (changes based on state)
```

---

## The Callback Pattern

### What is a Callback?

A **callback** is a function passed to another function to be called later.

```python
# Define a function
def start_game():
    print("Game starting!")

# Pass function as parameter (NO PARENTHESES!)
button = Button(..., on_click=start_game)

# Later, button calls it:
self.on_click()  # Executes start_game()
```

### Why Use Callbacks?

**Without callbacks (bad):**
```python
# Button has to know about the game
class Button:
    def on_click(self):
        game.start()  # Button depends on game!
```

**With callbacks (good):**
```python
# Button is reusable, game tells it what to do
class Button:
    def __init__(self, on_click):
        self.on_click = on_click

# Different uses:
button1 = Button(..., on_click=start_game)
button2 = Button(..., on_click=quit_game)
button3 = Button(..., on_click=open_settings)
```

**Benefits:**
- Button doesn't need to know about the game
- Same Button class works anywhere
- Easy to test (just check if callback was called)

### Callback Examples

```python
# Simple function
def say_hello():
    print("Hello!")
button = Button(..., on_click=say_hello)

# Method from a class
class TitleScreen:
    def on_new_game(self):
        self.next_screen = "new_game"
        self.running = False

    def __init__(self):
        button = Button(..., on_click=self.on_new_game)
        # Note: self.on_new_game is the method

# Lambda (inline function)
button = Button(..., on_click=lambda: print("Clicked!"))

# Function with parameters (use lambda)
def start_level(level_num):
    print(f"Starting level {level_num}")

button = Button(..., on_click=lambda: start_level(5))
```

---

## MenuButton - Inheritance Example

MenuButton **extends** Button to add enabled/disabled state.

### Inheritance Relationship

```python
class Button:
    # Base features
    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

class MenuButton(Button):
    # Inherited features + new features
    def __init__(self, ...):
        super().__init__(...)  # Call Button's __init__
        self.enabled = True    # Add new feature

    def update(self, mouse_pos):
        # Override Button's update
        if self.enabled:
            super().update(mouse_pos)  # Call Button's version
        else:
            self.is_hovered = False     # Disabled can't hover
```

### What MenuButton Adds

1. **enabled attribute** - Can button be clicked?
2. **Disabled appearance** - Grayed out when disabled
3. **Ignore events when disabled** - No hover or clicks

### Usage Example

```python
# Enable button if save file exists
has_save = check_for_save_file()

continue_button = MenuButton(
    x=760,
    y=580,
    text="Continue",
    on_click=load_game,
    enabled=has_save  # Disabled if no save
)
```

**Visual difference:**
```
Enabled:   [  Continue  ]  ← Normal colors, responds to hover
Disabled:  [  Continue  ]  ← Dim gray, no hover effect
```

---

## TextLabel - Simple Display

TextLabel is **not interactive** - it just shows text.

```python
title = TextLabel(
    x=960,               # X position
    y=240,               # Y position
    text="ELDRITCH TACTICS",
    font_size=120,
    color=(255, 200, 100),  # Golden
    center=True          # Treat (x,y) as center
)
```

### Positioning Modes

```python
# center=False (default): (x,y) is TOP-LEFT corner
label1 = TextLabel(0, 0, "Top Left", center=False)
# Text starts at (0, 0)

# center=True: (x,y) is CENTER of text
label2 = TextLabel(960, 540, "Centered", center=True)
# Text is centered at (960, 540)
```

### When to Use TextLabel vs Button

| Use Case | Component |
|----------|-----------|
| Display information | TextLabel |
| Clickable action | Button |
| Menu option | MenuButton |
| Title/heading | TextLabel |
| Dynamic text (score, health) | TextLabel with update_text() |

---

## Component Comparison Table

| Feature | Button | MenuButton | TextLabel |
|---------|--------|------------|-----------|
| Interactive | ✅ Yes | ✅ Yes | ❌ No |
| Hover effect | ✅ Yes | ✅ Yes | ❌ No |
| Click detection | ✅ Yes | ✅ Yes | ❌ No |
| Callback | ✅ Yes | ✅ Yes | ❌ No |
| Enabled/disabled | ❌ No | ✅ Yes | N/A |
| Update text | ❌ No | ❌ No | ✅ Yes |
| Center alignment | ❌ No | ❌ No | ✅ Yes |

---

## Creating Custom Components

### Template for New Component

```python
class MyComponent:
    """
    Brief description of component
    """

    def __init__(self, x, y, ...):
        """Initialize component"""
        self.rect = pygame.Rect(x, y, width, height)
        # ... other attributes ...

    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """Update component state (called every frame)"""
        # Check hover, update animations, etc.
        pass

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle input events"""
        # Check for clicks, key presses, etc.
        return False

    def draw(self, screen: pygame.Surface) -> None:
        """Render component"""
        # Draw to screen
        pass
```

### Example: Creating a Checkbox

```python
class Checkbox:
    """Interactive checkbox component"""

    def __init__(self, x, y, label, checked=False):
        self.rect = pygame.Rect(x, y, 20, 20)  # 20x20 box
        self.label = label
        self.checked = checked
        self.is_hovered = False

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.is_hovered:
                self.checked = not self.checked  # Toggle
                return True
        return False

    def draw(self, screen):
        # Draw box
        color = (100, 100, 140) if self.is_hovered else (60, 60, 90)
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2)

        # Draw checkmark if checked
        if self.checked:
            pygame.draw.line(screen,
                           (255, 255, 255),
                           (self.rect.x + 5, self.rect.centery),
                           (self.rect.centerx, self.rect.bottom - 5),
                           3)
            pygame.draw.line(screen,
                           (255, 255, 255),
                           (self.rect.centerx, self.rect.bottom - 5),
                           (self.rect.right - 5, self.rect.top + 5),
                           3)

        # Draw label
        font = pygame.font.Font(None, 36)
        text = font.render(self.label, True, (220, 220, 230))
        screen.blit(text, (self.rect.right + 10, self.rect.y))
```

---

## Performance Considerations

### Button Performance

**Memory per button:** ~500 bytes
- pygame.Rect: 16 bytes
- Strings: ~50-100 bytes
- Colors (tuples): ~100 bytes
- Callback reference: 8 bytes
- Other attributes: ~300 bytes

**Rendering cost:**
- `draw.rect()`: Very fast (hardware accelerated)
- `font.render()`: ~0.1ms per call
- `blit()`: ~0.01ms per call

**Title screen total:** 4 buttons + 3 labels = ~3.5KB memory, <1ms to render

### Optimization Tips

**Don't recreate objects every frame:**
```python
# ❌ BAD
def draw(self, screen):
    font = pygame.font.Font(None, 48)  # Creates new font every frame!
    text = font.render(self.text, True, color)

# ✅ GOOD
def __init__(self, ...):
    self.font = pygame.font.Font(None, 48)  # Create once

def draw(self, screen):
    text = self.font.render(self.text, True, color)
```

**Cache rendered text if it doesn't change:**
```python
# For static text
def __init__(self, ...):
    font = pygame.font.Font(None, 48)
    self.text_surface = font.render("Click Me", True, WHITE)
    # Render once, reuse every frame

def draw(self, screen):
    screen.blit(self.text_surface, self.rect)  # Just blit cached surface
```

---

## Testing UI Components

### Manual Testing Checklist

For each button:
- [ ] Appears at correct position
- [ ] Changes color on hover
- [ ] Changes color when pressed
- [ ] Executes callback when clicked
- [ ] Doesn't trigger if dragged away
- [ ] Border thickness increases on hover
- [ ] Text is centered properly

### Unit Test Example

```python
import pygame
from ui.ui_elements import Button

def test_button_hover():
    """Test button hover detection"""
    pygame.init()

    button = Button(100, 100, 200, 50, "Test")

    # Mouse inside button
    button.update((150, 125))
    assert button.is_hovered == True

    # Mouse outside button
    button.update((50, 50))
    assert button.is_hovered == False

def test_button_click():
    """Test button click callback"""
    clicked = []

    def on_click():
        clicked.append(True)

    button = Button(0, 0, 100, 50, "Test", on_click=on_click)
    button.is_hovered = True

    # Simulate click
    down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
    up_event = pygame.event.Event(pygame.MOUSEBUTTONUP, button=1)

    button.handle_event(down_event)
    assert len(clicked) == 0  # Not triggered yet

    button.handle_event(up_event)
    assert len(clicked) == 1  # Triggered!
```

---

## ActionButton Class

### Purpose

The ActionButton class is a **specialized button for action bars**:
- Small square button (70×70px) for ability/action slots
- Displays icon/emoji and text label
- Shows hotkey number in top-left corner
- Enabled/disabled states with visual feedback
- Hover and pressed states

### Anatomy of an ActionButton

```python
action_button = ActionButton(
    x=100,
    y=500,
    size=70,                    # Width and height (square)
    text="Move",                # Action label
    icon="↗",                   # Icon/emoji symbol
    on_click=move_action,       # Callback when clicked
    enabled=True,               # Whether button can be clicked
    hotkey="1"                  # Keyboard shortcut
)
```

### Visual States

```python
# Enabled and idle
bg_color = (40, 40, 55)         # Dark blue-gray
border_color = (100, 100, 140)  # Gray border
border_width = 2

# Enabled and hovered
bg_color = (60, 60, 80)         # Lighter blue-gray
border_color = (255, 200, 100)  # Golden border
border_width = 3

# Enabled and pressed
bg_color = (80, 80, 110)        # Even lighter blue-gray

# Disabled
bg_color = (25, 25, 35)         # Very dark
text_color = (120, 120, 130)    # Dimmed text
```

### Usage Example

```python
# Create action button
move_button = ActionButton(
    x=565, y=920,
    size=70,
    text="Move",
    icon="↗",
    on_click=lambda: execute_move(),
    enabled=True,
    hotkey="1"
)

# In game loop
move_button.update(mouse_pos)
move_button.handle_event(event)
move_button.draw(screen)

# Enable/disable dynamically
if unit.has_moved:
    move_button.set_enabled(False)
```

---

## ActionBar Class

### Purpose

The ActionBar manages a **row of 10 action slots** for the battle screen:
- Displays available actions for selected investigator
- Updates when selection changes
- Supports mouse clicks and keyboard hotkeys (1-0)
- Auto-enables/disables based on investigator state

### Anatomy of an ActionBar

```python
action_bar = ActionBar(
    x=565,           # Left edge (centered on 1920px screen)
    y=920,           # Top edge (below grid)
    button_size=70,  # Size of each button
    spacing=10       # Gap between buttons
)
```

### Layout Calculation

```
Total width = (button_size × 10) + (spacing × 9)
            = (70 × 10) + (10 × 9)
            = 700 + 90
            = 790 pixels

Centered X = (SCREEN_WIDTH - total_width) / 2
           = (1920 - 790) / 2
           = 565 pixels
```

### Internal Structure

```python
class ActionBar:
    def __init__(self, x, y, button_size, spacing):
        self.action_buttons = []  # List of 10 ActionButtons
        self.current_investigator = None

        # Create 10 slots with hotkeys 1-9, 0
        for i in range(10):
            button_x = x + (i * (button_size + spacing))
            hotkey = str((i + 1) % 10)  # 1,2,3...9,0
            button = ActionButton(
                x=button_x, y=y,
                size=button_size,
                hotkey=hotkey,
                on_click=lambda idx=i: self._on_action_click(idx)
            )
            self.action_buttons.append(button)
```

### Update Pattern

```python
# When investigator is selected
def update_for_investigator(self, investigator):
    if investigator and not investigator.is_incapacitated:
        # Enable available actions
        self.action_buttons[0].text = "Move"
        self.action_buttons[0].icon = "↗"
        self.action_buttons[0].enabled = True

        self.action_buttons[1].text = "Attack"
        self.action_buttons[1].icon = "⚔"
        self.action_buttons[1].enabled = True

        # Disable empty slots
        for i in range(2, 10):
            self.action_buttons[i].enabled = False
    else:
        # No selection or incapacitated - disable all
        for button in self.action_buttons:
            button.enabled = False
```

### Keyboard Hotkey Support

```python
def handle_event(self, event):
    # Check mouse clicks on buttons
    for button in self.action_buttons:
        if button.handle_event(event):
            return True

    # Check keyboard hotkeys (1-0)
    if event.type == pygame.KEYDOWN:
        if pygame.K_1 <= event.key <= pygame.K_9:
            slot_index = event.key - pygame.K_1  # 0-8
            if self.action_buttons[slot_index].enabled:
                self._on_action_click(slot_index)
                return True
        elif event.key == pygame.K_0:
            if self.action_buttons[9].enabled:
                self._on_action_click(9)
                return True
```

### Battle Screen Integration

```python
class BattleScreen:
    def __init__(self, screen):
        # ... other initialization ...

        # Create action bar
        action_bar_width = 10 * 70 + 9 * 10  # 790px
        action_bar_x = (config.SCREEN_WIDTH - action_bar_width) // 2
        action_bar_y = self.grid_offset_y + self.grid_pixel_size + 20

        self.action_bar = ActionBar(
            x=action_bar_x,
            y=action_bar_y,
            button_size=70,
            spacing=10
        )

    def _on_investigator_tile_click(self, investigator):
        self.selected_unit = investigator
        self._update_action_bar()  # Sync action bar with selection

    def _update_action_bar(self):
        if self.selected_unit:
            self.action_bar.update_for_investigator(self.selected_unit)
        else:
            self.action_bar.clear()

    def update(self):
        self.action_bar.update(self.mouse_pos)  # Update hover states

    def handle_events(self):
        for event in pygame.event.get():
            # Action bar handles events first (including hotkeys)
            if self.action_bar.handle_event(event):
                continue
            # ... other event handling ...

    def draw(self):
        # ... draw grid, units, etc. ...
        self.action_bar.draw(self.screen)  # Draw action bar
```

### Visual Layout

```
┌────────────────────────────────────────────────────┐
│              TURN 1 | PLAYER PHASE                 │
├─────────────┬──────────────────┬────────────────────┤
│ Inv Tile 1  │                  │ Selected Unit Info │
├─────────────┤   10×10 GRID     │                    │
│ Inv Tile 2  │   (800×800)      │                    │
├─────────────┤                  │                    │
│ Inv Tile 3  │                  │                    │
├─────────────┤                  │                    │
│ Inv Tile 4  │                  │                    │
└─────────────┴──────────────────┴────────────────────┘
             ┌────────────────────┐
             │    ACTION BAR      │ (790px wide)
             │ [1][2][3][4]...[0] │ (10 buttons)
             └────────────────────┘
                   ↑ centered ↑
```

### Future Enhancements

The action bar is designed to be extensible for Phase 2+:

```python
# Add abilities from investigator
def update_for_investigator(self, investigator):
    # Populate from investigator.abilities list
    for i, ability in enumerate(investigator.abilities):
        if i < 10:  # Max 10 slots
            self.action_buttons[i].text = ability.name
            self.action_buttons[i].icon = ability.icon
            self.action_buttons[i].enabled = ability.can_use()

# Cooldown visualization
class ActionButton:
    def draw(self, screen):
        # ... existing drawing ...

        # Draw cooldown overlay
        if self.cooldown_remaining > 0:
            # Semi-transparent dark overlay
            overlay = pygame.Surface((self.rect.width, self.rect.height))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, self.rect)

            # Draw cooldown number
            font = pygame.font.Font(None, 48)
            text = font.render(str(self.cooldown_remaining), True, (255, 255, 255))
            screen.blit(text, self.rect.center)
```

---

## Next Steps

- [Data Flow Guide](04_data_flow.md) - Trace how clicks flow through the system
- [Architecture Overview](02_architecture_overview.md) - High-level structure
- [Pygame Fundamentals](01_pygame_fundamentals.md) - Core concepts
- [Grid and Battle System](05_grid_and_battle_system.md) - Battle screen details

---

## Summary

**Key Takeaways:**

1. **Self-contained** - Components manage their own state and rendering
2. **Callback pattern** - Makes components reusable
3. **Game loop integration** - update() and draw() called every frame
4. **Two-step click** - Press down + release up = complete click
5. **Inheritance** - MenuButton extends Button to add features

**The pattern:**
```python
component = Component(...)     # Create
component.update(mouse_pos)    # Update (every frame)
component.handle_event(event)  # Handle events (per event)
component.draw(screen)         # Draw (every frame)
```

This pattern makes it easy to build complex UIs from simple, reusable parts!
