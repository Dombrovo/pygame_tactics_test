"""
Terrain Generation System for Eldritch Tactics

This module provides procedural terrain generation for tactical battles.
Different generators create varied, balanced battlefields with thematic layouts.

Generators:
- SymmetricGenerator: Mirror-symmetric maps for balanced combat
- ScatteredGenerator: Random scattered cover pieces
- UrbanRuinsGenerator: City ruins with walls and debris
- RitualSiteGenerator: Circular ritual pattern with center focal point
- OpenFieldGenerator: Minimal cover, favors ranged combat
- ChokepointGenerator: Narrow passages and defensive positions
"""

import random
from typing import List, Tuple, Set
import config


class TerrainGenerator:
    """
    Base class for terrain generators.

    All generators follow the same pattern:
    1. Initialize with grid size
    2. Call generate() to get list of cover placements
    3. Return list of (x, y, cover_type) tuples
    """

    def __init__(self, grid_size: int = config.GRID_SIZE):
        """
        Initialize terrain generator.

        Args:
            grid_size: Size of the grid (default 10x10)
        """
        self.grid_size = grid_size

    def generate(self) -> List[Tuple[int, int, str]]:
        """
        Generate terrain layout.

        Returns:
            List of (x, y, cover_type) tuples where:
            - x, y: Grid coordinates (0-9)
            - cover_type: "half_cover" or "full_cover"
        """
        raise NotImplementedError("Subclasses must implement generate()")

    def _is_valid_position(self, x: int, y: int) -> bool:
        """Check if position is within grid bounds."""
        return 0 <= x < self.grid_size and 0 <= y < self.grid_size

    def _keep_spawn_zones_clear(self, placements: List[Tuple[int, int, str]]) -> List[Tuple[int, int, str]]:
        """
        Remove cover from spawn zones to prevent blocking starting positions.

        Spawn zones:
        - Player spawns: Left side (x < 3)
        - Enemy spawns: Right side (x > 6)

        Args:
            placements: List of (x, y, cover_type) tuples

        Returns:
            Filtered list with spawn zones cleared
        """
        # Keep only tiles that are not in spawn zones
        return [(x, y, cover) for x, y, cover in placements
                if not (x < 3 or x > 6)]


class SymmetricGenerator(TerrainGenerator):
    """
    Generates mirror-symmetric maps for balanced combat.

    Strategy:
    - Generate cover on left half of map
    - Mirror it to right half
    - Ensures both sides have identical tactical opportunities
    """

    def generate(self) -> List[Tuple[int, int, str]]:
        """Generate symmetric terrain layout."""
        placements = []

        # Generate cover for left half only (x >= 3 and x < 5)
        # We'll mirror these to the right side
        # Avoid spawn zones: x < 3 (player) and x > 6 (enemy)

        # Central structures (mirrored)
        mid_y = self.grid_size // 2

        # Add central full cover block
        for dy in [-1, 0, 1]:
            y = mid_y + dy
            placements.append((4, y, "full_cover"))

        # Add flanking half cover positions
        for y in [2, 7]:
            placements.append((3, y, "half_cover"))
            placements.append((4, y, "half_cover"))

        # Add defensive positions (inside safe zone)
        placements.append((3, 3, "full_cover"))
        placements.append((3, 6, "full_cover"))

        # Mirror all placements to right side
        mirrored = []
        for x, y, cover_type in placements:
            # Mirror formula: new_x = (grid_size - 1) - old_x
            mirror_x = (self.grid_size - 1) - x
            mirrored.append((mirror_x, y, cover_type))

        # Combine both sides
        all_placements = placements + mirrored

        return all_placements


class ScatteredGenerator(TerrainGenerator):
    """
    Randomly scatters cover pieces across the battlefield.

    Strategy:
    - Random placement with density control
    - Mix of full and half cover
    - Keeps spawn zones clear
    """

    def __init__(self, grid_size: int = config.GRID_SIZE,
                 density: float = 0.15, full_cover_ratio: float = 0.4):
        """
        Initialize scattered generator.

        Args:
            grid_size: Size of the grid
            density: Percentage of tiles with cover (0.0-1.0)
            full_cover_ratio: Ratio of full cover to total cover (0.0-1.0)
        """
        super().__init__(grid_size)
        self.density = density
        self.full_cover_ratio = full_cover_ratio

    def generate(self) -> List[Tuple[int, int, str]]:
        """Generate scattered terrain layout."""
        placements = []

        # Calculate how many cover tiles to place
        total_tiles = self.grid_size * self.grid_size
        num_cover = int(total_tiles * self.density)

        # Generate random positions (avoid spawn zones)
        available_positions = []
        for x in range(3, 7):  # Center area only (x 3-6)
            for y in range(self.grid_size):
                available_positions.append((x, y))

        # Randomly select positions for cover
        random.shuffle(available_positions)
        selected_positions = available_positions[:num_cover]

        # Assign cover types (mix of full and half)
        num_full_cover = int(num_cover * self.full_cover_ratio)

        for i, (x, y) in enumerate(selected_positions):
            if i < num_full_cover:
                placements.append((x, y, "full_cover"))
            else:
                placements.append((x, y, "half_cover"))

        return placements


class UrbanRuinsGenerator(TerrainGenerator):
    """
    Generates city ruins with walls, debris, and building remnants.

    Strategy:
    - Vertical/horizontal wall segments (full cover)
    - Scattered debris piles (half cover)
    - Creates corridor-like pathways
    """

    def generate(self) -> List[Tuple[int, int, str]]:
        """Generate urban ruins layout."""
        placements = []

        # Vertical walls (building walls)
        # Left wall
        for y in range(2, 8):
            if random.random() < 0.7:  # 70% chance for each tile
                placements.append((3, y, "full_cover"))

        # Right wall
        for y in range(2, 8):
            if random.random() < 0.7:
                placements.append((6, y, "full_cover"))

        # Horizontal wall segments (fallen structures)
        for x in range(4, 6):
            if random.random() < 0.6:
                placements.append((x, 3, "full_cover"))
            if random.random() < 0.6:
                placements.append((x, 6, "full_cover"))

        # Debris piles (half cover scattered in open areas)
        debris_positions = [
            (4, 2), (5, 2),
            (4, 7), (5, 7),
            (4, 4), (5, 5)
        ]

        for x, y in debris_positions:
            if random.random() < 0.5:  # 50% chance for debris
                placements.append((x, y, "half_cover"))

        return placements


class RitualSiteGenerator(TerrainGenerator):
    """
    Generates a ritual site with circular pattern and central altar.

    Strategy:
    - Full cover altar in center
    - Half cover ritual markers in circular pattern
    - Creates dramatic centerpiece for eldritch battles
    """

    def generate(self) -> List[Tuple[int, int, str]]:
        """Generate ritual site layout."""
        placements = []

        center_x = self.grid_size // 2
        center_y = self.grid_size // 2

        # Central altar (2x2 full cover)
        for dx in [0, 1]:
            for dy in [0, 1]:
                x = center_x - 1 + dx
                y = center_y - 1 + dy
                placements.append((x, y, "full_cover"))

        # Ritual markers in circular pattern
        # Inner circle (distance 2-3 from center)
        # Avoid spawn zones: x < 3 (player) and x > 6 (enemy)
        ritual_positions = [
            # Top
            (center_x - 1, center_y - 3),
            (center_x, center_y - 3),
            (center_x + 1, center_y - 3),
            # Bottom
            (center_x - 1, center_y + 3),
            (center_x, center_y + 3),
            (center_x + 1, center_y + 3),
            # Left (moved to x=3 to avoid spawn zone)
            (3, center_y - 1),
            (3, center_y),
            (3, center_y + 1),
            # Right (moved to x=6 to avoid spawn zone)
            (6, center_y - 1),
            (6, center_y),
            (6, center_y + 1),
        ]

        for x, y in ritual_positions:
            if self._is_valid_position(x, y):
                placements.append((x, y, "half_cover"))

        return placements


class OpenFieldGenerator(TerrainGenerator):
    """
    Generates minimal cover for open battlefield.

    Strategy:
    - Very few cover pieces
    - Favors ranged combat and movement
    - High-risk, high-speed battles
    """

    def generate(self) -> List[Tuple[int, int, str]]:
        """Generate open field layout."""
        placements = []

        # Just a few scattered pieces for tactical variety
        sparse_cover = [
            (4, 3, "half_cover"),
            (5, 3, "half_cover"),
            (4, 6, "half_cover"),
            (5, 6, "half_cover"),
            (3, 4, "full_cover"),
            (6, 5, "full_cover"),
        ]

        # Only place 60% of these (very sparse)
        for x, y, cover_type in sparse_cover:
            if random.random() < 0.6:
                placements.append((x, y, cover_type))

        return placements


class ChokepointGenerator(TerrainGenerator):
    """
    Generates maps with narrow passages and defensive positions.

    Strategy:
    - Wall lines with gaps (chokepoints)
    - Forces tactical positioning
    - Defensive battles with limited flanking
    """

    def generate(self) -> List[Tuple[int, int, str]]:
        """Generate chokepoint layout."""
        placements = []

        # Vertical walls with gaps in center
        mid_y = self.grid_size // 2

        # Left wall line
        for y in range(self.grid_size):
            # Skip middle 2 tiles to create chokepoint
            if y < mid_y - 1 or y > mid_y + 1:
                placements.append((3, y, "full_cover"))

        # Right wall line
        for y in range(self.grid_size):
            if y < mid_y - 1 or y > mid_y + 1:
                placements.append((6, y, "full_cover"))

        # Add defensive positions near chokepoints
        chokepoint_cover = [
            (4, mid_y - 2, "half_cover"),
            (4, mid_y + 2, "half_cover"),
            (5, mid_y - 2, "half_cover"),
            (5, mid_y + 2, "half_cover"),
        ]

        for x, y, cover_type in chokepoint_cover:
            if self._is_valid_position(x, y):
                placements.append((x, y, cover_type))

        return placements


# ============================================================================
# Terrain Generator Selection
# ============================================================================

# Registry of all available generators
GENERATOR_CLASSES = {
    "symmetric": SymmetricGenerator,
    "scattered": ScatteredGenerator,
    "urban_ruins": UrbanRuinsGenerator,
    "ritual_site": RitualSiteGenerator,
    "open_field": OpenFieldGenerator,
    "chokepoint": ChokepointGenerator,
}


def generate_random_terrain(grid_size: int = config.GRID_SIZE) -> List[Tuple[int, int, str]]:
    """
    Generate terrain using a randomly selected generator.

    Args:
        grid_size: Size of the grid (default from config)

    Returns:
        List of (x, y, cover_type) tuples for terrain placement
    """
    # Randomly select a generator
    generator_name = random.choice(list(GENERATOR_CLASSES.keys()))
    generator_class = GENERATOR_CLASSES[generator_name]

    # Create generator instance and generate terrain
    generator = generator_class(grid_size)
    terrain = generator.generate()

    print(f"Generated terrain: {generator_name} ({len(terrain)} cover tiles)")

    return terrain


def generate_terrain(generator_type: str, grid_size: int = config.GRID_SIZE) -> List[Tuple[int, int, str]]:
    """
    Generate terrain using a specific generator.

    Args:
        generator_type: Name of generator to use (see GENERATOR_CLASSES)
        grid_size: Size of the grid (default from config)

    Returns:
        List of (x, y, cover_type) tuples for terrain placement

    Raises:
        ValueError: If generator_type is not recognized
    """
    if generator_type not in GENERATOR_CLASSES:
        raise ValueError(f"Unknown generator type: {generator_type}. "
                         f"Available: {list(GENERATOR_CLASSES.keys())}")

    generator_class = GENERATOR_CLASSES[generator_type]
    generator = generator_class(grid_size)
    terrain = generator.generate()

    print(f"Generated terrain: {generator_type} ({len(terrain)} cover tiles)")

    return terrain
