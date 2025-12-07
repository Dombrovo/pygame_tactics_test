"""
Investigator class - player-controlled units.

Investigators are the player's units in tactical battles.
They have additional attributes for progression and traits (Phase 2+).
"""

from entities.unit import Unit
from entities import equipment  # Import equipment module for weapons
from typing import List, Literal, Dict, Any, Optional
import random
import json
from pathlib import Path


# Cache for name data (loaded once)
_NAME_DATA: Dict[str, List[str]] = {}

# Track used character images (prevents reuse)
# These are lists of image filenames that have already been assigned
_USED_IMAGES: Dict[Literal["male", "female"], List[str]] = {
    "male": [],
    "female": []
}


def _load_name_data() -> Dict[str, List[str]]:
    """
    Load name data from JSON file (cached).

    Returns:
        Dictionary with keys: first_male, first_female, last, nick
    """
    global _NAME_DATA

    if not _NAME_DATA:
        # Find the assets/json/names_data.json file
        json_path = Path(__file__).parent.parent / "assets" / "json" / "names_data.json"

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


def _get_available_images(gender: Literal["male", "female"]) -> List[str]:
    """
    Get list of all available character images for a gender.

    Args:
        gender: "male" or "female"

    Returns:
        List of image filenames (without path)
    """
    # Get the path to the images folder for this gender
    images_dir = Path(__file__).parent.parent / "assets" / "images" / "investigators" / gender

    # Get all PNG files in the directory
    if images_dir.exists():
        # Get filenames only (not full paths)
        # Filter out .import files and other non-PNG files
        images = [
            img.name for img in images_dir.glob("*.png")
            if not img.name.endswith(".import")
        ]
        return sorted(images)  # Sort for consistency
    else:
        print(f"Warning: Images directory not found: {images_dir}")
        return []


def get_random_unused_image(gender: Literal["male", "female"]) -> Optional[str]:
    """
    Get a random unused character image for the specified gender.

    This function ensures each image is only used once. Once an image is
    assigned, it's added to the _USED_IMAGES tracker and won't be selected again.

    Args:
        gender: "male" or "female"

    Returns:
        Relative path to the image (e.g., "assets/images/investigators/male/detective.png")
        or None if no unused images are available
    """
    # Get all available images for this gender
    all_images = _get_available_images(gender)

    # Filter out already used images
    unused_images = [img for img in all_images if img not in _USED_IMAGES[gender]]

    # Check if we have any unused images left
    if not unused_images:
        print(f"Warning: No unused {gender} images available! Pool exhausted.")
        return None

    # Select a random unused image
    selected_image = random.choice(unused_images)

    # Mark this image as used
    _USED_IMAGES[gender].append(selected_image)

    # Return the full relative path
    image_path = f"assets/images/investigators/{gender}/{selected_image}"

    return image_path


def reset_image_pool():
    """
    Reset the used images tracker, making all images available again.

    Call this at the start of a new campaign to allow image reuse.
    This is necessary because we have a limited number of images (25 female, 31 male)
    but campaigns may recruit more investigators over time.
    """
    global _USED_IMAGES
    _USED_IMAGES["male"] = []
    _USED_IMAGES["female"] = []
    print("Image pool reset - all character images available again")


def get_image_pool_status() -> Dict[str, Dict[str, int]]:
    """
    Get status of the image pool for debugging/UI display.

    Returns:
        Dictionary with usage statistics for each gender:
        {
            "male": {"total": 31, "used": 4, "available": 27},
            "female": {"total": 25, "used": 2, "available": 23}
        }
    """
    status = {}

    for gender in ["male", "female"]:
        all_images = _get_available_images(gender)
        used_count = len(_USED_IMAGES[gender])
        total_count = len(all_images)
        available_count = total_count - used_count

        status[gender] = {
            "total": total_count,
            "used": used_count,
            "available": available_count
        }

    return status


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
        gender: Literal["male", "female"] = "male",
        image_path: Optional[str] = None
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
            image_path: Path to character portrait image (optional)
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
        self.image_path = image_path  # Path to character portrait

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
    - Unique character portrait (never reused)
    - Fixed stats based on their template role

    Phase 2+ will replace this with:
    - Procedural generation from background classes
    - Randomized stats within ranges
    - Starting traits/flaws
    - Equipment loadouts

    Returns:
        List of 4 investigators with randomized names, unique portraits, and varied stats
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

    # Define weapons for each role
    # Each template gets a weapon that matches their playstyle
    role_weapons = [
        equipment.REVOLVER,      # Balanced: Standard sidearm
        equipment.RIFLE,         # Sniper: Long-range precision (+10% accuracy)
        equipment.SHOTGUN,       # Tank: High damage close-range
        equipment.REVOLVER,      # Scout: Reliable standard weapon
    ]

    investigators = []
    for i, template in enumerate(stat_templates):
        # Generate random name and gender from name database
        name, gender = generate_random_name()

        # Assign a unique character portrait
        image_path = get_random_unused_image(gender)

        # Create investigator with random name, portrait, and template stats
        # **template unpacks the dict as keyword arguments
        # Equivalent to: Investigator(name=name, gender=gender, max_health=15, ...)
        inv = Investigator(
            name=name,
            gender=gender,
            image_path=image_path,
            **template
        )

        # Equip weapon based on role
        inv.equip_weapon(role_weapons[i])

        investigators.append(inv)

    return investigators
