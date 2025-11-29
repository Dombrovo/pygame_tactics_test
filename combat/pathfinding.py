"""
Pathfinding system for tactical movement.

This module implements A* pathfinding algorithm to find optimal paths
across the grid battlefield, respecting obstacles and movement costs.
"""

from typing import List, Tuple, Optional, Set
import math
from combat.grid import Grid


class PathNode:
    """
    Node in the A* pathfinding algorithm.

    Represents a tile being considered for the path, with costs
    for traveling to it and estimated cost to reach the goal.
    """

    def __init__(self, x: int, y: int, g_cost: float = 0, h_cost: float = 0, parent: Optional['PathNode'] = None):
        """
        Initialize a path node.

        Args:
            x: Grid X coordinate
            y: Grid Y coordinate
            g_cost: Cost from start to this node (actual cost)
            h_cost: Heuristic cost from this node to goal (estimated)
            parent: Previous node in the path (for reconstruction)
        """
        self.x = x
        self.y = y
        self.g_cost = g_cost  # Cost from start
        self.h_cost = h_cost  # Heuristic to goal
        self.parent = parent

    @property
    def f_cost(self) -> float:
        """
        Total cost (f = g + h).

        A* uses f_cost to prioritize which nodes to explore.
        Lower f_cost = better candidate for the path.
        """
        return self.g_cost + self.h_cost

    def __lt__(self, other: 'PathNode') -> bool:
        """Comparison for priority queue (lower f_cost = higher priority)."""
        return self.f_cost < other.f_cost

    def __eq__(self, other: object) -> bool:
        """Equality based on position only."""
        if not isinstance(other, PathNode):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        """Hash based on position for set operations."""
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"PathNode({self.x}, {self.y}, f={self.f_cost:.1f})"


def heuristic(x1: int, y1: int, x2: int, y2: int) -> float:
    """
    Calculate heuristic distance between two points.

    Uses Euclidean distance as the heuristic, which is admissible
    (never overestimates) for diagonal movement with sqrt(2) cost.

    Args:
        x1, y1: Start position
        x2, y2: Goal position

    Returns:
        Estimated distance between positions
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def reconstruct_path(goal_node: PathNode) -> List[Tuple[int, int]]:
    """
    Reconstruct path by following parent pointers from goal to start.

    Args:
        goal_node: The final node that reached the goal

    Returns:
        List of (x, y) coordinates from start to goal (inclusive)
    """
    path = []
    current = goal_node

    # Follow parent pointers back to start
    while current is not None:
        path.append((current.x, current.y))
        current = current.parent

    # Reverse to get start→goal order
    path.reverse()
    return path


def find_path(grid: Grid, start_x: int, start_y: int, goal_x: int, goal_y: int,
              max_distance: Optional[float] = None) -> Optional[List[Tuple[int, int]]]:
    """
    Find optimal path using A* algorithm.

    The algorithm explores tiles in order of their f_cost (g + h):
    - g_cost: Actual cost from start to current tile
    - h_cost: Estimated cost from current tile to goal
    - f_cost: Total estimated cost through this tile

    Movement costs:
    - Orthogonal (up/down/left/right): 1.0 per tile
    - Diagonal: ~1.414 (sqrt(2)) per tile

    Args:
        grid: The battlefield grid
        start_x, start_y: Starting position
        goal_x, goal_y: Destination position
        max_distance: Optional maximum path length (for movement range)

    Returns:
        List of (x, y) coordinates forming the path, or None if no path exists
        Path includes both start and goal positions

    Example:
        >>> path = find_path(grid, 0, 0, 3, 3, max_distance=5.0)
        >>> # Returns: [(0,0), (1,1), (2,2), (3,3)] or similar
    """
    # Validate positions
    if not grid.is_valid_position(start_x, start_y):
        return None
    if not grid.is_valid_position(goal_x, goal_y):
        return None

    # If already at goal, return single-tile path
    if start_x == goal_x and start_y == goal_y:
        return [(start_x, start_y)]

    # Check if goal is occupied (can't move to occupied tile)
    goal_tile = grid.get_tile(goal_x, goal_y)
    if goal_tile and goal_tile.is_occupied():
        return None

    # Initialize A* structures
    open_set: List[PathNode] = []  # Nodes to explore (priority queue)
    closed_set: Set[Tuple[int, int]] = set()  # Already explored positions

    # Create start node
    start_node = PathNode(
        start_x, start_y,
        g_cost=0,
        h_cost=heuristic(start_x, start_y, goal_x, goal_y)
    )
    open_set.append(start_node)

    # Main A* loop
    while open_set:
        # Get node with lowest f_cost
        open_set.sort()  # Sort by f_cost (PathNode.__lt__)
        current = open_set.pop(0)

        # Check if we reached the goal
        if current.x == goal_x and current.y == goal_y:
            return reconstruct_path(current)

        # Mark as explored
        closed_set.add((current.x, current.y))

        # Explore neighbors
        neighbors = grid.get_neighbors(current.x, current.y, diagonal=True)

        for nx, ny in neighbors:
            # Skip if already explored
            if (nx, ny) in closed_set:
                continue

            # Skip if tile is blocked
            tile = grid.get_tile(nx, ny)
            if not tile or tile.blocks_movement:
                continue

            # Skip if occupied (unless it's the goal - we're moving there)
            if tile.is_occupied() and not (nx == goal_x and ny == goal_y):
                continue

            # Calculate movement cost to this neighbor
            # Diagonal movement costs sqrt(2) ≈ 1.414
            # Orthogonal movement costs 1.0
            dx = abs(nx - current.x)
            dy = abs(ny - current.y)
            if dx + dy == 2:  # Diagonal
                move_cost = math.sqrt(2)
            else:  # Orthogonal
                move_cost = 1.0

            # Calculate g_cost for this path
            tentative_g_cost = current.g_cost + move_cost

            # If max_distance specified, skip if path is too long
            if max_distance is not None and tentative_g_cost > max_distance:
                continue

            # Check if neighbor is already in open set
            neighbor_node = None
            for node in open_set:
                if node.x == nx and node.y == ny:
                    neighbor_node = node
                    break

            # If not in open set, add it
            if neighbor_node is None:
                neighbor_node = PathNode(
                    nx, ny,
                    g_cost=tentative_g_cost,
                    h_cost=heuristic(nx, ny, goal_x, goal_y),
                    parent=current
                )
                open_set.append(neighbor_node)
            # If in open set but this path is better, update it
            elif tentative_g_cost < neighbor_node.g_cost:
                neighbor_node.g_cost = tentative_g_cost
                neighbor_node.parent = current

    # No path found
    return None


def get_reachable_tiles(grid: Grid, start_x: int, start_y: int,
                       movement_range: float) -> Set[Tuple[int, int]]:
    """
    Get all tiles reachable within movement range.

    Uses a flood-fill approach to find all tiles that can be reached
    from the starting position within the unit's movement range.

    This is more efficient than pathfinding to every tile individually,
    and is used to highlight valid movement destinations.

    Args:
        grid: The battlefield grid
        start_x, start_y: Starting position
        movement_range: Maximum movement distance

    Returns:
        Set of (x, y) coordinates of reachable tiles
        Does NOT include the starting position
        Does NOT include occupied tiles

    Example:
        >>> reachable = get_reachable_tiles(grid, 5, 5, 4.0)
        >>> # Returns set of tiles within 4 movement from (5,5)
    """
    reachable: Set[Tuple[int, int]] = set()

    # Track tiles and their distance from start
    # Format: {(x, y): distance}
    distances: dict[Tuple[int, int], float] = {(start_x, start_y): 0}

    # Frontier: tiles to explore next
    frontier: List[Tuple[int, int, float]] = [(start_x, start_y, 0)]

    while frontier:
        x, y, dist = frontier.pop(0)

        # Explore neighbors
        neighbors = grid.get_neighbors(x, y, diagonal=True)

        for nx, ny in neighbors:
            # Skip if already visited with better distance
            if (nx, ny) in distances:
                continue

            # Get the tile
            tile = grid.get_tile(nx, ny)
            if not tile:
                continue

            # Skip if blocked
            if tile.blocks_movement:
                continue

            # Skip if occupied
            if tile.is_occupied():
                continue

            # Calculate distance to this neighbor
            dx = abs(nx - x)
            dy = abs(ny - y)
            if dx + dy == 2:  # Diagonal
                move_cost = math.sqrt(2)
            else:  # Orthogonal
                move_cost = 1.0

            new_dist = dist + move_cost

            # Skip if out of range
            if new_dist > movement_range:
                continue

            # Add to reachable set (exclude starting position)
            if not (nx == start_x and ny == start_y):
                reachable.add((nx, ny))

            # Record distance
            distances[(nx, ny)] = new_dist

            # Add to frontier for further exploration
            frontier.append((nx, ny, new_dist))

    return reachable
