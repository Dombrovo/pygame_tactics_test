# Enemy AI System Documentation

**Created**: 2025-12-08 (Session 10)
**Updated**: 2025-12-13 (Session 14 - Attack Logic Added)
**Status**: ✅ Complete (Movement + Attacks)

---

## Overview

The enemy AI system implements tactical combat behaviors for enemy units during their turns. Different enemy types use different strategies to approach and engage player investigators, moving toward targets and attacking when in range. The system integrates with the combat resolution system to handle full attack sequences including line of sight checks, hit chance calculation, and damage application. The system also includes randomized squad generation to provide variety across battles.

---

## File Location

- **Module**: `combat/enemy_ai.py` (AI movement logic)
- **Module**: `entities/enemy.py` (Enemy classes and squad generation)
- **Integration**: `combat/battle_screen.py` (lines 15, 910-916)
- **Tests**: `testing/test_enemy_ai.py`

---

## AI Behaviors by Enemy Type

### Cultist (Ranged Enemy)

**Targeting Strategy**: Targets investigator with **highest current health**
**Movement**: Moves **1 tile** towards target per turn
**Attack**: After moving, attacks target if in range (3 tiles) with line of sight

**Rationale**: Cultists use conservative tactics, focusing fire on healthy targets rather than finishing off wounded ones. This creates pressure on the player's strongest units.

### Hound of Tindalos (Melee Enemy)

**Targeting Strategy**: Targets **nearest** investigator
**Movement**: Moves **2 tiles** towards target per turn
**Attack**: After moving, attacks target if in range (1 tile) with line of sight

**Rationale**: Hounds use aggressive pack tactics, rapidly closing distance with the nearest prey using their superior speed.

---

## Enemy Squad Generation

### Random Squad Selection

Each battle randomly selects one of four pre-configured squad types to provide variety and different tactical challenges.

**Function**: `create_test_enemies()` in `entities/enemy.py`

**Squad Types**:

1. **Balanced Squad** (`create_balanced_squad()`):
   - 2 Cultists + 2 Hounds
   - Balanced mix of ranged and melee threats
   - Original/standard difficulty

2. **Cultist Squad** (`create_cultist_squad()`):
   - 4 Cultists
   - All ranged attackers
   - Easier encounter (less mobility, spread out)

3. **Hound Pack** (`create_hound_pack()`):
   - 3 Hounds
   - All fast melee
   - Harder encounter (aggressive, high speed)

4. **Mixed Squad** (`create_cultists_with_hound_pack()`):
   - 3 Cultists + 1 Hound
   - Heavy ranged with single melee threat
   - Tactical variety

**Implementation**:
```python
def create_test_enemies() -> List[Enemy]:
    import random
    # Store function references (not calling them yet)
    enemy_squad_choices = {
        'balanced': create_balanced_squad,
        'cultist': create_cultist_squad,
        'hounds': create_hound_pack,
        'cultists_with_hound': create_cultists_with_hound_pack
    }
    # Pick a random squad type and call the function
    enemy_squad = random.choice(list(enemy_squad_choices.keys()))
    return enemy_squad_choices[enemy_squad]()
```

### Enemy Class Constructors

**Important**: Enemy constructors have been simplified to use the equipment system. Weapon stats (range, attack type, sanity damage) are provided by equipped weapons, not constructor parameters.

**Cultist Constructor**:
```python
def __init__(self, name: str = "Cultist"):
    super().__init__(
        name=name,
        max_health=10,
        max_sanity=8,
        accuracy=60,
        will=3,
        movement_range=4,
        symbol="🔫"
    )
    # Equip weapon (weapon provides range/attack type/damage)
    self.equip_weapon(equipment.CULTIST_PISTOL)
```

**Hound Constructor**:
```python
def __init__(self, name: str = "Hound of Tindalos"):
    super().__init__(
        name=name,
        max_health=8,
        max_sanity=15,
        accuracy=75,
        will=10,
        movement_range=6,
        symbol="🐺"
    )
    # Equip weapon (weapon provides range/attack type/sanity damage)
    self.equip_weapon(equipment.HOUND_CLAWS)
```

**Note**: The old parameters `weapon_range`, `attack_type`, and `sanity_damage` have been removed from enemy constructors. Use `enemy.equipped_weapon.weapon_range`, `enemy.equipped_weapon.attack_type`, and `enemy.equipped_weapon.sanity_damage` instead.

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

#### `execute_enemy_turn(enemy: Enemy, investigators: List[Investigator], grid: Grid) -> Optional[Dict[str, Any]]`

Main AI entry point - executes an enemy unit's turn.

**Process**:
1. Check if enemy can act (not incapacitated)
2. Select target based on enemy type
3. Calculate movement destination
4. Execute movement via `grid.move_unit()`
5. Check if target is in range with line of sight
6. If yes, execute attack via `combat_resolver.resolve_attack()`
7. Print turn information to console

**Parameters**:
- `enemy`: The enemy unit taking its turn
- `investigators`: List of all investigator units (for targeting)
- `grid`: The battlefield grid

**Returns**: Attack result dictionary if attack was executed (for popup display), None otherwise

**Console Output**:
```
Enemy Turn: Hound Alpha
  Hound Alpha targeting nearest investigator
  Target: Regina Cross (HP: 12/15)
  Hound Alpha moves from (9, 7) to (7, 6)
  Hound Alpha attacking Regina Cross...
```

---

## Integration with Battle Screen

The AI is called automatically during enemy turns in the turn order system.

**Location**: `combat/battle_screen.py`, `_advance_turn()` method (lines 1105-1128)

```python
# If enemy turn, execute AI
if self.current_turn_unit.team == "enemy":
    # Execute enemy AI behavior (move + attack)
    attack_result = enemy_ai.execute_enemy_turn(self.current_turn_unit, self.player_units, self.grid)

    # Redraw the screen to show the enemy's movement immediately
    self.draw()
    pygame.display.flip()

    # Pause to let player see the enemy's movement
    pygame.time.wait(500)  # 500ms pause after movement

    # If enemy attacked, show attack result popup
    if attack_result:
        target_unit = attack_result.get("target")
        if target_unit:
            self._show_attack_result(attack_result, target_unit)
            # Redraw to show any changes from attack (HP, incapacitation)
            self.draw()
            pygame.display.flip()
            # Additional pause after attack
            pygame.time.wait(500)  # 500ms pause after attack

    # After AI completes its actions, advance to next turn
    self._advance_turn()
```

**Turn Flow**:
1. Player investigator's turn (user controlled)
2. `_advance_turn()` called (via End Turn button or Space key)
3. Next unit in turn order becomes active
4. If enemy unit, AI executes immediately
5. AI completes movement → screen redraws → 500ms pause
6. AI attempts attack if in range → damage popup shown → 500ms pause
7. `_advance_turn()` called again automatically
8. Next unit's turn begins

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

## Attack System Integration

### ✅ Implemented Attack Logic (Session 14)

After movement, enemies check if targets are in range and attack:

```python
# In execute_enemy_turn() after movement completes
if not enemy.position or not target.position:
    return None

# Check if target is within attack range and has line of sight
can_attack_result, reason = can_attack(
    enemy.position,
    target.position,
    enemy.weapon_range,
    grid
)

if can_attack_result:
    # Target is in range with LOS - execute attack!
    print(f"  {enemy.name} attacking {target.name}...")
    attack_result = resolve_attack(enemy, target, grid)

    # Add attacker and target info to result for popup display
    attack_result["attacker"] = enemy
    attack_result["target"] = target

    return attack_result
else:
    # Can't attack (out of range or no LOS)
    print(f"  {enemy.name} cannot attack: {reason}")
    return None
```

**Attack Result Display**:
- Damage popups shown via `Popup.show_damage_notification()`
- No combat cards for enemies (investigators-only feature)
- Hit/miss displayed with damage amount
- Incapacitation notifications shown if target dies

### Future Enhancements - Phase 2+ Advanced AI

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
from entities import equipment

class Shoggoth(Enemy):
    """
    Shoggoth - Large amorphous horror
    Targets investigators with low sanity to break morale
    """
    def __init__(self, name: str = "Shoggoth"):
        super().__init__(
            name=name,
            max_health=20,      # Very tanky
            max_sanity=20,      # Eldritch entity
            accuracy=50,        # Slow but hits hard
            will=15,            # High will
            movement_range=3,   # Slow movement
            symbol="🦑"         # Tentacle symbol
        )
        # Equip weapon (provides attack stats)
        self.equip_weapon(equipment.TENTACLE_STRIKE)

# In enemy_ai.py execute_enemy_turn():
elif isinstance(enemy, Shoggoth):
    # Shoggoths target lowest sanity investigator, move 1 tile
    target = find_lowest_sanity_target(investigators)
    max_movement = 1
    print(f"  {enemy.name} targeting lowest sanity investigator")

# Add to squad generation in entities/enemy.py:
def create_shoggoth_encounter() -> List[Enemy]:
    """Create a boss encounter with 1 Shoggoth + 2 Cultists."""
    return [
        Shoggoth(name="Primordial Shoggoth"),
        Cultist(name="Cultist Alpha"),
        Cultist(name="Cultist Beta"),
    ]
```

---

**Last Updated**: 2025-12-13 (Session 14 - Attack Logic Implementation)
**Author**: Claude Sonnet 4.5
**Status**: Production Ready (Movement + Attacks Complete)
