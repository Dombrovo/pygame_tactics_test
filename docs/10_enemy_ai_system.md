# Enemy AI System Documentation

**Created**: 2025-12-08 (Session 10)
**Status**: ✅ Complete

---

## Overview

The enemy AI system implements basic tactical movement behaviors for enemy units during their turns in tactical combat. Different enemy types use different strategies to approach and engage player investigators.

---

## File Location

- **Module**: `combat/enemy_ai.py`
- **Integration**: `combat/battle_screen.py` (lines 15, 910-916)
- **Tests**: `testing/test_enemy_ai.py`

---

## AI Behaviors by Enemy Type

### Cultist (Ranged Enemy)

**Targeting Strategy**: Targets investigator with **highest current health**
**Movement**: Moves **1 tile** towards target per turn

**Rationale**: Cultists use conservative tactics, focusing fire on healthy targets rather than finishing off wounded ones. This creates pressure on the player's strongest units.

### Hound of Tindalos (Melee Enemy)

**Targeting Strategy**: Targets **nearest** investigator
**Movement**: Moves **2 tiles** towards target per turn

**Rationale**: Hounds use aggressive pack tactics, rapidly closing distance with the nearest prey using their superior speed.

---

## Implementation Details

### Core Functions

#### `find_highest_health_target(investigators: List[Investigator]) -> Optional[Investigator]`

Finds the investigator with the highest current health.

**Parameters**:
- `investigators`: List of all investigator units

**Returns**: Investigator with max current_health, or None if all incapacitated

**Example**:
```python
# Investigators: A (5 HP), B (15 HP), C (10 HP)
target = find_highest_health_target([inv_a, inv_b, inv_c])
# Returns inv_b (15 HP)
```

---

#### `find_nearest_target(enemy: Enemy, investigators: List[Investigator], grid: Grid) -> Optional[Investigator]`

Finds the investigator closest to the enemy unit.

**Parameters**:
- `enemy`: The enemy unit searching for a target
- `investigators`: List of all investigator units
- `grid`: The battlefield grid (for distance calculations)

**Returns**: Nearest investigator, or None if all incapacitated

**Distance Calculation**: Uses `grid.get_distance()` (Euclidean distance)

**Example**:
```python
# Hound at (5,5)
# Investigators: A at (0,0), B at (6,6), C at (2,5)
target = find_nearest_target(hound, investigators, grid)
# Returns B (distance ~1.41)
```

---

#### `calculate_movement_target(enemy: Enemy, target: Unit, grid: Grid, max_tiles: int) -> Optional[Tuple[int, int]]`

Calculates where the enemy should move to approach the target.

**Algorithm**:
1. Find all tiles adjacent to the target (8 neighbors, including diagonals)
2. Filter to only unoccupied, non-blocking tiles
3. Select the tile closest to the enemy
4. Use A* pathfinding to find optimal path
5. Move N tiles along the path (1 for Cultists, 2 for Hounds)

**Parameters**:
- `enemy`: The enemy unit that's moving
- `target`: The target unit to move towards
- `grid`: The battlefield grid
- `max_tiles`: Maximum tiles to move (1 or 2)

**Returns**: (x, y) coordinates to move to, or None if no valid move

**Special Cases**:
- **Target surrounded**: If no adjacent tiles are free, returns None
- **Already adjacent**: If enemy is already next to target, returns None
- **Blocked path**: A* finds path around obstacles

**Example**:
```python
# Cultist at (8,5), Investigator at (0,5)
# max_tiles = 1
move_to = calculate_movement_target(cultist, target, grid, 1)
# Returns (7, 5) - one tile closer
```

---

#### `execute_enemy_turn(enemy: Enemy, investigators: List[Investigator], grid: Grid) -> None`

Main AI entry point - executes an enemy unit's turn.

**Process**:
1. Check if enemy can act (not incapacitated)
2. Select target based on enemy type
3. Calculate movement destination
4. Execute movement via `grid.move_unit()`
5. Print turn information to console
6. **(Future)** Attack if target in range

**Parameters**:
- `enemy`: The enemy unit taking its turn
- `investigators`: List of all investigator units (for targeting)
- `grid`: The battlefield grid

**Returns**: None (modifies game state directly)

**Console Output**:
```
Enemy Turn: Hound Alpha
  Hound Alpha targeting nearest investigator
  Target: Regina Cross (HP: 12/15)
  Hound Alpha moves from (9, 7) to (7, 6)
```

---

## Integration with Battle Screen

The AI is called automatically during enemy turns in the turn order system.

**Location**: `combat/battle_screen.py`, `_advance_turn()` method (lines 910-916)

```python
# If enemy turn, execute AI
if self.current_turn_unit.team == "enemy":
    # Execute enemy AI behavior
    enemy_ai.execute_enemy_turn(self.current_turn_unit, self.player_units, self.grid)

    # After AI completes its actions, advance to next turn
    self._advance_turn()
```

**Turn Flow**:
1. Player investigator's turn (user controlled)
2. `_advance_turn()` called (via End Turn button or Space key)
3. Next unit in turn order becomes active
4. If enemy unit, AI executes immediately
5. AI completes movement
6. `_advance_turn()` called again automatically
7. Next unit's turn begins

---

## Pathfinding Notes

### Challenge: Occupied Goal Tiles

**Problem**: The `find_path()` function returns None if the goal tile is occupied (line 147-148 of pathfinding.py). Since investigators occupy their tiles, pathing directly to them fails.

**Solution**: Path to an **adjacent tile** instead of the target's exact position.

**Algorithm**:
1. Find all 8 neighbors of target position
2. Filter to unoccupied, non-blocking tiles
3. Select the adjacent tile closest to the enemy
4. Path to that tile instead

**Example**:
```
Investigator at (5, 5) - OCCUPIED
Adjacent tiles: (4,4), (4,5), (4,6), (5,4), (5,6), (6,4), (6,5), (6,6)
Enemy at (9, 5)
Best adjacent tile: (6, 5) - straight line, closest
Path to (6, 5) instead of (5, 5)
```

---

## Testing

### Test Suite

**File**: `testing/test_enemy_ai.py`

**Tests**:
1. ✅ `test_cultist_targeting()` - Cultists select highest health target
2. ✅ `test_hound_targeting()` - Hounds select nearest target
3. ✅ `test_cultist_movement()` - Cultists move 1 tile towards target
4. ✅ `test_hound_movement()` - Hounds move 2 tiles towards target
5. ✅ `test_blocked_movement()` - AI pathfinds around obstacles

**Run Tests**:
```bash
uv run python testing/test_enemy_ai.py
```

**Expected Output**:
```
============================================================
ENEMY AI TEST SUITE
============================================================

=== TEST: Cultist Targeting ===
[OK] Cultist correctly targets highest health investigator

=== TEST: Hound Targeting ===
[OK] Hound correctly targets nearest investigator

=== TEST: Cultist Movement (1 tile) ===
[OK] Cultist moved 1 tile towards target

=== TEST: Hound Movement (2 tiles) ===
[OK] Hound moved 2 tiles towards target

=== TEST: Blocked Movement ===
[OK] Hound handled blocked terrain (moved to (6, 6))

============================================================
ALL TESTS PASSED!
============================================================
```

---

## Future Enhancements

### Phase 1.5 - Attack Logic

After movement, enemies should check if targets are in range and attack:

```python
# TODO in execute_enemy_turn() (line 208)
if enemy.can_attack():
    # Check if target is in weapon range
    distance = grid.get_distance(enemy.position[0], enemy.position[1],
                                target.position[0], target.position[1])

    if distance <= enemy.weapon_range:
        # Check line of sight (requires line_of_sight.py)
        if line_of_sight.has_clear_shot(enemy.position, target.position, grid):
            # Execute attack (requires combat_resolver.py)
            combat_resolver.resolve_attack(enemy, target, grid)
```

### Phase 2+ - Advanced AI

**Tactical Improvements**:
- Use cover (prefer moving to cover tiles)
- Flanking maneuvers (coordinate with other enemies)
- Focus fire (all enemies target same investigator)
- Retreat when low health
- Use special abilities

**Strategic Improvements**:
- Threat assessment (prioritize dangerous investigators)
- Formation tactics (maintain group cohesion)
- Objective-based behavior (protect VIPs, hold positions)

---

## Design Decisions

### Why Highest Health (Cultists) vs Nearest (Hounds)?

**Cultists** (ranged):
- Stay at distance (3 tile range)
- Target healthy units to spread damage
- Avoid overkill on wounded targets
- Simulation of cautious human tactics

**Hounds** (melee):
- Must close to 1 tile range
- Prioritize speed over strategy
- Animalistic "chase nearest prey" behavior
- Creates pressure on frontline units

### Why Different Movement Speeds?

**Cultists**: 1 tile per turn
- Matches their 4 tile movement range (used for positioning)
- Conservative advancement
- Time to shoot before closing distance

**Hounds**: 2 tiles per turn
- Uses their 6 tile movement range (fast movement)
- Aggressive closing speed
- Compensates for melee-only attacks
- Creates urgency for player

---

## Common Issues

### Issue: Enemy doesn't move

**Possible Causes**:
1. No valid path (surrounded by terrain/units)
2. All targets incapacitated
3. Already adjacent to target

**Debug**: Check console output for AI messages

### Issue: Enemy moves inefficiently

**Possible Causes**:
1. Terrain obstacles force longer path
2. Diagonal movement preference (A* shortest path)
3. Multiple equidistant goals (selects first found)

**Solution**: This is expected behavior - A* finds *shortest* path, not "smartest"

---

## Code Example: Adding New Enemy Type

```python
from entities.enemy import Enemy

class Shoggoth(Enemy):
    def __init__(self, name: str = "Shoggoth"):
        super().__init__(
            name=name,
            max_health=20,
            max_sanity=20,
            accuracy=50,
            will=15,
            movement_range=3,
            symbol="[S]"
        )
        self.equip_weapon(equipment.SHOGGOTH_SLAM)

# In enemy_ai.py execute_enemy_turn():
elif isinstance(enemy, Shoggoth):
    # Shoggoths target lowest sanity investigator, move 1 tile
    target = find_lowest_sanity_target(investigators)
    max_movement = 1
    print(f"  {enemy.name} targeting lowest sanity investigator")
```

---

**Last Updated**: 2025-12-08 (Session 10)
**Author**: Claude Sonnet 4.5
**Status**: Production Ready
