"""
Grid system for tactical battles.

This module defines the battlefield grid and individual tiles.
Each tile can contain terrain (cover) and units.
"""

import pygame
from typing import Optional, Tuple, List
import config


class Tile:
    """
    Represents a single tile on the battlefield grid.

    Each tile has:
    - Position (x, y coordinates)
    - Terrain type (empty, half cover, full cover)
    - Optional unit occupying the tile
    - Movement and sight blocking properties
    """

    def __init__(self, x: int, y: int, terrain_type: str = "empty"):
        """
        Initialize a tile.

        Args:
            x: Grid X coordinate (0-9)
            y: Grid Y coordinate (0-9)
            terrain_type: Type of terrain ("empty", "half_cover", "full_cover")
        """
        self.x = x
        self.y = y
        self.terrain_type = terrain_type
        self.occupied_by = None  # Will hold Unit reference when occupied

        # Set properties based on terrain type
        if terrain_type == "full_cover":
            self.blocks_movement = False  # Units can move through cover
            self.blocks_sight = True      # Full cover blocks line of sight
            self.defense_bonus = 40       # -40% hit chance for attackers
            self.symbol = "⬛"
        elif terrain_type == "half_cover":
            self.blocks_movement = False
            self.blocks_sight = False     # Half cover doesn't block LOS
            self.defense_bonus = 20       # -20% hit chance for attackers
            self.symbol = "▪️"
        else:  # empty
            self.blocks_movement = False
            self.blocks_sight = False
            self.defense_bonus = 0
            self.symbol = "⬜"

    def is_occupied(self) -> bool:
        """Check if this tile has a unit on it."""
        return self.occupied_by is not None

    def can_move_through(self) -> bool:
        """Check if units can move through this tile."""
        return not self.blocks_movement and not self.is_occupied()

    def get_position(self) -> Tuple[int, int]:
        """Get tile coordinates as tuple."""
        return (self.x, self.y)

    def __repr__(self) -> str:
        """String representation for debugging."""
        unit_str = f", occupied by {self.occupied_by.name}" if self.occupied_by else ""
        return f"Tile({self.x}, {self.y}, {self.terrain_type}{unit_str})"


class Grid:
    """
    Represents the 10x10 battlefield grid.

    The grid contains all tiles and provides methods for:
    - Accessing tiles by coordinates
    - Finding valid movement paths
    - Calculating distances
    - Managing unit placement
    """

    def __init__(self, size: int = config.GRID_SIZE):
        """
        Initialize the grid.

        Args:
            size: Grid dimensions (default 10x10 from config)
        """
        self.size = size
        self.tiles: List[List[Tile]] = []

        # Create grid of empty tiles
        for y in range(size):
            row = []
            for x in range(size):
                row.append(Tile(x, y, "empty"))
            self.tiles.append(row)

    def get_tile(self, x: int, y: int) -> Optional[Tile]:
        """
        Get tile at coordinates.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Tile object or None if coordinates are out of bounds
        """
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.tiles[y][x]
        return None

    def is_valid_position(self, x: int, y: int) -> bool:
        """
        Check if coordinates are within grid bounds.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            True if position is valid, False otherwise
        """
        return 0 <= x < self.size and 0 <= y < self.size

    def place_unit(self, unit, x: int, y: int) -> bool:
        """
        Place a unit on the grid.

        Args:
            unit: Unit object to place
            x: X coordinate
            y: Y coordinate

        Returns:
            True if placement successful, False if tile occupied or invalid
        """
        tile = self.get_tile(x, y)
        if tile and not tile.is_occupied():
            tile.occupied_by = unit
            unit.position = (x, y)
            return True
        return False

    def remove_unit(self, x: int, y: int) -> bool:
        """
        Remove unit from a tile.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            True if unit was removed, False if no unit there
        """
        tile = self.get_tile(x, y)
        if tile and tile.is_occupied():
            tile.occupied_by = None
            return True
        return False

    def move_unit(self, from_x: int, from_y: int, to_x: int, to_y: int) -> bool:
        """
        Move a unit from one tile to another.

        Args:
            from_x: Starting X coordinate
            from_y: Starting Y coordinate
            to_x: Destination X coordinate
            to_y: Destination Y coordinate

        Returns:
            True if move successful, False otherwise
        """
        from_tile = self.get_tile(from_x, from_y)
        to_tile = self.get_tile(to_x, to_y)

        if not from_tile or not to_tile:
            return False

        if not from_tile.is_occupied():
            return False

        if to_tile.is_occupied():
            return False

        # Move the unit
        unit = from_tile.occupied_by
        from_tile.occupied_by = None
        to_tile.occupied_by = unit
        unit.position = (to_x, to_y)

        return True

    def get_distance(self, x1: int, y1: int, x2: int, y2: int) -> float:
        """
        Calculate Euclidean distance between two tiles.

        Args:
            x1, y1: First tile coordinates
            x2, y2: Second tile coordinates

        Returns:
            Distance in tiles (diagonal = ~1.4, orthogonal = 1.0)
        """
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def get_manhattan_distance(self, x1: int, y1: int, x2: int, y2: int) -> int:
        """
        Calculate Manhattan distance between two tiles.

        Args:
            x1, y1: First tile coordinates
            x2, y2: Second tile coordinates

        Returns:
            Manhattan distance (only orthogonal moves)
        """
        return abs(x2 - x1) + abs(y2 - y1)

    def get_neighbors(self, x: int, y: int, diagonal: bool = True) -> List[Tuple[int, int]]:
        """
        Get all neighboring tile coordinates.

        Args:
            x: X coordinate
            y: Y coordinate
            diagonal: Include diagonal neighbors (default True)

        Returns:
            List of (x, y) tuples for valid neighbors
        """
        neighbors = []

        # Orthogonal directions (up, down, left, right)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if self.is_valid_position(nx, ny):
                neighbors.append((nx, ny))

        # Diagonal directions
        if diagonal:
            for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                nx, ny = x + dx, y + dy
                if self.is_valid_position(nx, ny):
                    neighbors.append((nx, ny))

        return neighbors

    def add_cover(self, x: int, y: int, cover_type: str) -> bool:
        """
        Add cover to a tile.

        Args:
            x: X coordinate
            y: Y coordinate
            cover_type: "half_cover" or "full_cover"

        Returns:
            True if cover added, False if invalid position
        """
        tile = self.get_tile(x, y)
        if tile:
            tile.terrain_type = cover_type
            if cover_type == "full_cover":
                tile.blocks_sight = True
                tile.defense_bonus = 40
                tile.symbol = "⬛"
            elif cover_type == "half_cover":
                tile.blocks_sight = False
                tile.defense_bonus = 20
                tile.symbol = "▪️"
            return True
        return False

    def setup_generated_terrain(self, terrain_data: List[Tuple[int, int, str]]):
        """
        Apply procedurally generated terrain to the grid.

        This method takes terrain data from a terrain generator and applies
        it to the grid by calling add_cover() for each piece.

        Args:
            terrain_data: List of (x, y, cover_type) tuples from a terrain generator

        Example:
            from combat.terrain_generator import generate_random_terrain
            terrain = generate_random_terrain(grid_size=10)
            grid.setup_generated_terrain(terrain)
        """
        for x, y, cover_type in terrain_data:
            self.add_cover(x, y, cover_type)

    def setup_test_cover(self):
        """
        Add some test cover to the grid for initial testing.
        This creates a simple layout with scattered cover pieces.

        DEPRECATED: Use setup_generated_terrain() with terrain_generator module instead.
        This method is kept for backwards compatibility but will be removed in Phase 2.
        """
        # Add some full cover in the center
        self.add_cover(4, 4, "full_cover")
        self.add_cover(5, 4, "full_cover")
        self.add_cover(4, 5, "full_cover")
        self.add_cover(5, 5, "full_cover")

        # Add some half cover scattered around
        self.add_cover(2, 2, "half_cover")
        self.add_cover(7, 2, "half_cover")
        self.add_cover(2, 7, "half_cover")
        self.add_cover(7, 7, "half_cover")

        # Add some walls (full cover) on edges
        self.add_cover(0, 3, "full_cover")
        self.add_cover(0, 4, "full_cover")
        self.add_cover(9, 5, "full_cover")
        self.add_cover(9, 6, "full_cover")

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Grid({self.size}x{self.size})"
