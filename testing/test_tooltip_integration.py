"""
Test script to verify terrain tooltips work with the grid system.

This tests the integration between:
- Tile tooltip data
- Grid.add_cover() method
- Terrain tooltip display

Run with: uv run python testing/test_tooltip_integration.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from combat.grid import Grid, Tile


def test_tile_tooltip_on_creation():
    """Test that tiles have correct tooltip data on creation."""
    print("=" * 60)
    print("TEST 1: Tile Tooltip Data on Creation")
    print("=" * 60)

    # Test empty tile
    empty_tile = Tile(0, 0, "empty")
    print(f"\nEmpty tile:")
    print(f"  terrain_type: {empty_tile.terrain_type}")
    print(f"  has_tooltip(): {empty_tile.has_tooltip()}")
    print(f"  tooltip_title: '{empty_tile.tooltip_title}'")
    assert empty_tile.has_tooltip() == False, "Empty tile should not have tooltip"

    # Test full cover tile
    full_tile = Tile(1, 1, "full_cover")
    print(f"\nFull cover tile (created directly):")
    print(f"  terrain_type: {full_tile.terrain_type}")
    print(f"  has_tooltip(): {full_tile.has_tooltip()}")
    print(f"  tooltip_title: '{full_tile.tooltip_title}'")
    print(f"  tooltip_flavor: '{full_tile.tooltip_flavor}'")
    print(f"  tooltip_mechanics: '{full_tile.tooltip_mechanics}'")
    assert full_tile.has_tooltip() == True, "Full cover tile should have tooltip"
    assert full_tile.tooltip_title == "Full Cover", "Full cover should have correct title"

    # Test half cover tile
    half_tile = Tile(2, 2, "half_cover")
    print(f"\nHalf cover tile (created directly):")
    print(f"  terrain_type: {half_tile.terrain_type}")
    print(f"  has_tooltip(): {half_tile.has_tooltip()}")
    print(f"  tooltip_title: '{half_tile.tooltip_title}'")
    assert half_tile.has_tooltip() == True, "Half cover tile should have tooltip"
    assert half_tile.tooltip_title == "Half Cover", "Half cover should have correct title"

    print("\n[OK] All tile creation tests passed!")


def test_add_cover_updates_tooltip():
    """Test that add_cover() updates tooltip data correctly."""
    print("\n" + "=" * 60)
    print("TEST 2: Grid.add_cover() Updates Tooltip Data")
    print("=" * 60)

    grid = Grid(size=10)

    # All tiles start as empty
    tile = grid.get_tile(5, 5)
    print(f"\nTile (5, 5) before adding cover:")
    print(f"  terrain_type: {tile.terrain_type}")
    print(f"  has_tooltip(): {tile.has_tooltip()}")
    print(f"  tooltip_title: '{tile.tooltip_title}'")
    assert tile.terrain_type == "empty", "Tile should start as empty"
    assert tile.has_tooltip() == False, "Empty tile should not have tooltip"

    # Add full cover
    grid.add_cover(5, 5, "full_cover")
    print(f"\nTile (5, 5) after adding full cover:")
    print(f"  terrain_type: {tile.terrain_type}")
    print(f"  has_tooltip(): {tile.has_tooltip()}")
    print(f"  tooltip_title: '{tile.tooltip_title}'")
    print(f"  tooltip_flavor: '{tile.tooltip_flavor}'")
    print(f"  tooltip_mechanics: '{tile.tooltip_mechanics}'")

    assert tile.terrain_type == "full_cover", "Tile should now be full_cover"
    assert tile.has_tooltip() == True, "Full cover tile should have tooltip"
    assert tile.tooltip_title == "Full Cover", "Should have correct title"
    assert "40%" in tile.tooltip_mechanics, "Should mention 40% defense bonus"

    # Test half cover on another tile
    tile2 = grid.get_tile(3, 3)
    grid.add_cover(3, 3, "half_cover")
    print(f"\nTile (3, 3) after adding half cover:")
    print(f"  terrain_type: {tile2.terrain_type}")
    print(f"  has_tooltip(): {tile2.has_tooltip()}")
    print(f"  tooltip_title: '{tile2.tooltip_title}'")

    assert tile2.terrain_type == "half_cover", "Tile should now be half_cover"
    assert tile2.has_tooltip() == True, "Half cover tile should have tooltip"
    assert tile2.tooltip_title == "Half Cover", "Should have correct title"
    assert "20%" in tile2.tooltip_mechanics, "Should mention 20% defense bonus"

    print("\n[OK] add_cover() correctly updates tooltip data!")


def test_generated_terrain_has_tooltips():
    """Test that procedurally generated terrain has tooltips."""
    print("\n" + "=" * 60)
    print("TEST 3: Generated Terrain Has Tooltips")
    print("=" * 60)

    from combat.terrain_generator import generate_terrain

    # Test with each generator type
    generators = ["symmetric", "scattered", "urban_ruins", "ritual_site", "open_field", "chokepoint"]

    for gen_name in generators:
        print(f"\nTesting {gen_name} generator:")

        # Create grid and generate terrain
        grid = Grid(size=10)
        terrain_data = generate_terrain(gen_name, grid_size=10)
        grid.setup_generated_terrain(terrain_data)

        # Count tiles with tooltips
        tooltip_count = 0
        for x in range(10):
            for y in range(10):
                tile = grid.get_tile(x, y)
                if tile and tile.has_tooltip():
                    tooltip_count += 1

        print(f"  Terrain pieces: {len(terrain_data)}")
        print(f"  Tiles with tooltips: {tooltip_count}")

        # Verify each terrain piece has a tooltip
        assert tooltip_count == len(terrain_data), f"{gen_name}: All terrain should have tooltips"

        # Spot check a few tiles
        if len(terrain_data) > 0:
            x, y, cover_type = terrain_data[0]
            tile = grid.get_tile(x, y)
            print(f"  Sample tile at ({x}, {y}): {tile.tooltip_title}")
            assert tile.has_tooltip(), "Sample tile should have tooltip"

    print("\n[OK] All generated terrain has tooltips!")


def run_all_tests():
    """Run all tooltip integration tests."""
    print("\n")
    print("=" * 60)
    print("    TERRAIN TOOLTIP INTEGRATION TESTS")
    print("=" * 60)
    print()

    try:
        test_tile_tooltip_on_creation()
        test_add_cover_updates_tooltip()
        test_generated_terrain_has_tooltips()

        print("\n" + "=" * 60)
        print("[OK] ALL INTEGRATION TESTS PASSED!")
        print("=" * 60)
        print("\nTooltips are now working correctly:")
        print("  - Tiles created with terrain have tooltips")
        print("  - add_cover() updates tooltip data")
        print("  - Generated terrain has tooltips")
        print("\nThe terrain tooltip system is ready to use!")
        print()

    except AssertionError as e:
        print("\n" + "=" * 60)
        print("[X] TEST FAILED!")
        print("=" * 60)
        print(f"Assertion Error: {e}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print("\n" + "=" * 60)
        print("[X] TEST FAILED!")
        print("=" * 60)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
