"""
Eldritch Tactics - Main Entry Point
Lovecraftian Turn-Based Tactical Game

This is the ORCHESTRATOR - the first file that runs when the game starts.

Responsibilities:
1. Initialize Pygame and create the game window
2. Create the master clock for FPS control
3. Show the title screen and wait for user's choice
4. Navigate to the appropriate screen based on user's choice
5. Clean up and exit when done

This file demonstrates:
- Pygame initialization sequence
- Screen/display management (fullscreen)
- Navigation between different game screens
- Proper cleanup on exit
"""

import pygame
import sys
import config
from ui.title_screen import TitleScreen
from ui.settings_screen import SettingsScreen
from combat.battle_screen import BattleScreen


def main():
    """
    Main game entry point

    This function is called when the user runs: uv run python main.py

    Flow:
    1. Initialize Pygame
    2. Create fullscreen window (1920x1080)
    3. Create clock for framerate control
    4. Show title screen
    5. Handle user's menu choice
    6. Clean up and exit

    The function exits after the title screen - in future phases,
    this will loop through different screens (battle, campaign, etc.)
    """

    # ========================================================================
    # STEP 1: Initialize Pygame
    # ========================================================================
    # This MUST be called before using any Pygame features!
    # It initializes all Pygame subsystems:
    # - Display system (for creating windows and drawing)
    # - Font system (for rendering text)
    # - Event system (for handling mouse/keyboard input)
    # - Sound system (even though we don't use it yet)
    pygame.init()

    # ========================================================================
    # STEP 2: Create the game window (display Surface)
    # ========================================================================
    # pygame.display.set_mode() creates the window and returns a Surface
    # Surface = drawable area in Pygame (like a canvas)
    #
    # Fullscreen vs Windowed Mode:
    # - FULLSCREEN flag: True fullscreen, covers entire screen
    # - Without flag: Windowed mode with title bar and borders
    if config.FULLSCREEN:
        screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT),  # Resolution: (1920, 1080)
            pygame.FULLSCREEN  # Fullscreen flag
        )
    else:
        # Windowed mode (for testing/development)
        screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )

    # Set the window title (shown in taskbar and title bar if windowed)
    pygame.display.set_caption("Eldritch Tactics")

    # ========================================================================
    # STEP 3: Create master clock for FPS control
    # ========================================================================
    # pygame.time.Clock manages framerate timing
    # We create ONE clock for the entire game and pass it to each screen
    #
    # clock.tick(60) in each game loop ensures consistent 60 FPS:
    # - If frame took 10ms, it waits ~6.67ms to reach 16.67ms (1000ms/60fps)
    # - If frame took 20ms, it doesn't wait (running slower than target)
    clock = pygame.time.Clock()

    # ========================================================================
    # STEP 4: Main game loop - navigate between screens
    # ========================================================================
    # Start at title screen
    next_screen = "title"

    # Keep running until user chooses to exit
    game_running = True

    # ========================================================================
    # STEP 5: Main navigation loop - handle screen transitions
    # ========================================================================
    # Navigation loop allows moving between different screens
    # (title → settings → title, title → battle → title, etc.)
    #
    # Each screen's run() method returns the next screen to show:
    # - "title" = Go back to main menu
    # - "new_game" = Start a battle
    # - "settings" = Open settings menu
    # - "exit" or "quit" = Exit the game

    while game_running:
        if next_screen == "title":
            # Show title screen
            title_screen = TitleScreen(screen)
            next_screen = title_screen.run(clock)

        elif next_screen == "new_game":
            print("Starting new game...")
            # Launch tactical battle (Phase 1 MVP)
            battle = BattleScreen(screen)
            battle_result = battle.run(clock)

            # Handle battle result
            if battle_result == "victory":
                print("VICTORY! Returning to title screen...")
                next_screen = "title"
            elif battle_result == "defeat":
                print("DEFEAT! Returning to title screen...")
                next_screen = "title"
            elif battle_result == "title":
                # User pressed ESC during battle
                next_screen = "title"
            else:
                # Fallback to title
                next_screen = "title"

        elif next_screen == "continue":
            print("Loading saved game...")
            # TODO: Load saved game (Phase 2)
            # save_data = load_save_file()
            # campaign = CampaignScreen(screen, save_data)
            # next_screen = campaign.run(clock)
            print("Save/load system not yet implemented")
            # For now, return to title
            next_screen = "title"

        elif next_screen == "settings":
            print("Opening settings...")
            # Launch settings screen
            settings = SettingsScreen(screen)
            next_screen = settings.run(clock)
            # Settings screen returns "title" when done

        elif next_screen == "exit" or next_screen == "quit":
            # User chose to exit
            print("Thank you for playing Eldritch Tactics!")
            game_running = False

        else:
            # Unknown screen - fallback to title
            print(f"Unknown screen: {next_screen}, returning to title")
            next_screen = "title"

    # ========================================================================
    # STEP 6: Clean up and exit
    # ========================================================================
    # pygame.quit() shuts down all Pygame subsystems cleanly
    # This releases resources (window handle, graphics context, etc.)
    pygame.quit()

    # sys.exit(0) terminates the Python program
    # Exit code 0 = successful termination (no errors)
    # Non-zero codes indicate errors (1, 2, etc.)
    sys.exit(0)


# ============================================================================
# Python Entry Point Check
# ============================================================================
# This is a Python idiom that checks if this file is being run directly
# vs being imported as a module.
#
# __name__ is a special Python variable:
# - When file is run directly: __name__ == "__main__"
# - When file is imported: __name__ == "main" (the module name)
#
# This allows the file to be both:
# 1. Runnable as a script: python main.py
# 2. Importable as a module: from main import some_function
if __name__ == "__main__":
    main()  # Run the game!
