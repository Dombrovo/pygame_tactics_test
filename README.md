# Eldritch Tactics

A turn-based tactical game inspired by X-COM, featuring squads of flawed investigators fighting against Lovecraftian horrors. The game combines grid-based tactical combat with strategic meta-layer management, including permadeath, sanity mechanics, and escalating cosmic threats.

**Core Theme**: Psychological horror meets tactical strategy - fragile humans against incomprehensible eldritch entities.

## Technology Stack

- **Engine**: Pygame CE (Community Edition)
- **Language**: Python 3.10+
- **Package Manager**: UV (fast Python package installer and resolver)

## Installation

### Using UV (Recommended)

```bash
# Create virtual environment
uv venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
uv pip install -e .

# Install development dependencies
uv pip install -e ".[dev]"
```

### Using pip

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

## Running the Game

```bash
# Run the game
python main.py

# Debug mode (shows grid coordinates, hit chances, etc.)
python main.py --debug
```

## Development Status

**Current Phase**: Phase 1 - MVP (Playable Combat Prototype)

### MVP Features (In Development)
- 10x10 grid battlefield
- Turn-based combat (player phase -> enemy phase)
- 3-4 investigators vs 3-4 enemies per battle
- Two enemy types: Cultists (ranged) and Hounds of Tindalos (melee)
- Basic cover system (half/full cover)
- Line of sight calculations
- Hit chance based on distance and cover
- Dual resource bars: Health and Sanity
- Simple unicode/emoji-based graphics

## Project Structure

```
eldritch_tactics/
├── main.py                 # Entry point, game loop
├── config.py              # Constants and configuration
├── game_state.py          # Core game state manager
├── combat/                # Combat systems
├── entities/              # Unit classes
├── ui/                    # User interface
├── data/                  # Game data definitions
└── meta/                  # Meta-layer (Phase 2+)
```

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_combat.py

# Run with coverage
pytest --cov=. --cov-report=html
```

## Roadmap

### Phase 1: MVP (Current)
Playable tactical battle with core mechanics

### Phase 2: Meta-Layer Foundation
Campaign mode, mission select, investigator roster

### Phase 3: Depth & Variety
Classes, abilities, equipment, research tree

### Phase 4: Advanced Combat
Status effects, environmental hazards, procedural maps

### Phase 5: Polish
Sprites, animations, audio, narrative events

## Contributing

This is currently a personal project in early development. Contributions, suggestions, and bug reports are welcome!

## License

MIT License - See LICENSE file for details

## Documentation

For detailed design documentation, see [CLAUDE.md](CLAUDE.md)
