# Eldritch Tactics - Lovecraftian Turn-Based Tactical Game

## Game Overview
A turn-based tactical game inspired by X-COM, featuring squads of flawed investigators fighting against Lovecraftian horrors. The game combines grid-based tactical combat with strategic meta-layer management, including permadeath, sanity mechanics, and escalating cosmic threats.

**Core Theme**: Psychological horror meets tactical strategy - fragile humans against incomprehensible eldritch entities.

---

## Technology Stack
- **Engine**: Pygame CE (Community Edition)
- **Language**: Python 3.10+
- **Package Manager**: UV (fast Python package installer and resolver)
- **Installation**: `uv add pygame-ce` (recommended)

---

## Current Development State

**Last Updated**: 2025-11-28 (Session 3)
**Current Phase**: Phase 1 - MVP (Visual Systems Complete, Combat Mechanics Next)

### ✅ Completed Components

#### 1. Project Foundation
- ✅ UV package manager configured with pyproject.toml
- ✅ Virtual environment (.venv) created
- ✅ Pygame-CE installed and tested (2.5.6)
- ✅ Git repository initialized

#### 2. Configuration System
- ✅ Centralized config.py with all constants
- ✅ Screen settings (1920x1080 fullscreen)
- ✅ Color palette for Lovecraftian theme
- ✅ UI dimensions and game balance constants
- ✅ Grid and tile constants (10x10, 80px tiles)

#### 3. UI Framework
- ✅ Button class (interactive, hover/click detection)
- ✅ MenuButton class (extends Button with enabled/disabled state)
- ✅ TextLabel class (non-interactive text display)
- ✅ Callback pattern implementation

#### 4. Title Screen
- ✅ Fullscreen title screen (1920x1080)
- ✅ Menu navigation (New Game, Continue, Settings, Exit)
- ✅ Keyboard shortcuts (ESC, Enter, Space)
- ✅ Visual feedback (hover effects, button states)
- ✅ Game loop implementation (60 FPS)

#### 5. Main Entry Point
- ✅ Pygame initialization sequence
- ✅ Display/window management
- ✅ Clock for FPS control
- ✅ Screen navigation orchestration
- ✅ Battle screen integration
- ✅ Clean shutdown procedures

#### 6. Grid System
- ✅ Tile class (position, terrain, cover, occupancy)
- ✅ Grid class (10x10 battlefield)
- ✅ Cover system (empty, half cover, full cover)
- ✅ Unit placement and movement tracking
- ✅ Distance calculations (Euclidean, Manhattan)
- ✅ Neighbor finding (orthogonal + diagonal)
- ✅ Test cover generation

#### 7. Entity System
- ✅ Base Unit class (health, sanity, stats, team)
- ✅ **Stat System with Modifiers** (NEW!)
  - Base stats + modifier pattern
  - Properties auto-calculate effective stats
  - Easy modifier application for backgrounds/traits
  - Auto-clamping (accuracy 5-95%, stats min values)
- ✅ Investigator class (player units)
  - **Random name generation with gender** (NEW!)
  - 50/50 male/female assignment
  - 30% chance for nicknames (e.g., "John 'Bones' Smith")
  - Dual resource system (health + sanity)
  - Experience/progression hooks (Phase 2+)
- ✅ Enemy base class
- ✅ Cultist class (🔫 ranged attacker)
- ✅ Hound of Tindalos class (🐺 fast melee horror)
- ✅ Test squad/enemy generators (now with random names)

#### 8. Battle Screen
- ✅ Grid rendering (10x10 with cover symbols)
- ✅ Unit rendering (emoji symbols + health/sanity bars)
- ✅ Unit selection (mouse click, Tab cycling)
- ✅ Turn-based system (player phase ↔ enemy phase)
- ✅ Selected unit highlighting (yellow border)
- ✅ Unit info panel (right side display)
- ✅ Turn counter and phase display
- ✅ Controls help overlay
- ✅ Screen navigation (ESC to menu)
- ✅ Pixel ↔ grid coordinate conversion

#### 9. Name Generation System
- ✅ JSON name database (assets/json/names_data.json)
  - 84 male first names, 84 female first names
  - 90 last names, 113 nicknames
  - 1920s Lovecraftian theme
- ✅ Random generation function
  - 50/50 gender distribution
  - 30% nickname probability
  - Cached loading for performance
- ✅ Test suite (testing/test_names.py)

#### 10. Character Portrait System (NEW!)
- ✅ **Unique image assignment** - Each investigator gets a unique portrait
  - 25 female character images in `assets/images/investigators/female/`
  - 30 male character images in `assets/images/investigators/male/`
- ✅ **No image reuse** - Once assigned, images are never used again
- ✅ **Pool tracking system**
  - Global `_USED_IMAGES` tracker prevents duplicates
  - `get_random_unused_image()` - Assigns random unused portrait
  - `reset_image_pool()` - Resets for new campaigns
  - `get_image_pool_status()` - Check available images
- ✅ **Automatic assignment** - Images assigned in `create_test_squad()`
- ✅ **Investigator.image_path** attribute stores portrait path
- ✅ Test suite (testing/test_image_assignment.py)

#### 11. Visual Rendering System
- ✅ Emoji font support with automatic detection
  - Windows: Segoe UI Emoji
  - macOS: Apple Color Emoji
  - Linux: Noto Color Emoji/Symbola
- ✅ ASCII fallback system for systems without emoji fonts
  - Text symbols: [I], [C], [H] for units
  - ASCII cover: ##, ::, .. for terrain
- ✅ Team-based color coding
  - Blue for player investigators
  - Red for enemy units
- ✅ Ensures visual clarity across all platforms

#### 12. Documentation
- ✅ Comprehensive inline code comments (all files)
- ✅ docs/01_pygame_fundamentals.md - Pygame-CE basics
- ✅ docs/02_architecture_overview.md - System structure
- ✅ docs/03_ui_components.md - UI deep dive
- ✅ docs/04_data_flow.md - Interaction patterns
- ✅ docs/05_grid_and_battle_system.md - Grid and battle system
- ✅ docs/06_stat_system.md - Stat system with modifiers (NEW!)
- ✅ docs/doc_index.md - Documentation index

### 🚧 In Progress

**Next Task**: Combat Mechanics (Movement, Attacks, Line of Sight)

### 📋 Current File Structure

```
pygame_tactics_test/
├── main.py                    # ✅ Entry point (battle integration complete)
├── config.py                  # ✅ Configuration (complete)
├── pyproject.toml            # ✅ Project metadata (complete)
├── README.md                 # ✅ Project intro (complete)
├── CLAUDE.md                 # 📝 This file
│
├── ui/                       # ✅ UI Framework (complete)
│   ├── __init__.py
│   ├── ui_elements.py        # Button, MenuButton, TextLabel
│   └── title_screen.py       # Title screen implementation
│
├── combat/                   # ✅ Combat System (grid & battle screen complete)
│   ├── __init__.py
│   ├── grid.py               # Grid, Tile classes, cover system
│   └── battle_screen.py      # Battle UI, rendering, turn system
│
├── entities/                 # ✅ Entity System (complete with stat modifiers)
│   ├── __init__.py
│   ├── unit.py               # Base Unit class (with stat system)
│   ├── investigator.py       # Player units (random names + gender)
│   └── enemy.py              # Enemy units (Cultist, Hound)
│
├── assets/                   # ✅ Game assets
│   ├── images/               # Image assets
│   └── json/                 # Data files
│       └── names_data.json   # Name database (male/female/last/nick)
│
├── testing/                  # ✅ Test scripts
│   ├── test_names.py         # Name generation tests
│   └── test_stat_system.py   # Stat modifier tests
│
├── docs/                     # ✅ Documentation (complete)
│   ├── doc_index.md
│   ├── 01_pygame_fundamentals.md
│   ├── 02_architecture_overview.md
│   ├── 03_ui_components.md
│   ├── 04_data_flow.md
│   ├── 05_grid_and_battle_system.md
│   └── 06_stat_system.md     # NEW: Stat modifiers documentation
│
├── .venv/                    # Virtual environment
├── .git/                     # Git repository
└── uv.lock                   # UV lockfile
```

### 🎯 Next Session Goals

**Primary Objective**: Implement combat mechanics (movement, attacks, line of sight)

**Files to Create/Enhance**:
1. `combat/pathfinding.py` - A* pathfinding for movement
2. `combat/line_of_sight.py` - LOS calculations (Bresenham's line)
3. `combat/combat_resolver.py` - Hit chance, damage resolution
4. Update `combat/battle_screen.py` - Add movement and attack actions

**Estimated Session Time**: 2-3 hours

---

## MVP (Phase 1) - Playable Combat Prototype

### MVP Scope
**Goal**: Get a single tactical battle playable with core mechanics working.

#### Tactical Combat Features
- 10x10 grid battlefield
- Turn-based combat (player phase → enemy phase)
- 3-4 investigators vs 3-4 enemies per battle
- Two enemy types:
  - **Cultists**: Ranged attackers (3 tile range)
  - **Hounds of Tindalos**: Melee monsters (sanity damage on hit)
- Basic cover system (half/full cover)
- Line of sight calculations
- Hit chance based on distance and cover

#### Character Systems
- **Dual resource bars**: Health and Sanity (0 in either = incapacitated)
- **Actions per turn**: Move + Attack OR Move twice
- **Three attack types**:
  - Move (up to movement range)
  - Ranged Attack (3 tile range, requires line of sight)
  - Melee Attack (adjacent tile only)

#### Visual Representation
- **Emoji symbols** (with font support):
  - 👤 Investigator (BLUE - player team)
  - 🔫 Cultist (RED - enemy team)
  - 🐺 Hound of Tindalos (RED - enemy team)
  - ⬛ Full cover
  - ▪️ Half cover
  - ⬜ Empty tile
- **ASCII fallback** (without emoji fonts):
  - [I] Investigator (BLUE - player team)
  - [C] Cultist (RED - enemy team)
  - [H] Hound (RED - enemy team)
  - ## Full cover
  - :: Half cover
  - .. Empty tile
- **Team color coding**: Blue = Player, Red = Enemy
- Grid-based display with coordinates
- Health/sanity bars (red/blue)
- Selected unit highlighting (yellow border)

#### Win/Lose Conditions
- **Win**: Eliminate all enemies
- **Lose**: All investigators incapacitated
- **Post-battle**: Return to simple mission select screen

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

#### Unit (Base Class)
```python
class Unit:
    def __init__(self):
        self.name: str
        self.position: tuple[int, int]  # (x, y) grid coordinates
        self.max_health: int
        self.current_health: int
        self.max_sanity: int
        self.current_sanity: int
        self.movement_range: int
        self.accuracy: int  # Base hit chance %
        self.will: int      # Sanity defense
        self.is_incapacitated: bool
        self.team: str      # "player" or "enemy"
```

#### Investigator (extends Unit)
```python
class Investigator(Unit):
    def __init__(self):
        super().__init__()
        self.traits: list[Trait]  # Character flaws/bonuses
        self.experience: int
        self.kills: int
        self.missions_survived: int
        self.permanent_injuries: list[str]
        self.permanent_madness: list[str]
```

#### Enemy Types
```python
class Cultist(Unit):
    # Ranged attacker
    weapon_range: int = 3
    attack_type: str = "ranged"
    sanity_damage: int = 0

class HoundOfTindalos(Unit):
    # Melee horror
    weapon_range: int = 1
    attack_type: str = "melee"
    sanity_damage: int = 5  # Causes sanity damage on hit
    movement_range: int = 6  # Fast moving
```

#### Grid/Tile
```python
class Tile:
    def __init__(self):
        self.x: int
        self.y: int
        self.terrain_type: str  # "empty", "half_cover", "full_cover"
        self.occupied_by: Unit | None
        self.blocks_movement: bool
        self.blocks_sight: bool
        self.defense_bonus: int  # Cover provides hit chance penalty for attackers
```

#### Battle State
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
```

---

## Core Systems Design

### 1. Grid & Movement System

#### Grid Representation
- 10x10 tile grid
- Each tile has coordinates (x, y) from (0,0) to (9,9)
- Tiles can contain terrain (cover) and units

#### Movement Rules
- Units can move up to their `movement_range` in tiles per turn
- Movement costs 1 tile per orthogonal move, 1.4 for diagonal (Euclidean distance)
- Cannot move through enemy units
- Cannot move through full cover/obstacles
- Pathfinding uses A* algorithm

#### Cover System
- **Half Cover** (▪️): -20% hit chance for attackers
- **Full Cover** (⬛): -40% hit chance for attackers
- Cover only applies if it's between attacker and target
- Cover doesn't block movement (units can move into/through it)

### 2. Combat System

#### Turn Structure
1. **Player Phase**
   - Player selects unit
   - Unit can perform actions (move + attack, or move twice)
   - Can be done in any order until all units acted
   - End turn button confirms

2. **Enemy Phase**
   - AI controls each enemy unit
   - Simple AI: Move toward nearest investigator, attack if in range
   - Hounds prioritize closing distance for melee
   - Cultists maintain distance and shoot

#### Attack Resolution
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

### 3. Line of Sight System

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

### 5. UI System

#### Screen Layout (1920x1080 resolution)
```
┌──────────────────────────────────────────────────────────────┐
│  TURN 3 | PLAYER PHASE                        [END TURN]     │
├───────────────────────────┬──────────────────────────────────┤
│                           │  SELECTED UNIT                   │
│                           │  👤 John Carter                  │
│                           │  ❤️  HP: 12/15                   │
│      GRID (10x10)         │  🧠 SAN: 8/10                    │
│      800x800px            │  🎯 Acc: 75%                     │
│                           │  🏃 Move: 4                      │
│                           │                                  │
│                           │  ACTIONS:                        │
│                           │  [Move] [Shoot] [Overwatch]      │
│                           │                                  │
│                           │  TARGET INFO:                    │
│                           │  🔫 Cultist                      │
│                           │  Range: 3 tiles                  │
│                           │  Hit Chance: 65%                 │
│                           │  (Cover: -20%)                   │
└───────────────────────────┴──────────────────────────────────┘
```

#### Rendering Layers
1. **Grid Layer**: Tiles, terrain
2. **Unit Layer**: Unit symbols, health bars
3. **UI Overlay**: Selection highlights, range indicators
4. **Info Panel**: Selected unit stats, available actions
5. **Feedback Layer**: Hit/miss notifications, damage numbers

#### Input Handling
- **Mouse Click**: Select tile/unit
- **Mouse Hover**: Show tile info, valid move/attack ranges
- **Keyboard**:
  - Arrow keys: Scroll camera (future)
  - Tab: Cycle through player units
  - Space: End turn
  - ESC: Deselect/cancel

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

```python
class Equipment:
    def __init__(self):
        self.name: str
        self.slot: str  # "weapon", "armor", "accessory"
        self.modifiers: dict  # Stat bonuses

class Investigator:
    # ... existing attributes ...
    equipped_weapon: Equipment | None
    equipped_armor: Equipment | None
    equipped_accessories: list[Equipment]  # Max 2
```

**Equipment Examples**:
- **Weapons**: Revolver, Shotgun, Rifle, Tommy Gun, Blessed Blade
- **Armor**: Vest (+2 HP), Warded Coat (+1 will)
- **Accessories**: First Aid Kit, Elder Sign (1-time sanity protection), Night Vision Goggles

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
- Hound of Tindalos (fast melee, sanity damage)
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

### Phase 1: MVP (Current - 70% Complete)
**Deliverable**: Playable tactical battle

**Completed**:
- ✅ Project foundation & UV setup
- ✅ Configuration system
- ✅ UI framework (Button, MenuButton, TextLabel)
- ✅ Title screen with navigation
- ✅ Grid system (10x10, cover, distance calculations)
- ✅ Entity system (Unit, Investigator, Cultist, Hound)
- ✅ Battle screen (rendering, selection, turn system)
- ✅ Comprehensive documentation

**Remaining**:
- Movement system with pathfinding
- Line of sight calculation
- Combat resolution (hit chance, damage)
- Attack actions (ranged, melee)
- Enemy AI (basic movement and attacks)

### Phase 2: Meta-Layer Foundation (Weeks 3-4)
- Campaign state management
- Mission select screen
- Investigator roster system
- Character generation with traits
- Post-mission healing/recovery
- Basic threat meter
- Simple resource system (funds)
- Save/load functionality

**Deliverable**: Campaign with multiple missions

### Phase 3: Depth & Variety (Weeks 5-6)
- Class system and specializations
- Expanded ability system (5+ abilities per class)
- 5+ enemy types
- Equipment/loadout system
- Base building (3-4 facilities)
- Research tree (10+ projects)
- Mission variety (3+ mission types)
- Advanced AI behaviors

**Deliverable**: Full strategy layer

### Phase 4: Advanced Combat (Weeks 7-8)
- Status effects system (bleeding, stunned, panicked)
- Environmental hazards
- Destructible terrain
- Overwatch system
- Enemy reinforcements
- Boss enemies with phases
- Procedural map generation

**Deliverable**: Tactical depth on par with X-COM

### Phase 5: Polish (Weeks 9-10)
- Replace unicode with sprites
- Animation system
- Particle effects
- Audio implementation
- Narrative events
- Tutorial/intro sequence
- Balance pass
- Bug fixes

**Deliverable**: Polished, complete game

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

## UV Best Practices (2025)

### What is UV?

UV is a revolutionary Python package manager written in Rust by Astral (creators of Ruff). It's an all-in-one tool that replaces pip, pip-tools, pipx, poetry, pyenv, twine, virtualenv, and more. UV is **10-100x faster than pip** and provides superior dependency management.

### Core Principles

#### 1. Use `uv add` Instead of `uv pip install`
**ALWAYS** use `uv add` for adding dependencies. This automatically updates `pyproject.toml` and maintains the lockfile.

```bash
# ✅ CORRECT - Modern UV workflow
uv add pygame-ce
uv add --dev pytest

# ❌ AVOID - Legacy pip-style workflow
uv pip install pygame-ce
```

#### 2. Use `uv run` for Execution
**NO ACTIVATION REQUIRED** - `uv run` automatically manages the environment.

```bash
# ✅ CORRECT - Auto-manages environment
uv run python main.py
uv run pytest

# ❌ AVOID - Manual activation
source .venv/bin/activate
python main.py
```

#### 3. Let UV Manage Python Versions
UV automatically installs missing Python versions. You don't need to install Python separately.

```bash
# UV will auto-install Python 3.10 if needed
uv python install 3.10
uv venv --python 3.10
```

#### 4. Leverage the Lockfile
UV automatically generates `uv.lock` which ensures **deterministic builds** across all systems.

```bash
# Install exact versions from lockfile
uv sync

# Update dependencies and lockfile
uv lock --upgrade
```

#### 5. Use Local .venv Folders
Store virtual environments in `.venv` local to your project (industry standard).

```bash
# ✅ Creates .venv in project root
uv venv

# The .venv folder should be in .gitignore
```

### Project Workflow with UV

#### Initial Project Setup
```bash
# Create new project with UV
uv init eldritch-tactics
cd eldritch-tactics

# Or initialize in existing directory
uv init

# Create virtual environment
uv venv

# Add dependencies (auto-updates pyproject.toml)
uv add pygame-ce
uv add --dev pytest pytest-cov
```

#### Daily Development
```bash
# Run the game
uv run python main.py

# Run tests
uv run pytest

# Add new dependency
uv add requests

# Update all dependencies
uv lock --upgrade
uv sync
```

#### CI/CD Pipeline
```bash
# Install exact versions from lockfile
uv sync --frozen

# Run tests in CI
uv run pytest --cov
```

### Performance Advantages

- **Speed**: 10-100x faster than pip for installations
- **Caching**: Central cache with Copy-on-Write and hardlinks minimizes disk space
- **Parallel**: Concurrent downloads and installations
- **No Re-downloads**: Cached packages reused across projects

### Common Commands Reference

| Task | Command | Description |
|------|---------|-------------|
| Create venv | `uv venv` | Creates .venv in project root |
| Add package | `uv add <pkg>` | Installs and adds to pyproject.toml |
| Add dev package | `uv add --dev <pkg>` | Adds to dev dependencies |
| Remove package | `uv remove <pkg>` | Uninstalls and removes from pyproject.toml |
| Install all deps | `uv sync` | Installs from lockfile |
| Update deps | `uv lock --upgrade` | Updates lockfile with latest versions |
| Run command | `uv run <cmd>` | Runs in managed environment |
| List packages | `uv pip list` | Shows installed packages |
| Install Python | `uv python install 3.10` | Installs Python version |

### Migration from pip/poetry/pipenv

If migrating from other tools:

```bash
# From requirements.txt
uv pip install -r requirements.txt
uv add $(cat requirements.txt)  # Migrate to pyproject.toml

# From poetry
# Copy dependencies from pyproject.toml [tool.poetry.dependencies]
# to [project.dependencies]
uv sync

# From pipenv (Pipfile)
# Manually add dependencies to pyproject.toml
uv add <each-package>
```

### Resources
- **Official Docs**: https://docs.astral.sh/uv/
- **GitHub**: https://github.com/astral-sh/uv
- **Guides**: https://realpython.com/python-uv/

---

## Configuration Reference

### Game Constants (config.py)
Current values as of 2025-11-27:

```python
# Display
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FULLSCREEN = True
GRID_SIZE = 10
TILE_SIZE = 80
FPS = 60

# Colors
COLOR_BG = (15, 15, 25)
COLOR_UI_BG = (25, 25, 35)
COLOR_TEXT = (220, 220, 230)
COLOR_TEXT_HIGHLIGHT = (255, 200, 100)
COLOR_GRID = (50, 50, 60)
COLOR_PLAYER = (100, 150, 255)
COLOR_ENEMY = (255, 100, 100)
COLOR_SELECTED = (255, 255, 100)
COLOR_VALID_MOVE = (100, 255, 100)
COLOR_ATTACK_RANGE = (255, 100, 100)

# Combat
BASE_HIT_CHANCE = 75
DISTANCE_PENALTY_PER_TILE = 10
HALF_COVER_BONUS = 20
FULL_COVER_BONUS = 40
MIN_HIT_CHANCE = 5
MAX_HIT_CHANCE = 95

# Balance
PLAYER_STARTING_SQUAD_SIZE = 4
PLAYER_MAX_ROSTER = 12
STARTING_FUNDS = 1000
MISSION_REWARD_BASE = 200
```

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

## Session 3: Visual Rendering System ✅ COMPLETE

**Completed**: 2025-11-28

### What Was Built

Successfully implemented emoji font support and team color coding:

1. ✅ **Emoji Font System** (`combat/battle_screen.py`)
   - Automatic detection and loading of emoji-capable fonts
   - Platform support: Windows (Segoe UI Emoji), macOS (Apple Color Emoji), Linux (Noto Color Emoji)
   - Graceful fallback to ASCII symbols when emoji fonts unavailable
   - Applies to both unit symbols AND cover symbols

2. ✅ **Team Color Coding**
   - Blue color for player investigators (easy identification)
   - Red color for enemy units (instant threat recognition)
   - Color-coded symbols improve battlefield clarity at a glance

3. ✅ **ASCII Fallback Mode**
   - Units: `[I]` Investigator, `[C]` Cultist, `[H]` Hound
   - Cover: `##` Full cover, `::` Half cover, `..` Empty
   - Ensures game is playable on all systems, even without emoji support

### Test Results
```
✅ Emoji font loads successfully on Windows (Segoe UI Emoji)
✅ Unit symbols render properly (👤 🔫 🐺)
✅ Cover symbols render properly (⬛ ▪️)
✅ Color coding works (blue vs red teams)
✅ Visual distinction between all unit types
✅ Game is visually clear and readable
```

### Impact
- **Problem Solved**: Units were rendering as boxes/question marks with default font
- **User Experience**: Battlefield is now instantly readable with color-coded teams
- **Cross-Platform**: Works on all operating systems with automatic fallback

---

## Session 2: Tactical Battle Development ✅ COMPLETE

**Completed**: 2025-11-27

### What Was Built

Successfully implemented the tactical battle system foundation:

1. ✅ **Grid System** (`combat/grid.py`)
   - 10x10 battlefield with Tile and Grid classes
   - Cover system (empty, half cover, full cover)
   - Unit placement and tracking
   - Distance calculations (Euclidean, Manhattan)
   - Test cover generation

2. ✅ **Entity System** (`entities/`)
   - Base Unit class with health/sanity dual resource
   - Investigator class (4 test investigators)
   - Enemy base class and two enemy types (Cultist, Hound)
   - Test squad/enemy generators

3. ✅ **Battle Screen** (`combat/battle_screen.py`)
   - Full grid rendering with cover symbols
   - Unit rendering with health/sanity bars
   - Unit selection (mouse click, Tab cycling)
   - Turn-based system (player/enemy phases)
   - Unit info panel (right side display)
   - Controls help overlay
   - Navigation (ESC to menu)

### Test Results
```
✅ Game launches and displays title screen
✅ "New Game" navigates to battle screen
✅ 10x10 grid renders with cover
✅ 4 investigators + 4 enemies placed
✅ Unit selection works (click + Tab)
✅ Turn system works (Space to end turn)
✅ Clean navigation (ESC returns to menu)
```

---

## Questions for Future Design Sessions

1. **Sanity mechanics depth**: Should low sanity cause hallucinations (fake enemies)? Friendly fire? Specific phobias?

2. **Injury system**: Should injuries be more granular (broken arm = -accuracy, leg wound = -movement)?

3. **Relationships**: Should investigators have bonds that affect morale/performance?

4. **Base location**: Does base location matter strategically (closer to certain regions)?

5. **Difficulty modes**: Should there be multiple difficulty levels with different threat escalation rates?

6. **Narrative branch points**: Should major decisions affect story direction (ally with cult faction, sacrifice investigator for power)?

---

## End Notes

This document will evolve as the game is developed. Update it when:
- New systems are added
- Balance changes are made
- Design decisions change
- Bugs reveal architectural issues

**Current Version**: 1.3 (Visual Rendering System)
**Last Updated**: 2025-11-28
**Target Platform**: Windows/Mac/Linux Desktop
**Engine**: Pygame CE 2.5.x
**Python**: 3.10+

---

## Quick Start Checklist for Claude Code

When starting a new session, Claude Code should:
1. ✓ Read this entire document
2. ✓ Understand current phase (Phase 1 MVP - 70% complete)
3. ✓ Check which files exist
4. ✓ Ask which system to work on next
5. ✓ Implement one small feature at a time
6. ✓ Test before moving to next feature

**MVP Goal**: Get a single tactical battle playable where you can move investigators, attack enemies, and win/lose the battle.

Let's build something great! 🎲🐙
