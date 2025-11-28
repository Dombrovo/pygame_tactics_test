# Character Image Assignment System

## Overview

The character image assignment system ensures each investigator receives a unique portrait that is never reused within a campaign. This provides visual variety and makes each character feel distinct.

## Features

### 1. **Automatic Image Assignment**
- When creating an investigator, the system automatically assigns a random character portrait
- Images are gender-specific (male investigators get male portraits, female get female)
- Each image is only used once per campaign

### 2. **Gender-Based Image Pools**
Located in `assets/images/investigators/`:
- **Female pool**: 25 unique character portraits
- **Male pool**: 30 unique character portraits

### 3. **Pool Tracking**
The system tracks which images have been used globally:
- `_USED_IMAGES` dictionary maintains lists of used images per gender
- Prevents any image from being assigned twice
- Returns `None` when pool is exhausted

### 4. **Pool Management Functions**

#### `get_random_unused_image(gender)`
Assigns a random unused image from the pool.
```python
from entities.investigator import get_random_unused_image

image_path = get_random_unused_image("male")
# Returns: "assets/images/investigators/male/detective.png"
```

#### `reset_image_pool()`
Resets the used images tracker (call at start of new campaign).
```python
from entities.investigator import reset_image_pool

reset_image_pool()
# All 55 images (25 female + 30 male) are now available again
```

#### `get_image_pool_status()`
Check pool status for debugging or UI display.
```python
from entities.investigator import get_image_pool_status

status = get_image_pool_status()
# Returns:
# {
#     "male": {"total": 30, "used": 4, "available": 26},
#     "female": {"total": 25, "used": 2, "available": 23}
# }
```

## Usage

### Creating Investigators with Images

Images are automatically assigned when using `create_test_squad()`:

```python
from entities.investigator import create_test_squad

squad = create_test_squad()

for inv in squad:
    print(f"{inv.name} ({inv.gender})")
    print(f"Portrait: {inv.image_path}")
    # Example: "Portrait: assets/images/investigators/female/detective.png"
```

### Manual Image Assignment

```python
from entities.investigator import Investigator, get_random_unused_image

# Generate name and gender
name = "John Carter"
gender = "male"

# Get a unique portrait
image = get_random_unused_image(gender)

# Create investigator with portrait
investigator = Investigator(
    name=name,
    gender=gender,
    image_path=image,
    max_health=15,
    max_sanity=10
)
```

## Architecture

### Data Flow

```
create_test_squad()
    └─> generate_random_name()  # Random name + gender
    └─> get_random_unused_image(gender)
            └─> _get_available_images(gender)  # List all images
            └─> Filter out used images
            └─> random.choice(unused_images)
            └─> Mark as used in _USED_IMAGES
            └─> Return path: "assets/images/investigators/{gender}/{filename}.png"
```

### Global State

```python
# Track used images (prevents reuse)
_USED_IMAGES = {
    "male": ["detective.png", "soldier.png", ...],    # Used male images
    "female": ["scientist.png", "nurse.png", ...]     # Used female images
}
```

## Testing

Run the comprehensive test suite:

```bash
uv run python testing/test_image_assignment.py
```

**Test Coverage:**
1. ✅ Basic image assignment to investigators
2. ✅ No duplicate images across multiple squads
3. ✅ Pool exhaustion handling (returns None gracefully)
4. ✅ Reset functionality works correctly

## Campaign Integration

### Starting a New Campaign

```python
from entities.investigator import reset_image_pool, create_test_squad

# Reset pool for new campaign
reset_image_pool()

# Create initial squad (each gets unique portrait)
starting_squad = create_test_squad()
```

### Recruiting New Investigators (Phase 2+)

```python
from entities.investigator import Investigator, get_random_unused_image, generate_random_name

# Generate random investigator
name, gender = generate_random_name()
image = get_random_unused_image(gender)

# Check if images are still available
if image is None:
    print("Warning: No more unique portraits available!")
    # Use a placeholder or allow duplicates
    image = "assets/images/investigators/placeholder.png"

new_recruit = Investigator(name=name, gender=gender, image_path=image)
```

## File Structure

```
assets/
└── images/
    └── investigators/
        ├── male/               # 30 male character portraits
        │   ├── detective.png
        │   ├── soldier.png
        │   ├── scientist.png
        │   └── ...
        └── female/             # 25 female character portraits
            ├── detective.png
            ├── nurse.png
            ├── scientist.png
            └── ...
```

## Investigator Class Changes

### New Attribute: `image_path`

```python
class Investigator(Unit):
    def __init__(self, ..., image_path: Optional[str] = None):
        # ...
        self.image_path = image_path  # Path to character portrait
```

**Usage in UI:**
```python
# Load and display character portrait
if investigator.image_path:
    portrait = pygame.image.load(investigator.image_path)
    screen.blit(portrait, position)
```

## Image Specifications

All character portraits should be:
- **Format**: PNG with transparency
- **Dimensions**: (Consistent across all images)
- **Style**: 1920s Lovecraftian theme
- **Naming**: Descriptive lowercase with underscores (e.g., `private_detective.png`)

## Future Enhancements (Phase 2+)

1. **Background-Based Images**: Match portraits to character backgrounds
   ```python
   # If investigator.background == "Detective":
   #     prefer images from detective-themed portraits
   ```

2. **Image Variants**: Multiple images per background class
   - `detective_1.png`, `detective_2.png`, etc.

3. **Custom Portraits**: Allow players to add custom images
   - Place in `assets/images/investigators/custom/`
   - Automatically detected and added to pool

4. **Portrait Persistence**: Save assigned portraits with campaign data
   ```python
   save_data = {
       "investigators": [
           {"name": "John Carter", "image": "male/detective.png", ...}
       ]
   }
   ```

## Notes

- **Pool Size**: With 25 female and 30 male images, you can recruit up to 55 unique investigators per campaign
- **Exhaustion**: When pool is exhausted, `get_random_unused_image()` returns `None`
- **Reset**: Call `reset_image_pool()` at the start of each new campaign
- **Thread Safety**: Current implementation is not thread-safe (single-threaded game is fine)

## Example: Complete Character Creation

```python
from entities.investigator import (
    generate_random_name,
    get_random_unused_image,
    Investigator
)

# Generate random character
name, gender = generate_random_name()
image = get_random_unused_image(gender)

# Create investigator
character = Investigator(
    name=name,
    gender=gender,
    image_path=image,
    max_health=15,
    max_sanity=10,
    accuracy=75,
    will=5,
    movement_range=4
)

print(f"Created: {character.name}")
print(f"Gender: {character.gender}")
print(f"Portrait: {character.image_path}")
```

Output:
```
Created: Arthur 'Bones' Blackwood
Gender: male
Portrait: assets/images/investigators/male/archaeologist.png
```
