"""
Enemy AI system for tactical combat.

This module implements basic AI behaviors for enemy units during their turns.
Different enemy types have different movement and targeting behaviors:
- Cultists: Move up to 4 tiles towards investigator with highest health
- Hounds: Move up to 6 tiles towards nearest investigator

Enemies use their full movement_range stat for aggressive positioning.
"""

import math
from typing import List, Optional, Tuple, Dict, Any, TYPE_CHECKING
from entities.unit import Unit
from entities.investigator import Investigator
from entities.enemy import Enemy, Cultist, HoundOfTindalos
from combat.grid import Grid
from combat.pathfinding import find_path
from combat.line_of_sight import can_attack
from combat.combat_resolver import resolve_attack

if TYPE_CHECKING:
    from entities.combat_deck import CombatDeck


def find_highest_health_target(investigators: List[Investigator]) -> Optional[Investigator]:
    """
    Find the investigator with the highest current health.

    Cultists target the healthiest investigator to maximize damage output
    over time (finish off weak targets less efficiently than focusing fire).

    Args:
        investigators: List of all investigator units

    Returns:
        Investigator with highest current health, or None if all incapacitated
    """
    active_investigators = [inv for inv in investigators if inv.can_act()]

    if not active_investigators:
        return None

    # Find investigator with maximum current health
    return max(active_investigators, key=lambda inv: inv.current_health)


def find_nearest_target(enemy: Enemy, investigators: List[Investigator], grid: Grid) -> Optional[Investigator]:
    """
    Find the nearest investigator to the enemy unit.

    Hounds use pack tactics to quickly close distance with the nearest prey.

    Args:
        enemy: The enemy unit searching for a target
        investigators: List of all investigator units
        grid: The battlefield grid (for distance calculations)

    Returns:
        Nearest investigator, or None if all incapacitated
    """
    active_investigators = [inv for inv in investigators if inv.can_act()]

    if not active_investigators:
        return None

    if not enemy.position:
        return None

    # Find investigator with minimum distance
    # grid.get_distance() uses Euclidean distance formula
    return min(
        active_investigators,
        key=lambda inv: grid.get_distance(enemy.position[0], enemy.position[1],
                                         inv.position[0], inv.position[1]) if inv.position else float('inf')
    )


def calculate_movement_target(enemy: Enemy, target: Unit, grid: Grid, max_tiles: int) -> Optional[Tuple[int, int]]:
    """
    Calculate where the enemy should move to approach the target.

    Uses A* pathfinding to find optimal path, then takes N steps along it.

    Args:
        enemy: The enemy unit that's moving
        target: The target unit to move towards
        grid: The battlefield grid
        max_tiles: Maximum number of tiles to move (1 for Cultists, 2 for Hounds)

    Returns:
        (x, y) coordinates to move to, or None if no valid move exists
    """
    if not enemy.position or not target.position:
        return None

    # Target tile is occupied, so we need to path to an adjacent tile instead
    # Find all tiles adjacent to the target
    target_neighbors = grid.get_neighbors(target.position[0], target.position[1], diagonal=True)

    # Filter to only unoccupied tiles
    valid_goals = []
    for nx, ny in target_neighbors:
        tile = grid.get_tile(nx, ny)
        if tile and not tile.blocks_movement and not tile.is_occupied():
            valid_goals.append((nx, ny))

    if not valid_goals:
        # No valid adjacent tiles (target is surrounded)
        return None

    # Find the valid goal closest to the enemy
    best_goal = min(
        valid_goals,
        key=lambda pos: grid.get_distance(enemy.position[0], enemy.position[1], pos[0], pos[1])
    )

    # Find path from enemy to best adjacent tile
    path = find_path(
        grid,
        start_x=enemy.position[0],
        start_y=enemy.position[1],
        goal_x=best_goal[0],
        goal_y=best_goal[1]
    )

    if not path or len(path) <= 1:
        # No path found, or already adjacent to target
        return None

    # Path includes starting position, so:
    # path[0] = current position
    # path[1] = first step
    # path[2] = second step, etc.

    # Calculate how far along the path we can move within our movement budget
    # We need to account for diagonal movement costing sqrt(2) ≈ 1.414
    accumulated_cost = 0.0
    destination_index = 0

    for i in range(1, len(path)):
        # Calculate cost to move from path[i-1] to path[i]
        prev_x, prev_y = path[i-1]
        curr_x, curr_y = path[i]

        dx = abs(curr_x - prev_x)
        dy = abs(curr_y - prev_y)

        # Diagonal movement costs sqrt(2), orthogonal costs 1.0
        if dx + dy == 2:  # Diagonal
            step_cost = math.sqrt(2)
        else:  # Orthogonal
            step_cost = 1.0

        # Check if we can afford this step
        if accumulated_cost + step_cost <= max_tiles:
            accumulated_cost += step_cost
            destination_index = i
        else:
            # Can't afford this step, stop here
            break

    if destination_index < 1:
        # Can't move anywhere within budget
        return None

    # Get the destination tile (furthest we can move within budget)
    destination = path[destination_index]

    # Verify destination is not occupied (except by the target, which we can't reach anyway)
    dest_tile = grid.get_tile(destination[0], destination[1])
    if dest_tile and dest_tile.occupied_by and dest_tile.occupied_by != target:
        # Destination is occupied by another unit - can't move there
        # Try moving one tile less
        if move_distance > 1:
            destination = path[move_distance - 1]
            dest_tile = grid.get_tile(destination[0], destination[1])
            if dest_tile and dest_tile.occupied_by:
                return None  # Still occupied, can't move
        else:
            return None

    return destination


def execute_enemy_turn(
    enemy: Enemy,
    investigators: List[Investigator],
    grid: Grid,
    monster_deck: Optional["CombatDeck"] = None
) -> Optional[Dict[str, Any]]:
    """
    Execute AI behavior for an enemy unit's turn.

    Different enemy types have different behaviors:
    - Cultists: Target investigator with highest health, move up to 4 tiles, attack if in range
    - Hounds: Target nearest investigator, move up to 6 tiles, attack if in range

    Movement uses the enemy's full movement_range stat:
    - Cultists: 4 tiles per turn
    - Hounds: 6 tiles per turn (very fast!)

    Args:
        enemy: The enemy unit taking its turn
        investigators: List of all investigator units (for targeting)
        grid: The battlefield grid
        monster_deck: Optional universal monster deck (for attack resolution)

    Returns:
        Dictionary with attack result if attack was made, None otherwise.
        Result format matches combat_resolver.resolve_attack() return value.
    """
    if not enemy.can_act():
        # Enemy is incapacitated, skip turn
        return

    # Determine target based on enemy type
    target = None

    if isinstance(enemy, Cultist):
        # Cultists target highest health investigator
        target = find_highest_health_target(investigators)
        print(f"  {enemy.name} targeting highest health investigator")

    elif isinstance(enemy, HoundOfTindalos):
        # Hounds target nearest investigator
        target = find_nearest_target(enemy, investigators, grid)
        print(f"  {enemy.name} targeting nearest investigator")

    # Use the enemy's full movement_range stat
    max_movement = enemy.movement_range

    if not target:
        # No valid targets (all investigators incapacitated)
        print(f"  {enemy.name} has no valid targets")
        return

    print(f"  Target: {target.name} (HP: {target.current_health}/{target.max_health})")

    # Calculate movement destination
    move_to = calculate_movement_target(enemy, target, grid, max_movement)

    if move_to:
        # Execute movement
        old_pos = enemy.position
        grid.move_unit(old_pos[0], old_pos[1], move_to[0], move_to[1])
        print(f"  {enemy.name} moves from {old_pos} to {move_to}")
    else:
        print(f"  {enemy.name} cannot move (no valid path)")

    # Attack logic: After moving, check if target is in range and attack if possible
    if not enemy.position or not target.position:
        # No position (shouldn't happen, but safety check)
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
        attack_result = resolve_attack(enemy, target, grid, monster_deck)

        # Add attacker and target info to result for popup display
        attack_result["attacker"] = enemy
        attack_result["target"] = target

        return attack_result
    else:
        # Can't attack (out of range or no LOS)
        print(f"  {enemy.name} cannot attack: {reason}")
        return None
