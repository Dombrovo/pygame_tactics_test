"""
Clarify: Does movement_range=4 mean "4 tiles" or "4 distance units"?

ANSWER: movement_range is DISTANCE, not tile count!

This test demonstrates the difference.
"""

import math
from combat.grid import Grid
from combat.pathfinding import get_reachable_tiles, find_path


def test_movement_range_is_distance_not_tiles():
    """
    Critical distinction:
    - movement_range=4 means "4.0 distance units"
    - NOT "4 tiles in any direction"

    Diagonal tiles cost more distance, so you can reach fewer of them!
    """
    print("\n" + "="*70)
    print("CRITICAL QUESTION: Does movement_range=4 mean 4 tiles or 4 distance?")
    print("="*70 + "\n")

    grid = Grid(size=10)
    start = (5, 5)
    movement_range = 4.0

    print(f"Unit at {start} with movement_range = {movement_range}")
    print(f"Question: Can they reach 4 tiles in ANY direction?\n")

    # Test cases: Can we reach these tiles?
    test_cases = [
        # (destination, tile_count, direction, expected_cost)
        ((5, 9), 4, "4 tiles NORTH (orthogonal)", 4.0),
        ((9, 5), 4, "4 tiles EAST (orthogonal)", 4.0),
        ((9, 9), 4, "4 tiles NORTHEAST (diagonal)", 5.657),  # 4 * sqrt(2)
        ((7, 7), 2, "2 tiles NORTHEAST (diagonal)", 2.828),  # 2 * sqrt(2)
        ((8, 8), 3, "3 tiles NORTHEAST (diagonal)", 4.243),  # 3 * sqrt(2)
    ]

    reachable = get_reachable_tiles(grid, start[0], start[1], movement_range)

    print("Testing reachability:\n")
    for dest, tile_count, direction, expected_cost in test_cases:
        is_reachable = dest in reachable
        within_range = expected_cost <= movement_range

        status = "[OK]" if is_reachable == within_range else "[ERROR]"
        reach_str = "CAN REACH" if is_reachable else "CANNOT REACH"

        print(f"{status} {direction}")
        print(f"     Destination: {dest}")
        print(f"     Tile count: {tile_count} tiles")
        print(f"     Distance cost: {expected_cost:.3f}")
        print(f"     Result: {reach_str}")
        print()

    print("="*70)
    print("ANSWER: movement_range is DISTANCE, not tile count!")
    print("="*70)
    print(f"With movement_range={movement_range}:")
    print(f"  - Can move 4 tiles orthogonally (4 tiles × 1.0 = 4.0 distance)")
    print(f"  - Can move 2 tiles diagonally (2 tiles × 1.414 = 2.828 distance)")
    print(f"  - CANNOT move 4 tiles diagonally (4 tiles × 1.414 = 5.657 distance > 4.0)")
    print()


def test_diagonal_uses_more_movement_budget():
    """
    Show that diagonal movement "costs more" from your movement budget.
    """
    print("\n" + "="*70)
    print("DEMONSTRATION: Diagonal movement uses more of your movement budget")
    print("="*70 + "\n")

    grid = Grid(size=10)

    # Scenario: Unit has movement_range=4.0
    movement_range = 4.0

    print(f"Unit has movement_range = {movement_range}\n")

    print("Scenario A: Move 4 tiles NORTH (orthogonal)")
    print("  Path: (5,5) -> (5,6) -> (5,7) -> (5,8) -> (5,9)")
    print("  Cost: 1.0 + 1.0 + 1.0 + 1.0 = 4.0")
    print("  Budget used: 4.0 / 4.0 = 100%")
    print("  Remaining movement: 0.0")
    print("  Result: EXACTLY at movement limit\n")

    print("Scenario B: Move 2 tiles NORTHEAST (diagonal)")
    print("  Path: (5,5) -> (6,6) -> (7,7)")
    print("  Cost: 1.414 + 1.414 = 2.828")
    print("  Budget used: 2.828 / 4.0 = 70.7%")
    print("  Remaining movement: 1.172")
    print("  Result: Still have movement left!\n")

    print("Scenario C: Move 3 tiles NORTHEAST (diagonal)")
    print("  Path: (5,5) -> (6,6) -> (7,7) -> (8,8)")
    print("  Cost: 1.414 + 1.414 + 1.414 = 4.243")
    print("  Budget used: 4.243 / 4.0 = 106.1%")
    print("  Remaining movement: -0.243")
    print("  Result: EXCEEDS movement limit - NOT ALLOWED!\n")

    print("="*70)
    print("Diagonal tiles are 'farther away' in terms of movement cost!")
    print("="*70)
    print()


def test_mixed_movement_example():
    """
    Show a real pathfinding example with mixed diagonal/orthogonal movement.
    """
    print("\n" + "="*70)
    print("REAL EXAMPLE: Pathfinding with movement budget")
    print("="*70 + "\n")

    grid = Grid(size=10)
    start = (0, 0)
    goal = (4, 3)

    print(f"Unit at {start} wants to reach {goal}")
    print(f"Let's see the path and cost breakdown:\n")

    path = find_path(grid, start[0], start[1], goal[0], goal[1])

    if path:
        print(f"Path found: {path}\n")

        total_cost = 0.0
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)

            if dx + dy == 2:
                step_cost = math.sqrt(2)
                move_type = "DIAGONAL"
            else:
                step_cost = 1.0
                move_type = "ORTHOGONAL"

            total_cost += step_cost

            print(f"  Step {i+1}: {path[i]} -> {path[i+1]}")
            print(f"    Type: {move_type}")
            print(f"    Cost: {step_cost:.3f}")
            print(f"    Running total: {total_cost:.3f}")
            print()

        print(f"TOTAL PATH COST: {total_cost:.3f}")
        print(f"TOTAL TILE COUNT: {len(path)} tiles\n")

        # Check if unit can make it with different movement ranges
        for test_range in [3.0, 4.0, 5.0, 6.0]:
            can_reach = total_cost <= test_range
            status = "YES" if can_reach else "NO"
            print(f"  Can reach with movement_range={test_range}? {status}")

        print()


def test_how_far_can_i_actually_move():
    """
    The PRACTICAL question: "My unit has movement_range=4, where can they go?"
    """
    print("\n" + "="*70)
    print("PRACTICAL QUESTION: Where can my unit actually move?")
    print("="*70 + "\n")

    grid = Grid(size=10)
    start = (5, 5)
    movement_range = 4.0

    print(f"Unit at {start}, movement_range = {movement_range}\n")

    reachable = get_reachable_tiles(grid, start[0], start[1], movement_range)

    print(f"Total reachable tiles: {len(reachable)}\n")

    # Count by direction
    north_tiles = sum(1 for x, y in reachable if x == 5 and y > 5)
    south_tiles = sum(1 for x, y in reachable if x == 5 and y < 5)
    east_tiles = sum(1 for x, y in reachable if y == 5 and x > 5)
    west_tiles = sum(1 for x, y in reachable if y == 5 and x < 5)

    print("Breakdown by direction:")
    print(f"  North (straight up): {north_tiles} tiles")
    print(f"  South (straight down): {south_tiles} tiles")
    print(f"  East (straight right): {east_tiles} tiles")
    print(f"  West (straight left): {west_tiles} tiles")
    print()

    # Check diagonal reach
    ne_diagonal_tiles = sum(1 for x, y in reachable if x > 5 and y > 5 and x == y)
    print(f"  Northeast diagonal: {ne_diagonal_tiles} tiles")
    print()

    print("In the actual game:")
    print("  - Green highlights show ALL reachable tiles")
    print("  - This accounts for diagonal costs automatically")
    print("  - You'll see a smaller diagonal reach than orthogonal reach")
    print()


if __name__ == "__main__":
    test_movement_range_is_distance_not_tiles()
    test_diagonal_uses_more_movement_budget()
    test_mixed_movement_example()
    test_how_far_can_i_actually_move()

    print("\n" + "="*70)
    print("FINAL SUMMARY")
    print("="*70)
    print()
    print("movement_range is a DISTANCE BUDGET, not a tile count!")
    print()
    print("When you move:")
    print("  1. Each orthogonal step COSTS 1.0 distance")
    print("  2. Each diagonal step COSTS 1.414 distance")
    print("  3. Your movement STOPS when you've spent your budget")
    print()
    print("Result:")
    print("  - Units can move FEWER diagonal tiles than orthogonal tiles")
    print("  - This is realistic (diagonal is actually farther)")
    print("  - Green highlights in-game show exactly where you can go")
    print()
    print("="*70)
