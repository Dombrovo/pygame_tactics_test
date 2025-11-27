"""
Investigator class - player-controlled units.

Investigators are the player's units in tactical battles.
They have additional attributes for progression and traits (Phase 2+).
"""

from entities.unit import Unit
from typing import List, Literal, Dict, Any
import random
import json
from pathlib import Path


# Cache for name data (loaded once)
_NAME_DATA: Dict[str, List[str]] = {}


def _load_name_data() -> Dict[str, List[str]]:
    """
    Load name data from JSON file (cached).

    Returns:
        Dictionary with keys: first_male, first_female, last, nick
    """
    global _NAME_DATA

    if not _NAME_DATA:
        # Find the json/names_data.json file
        json_path = Path(__file__).parent.parent / "json" / "names_data.json"

        with open(json_path, 'r') as f:
            _NAME_DATA = json.load(f)

    return _NAME_DATA


def generate_random_name(include_nickname_chance: float = 0.3) -> tuple[str, Literal["male", "female"]]:
    """
    Generate a random investigator name with gender.

    Process:
    1. Randomly select gender (50% male, 50% female)
    2. Pick random first name based on gender
    3. Pick random last name
    4. 30% chance to add nickname

    Args:
        include_nickname_chance: Probability of including nickname (default 0.3)

    Returns:
        Tuple of (full_name, gender)
        Example: ("Arthur 'Bones' Blackwood", "male")
    """
    name_data = _load_name_data()

    # Step 1: Randomly select gender (50/50)
    gender: Literal["male", "female"] = random.choice(["male", "female"])

    # Step 2: Pick first name based on gender
    if gender == "male":
        first_name = random.choice(name_data["first_male"])
    else:
        first_name = random.choice(name_data["first_female"])

    # Step 3: Pick last name
    last_name = random.choice(name_data["last"])

    # Step 4: 30% chance for nickname
    nickname = None
    if random.random() < include_nickname_chance:
        nickname = random.choice(name_data["nick"])

    # Build full name
    if nickname:
        full_name = f"{first_name} '{nickname}' {last_name}"
    else:
        full_name = f"{first_name} {last_name}"

    return full_name, gender


class Investigator(Unit):
    """
    Player-controlled investigator unit.

    Extends Unit with:
    - Experience and progression tracking (Phase 2+)
    - Traits/flaws system (Phase 2+)
    - Mission statistics (Phase 2+)
    """

    def __init__(
        self,
        name: str,
        max_health: int = 15,
        max_sanity: int = 10,
        accuracy: int = 75,
        will: int = 5,
        movement_range: int = 4,
        gender: Literal["male", "female"] = "male"
    ):
        """
        Initialize an investigator.

        Default stats for MVP testing - can be randomized in Phase 2.

        Args:
            name: Investigator's name
            max_health: Maximum health (default 15)
            max_sanity: Maximum sanity (default 10)
            accuracy: Base hit chance % (default 75)
            will: Sanity defense (default 5)
            movement_range: Tiles per turn (default 4)
            gender: Character gender ("male" or "female")
        """
        # Initialize base Unit class
        super().__init__(
            name=name,
            max_health=max_health,
            max_sanity=max_sanity,
            accuracy=accuracy,
            will=will,
            movement_range=movement_range,
            team="player",
            symbol="👤"  # Unicode person symbol
        )

        # Identity
        self.gender = gender

        # Progression tracking (Phase 2+)
        self.experience = 0
        self.kills = 0
        self.missions_survived = 0

        # Traits and injuries (Phase 2+)
        self.traits: List[str] = []
        self.permanent_injuries: List[str] = []
        self.permanent_madness: List[str] = []

    def gain_experience(self, amount: int):
        """
        Add experience points (Phase 2+ feature).

        Args:
            amount: XP to add
        """
        self.experience += amount
        # TODO: Level up logic in Phase 2

    def record_kill(self):
        """Record an enemy kill (for stats and traits)."""
        self.kills += 1
        # TODO: Check for kill-based traits in Phase 2

    def complete_mission(self):
        """Record mission completion."""
        self.missions_survived += 1
        # TODO: Check for veteran traits in Phase 2

    def add_trait(self, trait: str):
        """
        Add a trait/flaw to the investigator.

        Args:
            trait: Trait name
        """
        if trait not in self.traits:
            self.traits.append(trait)

    def add_injury(self, injury: str):
        """
        Add a permanent injury (Phase 2+ feature).

        Args:
            injury: Injury description
        """
        if injury not in self.permanent_injuries:
            self.permanent_injuries.append(injury)
            # TODO: Apply stat penalties based on injury type

    def add_madness(self, madness: str):
        """
        Add permanent madness (Phase 2+ feature).

        Args:
            madness: Madness description
        """
        if madness not in self.permanent_madness:
            self.permanent_madness.append(madness)
            # TODO: Apply sanity penalties or behavioral changes

    def get_info_text(self) -> str:
        """
        Get formatted info string for UI display.

        Returns:
            Multi-line string with investigator stats
        """
        lines = [
            f"{self.symbol} {self.name}",
            f"❤️  HP: {self.current_health}/{self.max_health}",
            f"🧠 SAN: {self.current_sanity}/{self.max_sanity}",
            f"🎯 Acc: {self.accuracy}%",
            f"🏃 Move: {self.movement_range}",
        ]

        if self.is_incapacitated:
            lines.append("⚠️  INCAPACITATED")

        # Show traits if any (Phase 2+)
        if self.traits:
            lines.append(f"Traits: {', '.join(self.traits)}")

        return "\n".join(lines)

    def __repr__(self) -> str:
        """String representation for debugging."""
        status = " [INCAPACITATED]" if self.is_incapacitated else ""
        return f"Investigator '{self.name}': {self.current_health}/{self.max_health} HP, {self.current_sanity}/{self.max_sanity} SAN{status}"


def create_test_squad() -> List[Investigator]:
    """
    Create a test squad of 4 investigators for MVP testing.

    Squad composition uses 4 different stat templates to provide
    tactical variety and encourage different playstyles:

    1. **Balanced** - Jack of all trades, reliable in most situations
    2. **Sniper** - High accuracy glass cannon, best at range
    3. **Tank** - High HP frontline fighter, can take hits
    4. **Scout** - Fast and mentally resilient, good for flanking

    Each investigator gets:
    - Random name (with 30% chance for nickname)
    - Random gender (50/50 male/female)
    - Fixed stats based on their template role

    Phase 2+ will replace this with:
    - Procedural generation from background classes
    - Randomized stats within ranges
    - Starting traits/flaws
    - Equipment loadouts

    Returns:
        List of 4 investigators with randomized names and varied stats
    """
    # Define stat templates for variety
    # Each template represents a different tactical role
    stat_templates = [
        {  # Template 1: Balanced all-rounder
            "max_health": 15,      # Average durability
            "max_sanity": 10,      # Average mental fortitude
            "accuracy": 75,        # Standard hit chance
            "will": 5,             # Standard sanity defense
            "movement_range": 4    # Standard mobility
        },
        {  # Template 2: Sniper - precision shooter
            "max_health": 12,      # Low HP (glass cannon)
            "max_sanity": 12,      # Better mental resilience
            "accuracy": 80,        # High accuracy (best shooter)
            "will": 6,             # Good will
            "movement_range": 4    # Standard mobility
        },
        {  # Template 3: Tank - frontline bruiser
            "max_health": 18,      # High HP (can absorb damage)
            "max_sanity": 8,       # Low sanity (tough but unstable)
            "accuracy": 70,        # Lower accuracy
            "will": 4,             # Low will (vulnerable to horror)
            "movement_range": 3    # Slow (heavy armor implied)
        },
        {  # Template 4: Scout - mobile flanker
            "max_health": 14,      # Slightly below average HP
            "max_sanity": 11,      # Good sanity (stays calm)
            "accuracy": 75,        # Standard accuracy
            "will": 7,             # High will (brave)
            "movement_range": 5    # Fast (best mobility)
        },
    ]

    investigators = []
    for template in stat_templates:
        # Generate random name and gender from name database
        name, gender = generate_random_name()

        # Create investigator with random name and template stats
        # **template unpacks the dict as keyword arguments
        # Equivalent to: Investigator(name=name, gender=gender, max_health=15, ...)
        inv = Investigator(
            name=name,
            gender=gender,
            **template
        )
        investigators.append(inv)

    return investigators
