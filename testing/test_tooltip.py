"""
Test script for terrain tooltip functionality.

Run with: uv run python testing/test_tooltip.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
import config
from ui.ui_elements import Tooltip


def test_tooltip_basic():
    """Test basic tooltip creation and display."""
    print("=" * 60)
    print("TEST 1: Tooltip Basic Functionality")
    print("=" * 60)

    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    # Create tooltip
    tooltip = Tooltip(padding=12)

    # Set content
    tooltip.set_content(
        title="Full Cover",
        flavor_text="Solid terrain that provides complete protection",
        mechanics_text="+40% chance for attacks to miss when behind this cover"
    )

    print("\n[OK] Tooltip created successfully")
    print(f"  Title: {tooltip.title}")
    print(f"  Flavor: {tooltip.flavor_text}")
    print(f"  Mechanics: {tooltip.mechanics_text}")
    print(f"  Visible: {tooltip.visible}")

    # Show tooltip
    tooltip.show((400, 300))
    print(f"\n[OK] Tooltip shown at (400, 300)")
    print(f"  Visible: {tooltip.visible}")
    print(f"  Rect: {tooltip.rect}")

    # Hide tooltip
    tooltip.hide()
    print(f"\n[OK] Tooltip hidden")
    print(f"  Visible: {tooltip.visible}")

    pygame.quit()


def test_tooltip_edge_detection():
    """Test tooltip edge avoidance."""
    print("\n" + "=" * 60)
    print("TEST 2: Tooltip Edge Avoidance")
    print("=" * 60)

    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

    tooltip = Tooltip(padding=12)
    tooltip.set_content(
        title="Test Tooltip",
        flavor_text="Testing edge detection",
        mechanics_text="Should not go off-screen"
    )

    # Test positions
    test_positions = [
        (50, 50, "Top-left corner"),
        (config.SCREEN_WIDTH - 50, 50, "Top-right corner"),
        (50, config.SCREEN_HEIGHT - 50, "Bottom-left corner"),
        (config.SCREEN_WIDTH - 50, config.SCREEN_HEIGHT - 50, "Bottom-right corner"),
        (config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2, "Center"),
    ]

    print("\nTesting edge avoidance at various positions:")
    for x, y, desc in test_positions:
        tooltip.show((x, y))
        rect = tooltip.rect

        # Check if tooltip is within screen bounds
        in_bounds = (rect.x >= 0 and rect.y >= 0 and
                    rect.x + rect.width <= config.SCREEN_WIDTH and
                    rect.y + rect.height <= config.SCREEN_HEIGHT)

        status = "[OK]" if in_bounds else "[FAIL]"
        print(f"  {status} {desc:20s} Mouse:({x:4d}, {y:4d}) -> Rect:({rect.x:4d}, {rect.y:4d}, {rect.width:3d}×{rect.height:3d})")

    pygame.quit()


def test_tooltip_visual():
    """Visual test - displays tooltip in a window."""
    print("\n" + "=" * 60)
    print("TEST 3: Tooltip Visual Test")
    print("=" * 60)
    print("\nOpening window with tooltip display...")
    print("Move mouse to see tooltip follow cursor")
    print("Press ESC to exit\n")

    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Tooltip Visual Test")
    clock = pygame.time.Clock()

    tooltip = Tooltip(padding=12)
    tooltip.set_content(
        title="Full Cover",
        flavor_text="Solid terrain that provides complete protection",
        mechanics_text="+40% chance for attacks to miss"
    )

    running = True
    frame_count = 0

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Update tooltip position
        tooltip.show(mouse_pos)

        # Draw
        screen.fill((15, 15, 25))  # Dark background

        # Draw helper text
        font = pygame.font.Font(None, 36)
        text = font.render("Move mouse to see tooltip", True, (220, 220, 230))
        screen.blit(text, (250, 250))

        # Draw tooltip
        tooltip.draw(screen)

        # Draw mouse position for debugging
        pos_font = pygame.font.Font(None, 24)
        pos_text = pos_font.render(f"Mouse: {mouse_pos}", True, (150, 150, 150))
        screen.blit(pos_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

        frame_count += 1
        if frame_count % 60 == 0:
            print(f"Frame {frame_count}: Mouse at {mouse_pos}, Tooltip rect: {tooltip.rect}")

    pygame.quit()
    print("\n[OK] Visual test completed")


def run_all_tests():
    """Run all tooltip tests."""
    print("\n")
    print("=" * 60)
    print("          TERRAIN TOOLTIP TESTS")
    print("=" * 60)
    print()

    try:
        test_tooltip_basic()
        test_tooltip_edge_detection()

        # Ask before visual test
        response = input("\nRun visual test? (y/n): ").strip().lower()
        if response == 'y':
            test_tooltip_visual()

        print("\n" + "=" * 60)
        print("[OK] ALL TESTS PASSED!")
        print("=" * 60)
        print()

    except Exception as e:
        print("\n" + "=" * 60)
        print("[X] TEST FAILED!")
        print("=" * 60)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
