# Eldritch Tactics - Development Roadmap

**Last Updated**: 2025-11-29
**Current Phase**: Phase 1 MVP (~75% Complete)

This document outlines the long-term vision, planned features, and implementation roadmap for Eldritch Tactics. For current project state and completed features, see [CLAUDE.md](CLAUDE.md).

---

## Table of Contents

1. [MVP (Phase 1) - Playable Combat Prototype](#mvp-phase-1---playable-combat-prototype)
2. [Target Architecture (Full Game)](#target-architecture-full-game)
3. [Core Systems Design](#core-systems-design)
4. [Phase 2: Meta-Layer Strategy System](#phase-2-meta-layer-strategy-system)
5. [Phase 3: Advanced Combat Features](#phase-3-advanced-combat-features)
6. [Phase 4: Polish & Advanced Features](#phase-4-polish--advanced-features)
7. [Implementation Phases Summary](#implementation-phases-summary)
8. [Key Design Principles](#key-design-principles)
9. [Future Considerations](#future-considerations)
10. [Open Design Questions](#open-design-questions)

---

## MVP (Phase 1) - Playable Combat Prototype

### MVP Scope
**Goal**: Get a single tactical battle playable with core mechanics working.

### Remaining Tasks for MVP Completion

**Combat Mechanics** (Next Session):
- Line of sight calculation (Bresenham's algorithm)
- Combat resolution (hit chance, damage)
- Attack actions (ranged, melee)
- Basic enemy AI (move toward player, attack if in range)

**Completed in Session 9**:
- ✅ Equipment & Inventory System (weapons, damage, range, modifiers)

### Tactical Combat Features
- 10x10 grid battlefield ✅
- Turn-based combat (player phase → enemy phase) ✅
- 3-4 investigators vs 3-4 enemies per battle ✅
- Two enemy types:
  - **Cultists**: Ranged attackers (3 tile range) ✅
  - **Hounds of Tindalos**: Melee monsters (sanity damage on hit) ✅
- Basic cover system (half/full cover) ✅
- Line of sight calculations ⏳
- Hit chance based on distance and cover ⏳

### Character Systems
- **Dual resource bars**: Health and Sanity (0 in either = incapacitated) ✅
- **Actions per turn**: 2 action points (Move-Move, Move-Attack, Attack-Attack) ✅
- **Equipment system**: Weapons determine damage, range, attack type ✅
- **Attack types** (weapon-based):
  - Move (up to movement range) ✅
  - Ranged Attack (weapon_range, requires line of sight) ⏳
  - Melee Attack (weapon_range = 1) ⏳

### Win/Lose Conditions
- **Win**: Eliminate all enemies ✅
- **Lose**: All investigators incapacitated ✅
- **Post-battle**: Return to simple mission select screen ⏳

---

## Target Architecture (Full Game)

### Planned File Structure

```
eldritch_tactics/
├── main.py                 # Entry point, game loop
├── config.py              # Constants and configuration
├── game_state.py          # Core game state manager
│
├── combat/
│   ├── __init__.py
│   ├── battle.py          # Battle controller
│   ├── grid.py            # Grid/map representation
│   ├── pathfinding.py     # Movement calculations
│   ├── line_of_sight.py   # LOS calculations
│   └── combat_resolver.py # Hit chance, damage resolution
│
├── entities/
│   ├── __init__.py
│   ├── unit.py            # Base unit class
│   ├── investigator.py    # Player units
│   ├── enemy.py           # Enemy base class
│   └── abilities.py       # Ability system (extensible)
│
├── ui/
│   ├── __init__.py
│   ├── renderer.py        # Main rendering system
│   ├── grid_renderer.py   # Grid/battlefield drawing
│   ├── ui_elements.py     # Buttons, panels, info displays
│   └── input_handler.py   # Mouse/keyboard input
│
├── data/
│   ├── __init__.py
│   ├── unit_data.py       # Unit stat definitions
│   ├── map_data.py        # Map/scenario definitions
│   └── trait_data.py      # Character flaws/traits
│
└── meta/                  # (Phase 2+)
    ├── __init__.py
    ├── campaign.py        # Campaign state
    ├── roster.py          # Investigator management
    ├── base.py            # Base building
    └── research.py        # Tech/knowledge tree
```

### Core Data Structures

These represent the planned expansions to current classes:

#### Investigator (extends Unit)
```python
class Investigator(Unit):
    def __init__(self):
        super().__init__()
        # Phase 2+ additions:
        self.traits: list[Trait]  # Character flaws/bonuses
        self.experience: int
        self.kills: int
        self.missions_survived: int
        self.permanent_injuries: list[str]
        self.permanent_madness: list[str]
        self.background: str  # Professor, Soldier, Detective, etc.
        self.equipped_weapon: Equipment | None
        self.equipped_armor: Equipment | None
        self.equipped_accessories: list[Equipment]  # Max 2
```

#### Battle State (Phase 2+)
```python
class BattleState:
    def __init__(self):
        self.grid: Grid  # 10x10 grid of tiles
        self.player_units: list[Investigator]
        self.enemy_units: list[Enemy]
        self.current_phase: str  # "player_turn", "enemy_turn", "victory", "defeat"
        self.selected_unit: Unit | None
        self.available_actions: list[Action]
        self.turn_number: int
        self.objectives: list[Objective]  # Mission objectives
        self.turn_timer: int | None  # For timed missions
```

---

## Core Systems Design

### 1. Grid & Movement System

#### Movement Rules (To Be Implemented)
- Units can move up to their `movement_range` in tiles per turn
- Movement costs 1 tile per orthogonal move, 1.4 for diagonal (Euclidean distance)
- Cannot move through enemy units
- Cannot move through full cover/obstacles
- Pathfinding uses A* algorithm

#### Cover System Mechanics
- **Half Cover** (▪️): -20% hit chance for attackers
- **Full Cover** (⬛): -40% hit chance for attackers
- Cover only applies if it's between attacker and target
- Cover doesn't block movement (units can move into/through it)
- Future: Destructible cover

### 2. Combat System

#### Attack Resolution (To Be Implemented)
```python
def calculate_hit_chance(attacker: Unit, target: Unit, distance: int, cover_bonus: int) -> int:
    base_chance = attacker.accuracy
    distance_penalty = distance * 10  # -10% per tile
    cover_penalty = cover_bonus

    final_chance = base_chance - distance_penalty - cover_penalty
    final_chance = max(5, min(95, final_chance))  # Clamp between 5-95%

    return final_chance

def resolve_attack(attacker: Unit, target: Unit) -> dict:
    hit_chance = calculate_hit_chance(attacker, target, distance, cover)
    roll = random.randint(1, 100)

    if roll <= hit_chance:
        # Hit!
        damage = calculate_damage(attacker)
        sanity_damage = attacker.sanity_damage if hasattr(attacker, 'sanity_damage') else 0

        target.current_health -= damage
        target.current_sanity -= sanity_damage

        return {"hit": True, "damage": damage, "sanity_damage": sanity_damage}
    else:
        # Miss
        return {"hit": False}
```

#### Damage Types
- **Health Damage**: Physical attacks reduce health
- **Sanity Damage**: Eldritch attacks/witnessing horrors reduce sanity
- Both reach 0 → unit incapacitated

### 3. Line of Sight System (To Be Implemented)

```python
def has_line_of_sight(start: tuple, end: tuple, grid: Grid) -> bool:
    """
    Bresenham's line algorithm to check if path is clear
    Returns False if any blocking terrain between start and end
    """
    # Implementation uses raycasting
    # Full cover blocks LOS
    # Half cover does not block LOS
```

### 4. Action System (Extensible)

```python
class Action:
    def __init__(self):
        self.name: str
        self.action_type: str  # "move", "attack", "ability"
        self.action_points_cost: int  # Future: for action point system
        self.cooldown: int

    def can_execute(self, unit: Unit, target) -> bool:
        # Check if action is valid
        pass

    def execute(self, unit: Unit, target) -> dict:
        # Perform the action, return results
        pass

# MVP Actions
class MoveAction(Action):
    # Move to target tile

class RangedAttackAction(Action):
    # Attack target unit at range

class MeleeAttackAction(Action):
    # Attack adjacent unit
```

**Future Actions** (Phase 2+):
- Overwatch (shoot at moving enemies)
- Aimed Shot (bonus accuracy, costs more AP)
- Suppress (reduce enemy accuracy)
- First Aid (heal health)
- Calm Down (restore sanity)
- Use Item (grenades, talismans, etc.)
- Special abilities (class-based)

---

## Phase 2: Meta-Layer Strategy System

### Campaign Structure

#### Overview
- **Timeline**: Track days passed
- **Threat Meter**: Global doomsday counter (0-100%)
- **Locations**: Multiple regions with different threat levels
- **Mission Generation**: Dynamic missions based on threat levels

#### Threat/Doomsday System
```python
class CampaignState:
    def __init__(self):
        self.current_day: int = 0
        self.threat_level: int = 0  # 0-100%
        self.regions: dict[str, Region]
        self.available_missions: list[Mission]
        self.completed_missions: int

    def advance_time(self, days: int):
        # Time passes
        # Threat increases if missions ignored
        # New missions spawn
        # Investigators recover
```

**Threat Escalation**:
- Ignored missions increase threat in that region
- Regional threat spreads to adjacent regions
- At certain thresholds, special events trigger:
  - 25%: Stronger enemy types appear
  - 50%: Multi-mission crisis events
  - 75%: Avatar/boss preparation begins
  - 100%: Game over / final mission

#### Mission Types (Phase 2+)
1. **Investigation**: Gather intel, low combat
2. **Raid**: Assault cultist hideout, medium combat
3. **Defense**: Protect location from attack
4. **Terror**: Respond to public incident, time pressure
5. **Ritual Disruption**: Stop summoning, boss fight
6. **Recovery**: Retrieve artifacts/survivors
7. **Finale**: Confront Great Old One

### Investigator Roster Management

```python
class Roster:
    def __init__(self):
        self.investigators: list[Investigator]
        self.max_active: int = 4  # Squad size
        self.max_total: int = 12  # Roster size

    def recruit_investigator(self) -> Investigator:
        # Generate random investigator with traits

    def retire_investigator(self, inv: Investigator):
        # Remove from roster (death, madness, retirement)
```

#### Investigator Generation
```python
def generate_investigator() -> Investigator:
    inv = Investigator()
    inv.name = random_name()
    inv.background = random.choice(BACKGROUNDS)  # Professor, Soldier, Detective, etc.

    # Randomize stats (within ranges based on background)
    inv.max_health = random.randint(10, 20)
    inv.max_sanity = random.randint(8, 15)
    inv.accuracy = random.randint(60, 80)
    inv.will = random.randint(5, 10)
    inv.movement_range = random.randint(4, 6)

    # Assign starting traits (1-2 flaws, 0-1 bonuses)
    inv.traits = generate_starting_traits()

    return inv
```

#### Character Traits/Flaws System

**Starting Traits**:
- **Veteran**: +10% accuracy, -1 sanity
- **Alcoholic**: -5% accuracy, +2 health
- **Paranoid**: +1 will, -1 movement
- **Brave**: +2 sanity, -5% accuracy
- **Coward**: +5% accuracy, -2 sanity
- **Professor**: Can research, -2 health
- **Athlete**: +1 movement, standard stats
- **Occultist**: +2 will, sees sanity costs before missions

**Acquired Traits** (from experience):
- **Shell Shocked**: Witness 3+ deaths → -2 will permanently
- **Killer**: 10+ kills → +10% accuracy vs humans
- **Scarred**: Reduced to 0 HP → -2 max health permanently
- **Haunted**: Reduced to 0 sanity → -2 max sanity permanently
- **Veteran Commander**: 10+ missions → Nearby allies +5% accuracy
- **Eldritch Exposure**: Survive 5 encounters with high-tier enemies → +3 will, -1 sanity

### Base Building System

```python
class Base:
    def __init__(self):
        self.facilities: dict[str, Facility]
        self.resources: Resources

class Resources:
    def __init__(self):
        self.funds: int = 1000  # Money
        self.intel: int = 0     # Information/leads
        self.artifacts: int = 0  # Eldritch items

class Facility:
    name: str
    level: int
    build_cost: Resources
    build_time: int  # Days
    effect: callable
```

**Facility Types**:
1. **Infirmary**: Heal investigators faster
2. **Asylum**: Recover sanity faster
3. **Library**: Research eldritch knowledge
4. **Workshop**: Craft items/equipment
5. **Training Room**: Improve investigator stats
6. **Containment**: Study artifacts for bonuses
7. **Communications**: Detect missions earlier, reduce threat spread

### Research/Knowledge Tree

```python
class ResearchProject:
    def __init__(self):
        self.name: str
        self.description: str
        self.cost: int  # Intel/artifacts required
        self.time: int  # Days
        self.prerequisites: list[str]  # Other research needed
        self.unlocks: list[str]  # Items, abilities, intel
```

**Research Categories**:
- **Weapons**: Better firearms, blessed ammunition, eldritch weapons
- **Armor**: Protective gear, warding talismans
- **Medicine**: Advanced healing, sanity treatment
- **Occult**: Learn enemy weaknesses, special abilities
- **Enemy Intel**: Reveal enemy stats, unlock countermeasures

**Example Research Tree**:
```
Basic Firearms
  ├── Improved Weapons (+1 damage)
  │     └── Blessed Ammunition (+2 vs eldritch)
  └── Scoped Rifles (+10% accuracy at range)

Occult Studies
  ├── Lesser Ward (ability: +2 will for 3 turns)
  │     └── Greater Ward (area effect)
  └── Banishment Ritual (ability: damage eldritch)
```

### Equipment/Loadout System

**IMPLEMENTED IN PHASE 1 MVP** (Session 9):
- ✅ Base Equipment class
- ✅ Weapon class with damage, range, attack type, accuracy modifiers
- ✅ 12 pre-defined weapons (9 investigator, 3 enemy)
- ✅ Automatic weapon assignment for investigators and enemies
- ✅ Property-based stat delegation

```python
class Equipment:
    def __init__(self):
        self.name: str
        self.slot: str  # "weapon", "armor", "accessory"
        self.icon: str  # Display symbol

class Weapon(Equipment):
    damage: int
    weapon_range: int
    attack_type: str  # "melee" or "ranged"
    accuracy_modifier: int
    sanity_damage: int

class Investigator:
    # ... existing attributes ...
    equipped_weapon: Weapon | None  # ✅ IMPLEMENTED
    equipped_armor: Equipment | None  # Phase 2+
    equipped_accessories: list[Equipment]  # Phase 2+
```

**Equipment Examples**:
- **Weapons** ✅: Revolver, Shotgun, Rifle, Tommy Gun, Combat Knife, Fire Axe, Blessed Blade, Elder Sign Amulet
- **Armor** (Phase 2+): Vest (+2 HP), Warded Coat (+1 will)
- **Accessories** (Phase 2+): First Aid Kit, Elder Sign (1-time sanity protection), Night Vision Goggles

### Crafting System (Phase 3+)
- Combine artifacts + resources to create unique items
- Risky: Crafting with eldritch materials can cause sanity loss
- Recipes discovered through research or missions

---

## Phase 3: Advanced Combat Features

### Expanded Ability System

#### Class-Based Abilities
Investigators develop specializations:

**Classes**:
1. **Soldier**: Combat focused
   - Abilities: Overwatch, Suppressing Fire, Hunker Down
2. **Detective**: Utility focused
   - Abilities: Mark Target (allies get +accuracy), Scan Area (reveal enemy positions)
3. **Occultist**: Anti-eldritch specialist
   - Abilities: Ward (protect against sanity damage), Banish (extra damage vs eldritch)
4. **Medic**: Support focused
   - Abilities: First Aid, Stabilize (prevent death), Rally (restore sanity)
5. **Veteran**: Balanced
   - Abilities: Aimed Shot, Leadership (buff nearby allies)

#### Ability Implementation
```python
class Ability:
    def __init__(self):
        self.name: str
        self.description: str
        self.cooldown: int  # Turns between uses
        self.range: int
        self.target_type: str  # "self", "ally", "enemy", "tile"
        self.effect: callable

    def can_use(self, user: Unit, target) -> bool:
        # Check cooldown, range, LOS

    def use(self, user: Unit, target) -> dict:
        # Execute ability effect
```

### Advanced Enemy Behaviors

#### Enemy AI Types
- **Aggressive**: Rush toward player, prioritize weakest target
- **Defensive**: Use cover, kite players
- **Support**: Buff allies, debuff players
- **Boss**: Multi-phase, special abilities

#### Enemy Variety (Full Game)
**Cultists** (Human enemies):
- Cultist Acolyte (weak ranged)
- Cultist Gunner (strong ranged)
- Cultist Priest (buffs other cultists)
- Cultist Summoner (spawns minor horrors)

**Lesser Horrors**:
- Hound of Tindalos (fast melee, sanity damage) ✅
- Deep One (melee, regeneration)
- Byakhee (flying, ranged)
- Shoggoth (slow, very high HP, area attack)

**Greater Horrors** (Mini-bosses):
- Star Spawn (tanky, multiple abilities)
- Mi-Go (high mobility, abduction mechanic)
- Dark Young (area sanity damage aura)

**Great Old Ones** (Final bosses):
- Cthulhu
- Nyarlathotep
- Yog-Sothoth
- Each with unique multi-phase mechanics

### Environmental Hazards
- **Darkness**: Reduces accuracy, increases sanity loss
- **Fog**: Limits line of sight
- **Ritual Circles**: Enemies spawn/buff here
- **Eldritch Rifts**: Sanity damage per turn if nearby
- **Destructible Objects**: Cover can be destroyed

---

## Phase 4: Polish & Advanced Features

### Mission Generation System
- **Procedural Maps**: Random cover placement, spawn points
- **Objectives**: Not just "kill all enemies"
  - Protect VIP
  - Reach extraction point
  - Survive X turns
  - Destroy ritual objects
  - Collect intel items

### Permadeath Consequences
- **Memorial Wall**: Remember fallen investigators
- **Legacy Bonuses**: Dead veterans give small bonuses to recruits
- **Trauma Events**: Squadmates who witness death get temporary debuffs

### Narrative Elements
- **Mission Briefings**: Text descriptions of scenarios
- **Post-Mission Reports**: Summarize results, note character changes
- **Random Events**: Between missions
  - Investigator has nightmare (-1 sanity)
  - Discovery in library (+intel)
  - Reporter asks questions (increase public panic?)

### Save/Load System
```python
class SaveGame:
    campaign_state: CampaignState
    roster: Roster
    base: Base
    research_progress: dict
    timestamp: datetime
```

### Audio (Phase 5)
- Ambient sounds during battles
- UI feedback sounds
- Music tracks for tension
- Enemy-specific sounds (cultist chants, monster roars)

### Visual Improvements (Phase 5)
- Replace unicode with sprite sheets
- Animation for movement, attacks
- Particle effects for abilities
- Screen shake on hits
- Health/sanity bar animations

---

## Implementation Phases Summary

### Phase 1: MVP (~98% Complete)
**Deliverable**: Playable tactical battle

**Completed**:
- ✅ Project foundation & UV setup
- ✅ Configuration system
- ✅ UI framework (Button, MenuButton, TextLabel, InvestigatorTile, ActionBar, TurnOrderTracker, Tooltip, ActionPointsDisplay)
- ✅ Title screen with navigation
- ✅ Grid system (10x10, cover, distance calculations)
- ✅ Entity system (Unit, Investigator, Cultist, Hound)
- ✅ Battle screen (rendering, selection, turn system)
- ✅ Investigator tiles panel (tactical overview)
- ✅ Movement system (A* pathfinding, flood-fill range)
- ✅ Action points system (2 actions per turn)
- ✅ Terrain generation (6 procedural generators)
- ✅ Tooltip system (terrain tooltips)
- ✅ Equipment system (weapons, damage, range, modifiers)
- ✅ Comprehensive documentation (8 docs)

**Remaining**:
- Line of sight calculation
- Combat resolution (hit chance, damage)
- Attack actions (ranged, melee)
- Enemy AI (basic movement and attacks)

### Phase 2: Meta-Layer Foundation
**Timeline**: Weeks 3-4
**Deliverable**: Campaign with multiple missions

- Campaign state management
- Mission select screen
- Investigator roster system
- Character generation with traits
- Post-mission healing/recovery
- Basic threat meter
- Simple resource system (funds)
- Save/load functionality

### Phase 3: Depth & Variety
**Timeline**: Weeks 5-6
**Deliverable**: Full strategy layer

- Class system and specializations
- Expanded ability system (5+ abilities per class)
- 5+ enemy types
- Equipment expansion (armor, accessories, more weapons)
- Base building (3-4 facilities)
- Research tree (10+ projects)
- Mission variety (3+ mission types)
- Advanced AI behaviors

### Phase 4: Advanced Combat
**Timeline**: Weeks 7-8
**Deliverable**: Tactical depth on par with X-COM

- Status effects system (bleeding, stunned, panicked)
- Environmental hazards
- Destructible terrain
- Overwatch system
- Enemy reinforcements
- Boss enemies with phases
- Procedural map generation

### Phase 5: Polish
**Timeline**: Weeks 9-10
**Deliverable**: Polished, complete game

- Replace unicode with sprites
- Animation system
- Particle effects
- Audio implementation
- Narrative events
- Tutorial/intro sequence
- Balance pass
- Bug fixes

---

## Key Design Principles

### 1. Modularity
Every system should be self-contained and extensible:
- Add new enemies by extending `Enemy` class
- Add new abilities by implementing `Ability` interface
- Add new facilities without refactoring core systems

### 2. Data-Driven Design
Configuration in separate files:
```python
# data/unit_data.py
INVESTIGATOR_STATS = {
    "soldier": {
        "health": (15, 20),
        "sanity": (8, 12),
        "accuracy": (70, 85),
        # ...
    }
}

ENEMY_STATS = {
    "cultist": {
        "health": 10,
        "accuracy": 60,
        "weapon_range": 3,
        # ...
    }
}
```

### 3. Testability
- Deterministic combat (seed RNG for testing)
- Unit tests for core mechanics (hit chance, pathfinding, LOS)
- Debug mode to spawn specific scenarios

### 4. Performance
- Efficient grid updates (only redraw changed tiles)
- Pathfinding caching
- AI decision caching within turn

### 5. Player Agency
- Always show hit chances before confirming
- Display enemy stats after first encounter
- Allow saving mid-campaign
- No hidden mechanics that feel unfair

---

## Future Considerations

### Multiplayer (Post-Launch)
- Turn-based PvP (player vs player tactical battles)
- Async multiplayer (upload squad, AI plays it vs others)
- Co-op campaign (shared base, different squads)

### Modding Support
- JSON-based unit/ability definitions
- Custom maps in simple text format
- Lua scripting for complex behaviors

### Mobile/Console Ports
- Touch controls for grid selection
- Simplified UI for smaller screens
- Controller support

---

## Open Design Questions

These are questions to resolve during implementation:

1. **Sanity mechanics depth**: Should low sanity cause hallucinations (fake enemies)? Friendly fire? Specific phobias?

2. **Injury system**: Should injuries be more granular (broken arm = -accuracy, leg wound = -movement)?

3. **Relationships**: Should investigators have bonds that affect morale/performance?

4. **Base location**: Does base location matter strategically (closer to certain regions)?

5. **Difficulty modes**: Should there be multiple difficulty levels with different threat escalation rates?

6. **Narrative branch points**: Should major decisions affect story direction (ally with cult faction, sacrifice investigator for power)?

---

**Last Updated**: 2025-11-29
**See Also**: [CLAUDE.md](CLAUDE.md) for current project state, [CONTRIBUTING.md](CONTRIBUTING.md) for developer guidelines
