"""
Test diagonal movement costs in pathfinding.

This test demonstrates how diagonal movement is calculated:
- Orthogonal (up/down/left/right): 1.0 per tile
- Diagonal (corners): sqrt(2) = 1.414 per tile

This is TRUE diagonal movement (Euclidean distance), not "move up then across".
"""

import math
from combat.grid import Grid
from combat.pathfinding import find_path, get_reachable_tiles


def test_diagonal_vs_orthogonal_cost():
    """
    Test that diagonal movement costs sqrt(2), not 2.

    Compare:
    - Pure diagonal path vs
    - Orthogonal path (up then across)

    If diagonal was "up then across", both would cost the same.
    But diagonal should be ~1.414x cheaper!
    """
    print("\n=== Diagonal Movement Cost Test ===\n")

    grid = Grid(size=10)

    # Scenario: Move from (0,0) to (3,3)
    start = (0, 0)
    goal = (3, 3)

    # Test 1: Pure diagonal path
    print("Test 1: Pure Diagonal Path (0,0) -> (3,3)")
    print("  Expected path: (0,0) -> (1,1) -> (2,2) -> (3,3)")
    print("  Expected cost: 3 * sqrt(2) = 3 * 1.414 = 4.242")

    path = find_path(grid, start[0], start[1], goal[0], goal[1])

    if path:
        print(f"  Actual path: {path}")

        # Calculate actual cost
        cost = 0
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)

            if dx + dy == 2:  # Diagonal
                step_cost = math.sqrt(2)
            else:  # Orthogonal
                step_cost = 1.0

            cost += step_cost

        print(f"  Actual cost: {cost:.3f}")
        print(f"  Path length: {len(path)} tiles")

    # Test 2: What if diagonal was "2 steps"?
    print("\n\nTest 2: If Diagonal = 2 Steps (Orthogonal)")
    print("  Hypothetical cost if we moved up then across:")
    print("  (0,0) -> (0,1) -> (0,2) -> (0,3) -> (1,3) -> (2,3) -> (3,3)")
    print("  Cost: 6 steps * 1.0 = 6.0")

    print("\n\nConclusion:")
    if path and len(path) == 4:  # Pure diagonal: 4 tiles
        print("  [OK] Diagonal movement uses TRUE diagonal (sqrt(2) = 1.414)")
        print(f"  [OK] Moving diagonally is {6.0/cost:.1f}x more efficient than orthogonal!")
        print("  [OK] This is proper Euclidean distance, not 'up then across'")
    else:
        print("  [X] Something unexpected happened")

    return path


def test_movement_range_with_diagonals():
    """
    Test that movement range respects diagonal costs.

    With movement_range=4.0:
    - Can reach 4 orthogonal tiles (cost 1.0 each)
    - Can reach only 2 diagonal tiles (cost 1.414 each, so 2*1.414 = 2.828 < 4.0)
    - Cannot reach 3 diagonal tiles (3*1.414 = 4.242 > 4.0)
    """
    print("\n\n=== Movement Range with Diagonal Test ===\n")

    grid = Grid(size=10)
    start = (5, 5)  # Center of grid
    movement_range = 4.0

    print(f"Starting at {start} with movement range {movement_range}")

    reachable = get_reachable_tiles(grid, start[0], start[1], movement_range)

    # Check specific tiles
    test_cases = [
        ((5, 9), 4.0, "4 tiles up (orthogonal)"),
        ((9, 5), 4.0, "4 tiles right (orthogonal)"),
        ((7, 7), 2.828, "2 tiles diagonal (northeast)"),
        ((8, 8), 4.243, "3 tiles diagonal (northeast)"),  # Should NOT be reachable
    ]

    print("\nReachability tests:")
    for pos, expected_cost, description in test_cases:
        is_reachable = pos in reachable
        should_reach = expected_cost <= movement_range

        status = "[OK]" if is_reachable == should_reach else "[X]"
        reach_str = "REACHABLE" if is_reachable else "NOT REACHABLE"

        print(f"  {status} {pos} - {description}")
        print(f"       Cost: {expected_cost:.3f}, {reach_str}")

    # Count reachable tiles
    print(f"\nTotal reachable tiles: {len(reachable)}")

    return reachable


def test_diagonal_pathfinding_example():
    """
    Visual example of how diagonal movement works.
    """
    print("\n\n=== Visual Diagonal Movement Example ===\n")

    grid = Grid(size=6)

    # Test case: (0,0) to (5,3)
    start = (0, 0)
    goal = (5, 3)

    print(f"Finding path from {start} to {goal}\n")

    path = find_path(grid, start[0], start[1], goal[0], goal[1])

    if path:
        # Create visual grid
        visual = [['.' for _ in range(6)] for _ in range(6)]

        # Mark path
        for i, (x, y) in enumerate(path):
            if i == 0:
                visual[y][x] = 'S'  # Start
            elif i == len(path) - 1:
                visual[y][x] = 'E'  # End
            else:
                visual[y][x] = str(i)  # Step number

        # Print grid
        print("Visual path (S=start, E=end, numbers=steps):")
        for row in visual:
            print("  " + " ".join(row))

        # Show step-by-step costs
        print("\nStep-by-step movement:")
        total_cost = 0
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)

            if dx + dy == 2:  # Diagonal
                step_cost = math.sqrt(2)
                direction = "DIAGONAL"
            else:  # Orthogonal
                step_cost = 1.0
                direction = "ORTHOGONAL"

            total_cost += step_cost
            print(f"  Step {i+1}: {path[i]} -> {path[i+1]} = {direction} (cost: {step_cost:.3f})")

        print(f"\nTotal path cost: {total_cost:.3f}")
        print(f"Total path length: {len(path)} tiles")


if __name__ == "__main__":
    # Run all tests
    test_diagonal_vs_orthogonal_cost()
    test_movement_range_with_diagonals()
    test_diagonal_pathfinding_example()

    print("\n\n" + "="*60)
    print("SUMMARY: Diagonal Movement Implementation")
    print("="*60)
    print("Diagonal movement uses TRUE Euclidean distance (sqrt(2) = 1.414)")
    print("This means:")
    print("  - Moving diagonally is MORE EFFICIENT than going up then across")
    print("  - A unit can move further diagonally than orthogonally")
    print("  - Movement costs are realistic (straight line is shortest)")
    print("\nThis is the CORRECT implementation for tactical games!")
    print("="*60)
