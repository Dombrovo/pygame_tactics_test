"""
Test the Popup notification system.

This script tests the new Popup class for turn notifications
and damage notifications.
"""

import pygame
import sys

# Add parent directory to path for imports
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config
from ui.ui_elements import Popup


def test_turn_popup():
    """Test the turn notification popup."""
    print("\n=== TEST: Turn Notification Popup ===")

    # Initialize Pygame
    pygame.init()

    # Create a test screen
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Popup Test")

    # Fill screen with dark background
    screen.fill(config.COLOR_BG)

    # Show a test turn notification for player
    print("Showing player turn notification...")
    Popup.show_turn_notification(screen, "Arthur 'Bones' Blackwood", duration_ms=1000)

    # Fill screen again
    screen.fill(config.COLOR_BG)

    # Show a test turn notification for enemy
    print("Showing enemy turn notification...")
    Popup.show_turn_notification(screen, "Cultist Alpha", duration_ms=1000)

    print("[OK] Turn notification popups displayed successfully")


def test_damage_popup():
    """Test the damage notification popup (future feature)."""
    print("\n=== TEST: Damage Notification Popup ===")

    # Initialize Pygame
    pygame.init()

    # Create a test screen
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Popup Test - Damage")

    # Test different card types
    test_cases = [
        (8, "+2", "positive modifier"),
        (5, "+0", "neutral card"),
        (4, "-1", "negative modifier"),
        (16, "x2", "critical hit"),
        (0, "NULL", "auto-miss")
    ]

    for damage, card_name, description in test_cases:
        # Fill screen with dark background
        screen.fill(config.COLOR_BG)

        # Show damage notification with card value
        print(f"Showing {description}: {damage} damage with {card_name} card...")
        Popup.show_damage_notification(screen, damage=damage, card_name=card_name, duration_ms=800)

    print("[OK] All damage notification variants displayed successfully")


def test_custom_popup():
    """Test creating a custom popup."""
    print("\n=== TEST: Custom Popup ===")

    # Initialize Pygame
    pygame.init()

    # Create a test screen
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Popup Test - Custom")

    # Fill screen with dark background
    screen.fill(config.COLOR_BG)

    # Create a custom popup
    print("Showing custom popup...")
    popup = Popup(
        width=700,
        height=300,
        bg_color=(25, 15, 35),  # Purple tint
        border_color=(150, 100, 200),  # Purple border
        text_color=(200, 150, 255),  # Light purple text
        font_size=60,
        alpha=250
    )
    popup.set_content(title="VICTORY!", subtitle="All enemies defeated")
    popup.show_blocking(screen, duration_ms=1500)

    print("[OK] Custom popup displayed successfully")


if __name__ == "__main__":
    print("============================================================")
    print("POPUP TEST SUITE")
    print("============================================================")

    try:
        # Test turn notifications
        test_turn_popup()

        # Test damage notifications
        test_damage_popup()

        # Test custom popup
        test_custom_popup()

        print("\n============================================================")
        print("ALL TESTS PASSED!")
        print("============================================================")

    except Exception as e:
        print(f"\n[FAIL] Test failed with error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Clean up
        pygame.quit()
