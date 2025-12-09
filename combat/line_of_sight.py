"""
Line of Sight system for tactical combat.

This module implements line of sight (LOS) calculations using Bresenham's
line algorithm. LOS is required for ranged attacks - you can't shoot what
you can't see.

Rules:
- Full cover blocks LOS (can't shoot through walls)
- Half cover does NOT block LOS (can shoot over low obstacles)
- Empty tiles don't block LOS
- Units don't block LOS to themselves
"""

from typing import Tuple, List, Optional
from combat.grid import Grid


def bresenham_line(start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Generate all points along a line using Bresenham's line algorithm.

    This is the classic algorithm for drawing lines on a grid, adapted for
    LOS calculations. It ensures we check every tile the "shot" passes through.

    Args:
        start: Starting coordinates (x, y)
        end: Ending coordinates (x, y)

    Returns:
        List of all (x, y) coordinates along the line, INCLUDING start and end

    Example:
        >>> bresenham_line((0, 0), (3, 3))
        [(0, 0), (1, 1), (2, 2), (3, 3)]

        >>> bresenham_line((0, 0), (4, 2))
        [(0, 0), (1, 0), (2, 1), (3, 1), (4, 2)]
    """
    x0, y0 = start
    x1, y1 = end

    points = []

    # Calculate deltas
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    # Determine direction of line (step +1 or -1)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    # Initialize error term
    err = dx - dy

    # Current position
    x, y = x0, y0

    while True:
        # Add current point to list
        points.append((x, y))

        # Check if we've reached the end
        if x == x1 and y == y1:
            break

        # Calculate error for next step
        e2 = 2 * err

        # Step in x direction
        if e2 > -dy:
            err -= dy
            x += sx

        # Step in y direction
        if e2 < dx:
            err += dx
            y += sy

    return points


def has_line_of_sight(
    start: Tuple[int, int],
    end: Tuple[int, int],
    grid: Grid,
    ignore_units: bool = True
) -> bool:
    """
    Check if there is a clear line of sight between two positions.

    Line of sight is blocked by:
    - Full cover tiles (blocks_sight = True)
    - Tiles outside the grid bounds

    Line of sight is NOT blocked by:
    - Half cover (can shoot over low obstacles)
    - Empty tiles
    - Other units (unless ignore_units = False)

    Args:
        start: Starting position (x, y) - attacker position
        end: Target position (x, y) - defender position
        grid: The battlefield grid
        ignore_units: If True, units don't block LOS (default True)

    Returns:
        True if clear line of sight exists, False if blocked

    Example:
        >>> has_line_of_sight((0, 0), (5, 5), grid)
        True  # Clear shot

        >>> has_line_of_sight((0, 0), (5, 5), grid)  # Wall at (3, 3)
        False  # Blocked by wall
    """
    # Get all points along the line
    line_points = bresenham_line(start, end)

    # Check each point along the line
    for i, (x, y) in enumerate(line_points):
        # Skip the starting position (attacker's tile)
        if i == 0:
            continue

        # Skip the ending position (target's tile - we can always see the target tile itself)
        if i == len(line_points) - 1:
            continue

        # Get the tile at this position
        tile = grid.get_tile(x, y)

        # Out of bounds = no LOS
        if tile is None:
            return False

        # Full cover blocks LOS
        if tile.blocks_sight:
            return False

        # Optionally check if a unit blocks LOS
        if not ignore_units and tile.is_occupied():
            return False

    # No obstacles found - clear line of sight!
    return True


def get_tiles_with_los(
    start: Tuple[int, int],
    grid: Grid,
    max_range: Optional[int] = None
) -> List[Tuple[int, int]]:
    """
    Get all tiles that have line of sight from a starting position.

    Useful for highlighting valid attack targets.

    Args:
        start: Starting position (x, y)
        grid: The battlefield grid
        max_range: Maximum distance to check (None = entire grid)

    Returns:
        List of (x, y) coordinates with clear LOS from start

    Example:
        >>> visible_tiles = get_tiles_with_los((5, 5), grid, max_range=6)
        >>> # Returns all tiles within 6 tiles that have clear LOS
    """
    visible_tiles = []

    # Check every tile on the grid
    for y in range(grid.size):
        for x in range(grid.size):
            # Skip the starting position
            if (x, y) == start:
                continue

            # If max_range specified, skip tiles beyond range
            if max_range is not None:
                distance = grid.get_distance(start[0], start[1], x, y)
                if distance > max_range:
                    continue

            # Check LOS
            if has_line_of_sight(start, (x, y), grid):
                visible_tiles.append((x, y))

    return visible_tiles


def get_cover_between(
    start: Tuple[int, int],
    end: Tuple[int, int],
    grid: Grid
) -> str:
    """
    Determine the best cover between attacker and target.

    This checks all tiles along the line of sight and returns the best
    cover the target benefits from.

    Cover priority (best to worst):
    - Full cover (+40% defense, blocks sight)
    - Half cover (+20% defense)
    - No cover (0% defense)

    Args:
        start: Attacker position (x, y)
        end: Target position (x, y)
        grid: The battlefield grid

    Returns:
        Cover type: "full_cover", "half_cover", or "empty"

    Note:
        If full cover exists, has_line_of_sight() would return False,
        so this is mainly for determining half cover bonus.
    """
    line_points = bresenham_line(start, end)

    best_cover = "empty"

    # Check each point along the line (excluding start and end)
    for i, (x, y) in enumerate(line_points):
        # Skip start and end positions
        if i == 0 or i == len(line_points) - 1:
            continue

        tile = grid.get_tile(x, y)
        if tile is None:
            continue

        # Check for cover
        if tile.terrain_type == "full_cover":
            return "full_cover"  # Best cover, return immediately
        elif tile.terrain_type == "half_cover" and best_cover == "empty":
            best_cover = "half_cover"

    return best_cover


def can_attack(
    attacker_pos: Tuple[int, int],
    target_pos: Tuple[int, int],
    weapon_range: int,
    grid: Grid
) -> Tuple[bool, str]:
    """
    Check if an attack is possible from attacker to target.

    Combines range check and line of sight check.

    Args:
        attacker_pos: Attacker position (x, y)
        target_pos: Target position (x, y)
        weapon_range: Maximum attack range in tiles
        grid: The battlefield grid

    Returns:
        Tuple of (can_attack: bool, reason: str)
        - (True, "valid") if attack is possible
        - (False, "out_of_range") if target too far
        - (False, "no_line_of_sight") if LOS blocked

    Example:
        >>> can_attack((0, 0), (5, 5), weapon_range=6, grid)
        (True, "valid")

        >>> can_attack((0, 0), (9, 9), weapon_range=6, grid)
        (False, "out_of_range")
    """
    # Check range
    distance = grid.get_distance(attacker_pos[0], attacker_pos[1],
                                 target_pos[0], target_pos[1])

    if distance > weapon_range:
        return (False, "out_of_range")

    # Check line of sight
    if not has_line_of_sight(attacker_pos, target_pos, grid):
        return (False, "no_line_of_sight")

    return (True, "valid")


def get_valid_attack_targets(
    attacker_pos: Tuple[int, int],
    weapon_range: int,
    grid: Grid,
    target_team: str
) -> List[Tuple[int, int]]:
    """
    Get all valid attack targets for a unit.

    Returns positions of enemy units that are:
    1. Within weapon range
    2. Have clear line of sight
    3. On the opposing team

    Args:
        attacker_pos: Attacker position (x, y)
        weapon_range: Maximum attack range in tiles
        grid: The battlefield grid
        target_team: Team to target ("player" or "enemy")

    Returns:
        List of (x, y) positions that can be attacked

    Example:
        >>> targets = get_valid_attack_targets((0, 0), 5, grid, "enemy")
        >>> # Returns positions of all enemies within range and LOS
    """
    valid_targets = []

    # Check every tile on the grid
    for y in range(grid.size):
        for x in range(grid.size):
            tile = grid.get_tile(x, y)
            if tile is None or not tile.is_occupied():
                continue

            # Check if unit is on target team
            if tile.occupied_by.team != target_team:
                continue

            # Check if attack is valid
            can_attack_result, _ = can_attack(attacker_pos, (x, y), weapon_range, grid)
            if can_attack_result:
                valid_targets.append((x, y))

    return valid_targets
