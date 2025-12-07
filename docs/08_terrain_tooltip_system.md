# Terrain Tooltip System

**Purpose**: Display contextual information when hovering over terrain tiles in battle.

**Status**: ✅ Implemented and tested (Session 8)

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Tooltip UI Component](#tooltip-ui-component)
4. [Tile Tooltip Data](#tile-tooltip-data)
5. [Battle Screen Integration](#battle-screen-integration)
6. [Screen Edge Avoidance](#screen-edge-avoidance)
7. [Creating Tooltips](#creating-tooltips)
8. [Testing](#testing)
9. [Bug Fix History](#bug-fix-history)
10. [Future Enhancements](#future-enhancements)

---

## Overview

The terrain tooltip system provides contextual information about cover tiles when players hover their mouse over them. This enhances tactical decision-making by showing:

- **Cover type** (Full Cover, Half Cover)
- **Flavor description** (what the terrain represents)
- **Mechanical effect** (defense bonus percentage)

### User Experience

1. Player hovers mouse over a terrain tile with cover
2. Tooltip appears near cursor (15px offset)
3. Tooltip displays 3 lines: title, flavor, mechanics
4. Tooltip follows mouse movement
5. Tooltip disappears when leaving terrain

### Visual Design

```
┌────────────────────────────────────────┐
│ Full Cover                             │ <- Golden, bold (title)
│ Solid terrain that provides complete   │ <- Dim, italic (flavor)
│ protection                             │
│ +40% chance for attacks to miss when   │ <- Normal (mechanics)
│ behind this cover                      │
└────────────────────────────────────────┘
  ↑ Semi-transparent dark background (alpha=230)
```

---

## Architecture

The tooltip system consists of three main components:

### Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Battle Screen                        │
│                                                         │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────┐ │
│  │   Mouse Pos  │───>│   Tooltip    │───>│  Screen  │ │
│  │   Tracking   │    │   Update     │    │  Draw    │ │
│  └──────────────┘    └──────────────┘    └──────────┘ │
│         │                    │                         │
│         │                    │                         │
│         v                    v                         │
│  ┌──────────────┐    ┌──────────────┐                 │
│  │  Grid Coord  │    │  Tooltip UI  │                 │
│  │  Conversion  │    │  Component   │                 │
│  └──────────────┘    └──────────────┘                 │
│         │                                              │
│         v                                              │
│  ┌──────────────┐                                     │
│  │     Tile     │                                     │
│  │  Tooltip Data│                                     │
│  └──────────────┘                                     │
└─────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Input**: Mouse position (pixel coordinates)
2. **Conversion**: Pixel → Grid coordinates
3. **Lookup**: Get tile at grid position
4. **Check**: Does tile have tooltip? (`has_tooltip()`)
5. **Update**: Set tooltip content from tile data
6. **Position**: Calculate tooltip position with edge avoidance
7. **Render**: Draw tooltip on screen

---

## Tooltip UI Component

**File**: `ui/ui_elements.py`
**Class**: `Tooltip`
**Lines**: 191

### Class Interface

```python
class Tooltip:
    def __init__(self, padding: int = 12):
        """Initialize tooltip with configurable padding."""

    def set_content(self, title: str, flavor_text: str, mechanics_text: str):
        """Set tooltip text content."""

    def show(self, mouse_pos: Tuple[int, int]):
        """Show tooltip at mouse position."""

    def hide(self):
        """Hide tooltip."""

    def draw(self, screen: pygame.Surface):
        """Render tooltip to screen."""
```

### Visual Properties

| Property | Value | Description |
|----------|-------|-------------|
| **Background** | `(25, 25, 35, 230)` | Semi-transparent dark |
| **Border** | `config.COLOR_MENU_BORDER` | 2px solid border |
| **Title Color** | `config.COLOR_TEXT_HIGHLIGHT` | Golden (#FFC864) |
| **Flavor Color** | `config.COLOR_TEXT_DIM` | Dimmed gray |
| **Mechanics Color** | `config.COLOR_TEXT` | Off-white |
| **Title Font** | 26px | Bold (double-render) |
| **Body Font** | 22px | Normal |
| **Padding** | 12px | Internal spacing |
| **Offset** | 15px | Distance from cursor |

### Example Usage

```python
# Create tooltip
tooltip = Tooltip(padding=12)

# Set content
tooltip.set_content(
    title="Full Cover",
    flavor_text="Solid terrain that provides complete protection",
    mechanics_text="+40% chance for attacks to miss when behind this cover"
)

# Show at mouse position
tooltip.show((mouse_x, mouse_y))

# Draw
tooltip.draw(screen)

# Hide
tooltip.hide()
```

---

## Tile Tooltip Data

**File**: `combat/grid.py`
**Class**: `Tile`

### Data Structure

Each `Tile` has three tooltip fields:

```python
class Tile:
    def __init__(self, x: int, y: int, terrain_type: str = "empty"):
        # ... other fields ...

        # Tooltip data
        self.tooltip_title: str       # Short name (e.g., "Full Cover")
        self.tooltip_flavor: str      # Description
        self.tooltip_mechanics: str   # Game mechanics explanation
```

### Tooltip Content by Terrain Type

#### Empty Terrain

```python
tooltip_title = ""
tooltip_flavor = ""
tooltip_mechanics = ""
# has_tooltip() returns False
```

#### Full Cover

```python
tooltip_title = "Full Cover"
tooltip_flavor = "Solid terrain that provides complete protection"
tooltip_mechanics = "+40% chance for attacks to miss when behind this cover"
# has_tooltip() returns True
```

#### Half Cover

```python
tooltip_title = "Half Cover"
tooltip_flavor = "Low obstacles that provide partial protection"
tooltip_mechanics = "+20% chance for attacks to miss when behind this cover"
# has_tooltip() returns True
```

### The `has_tooltip()` Method

```python
def has_tooltip(self) -> bool:
    """Check if this tile has tooltip content to display."""
    return self.tooltip_title != ""
```

**Why it works**:
- Empty tiles have `tooltip_title = ""`
- Tiles with cover have non-empty titles
- Simple boolean check for display logic

### Critical: The `add_cover()` Fix

**Problem**: Originally, `add_cover()` updated terrain type but **not tooltip data**.

**Solution**: Update tooltip fields when adding cover:

```python
def add_cover(self, x: int, y: int, cover_type: str) -> bool:
    tile = self.get_tile(x, y)
    if tile:
        tile.terrain_type = cover_type
        if cover_type == "full_cover":
            tile.blocks_sight = True
            tile.defense_bonus = 40
            tile.symbol = "⬛"
            # ✅ CRITICAL: Update tooltip data
            tile.tooltip_title = "Full Cover"
            tile.tooltip_flavor = "Solid terrain that provides complete protection"
            tile.tooltip_mechanics = "+40% chance for attacks to miss when behind this cover"
        elif cover_type == "half_cover":
            # ... similar for half cover
        return True
    return False
```

**Why this matters**: All tiles start as `"empty"`. Cover is added later via `add_cover()`. If tooltip data isn't updated, tiles will have `terrain_type = "full_cover"` but `tooltip_title = ""`, causing tooltips to never appear.

---

## Battle Screen Integration

**File**: `combat/battle_screen.py`
**Method**: `_update_terrain_tooltip()`

### Initialization

```python
class BattleScreen:
    def __init__(self, screen: pygame.Surface):
        # ... other initialization ...

        # Tooltip system
        self.terrain_tooltip = Tooltip(padding=12)
        self.hovered_tile: Optional[Tuple[int, int]] = None
```

### Update Loop

Called every frame (60 FPS):

```python
def _update_terrain_tooltip(self) -> None:
    """Update terrain tooltip based on mouse hover position."""

    # Step 1: Convert mouse position to grid coordinates
    grid_x, grid_y = self._pixel_to_grid(self.mouse_pos)

    # Step 2: Check if hovering over valid grid tile
    if grid_x is not None and grid_y is not None:
        tile = self.grid.get_tile(grid_x, grid_y)

        # Step 3: Only show tooltip for tiles with terrain
        if tile and tile.has_tooltip():
            # Step 4: Update tooltip if hovering over new tile
            if self.hovered_tile != (grid_x, grid_y):
                self.hovered_tile = (grid_x, grid_y)
                self.terrain_tooltip.set_content(
                    title=tile.tooltip_title,
                    flavor_text=tile.tooltip_flavor,
                    mechanics_text=tile.tooltip_mechanics
                )

            # Step 5: Show tooltip at mouse position
            self.terrain_tooltip.show(self.mouse_pos)
        else:
            # Not hovering over terrain - hide tooltip
            self.hovered_tile = None
            self.terrain_tooltip.hide()
    else:
        # Mouse outside grid - hide tooltip
        self.hovered_tile = None
        self.terrain_tooltip.hide()
```

### Drawing

Tooltip is drawn **last** (appears on top of all other UI):

```python
def draw(self) -> None:
    # ... draw grid, units, UI, etc. ...

    # Draw terrain tooltip (drawn last so it appears on top)
    self.terrain_tooltip.draw(self.screen)
```

### Coordinate Conversion

The `_pixel_to_grid()` method converts mouse position to grid coordinates:

```python
def _pixel_to_grid(self, pixel_pos: Tuple[int, int]) -> Tuple[Optional[int], Optional[int]]:
    """
    Convert pixel coordinates to grid coordinates.

    Returns (grid_x, grid_y) or (None, None) if outside grid.
    """
    px, py = pixel_pos

    # Subtract grid offset
    grid_px = px - self.grid_offset_x
    grid_py = py - self.grid_offset_y

    # Bounds check
    if grid_px < 0 or grid_py < 0:
        return (None, None)
    if grid_px >= self.grid_pixel_size or grid_py >= self.grid_pixel_size:
        return (None, None)

    # Convert to tile index
    grid_x = grid_px // config.TILE_SIZE
    grid_y = grid_py // config.TILE_SIZE

    return (grid_x, grid_y)
```

---

## Screen Edge Avoidance

The tooltip automatically adjusts position to stay on-screen.

### Algorithm

```python
def _calculate_position(self, mouse_pos: Tuple[int, int]) -> None:
    """Calculate tooltip position with automatic edge avoidance."""

    # Step 1: Default position (offset from cursor)
    tooltip_x = mouse_pos[0] + self.offset_x  # +15px right
    tooltip_y = mouse_pos[1] + self.offset_y  # +15px down

    # Step 2: Measure tooltip size
    # (Render text to calculate width/height)

    # Step 3: Right edge check
    if tooltip_x + tooltip_width > config.SCREEN_WIDTH:
        # Flip to left of cursor
        tooltip_x = mouse_pos[0] - tooltip_width - self.offset_x

    # Step 4: Bottom edge check
    if tooltip_y + tooltip_height > config.SCREEN_HEIGHT:
        # Flip to above cursor
        tooltip_y = mouse_pos[1] - tooltip_height - self.offset_y

    # Step 5: Clamp to screen bounds
    tooltip_x = max(0, tooltip_x)
    tooltip_y = max(0, tooltip_y)

    self.rect = pygame.Rect(tooltip_x, tooltip_y, tooltip_width, tooltip_height)
```

### Visual Example

```
Case 1: Normal (bottom-right of cursor)
    Cursor
      ↓
      ●───────┐
          ┌───┴───────────┐
          │ Tooltip       │
          │               │
          └───────────────┘

Case 2: Near right edge (bottom-left of cursor)
              Cursor
                ↓
     ┌──────────●
     │ Tooltip  │
     │          │
     └──────────┘

Case 3: Near bottom edge (top-right of cursor)
          ┌───────────────┐
          │ Tooltip       │
          │               │
          └───┬───────────┘
      ●───────┘
      ↑
    Cursor
```

---

## Creating Tooltips

### For New Terrain Types

If you add a new terrain type, update both:

1. **`Tile.__init__()`** - Set tooltip data when created:

```python
elif terrain_type == "my_new_terrain":
    self.tooltip_title = "My Terrain"
    self.tooltip_flavor = "Description of this terrain"
    self.tooltip_mechanics = "Game mechanics effect"
```

2. **`Grid.add_cover()`** - Set tooltip data when added:

```python
elif cover_type == "my_new_terrain":
    tile.tooltip_title = "My Terrain"
    tile.tooltip_flavor = "Description of this terrain"
    tile.tooltip_mechanics = "Game mechanics effect"
```

### For Unit Tooltips (Future)

To add tooltips for units:

```python
# In battle_screen.py _update_terrain_tooltip():
if grid_x is not None and grid_y is not None:
    tile = self.grid.get_tile(grid_x, grid_y)

    # Check for unit first
    if tile and tile.is_occupied():
        unit = tile.occupied_by
        self.terrain_tooltip.set_content(
            title=unit.name,
            flavor_text=f"{unit.team.capitalize()} unit",
            mechanics_text=f"HP: {unit.current_health}/{unit.max_health}, "
                          f"SAN: {unit.current_sanity}/{unit.max_sanity}"
        )
        self.terrain_tooltip.show(self.mouse_pos)
    # Then check for terrain
    elif tile and tile.has_tooltip():
        # ... existing terrain tooltip code
```

---

## Testing

### Test Files

#### 1. `testing/test_tooltip.py` - Component Tests

Tests the `Tooltip` class in isolation:

```python
def test_tooltip_basic():
    """Test basic tooltip creation and display."""
    tooltip = Tooltip(padding=12)
    tooltip.set_content(title="Test", flavor_text="Flavor", mechanics_text="Mechanics")
    tooltip.show((400, 300))
    assert tooltip.visible == True

def test_tooltip_edge_detection():
    """Test tooltip edge avoidance."""
    # Test all four corners of screen
    # Verify tooltip stays within bounds
```

**Run**: `uv run python testing/test_tooltip.py`

#### 2. `testing/test_tooltip_integration.py` - Integration Tests

Tests tooltip integration with grid system:

```python
def test_tile_tooltip_on_creation():
    """Test that tiles have correct tooltip data on creation."""
    tile = Tile(0, 0, "full_cover")
    assert tile.has_tooltip() == True
    assert tile.tooltip_title == "Full Cover"

def test_add_cover_updates_tooltip():
    """Test that add_cover() updates tooltip data correctly."""
    grid = Grid(size=10)
    grid.add_cover(5, 5, "full_cover")
    tile = grid.get_tile(5, 5)
    assert tile.has_tooltip() == True  # ✅ This was the bug!

def test_generated_terrain_has_tooltips():
    """Test that procedurally generated terrain has tooltips."""
    terrain_data = generate_terrain("symmetric", grid_size=10)
    grid.setup_generated_terrain(terrain_data)
    # Verify all terrain tiles have tooltips
```

**Run**: `uv run python testing/test_tooltip_integration.py`

### Test Results

```
============================================================
[OK] ALL INTEGRATION TESTS PASSED!
============================================================

Tooltips are now working correctly:
  - Tiles created with terrain have tooltips
  - add_cover() updates tooltip data
  - Generated terrain has tooltips
```

---

## Bug Fix History

### The Original Bug

**Symptom**: Tooltips not appearing when hovering over terrain.

**Investigation**:
1. Tooltip component worked in isolation ✅
2. Battle screen integration looked correct ✅
3. `has_tooltip()` was returning `False` ❌

**Root Cause**: The `Grid.add_cover()` method updated tile properties but **not tooltip fields**.

**Timeline**:
1. Tiles created as `"empty"` → tooltip fields set to `""`
2. `add_cover()` called → changes `terrain_type` to `"full_cover"`
3. **Tooltip fields not updated** → still `""`
4. `has_tooltip()` returns `False` → tooltip never shows

### The Fix

**File**: `combat/grid.py`
**Method**: `add_cover()`
**Change**: Added tooltip field updates when adding cover

**Before**:
```python
def add_cover(self, x: int, y: int, cover_type: str) -> bool:
    tile = self.get_tile(x, y)
    if tile:
        tile.terrain_type = cover_type
        if cover_type == "full_cover":
            tile.blocks_sight = True
            tile.defense_bonus = 40
            tile.symbol = "⬛"
            # ❌ Tooltip fields not updated!
        return True
```

**After**:
```python
def add_cover(self, x: int, y: int, cover_type: str) -> bool:
    tile = self.get_tile(x, y)
    if tile:
        tile.terrain_type = cover_type
        if cover_type == "full_cover":
            tile.blocks_sight = True
            tile.defense_bonus = 40
            tile.symbol = "⬛"
            # ✅ Tooltip fields updated!
            tile.tooltip_title = "Full Cover"
            tile.tooltip_flavor = "Solid terrain that provides complete protection"
            tile.tooltip_mechanics = "+40% chance for attacks to miss when behind this cover"
        return True
```

### Lessons Learned

**Pattern**: Data initialization vs. data mutation

When you have:
1. **Initialization**: Data set when object is created
2. **Mutation**: Data changed later via a method

**Always ensure**: Mutation methods update **all related fields**, not just the primary field.

**Example**:
- Tile created → All fields initialized consistently
- `add_cover()` called → **Must update ALL terrain-related fields** (type, symbol, defense, **tooltips**)

---

## Future Enhancements

### Planned Features

1. **Unit Tooltips**
   - Show unit stats on hover
   - Display health, sanity, accuracy, movement
   - Show weapon range and attack type

2. **Action Button Tooltips**
   - Show ability details
   - Display cooldown, range, cost
   - Show damage/effect preview

3. **Rich Text Formatting**
   - Bold/italic within tooltip
   - Color-coded text (damage=red, healing=green)
   - Icons/symbols inline

4. **Multi-line Wrapping**
   - Automatic text wrapping for long descriptions
   - Configurable max width

5. **Animations**
   - Fade-in/fade-out transitions
   - Smooth position interpolation
   - Delay before showing (debounce)

6. **Keyboard Toggle**
   - Press key to toggle tooltips on/off
   - Useful for experienced players

### Implementation Notes

**Rich Text**: Would require custom text rendering system or integration with a library like `pygame_gui`.

**Animations**: Use interpolation in `show()` method:
```python
def show(self, mouse_pos):
    self.target_alpha = 230  # Full opacity
    self.current_alpha = lerp(self.current_alpha, self.target_alpha, 0.2)
```

**Debounce**: Add delay before showing:
```python
def show(self, mouse_pos):
    if self.hover_timer < HOVER_DELAY:
        self.hover_timer += dt
        return
    # Show tooltip after delay
```

---

## Summary

The terrain tooltip system provides contextual information for tactical decision-making:

**Key Components**:
- `Tooltip` UI component (semi-transparent, multi-line, edge-aware)
- Tile tooltip data (title, flavor, mechanics)
- Battle screen integration (hover detection, update loop, drawing)

**Critical Fix**: `add_cover()` must update tooltip fields when adding terrain

**Testing**: Comprehensive test suite verifies component and integration

**User Experience**: Smooth, informative, non-intrusive tooltips that enhance gameplay

---

**Last Updated**: 2025-12-08 (Session 8)
**Status**: Production-ready ✅
