# Pygame-CE Fundamentals

This guide explains the core concepts of Pygame-CE that power Eldritch Tactics.

## What is Pygame-CE?

**Pygame-CE** (Community Edition) is a Python library for making games and multimedia applications. It's a drop-in replacement for the original Pygame, with community-driven improvements and faster updates.

Key features:
- **Cross-platform**: Works on Windows, Mac, Linux
- **Hardware accelerated**: Uses SDL2 for fast rendering
- **Easy to learn**: Simple, Pythonic API
- **Community-driven**: Active development and bug fixes

### Installation

```bash
# Install with UV (recommended)
uv add pygame-ce

# Import in code
import pygame  # Note: Still import as 'pygame', not 'pygame_ce'
```

---

## The Game Loop Pattern

**Every Pygame game runs on a continuous loop** that repeats ~60 times per second:

```
┌─────────────────────────────────────┐
│    while game_running:              │
│        ┌──────────────────────┐     │
│        │ 1. HANDLE INPUT      │←────┼─── User clicks, presses keys
│        └──────────────────────┘     │
│                 ↓                    │
│        ┌──────────────────────┐     │
│        │ 2. UPDATE STATE      │←────┼─── Move characters, update health
│        └──────────────────────┘     │
│                 ↓                    │
│        ┌──────────────────────┐     │
│        │ 3. DRAW EVERYTHING   │←────┼─── Render to hidden buffer
│        └──────────────────────┘     │
│                 ↓                    │
│        ┌──────────────────────┐     │
│        │ 4. DISPLAY           │←────┼─── Show hidden buffer on screen
│        └──────────────────────┘     │
│                 ↓                    │
│        ┌──────────────────────┐     │
│        │ 5. CONTROL FRAMERATE │←────┼─── Wait to maintain 60 FPS
│        └──────────────────────┘     │
│                 ↓                    │
│        (Loop back to step 1)        │
└─────────────────────────────────────┘
```

### Example Game Loop

```python
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

running = True
while running:
    # 1. HANDLE INPUT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. UPDATE
    player.move()
    enemy.update()

    # 3. DRAW
    screen.fill((0, 0, 0))  # Clear screen (black)
    screen.blit(player_image, player_pos)

    # 4. DISPLAY
    pygame.display.flip()  # Show what we drew

    # 5. CONTROL FRAMERATE
    clock.tick(60)  # Run at 60 FPS

pygame.quit()
```

---

## Core Pygame Objects

### 1. pygame.Surface

A **Surface** is any drawable area - the screen, an image, a button, etc.

```python
# The main screen is a Surface
screen = pygame.display.set_mode((1920, 1080))

# Drawing methods
screen.fill((255, 0, 0))  # Fill with red
pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(10, 10, 100, 50))
screen.blit(image, (x, y))  # Draw another surface onto this one
```

**Common operations:**
- `fill(color)` - Fill entire surface with a color
- `blit(source, dest)` - Copy one surface onto another
- `get_rect()` - Get the surface's bounding rectangle

### 2. pygame.Rect

A **Rect** represents a rectangular area with position and size.

```python
# Create a rectangle
rect = pygame.Rect(100, 50, 200, 80)  # (x, y, width, height)

# Useful attributes
print(rect.x, rect.y)          # Top-left position
print(rect.width, rect.height) # Dimensions
print(rect.center)             # Center point (tuple)
print(rect.topleft)            # Top-left corner
print(rect.bottomright)        # Bottom-right corner

# Collision detection
if rect.collidepoint(mouse_pos):
    print("Mouse is inside rectangle!")

if rect.colliderect(other_rect):
    print("Rectangles are overlapping!")
```

**Why Rect is powerful:**
- Built-in collision detection
- Easy positioning (center, topright, etc.)
- No math needed for common operations

### 3. pygame.event

**Events** represent user input and system messages.

```python
for event in pygame.event.get():  # Get all events since last frame
    # Mouse events
    if event.type == pygame.MOUSEBUTTONDOWN:
        print(f"Mouse button {event.button} pressed at {event.pos}")

    if event.type == pygame.MOUSEBUTTONUP:
        print("Mouse button released")

    if event.type == pygame.MOUSEMOTION:
        print(f"Mouse moved to {event.pos}")

    # Keyboard events
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            print("Spacebar pressed")
        if event.key == pygame.K_ESCAPE:
            print("Escape pressed")

    # Window events
    if event.type == pygame.QUIT:  # User clicked X
        print("Window closed")
```

**Event attributes:**
- `event.type` - The kind of event (MOUSEBUTTONDOWN, KEYDOWN, etc.)
- `event.pos` - Mouse position for mouse events
- `event.button` - Which mouse button (1=left, 2=middle, 3=right)
- `event.key` - Which keyboard key (pygame.K_SPACE, pygame.K_a, etc.)

### 4. pygame.time.Clock

**Clock** manages framerate timing to ensure consistent game speed.

```python
clock = pygame.time.Clock()

while running:
    # ... game loop ...

    clock.tick(60)  # Limit to 60 FPS
```

**How clock.tick() works:**
- Measures how long the frame took
- Waits the remaining time to reach target framerate
- Example: Frame took 10ms, target is 16.67ms (60 FPS), waits 6.67ms

**Why this matters:**
- Without it, game runs as fast as CPU allows (inconsistent)
- Different computers would run game at different speeds
- Game would waste CPU/battery

---

## Key Concepts

### Double Buffering

Pygame draws to a **hidden buffer**, then swaps it to the visible screen.

```python
# Draw to hidden buffer
screen.fill((0, 0, 0))
screen.blit(sprite, (x, y))

# Swap buffers (show what we drew)
pygame.display.flip()
```

**Why double buffering?**
- Prevents flickering
- Prevents seeing partially-drawn frames
- Standard technique in all game engines

### RGB Colors

Colors are tuples of (Red, Green, Blue), each from 0-255:

```python
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)      # Red + Green
PURPLE = (255, 0, 255)       # Red + Blue
CYAN = (0, 255, 255)         # Green + Blue
GRAY = (128, 128, 128)       # Half of each
DARK_BLUE = (40, 40, 60)     # Low values = dark
```

### Coordinate System

Pygame uses **screen coordinates** where (0, 0) is top-left:

```
(0, 0) ──────────→ X (1920)
  │
  │
  │
  ↓
  Y (1080)
```

- **X increases** going right
- **Y increases** going down (opposite of math class!)
- Bottom-right of 1920x1080 screen is (1920, 1080)

---

## Common Patterns

### Centering an Object

```python
# Center a 400x80 button on a 1920x1080 screen
screen_center_x = 1920 // 2  # = 960
button_width = 400

# Button needs to start half its width to the left of center
button_x = screen_center_x - (button_width // 2)  # = 760

# So button spans from 760 to 1160, centered at 960
```

### Handling Click Events

```python
button_rect = pygame.Rect(100, 100, 200, 50)
is_pressed = False

for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONDOWN:
        if button_rect.collidepoint(event.pos):
            is_pressed = True

    if event.type == pygame.MOUSEBUTTONUP:
        if button_rect.collidepoint(event.pos) and is_pressed:
            # Complete click!
            on_button_click()
        is_pressed = False
```

### Drawing Text

```python
# Create font
font = pygame.font.Font(None, 48)  # None = default font, 48 = size

# Render text to a Surface
text_surface = font.render("Hello World", True, (255, 255, 255))

# Get rectangle for positioning
text_rect = text_surface.get_rect(center=(960, 540))

# Draw it
screen.blit(text_surface, text_rect)
```

---

## Performance Tips

1. **Don't create objects in the game loop**
   ```python
   # ❌ BAD - creates new font every frame
   while running:
       font = pygame.font.Font(None, 48)
       text = font.render("Score: 100", True, WHITE)

   # ✅ GOOD - create once before loop
   font = pygame.font.Font(None, 48)
   while running:
       text = font.render("Score: 100", True, WHITE)
   ```

2. **Only redraw what changed** (advanced)
   - Clear only dirty rectangles
   - Use `pygame.display.update(rect_list)` instead of `flip()`

3. **Use convert() for images**
   ```python
   # ❌ Slow - wrong pixel format
   image = pygame.image.load("sprite.png")

   # ✅ Fast - converts to screen's pixel format
   image = pygame.image.load("sprite.png").convert_alpha()
   ```

---

## Debugging Tips

### Show FPS

```python
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)

while running:
    # ... game loop ...

    # Display FPS
    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, (255, 255, 0))
    screen.blit(fps_text, (10, 10))

    clock.tick(60)
```

### Print Event Types

```python
for event in pygame.event.get():
    print(f"Event: {pygame.event.event_name(event.type)}")
```

### Draw Debug Rectangles

```python
# Show button hitboxes
pygame.draw.rect(screen, (255, 0, 0), button_rect, 2)  # Red outline
```

---

## Next Steps

- [Architecture Overview](02_architecture_overview.md) - How Eldritch Tactics is structured
- [UI Components](03_ui_components.md) - Building interactive buttons
- [Data Flow](04_data_flow.md) - How user input flows through the system

---

## Further Reading

- [Official Pygame-CE Documentation](https://pyga.me/docs/)
- [Pygame-CE GitHub](https://github.com/pygame-community/pygame-ce)
- [Real Python - Pygame Tutorial](https://realpython.com/pygame-a-primer/)
