# Attack Resolution Popup Redesign

**Date**: 2025-12-15
**Feature**: Comprehensive tactical feedback for attack resolution

---

## Overview

Redesigned the attack resolution popup to provide complete tactical information at a glance, showing the full combat flow from hit chance calculation through final damage.

---

## New Popup Layout

```
┌─────────────────────────────────────┐
│  Hit Chance: 65%                    │  <- Calculated percentage
│                                     │
│  >>> HIT <<<                        │  <- Result (green=hit, red=miss)
│                                     │
│  Roll: 42/100                       │  <- D100 roll vs hit chance
│                                     │
│  Card: +2                           │  <- Combat deck card (if hit)
│                                     │
│  Damage: 7 HP + 5 SAN               │  <- Final damage (if hit)
└─────────────────────────────────────┘
```

---

## Information Flow

### All Attacks Show:
1. **Hit Chance**: The calculated percentage (after distance + cover penalties)
2. **Result**: HIT or MISS in large text with color coding
3. **Roll**: The D100 roll that determined success/failure

### On Hit, Additionally Shows:
4. **Card Drawn**: Combat deck modifier (if applicable)
   - Investigators: Personal deck cards (+2, x2, NULL, etc.)
   - Enemies: Monster deck cards (shared universal deck)
   - No card shown if using basic attack
5. **Damage**: Total damage dealt
   - Health damage always shown
   - Sanity damage added if > 0
   - Format: `Damage: 7 HP + 5 SAN`

---

## Visual Design

### Color Coding

**Border Colors**:
- 🟢 Green: Normal hit
- 🟡 Gold: Critical hit (x2 card)
- 🔴 Dark Red: Miss or NULL card

**Text Colors**:
- Hit chance: Dim gray (200, 200, 220) - informational
- HIT: Bright green (100, 255, 100) - success
- MISS: Bright red (255, 100, 100) - failure
- Roll: Dim gray (200, 200, 220) - informational
- Card: Yellow (255, 200, 100) - modifier highlight
- Damage: Bright red (255, 100, 100) - impact emphasis

### Font Sizes
- **Large (56px)**: HIT/MISS result, Damage
- **Medium (44px)**: Hit chance, Card drawn
- **Small (36px)**: Roll details

---

## Example Scenarios

### Scenario 1: Normal Hit with +2 Card
```
Hit Chance: 65%
>>> HIT <<<
Roll: 42/100

Card: +2
Damage: 7 HP
```
**Border**: Green
**Duration**: 1000ms

---

### Scenario 2: Critical Hit (x2 Card)
```
Hit Chance: 75%
>>> HIT <<<
Roll: 15/100

Card: x2
Damage: 12 HP
```
**Border**: Gold
**Duration**: 1000ms

---

### Scenario 3: Hound Attack (Sanity Damage)
```
Hit Chance: 85%
>>> HIT <<<
Roll: 55/100

Card: +1
Damage: 7 HP + 5 SAN
```
**Border**: Green
**Duration**: 1000ms

---

### Scenario 4: NULL Card (Hit but No Damage)
```
Hit Chance: 55%
>>> HIT <<<
Roll: 30/100

Card: NULL
Damage: 0 HP
```
**Border**: Dark Red
**Duration**: 1000ms

---

### Scenario 5: Miss
```
Hit Chance: 45%
>>> MISS <<<
Roll: 88/100
```
**Border**: Dark Red
**Duration**: 1000ms
**Note**: No card shown, no damage section

---

### Scenario 6: Enemy Attack (No Card)
```
Hit Chance: 50%
>>> HIT <<<
Roll: 35/100

Damage: 4 HP
```
**Border**: Green
**Duration**: 1000ms
**Note**: Enemies use monster deck, but we still show damage clearly

---

## Implementation Details

### New Method: `Popup.show_attack_result()`

**Location**: `ui/ui_elements.py` (lines 1920-2047)

**Signature**:
```python
@staticmethod
def show_attack_result(
    screen: pygame.Surface,
    attack_result: dict,
    duration_ms: int = 800
) -> None
```

**Parameters**:
- `screen`: Pygame surface to draw on
- `attack_result`: Dictionary from `combat_resolver.resolve_attack()` with keys:
  - `hit_chance`: int (percentage)
  - `hit`: bool
  - `roll`: int (D100 roll)
  - `card_drawn`: str (optional)
  - `damage_dealt`: int
  - `sanity_damage`: int (optional)
- `duration_ms`: Display duration (default 800ms)

---

### Updated Method: `BattleScreen._show_attack_result()`

**Location**: `combat/battle_screen.py` (lines 657-677)

**Changes**:
- Replaced individual `show_damage_notification()` calls
- Now uses single `show_attack_result()` call for all cases
- Simplified logic: just pass the full result dictionary

**Before** (old code):
```python
if not result.get("hit", False):
    card_name = result.get("card_drawn", "")
    if card_name:
        Popup.show_damage_notification(self.screen, 0, f"MISS ({card_name})")
    else:
        Popup.show_damage_notification(self.screen, 0, "MISS")
    return

damage = result.get("damage_dealt", 0)
card_name = result.get("card_drawn", "")
Popup.show_damage_notification(self.screen, damage, card_name, duration_ms=600)
```

**After** (new code):
```python
# Show comprehensive attack result popup
Popup.show_attack_result(self.screen, result, duration_ms=1000)
```

---

### Legacy Method: `Popup.show_damage_notification()`

**Status**: DEPRECATED
**Purpose**: Kept for backwards compatibility
**Usage**: Simple damage notifications only (not recommended)

---

## Benefits

### Player Experience
1. **Complete Tactical Picture**: See all combat math in one place
2. **Learn the System**: Understand how hit chance is calculated
3. **Strategic Decisions**: Know exact probabilities for positioning
4. **Satisfying Feedback**: Critical hits feel rewarding with gold borders

### Developer Benefits
1. **Single Call**: One method replaces multiple conditional calls
2. **Consistent Display**: All attacks show same information format
3. **Extensible**: Easy to add new info (armor, resistances, etc.)
4. **Debugging**: Clear display of all combat variables

---

## Testing

### Test Script: `testing/test_attack_popup.py`

Tests 7 scenarios:
1. Normal hit with +2 card
2. Critical x2 card
3. Hit with sanity damage
4. NULL card (hit but no damage)
5. Miss - failed roll
6. Miss - low hit chance
7. Enemy attack (no card)

**Run test**:
```bash
uv run python testing/test_attack_popup.py
```

**Controls**:
- SPACE: Next scenario
- ESC: Quit

---

## Future Enhancements

### Potential Additions
- **Cover indicator**: Show cover type that affected hit chance
- **Distance indicator**: Show actual distance vs weapon range
- **Armor mitigation**: If armor system added, show damage reduction
- **Status effects**: Show if attack applied bleed, stun, etc.
- **Animation**: Slide in/fade instead of instant appear
- **Sound effects**: Different sounds for hit/miss/crit

### Size Adjustments
- Current: 600x400px
- Could be made smaller (500x350px) if feels too large
- Could be repositioned (bottom-center instead of screen-center)

---

## Files Modified

1. **ui/ui_elements.py**
   - Added `Popup.show_attack_result()` (new method)
   - Deprecated `Popup.show_damage_notification()` (legacy support)

2. **combat/battle_screen.py**
   - Simplified `_show_attack_result()` to use new popup

3. **testing/test_attack_popup.py** (new file)
   - Interactive test for all popup scenarios

---

## Metrics

- **Lines Added**: ~130 (new popup method)
- **Lines Removed**: ~20 (simplified battle screen logic)
- **Net Impact**: More comprehensive with less coupling
- **Display Time**: 1000ms (up from 300-600ms for better readability)

---

**Status**: ✅ Complete and tested
**Version**: 3.5.0
**Ready for**: In-game playtesting
