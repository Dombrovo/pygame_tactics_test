# Combat Deck System Documentation

**Created**: 2025-12-08 (Session 11)
**Status**: ✅ Complete

---

## Overview

The combat deck system implements a personal deck-based combat resolution mechanic similar to **Gloomhaven** or **Arkham Horror LCG**. Each investigator has their own deck of 20 cards that they draw from during attack resolution, adding tactical variability and character progression opportunities.

**Key Benefits**:
- **Tactical Variability**: No guaranteed outcomes, adds tension to combat
- **Character Progression**: Upgrade decks over time by adding good cards or removing bad ones
- **Risk/Reward Gameplay**: Balance pushing your luck vs playing safe
- **Memorable Moments**: Critical hits and auto-misses create exciting stories

---

## File Locations

- **Module**: `entities/combat_deck.py` (Card and CombatDeck classes)
- **Integration**: `entities/investigator.py` (lines 10, 263)
- **Tests**: `testing/test_combat_deck.py`

---

## Card System

### CardType Enum

Cards come in five types, each with different effects:

```python
class CardType(Enum):
    NULL = "null"       # Auto-miss (ignore all modifiers)
    MULTIPLY = "x2"     # Double damage (critical hit)
    PLUS = "+"          # Positive modifier (+2, +1)
    MINUS = "-"         # Negative modifier (-1, -2)
    ZERO = "0"          # No modifier (baseline)
```

### Card Class

Represents a single combat card with a modifier value.

**Constructor**:
```python
Card(card_type: CardType, modifier: int = 0, name: str = None)
```

**Key Methods**:

#### `apply_to_damage(base_damage: int) -> int`

Applies the card's modifier to base damage.

**Rules**:
- **NULL**: Always returns 0 (auto-miss)
- **MULTIPLY**: Returns `base_damage * 2`
- **PLUS/MINUS/ZERO**: Returns `max(0, base_damage + modifier)`

**Examples**:
```python
# +2 card
card = Card(CardType.PLUS, 2)
card.apply_to_damage(5)  # Returns 7

# x2 card (critical hit)
card = Card(CardType.MULTIPLY, 2)
card.apply_to_damage(5)  # Returns 10

# NULL card (auto-miss)
card = Card(CardType.NULL, 0)
card.apply_to_damage(5)  # Returns 0

# -1 card
card = Card(CardType.MINUS, -1)
card.apply_to_damage(5)  # Returns 4
```

#### `is_null() -> bool`

Check if this is an auto-miss card.

#### `is_multiply() -> bool`

Check if this is a critical hit card.

---

## Combat Deck System

### Standard Deck Composition

All investigators start with a standard 20-card deck:

| Card | Count | Probability | Effect |
|------|-------|-------------|--------|
| NULL | 1 | 5% | Auto-miss (0 damage) |
| x2 | 1 | 5% | Double damage |
| +2 | 1 | 5% | +2 damage |
| +1 | 5 | 25% | +1 damage |
| +0 | 7 | 35% | No modifier |
| -1 | 5 | 25% | -1 damage |

**Total**: 20 cards

**Expected Value**: Approximately +0.15 modifier on average (slightly positive)

### CombatDeck Class

Manages a personal combat deck with draw pile, discard pile, and statistics.

**Constructor**:
```python
CombatDeck(owner_name: str = "Unknown")
```

**Attributes**:
- `draw_pile: List[Card]` - Cards available to draw
- `discard_pile: List[Card]` - Cards already drawn
- `total_cards_drawn: int` - Lifetime statistics
- `nulls_drawn: int` - Count of auto-misses
- `crits_drawn: int` - Count of critical hits

### Core Methods

#### `draw() -> Optional[Card]`

Draw a card from the deck.

**Behavior**:
1. If draw pile empty → automatically reshuffle discard pile
2. Draw top card from draw pile
3. Move card to discard pile
4. Update statistics
5. Return the card

**Example**:
```python
card = deck.draw()
print(f"Drew: {card.name}")  # "Drew: +1"
```

#### `shuffle()`

Shuffle the draw pile randomly.

#### `reshuffle_discard()`

Move all cards from discard pile back to draw pile and shuffle.

Called automatically when draw pile is empty.

#### `reset()`

Reset deck for a new battle.

Moves all cards from discard back to draw pile and shuffles. **Does NOT change deck composition** - permanent improvements persist.

**Example**:
```python
# At start of new battle
investigator.reset_combat_deck()
```

### Deck Management

#### `add_card(card: Card)`

Add a card to the deck (deck improvement).

**Example**:
```python
# Add a powerful +2 card as a reward
deck.add_card(Card(CardType.PLUS, 2))
```

#### `remove_card(card_name: str) -> bool`

Remove a card from the deck (deck improvement).

Searches both draw pile and discard pile for the first matching card.

**Returns**: True if card found and removed, False otherwise

**Example**:
```python
# Remove a -1 card to improve deck
success = deck.remove_card("-1")
if success:
    print("Deck improved! Removed -1 card")
```

### Information Methods

#### `size() -> int`

Total number of cards in deck (draw + discard).

#### `cards_remaining() -> int`

Cards left in draw pile before reshuffle.

#### `get_deck_composition() -> Dict[str, int]`

Get complete deck composition.

**Returns**: Dictionary mapping card names to counts

**Example**:
```python
composition = deck.get_deck_composition()
# {'+2': 1, '+1': 5, '+0': 7, '-1': 5, 'x2': 1, 'NULL': 1}
```

#### `get_statistics() -> Dict[str, float]`

Get performance statistics.

**Returns**:
```python
{
    "total_draws": 25,
    "crit_rate": 0.04,    # 4% crit rate
    "null_rate": 0.04,    # 4% miss rate
}
```

#### `peek(count: int = 1) -> List[Card]`

Look at top N cards without drawing them.

Useful for abilities that preview upcoming cards.

---

## Factory Functions

Pre-configured deck generators for different scenarios.

### `create_standard_deck(owner_name: str) -> CombatDeck`

Create the standard 20-card deck.

Default deck for all investigators.

**Example**:
```python
deck = create_standard_deck("John Doe")
```

### `create_improved_deck(owner_name: str, remove_negatives: int = 2) -> CombatDeck`

Create an improved deck with fewer negative cards.

Represents a veteran investigator who has upgraded their deck.

**Parameters**:
- `remove_negatives`: Number of -1 cards to remove (default 2)

**Composition**: Standard deck minus 2x -1 cards (18 total cards)

### `create_blessed_deck(owner_name: str) -> CombatDeck`

Create a blessed deck with enhanced positive cards.

Could represent divine protection or luck.

**Modifications**:
- +2x +1 cards
- +1x x2 card (extra crit)
- -1x -1 card

**Total**: 23 cards

### `create_cursed_deck(owner_name: str) -> CombatDeck`

Create a cursed deck with extra negative cards.

Could represent madness or bad luck.

**Modifications**:
- +2x -1 cards
- +1x NULL card (extra auto-miss)

**Total**: 23 cards

---

## Integration with Investigators

### Investigator Class Additions

Each investigator automatically gets a combat deck on creation.

**New Attributes**:
```python
class Investigator:
    combat_deck: CombatDeck  # Personal deck (persists across battles)
```

**New Methods**:

#### `reset_combat_deck()`

Reset the deck at the start of a battle.

```python
# At battle start
for inv in investigators:
    inv.reset_combat_deck()
```

#### `draw_combat_card() -> Optional[Card]`

Draw a card from the investigator's deck.

```python
# During attack resolution
card = investigator.draw_combat_card()
modified_damage = card.apply_to_damage(base_damage)
```

#### `get_deck_stats() -> Dict[str, Any]`

Get comprehensive deck information.

**Returns**:
```python
{
    "total_cards": 20,
    "cards_remaining": 15,
    "composition": {'+0': 7, '+1': 5, ...},
    "statistics": {"total_draws": 5, "crit_rate": 0.0, ...}
}
```

---

## Usage in Combat Resolution

When implementing combat resolution (Phase 1.5), integrate the deck system:

### Attack Resolution Flow

```python
def resolve_attack(attacker: Investigator, target: Unit, base_damage: int) -> dict:
    """
    Resolve an attack with deck-based modification.

    Args:
        attacker: The attacking investigator
        target: The target unit
        base_damage: Base damage before modifiers

    Returns:
        Dictionary with attack results
    """
    # Step 1: Calculate hit chance (existing system)
    hit_chance = calculate_hit_chance(attacker, target, distance, cover)
    roll = random.randint(1, 100)

    # Step 2: Draw combat card
    card = attacker.draw_combat_card()

    # Step 3: Check for auto-miss (NULL card)
    if card.is_null():
        return {
            "hit": False,
            "damage": 0,
            "card": card.name,
            "auto_miss": True
        }

    # Step 4: Check hit roll
    if roll > hit_chance:
        return {
            "hit": False,
            "damage": 0,
            "card": card.name
        }

    # Step 5: Apply card modifier to damage
    modified_damage = card.apply_to_damage(base_damage)

    # Step 6: Apply damage to target
    target.take_damage(modified_damage)

    return {
        "hit": True,
        "damage": modified_damage,
        "card": card.name,
        "crit": card.is_multiply()
    }
```

### UI Integration

Display the drawn card in the battle log:

```python
result = resolve_attack(attacker, target, base_damage)

if result["auto_miss"]:
    print(f"{attacker.name} drew {result['card']} - AUTO-MISS!")
elif result["crit"]:
    print(f"{attacker.name} drew {result['card']} - CRITICAL HIT! {result['damage']} damage!")
elif result["hit"]:
    print(f"{attacker.name} drew {result['card']} - Hit for {result['damage']} damage")
else:
    print(f"{attacker.name} drew {result['card']} - Miss!")
```

---

## Deck Progression System (Phase 2+)

### Upgrade Opportunities

Investigators can improve their decks through various means:

#### 1. Mission Rewards

```python
# After successful mission
investigator.combat_deck.remove_card("-1")  # Remove a curse
print("Deck improved! Removed -1 card")
```

#### 2. Base Facility (Training Room)

```python
# Spend resources to upgrade deck
cost = 100  # Gold
if player_funds >= cost:
    investigator.combat_deck.add_card(Card(CardType.PLUS, 1))
    player_funds -= cost
```

#### 3. Character Progression

```python
# On level up
if investigator.experience >= 1000:
    investigator.combat_deck.remove_card("-1")
    investigator.level_up()
```

#### 4. Trait-Based Modifications

```python
# Apply "Veteran Marksman" trait
if "Veteran Marksman" in investigator.traits:
    investigator.combat_deck.add_card(Card(CardType.PLUS, 1))
```

### Deck Degradation

Investigators can also suffer permanent deck penalties:

#### 1. Permanent Injuries

```python
# After being reduced to 0 HP
if investigator.current_health <= 0:
    investigator.add_injury("Shaky Hands")
    investigator.combat_deck.add_card(Card(CardType.MINUS, -1))
```

#### 2. Madness Effects

```python
# After witnessing eldritch horror
if investigator.current_sanity <= 0:
    investigator.add_madness("Paranoid Delusions")
    investigator.combat_deck.add_card(Card(CardType.NULL, 0))
```

---

## Balance Considerations

### Expected Damage Modifiers

For a standard 20-card deck:

| Card | Count | Modifier | Expected Value |
|------|-------|----------|----------------|
| NULL | 1 | 0 (auto-miss) | -5 |
| x2 | 1 | +5 (for 5 base) | +0.25 |
| +2 | 1 | +2 | +0.10 |
| +1 | 5 | +1 | +0.25 |
| +0 | 7 | 0 | 0 |
| -1 | 5 | -1 | -0.25 |

**Total Expected Modifier**: +0.10 per draw (slightly positive)

**Note**: The NULL card has significant impact (-5 damage on 5 base damage = -0.25 expected value).

### Deck Improvement Impact

Removing 2x -1 cards from standard deck:
- Old expected value: +0.10
- New expected value: +0.21
- **Impact**: ~+0.11 average damage increase (significant!)

### Balancing Upgrades

Recommended costs for deck improvements:

| Upgrade | Cost | Impact |
|---------|------|--------|
| Remove -1 card | 100 gold | +0.05 avg damage |
| Add +1 card | 150 gold | +0.05 avg damage |
| Remove -1 and add +1 | 200 gold | +0.10 avg damage |
| Add +2 card | 300 gold | +0.10 avg damage |
| Add x2 card | 500 gold | +0.25 avg damage |

---

## Testing

### Test Suite

**File**: `testing/test_combat_deck.py`

**Tests**:
1. ✅ `test_card_modifiers()` - Card damage calculations
2. ✅ `test_standard_deck_composition()` - Deck has correct cards
3. ✅ `test_deck_drawing()` - Drawing mechanics
4. ✅ `test_deck_reshuffle()` - Automatic reshuffle when empty
5. ✅ `test_deck_improvement()` - Removing cards
6. ✅ `test_deck_statistics()` - Statistics tracking
7. ✅ `test_investigator_integration()` - Investigator has deck
8. ✅ `test_special_decks()` - Blessed/cursed/improved variants
9. ✅ `test_combat_simulation()` - Simulate 25 attacks

**Run Tests**:
```bash
uv run python testing/test_combat_deck.py
```

**Expected Output**:
```
============================================================
COMBAT DECK TEST SUITE
============================================================

=== TEST: Card Modifiers ===
[OK] +2 card: 5 -> 7
[OK] +1 card: 5 -> 6
[OK] -1 card: 5 -> 4
...

============================================================
ALL TESTS PASSED!
============================================================
```

---

## Design Decisions

### Why Deck-Based Resolution?

**Alternatives Considered**:
1. **Pure RNG**: `damage = base_damage + random(-2, +2)`
   - Pros: Simple, fast
   - Cons: No player agency, no progression, forgettable

2. **D20 System**: Roll d20 + modifiers
   - Pros: Familiar to D&D players
   - Cons: Wide variance, hard to balance, no progression

3. **Deck System** (chosen):
   - Pros: Bounded variance, progression system, memorable moments, player agency
   - Cons: More complex to implement

### Why 20 Cards?

- **Small enough**: Easy to track, quick to cycle through
- **Large enough**: Enough variance to be interesting
- **Divisible**: Easy math for probabilities (5% per card)
- **Proven**: Gloomhaven uses 20-card decks successfully

### Why Auto-Reshuffle?

Instead of requiring manual reshuffle:
- **Convenience**: Players don't need to remember
- **Flow**: Keeps combat moving smoothly
- **Consistency**: No missed reshuffles leading to errors

### Why NULL Instead of Miss?

NULL is an auto-miss that ignores hit chance calculation:
- **Dramatic**: Creates tense moments ("Please don't draw NULL!")
- **Balanced**: Ensures even high accuracy can miss
- **Thematic**: Fits cosmic horror theme (reality betrays you)

---

## Future Enhancements

### Phase 2: Campaign Integration

- Persistent deck across battles
- Deck improvements as mission rewards
- Facility for deck training/upgrades
- Deck composition saved in save files

### Phase 3: Advanced Cards

Special cards with unique effects:

```python
class StunCard(Card):
    """Card that stuns target on hit."""
    def apply_to_damage(self, base_damage: int) -> int:
        # Apply stun effect to target
        return base_damage + 2

class PierceCard(Card):
    """Card that ignores armor."""
    def apply_to_damage(self, base_damage: int) -> int:
        # Set pierce flag
        return base_damage + 1
```

### Phase 4: Scenario Modifiers

Environmental or mission-specific deck modifications:

```python
# Cursed mission - all investigators draw from a shared curse deck
curse_deck = create_cursed_deck("Mission Curse")

# Dark ritual - extra NULL cards added temporarily
for inv in investigators:
    inv.combat_deck.add_card(Card(CardType.NULL, 0))
```

### Phase 5: Nemesis Decks

Bosses have their own deck that players draw from when attacked:

```python
class Boss:
    def __init__(self):
        self.nemesis_deck = create_boss_deck()  # Player draws from this!
```

---

## Common Issues

### Issue: Deck runs out mid-battle

**Cause**: Discard pile not being reshuffled

**Solution**: `draw()` method automatically reshuffles. If deck is completely empty (no cards in draw OR discard), returns None.

### Issue: Statistics don't persist

**Cause**: Statistics track lifetime draws, not saved to disk

**Solution**: In Phase 2, add statistics to save file.

### Issue: Deck feels too swingy

**Cause**: Small sample size (few draws per battle)

**Solution**: This is intentional! Creates exciting moments. Can reduce variance by removing extreme cards or increasing deck size.

---

## Code Examples

### Example 1: Drawing and Applying a Card

```python
# During attack resolution
investigator = get_current_investigator()
base_damage = investigator.weapon_damage

# Draw a card
card = investigator.draw_combat_card()
print(f"{investigator.name} drew: {card.name}")

# Apply modifier
if card.is_null():
    print("AUTO-MISS!")
    final_damage = 0
else:
    final_damage = card.apply_to_damage(base_damage)
    if card.is_multiply():
        print(f"CRITICAL HIT! {final_damage} damage!")
    else:
        print(f"{final_damage} damage")

# Apply to target
target.take_damage(final_damage)
```

### Example 2: Deck Improvement Reward

```python
def apply_mission_reward(investigator: Investigator, reward_type: str):
    """Apply mission reward to investigator."""
    if reward_type == "deck_improvement":
        # Remove a -1 card
        success = investigator.combat_deck.remove_card("-1")
        if success:
            print(f"{investigator.name}'s deck improved! Removed -1 card")
        else:
            print("No -1 cards left to remove!")

    elif reward_type == "blessed":
        # Add a +1 card
        investigator.combat_deck.add_card(Card(CardType.PLUS, 1))
        print(f"{investigator.name} received a blessing! Added +1 card")
```

### Example 3: Display Deck Composition in UI

```python
def render_deck_info(screen: pygame.Surface, investigator: Investigator):
    """Render deck composition on screen."""
    composition = investigator.combat_deck.get_deck_composition()
    stats = investigator.combat_deck.get_statistics()

    y = 100
    for card_name, count in sorted(composition.items()):
        text = f"{card_name}: {count}x"
        render_text(screen, text, (50, y))
        y += 30

    # Show statistics
    y += 20
    render_text(screen, f"Total draws: {stats['total_draws']}", (50, y))
    y += 30
    render_text(screen, f"Crit rate: {stats['crit_rate']:.1%}", (50, y))
    y += 30
    render_text(screen, f"Miss rate: {stats['null_rate']:.1%}", (50, y))
```

---

**Last Updated**: 2025-12-08 (Session 11)
**Author**: Claude Sonnet 4.5
**Status**: Production Ready
