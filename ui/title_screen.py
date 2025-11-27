"""
Title Screen for Eldritch Tactics
Main menu with New Game, Continue, Settings, and Exit options

This module demonstrates a COMPLETE GAME SCREEN implementation:
- Creating and positioning UI elements
- Running its own game loop (handle events → update → draw → display)
- Returning control to main.py when user makes a choice

Key Concepts:
- Composition: TitleScreen contains multiple Buttons and TextLabels
- Game Loop Pattern: The run() method implements the standard game loop
- Event Forwarding: Events are passed from this screen to each button
- State Management: Tracks running state and user's menu choice
"""

import pygame
import sys
from typing import Optional
import config
from ui.ui_elements import MenuButton, TextLabel


class TitleScreen:
    """
    Main title screen with menu options

    This class is responsible for:
    1. Creating all UI elements (title, buttons, labels)
    2. Positioning them on screen (with calculated centers)
    3. Running the game loop until user makes a choice
    4. Returning the user's choice to main.py
    """

    def __init__(self, screen: pygame.Surface):
        """
        Initialize the title screen and create all UI elements

        This constructor sets up everything needed for the menu:
        - Calculates screen center for positioning
        - Creates title and subtitle labels
        - Creates 4 menu buttons (New Game, Continue, Settings, Exit)
        - Stores buttons in a list for easy iteration

        Args:
            screen: The pygame display Surface (created in main.py)
        """
        self.screen = screen
        self.running = True      # Controls the game loop (set to False to exit)
        self.next_screen = None  # Stores user's choice ("new_game", "settings", etc.)

        # ====================================================================
        # Calculate screen center positions for symmetric layout
        # ====================================================================
        # Using // (integer division) ensures we get whole pixel values
        center_x = config.SCREEN_WIDTH // 2   # 1920 // 2 = 960 pixels
        center_y = config.SCREEN_HEIGHT // 2  # 1080 // 2 = 540 pixels

        # ====================================================================
        # Create title text (large golden text at top-center)
        # ====================================================================
        self.title = TextLabel(
            center_x,                       # Horizontal center
            center_y - 300,                 # 300 pixels above vertical center
            "ELDRITCH TACTICS",
            config.FONT_SIZE_TITLE,         # 120pt font
            config.COLOR_TEXT_HIGHLIGHT,    # Golden color
            center=True                     # Use (x,y) as center, not top-left
        )

        # ====================================================================
        # Create subtitle text (smaller, dimmed text below title)
        # ====================================================================
        self.subtitle = TextLabel(
            center_x,
            center_y - 200,                 # 200 pixels above center
            "A Lovecraftian Turn-Based Tactical Game",
            config.FONT_SIZE_SMALL,
            config.COLOR_TEXT_DIM,          # Dimmed for less emphasis
            center=True
        )

        # ====================================================================
        # Calculate button positions
        # ====================================================================
        # To center a button horizontally, we need to offset by half its width:
        # Button starts at: center_x - (button_width / 2)
        button_x = center_x - (config.MENU_BUTTON_WIDTH // 2)

        # First button slightly above vertical center
        first_button_y = center_y - 50

        # ====================================================================
        # Check if a save file exists (determines if Continue is enabled)
        # ====================================================================
        has_save_file = False  # TODO: Implement save file detection in Phase 2

        # ====================================================================
        # Create all menu buttons
        # ====================================================================
        # Using a list allows us to easily loop through all buttons
        # for updating and drawing
        self.buttons = []

        # ---- New Game Button ----
        new_game_btn = MenuButton(
            button_x,
            first_button_y,
            "New Game",
            on_click=self.on_new_game  # Callback: run this when clicked
        )
        self.buttons.append(new_game_btn)

        # ---- Continue Button ----
        # Y position calculation: first_button_y + (button_height + spacing)
        # = first_button_y + (80 + 30) = first_button_y + 110 pixels
        continue_btn = MenuButton(
            button_x,
            first_button_y + (config.MENU_BUTTON_HEIGHT + config.MENU_BUTTON_SPACING),
            "Continue",
            on_click=self.on_continue,
            enabled=has_save_file  # Disabled if no save file exists
        )
        self.buttons.append(continue_btn)

        # ---- Settings Button ----
        # Y position: Skip 2 buttons = multiply by 2
        settings_btn = MenuButton(
            button_x,
            first_button_y + 2 * (config.MENU_BUTTON_HEIGHT + config.MENU_BUTTON_SPACING),
            "Settings",
            on_click=self.on_settings
        )
        self.buttons.append(settings_btn)

        # ---- Exit Button ----
        # Y position: Skip 3 buttons = multiply by 3
        exit_btn = MenuButton(
            button_x,
            first_button_y + 3 * (config.MENU_BUTTON_HEIGHT + config.MENU_BUTTON_SPACING),
            "Exit",
            on_click=self.on_exit
        )
        self.buttons.append(exit_btn)

        # ====================================================================
        # Create atmospheric text elements
        # ====================================================================
        # Version label (bottom-right corner)
        self.version_label = TextLabel(
            config.SCREEN_WIDTH - 20,
            config.SCREEN_HEIGHT - 40,
            "v0.1.0 - MVP Phase 1",
            config.FONT_SIZE_TINY,
            config.COLOR_TEXT_DIM,
            center=False  # Use top-left positioning
        )

        # Flavor text (bottom center) - adds atmosphere
        self.flavor_text = TextLabel(
            center_x,
            config.SCREEN_HEIGHT - 100,
            "The stars are right. The horrors awaken. Humanity's last defenders stand ready.",
            config.FONT_SIZE_SMALL,
            config.COLOR_TEXT_DIM,
            center=True
        )

    # ========================================================================
    # CALLBACK METHODS - Called when buttons are clicked
    # ========================================================================
    # These methods are passed to buttons as on_click parameters.
    # When a button detects a click, it calls its on_click function.
    #
    # Each callback:
    # 1. Prints a message (for debugging)
    # 2. Sets self.next_screen to indicate user's choice
    # 3. Sets self.running = False to exit the game loop

    def on_new_game(self) -> None:
        """Handle New Game button click"""
        print("New Game selected")
        self.next_screen = "new_game"
        self.running = False  # Exit the title screen loop

    def on_continue(self) -> None:
        """Handle Continue button click"""
        print("Continue selected")
        self.next_screen = "continue"
        self.running = False

    def on_settings(self) -> None:
        """Handle Settings button click"""
        print("Settings selected")
        self.next_screen = "settings"
        self.running = False

    def on_exit(self) -> None:
        """Handle Exit button click"""
        print("Exiting game...")
        self.running = False
        self.next_screen = "exit"

    # ========================================================================
    # GAME LOOP METHODS - Called every frame
    # ========================================================================

    def handle_events(self) -> None:
        """
        Process input events

        CALLED EVERY FRAME (60 times per second)

        This method:
        1. Gets ALL events from pygame's event queue
        2. Checks for special events (window close, keyboard shortcuts)
        3. Forwards events to all buttons so they can check for clicks

        Event Queue Explanation:
        - Pygame collects all user inputs (clicks, keys, window events)
        - pygame.event.get() retrieves and clears the queue
        - We must call this every frame, or the queue fills up and freezes
        """
        for event in pygame.event.get():
            # ---- Window Close Event ----
            # User clicked the X button or Alt+F4
            if event.type == pygame.QUIT:
                self.on_exit()

            # ---- Keyboard Shortcuts ----
            if event.type == pygame.KEYDOWN:  # Key was just pressed (not held)
                if event.key == pygame.K_ESCAPE:
                    # ESC key exits the game
                    self.on_exit()
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    # Enter or Space starts a new game (quick start)
                    self.on_new_game()

            # ---- Forward Event to All Buttons ----
            # Each button checks if it was clicked
            # This is why using a list is convenient - we can loop through all buttons
            for button in self.buttons:
                button.handle_event(event)

    def update(self) -> None:
        """
        Update menu state

        CALLED EVERY FRAME (60 times per second)

        This method updates the hover state of all buttons.
        We get the current mouse position and pass it to each button
        so they can check if they're being hovered over.
        """
        mouse_pos = pygame.mouse.get_pos()  # Returns (x, y) tuple
        for button in self.buttons:
            button.update(mouse_pos)

    def draw(self) -> None:
        """
        Render the title screen

        CALLED EVERY FRAME (60 times per second)

        Drawing order matters! Things drawn later appear on top.

        Our rendering layers:
        1. Background fill (clears previous frame)
        2. Title and subtitle
        3. All buttons
        4. Flavor text and version label

        Note: We draw to a hidden buffer. pygame.display.flip()
        (called in run()) swaps the buffer to the visible screen.
        """
        # ---- Layer 1: Clear screen with background color ----
        # This erases the previous frame so we don't get ghosting/trails
        self.screen.fill(config.COLOR_BG)

        # ---- Layer 2: Draw title and subtitle ----
        self.title.draw(self.screen)
        self.subtitle.draw(self.screen)

        # ---- Layer 3: Draw all buttons ----
        for button in self.buttons:
            button.draw(self.screen)

        # ---- Layer 4: Draw flavor text ----
        self.flavor_text.draw(self.screen)

        # ---- Layer 5: Draw version label (bottom-right corner) ----
        # We manually position this one for precise alignment
        font = pygame.font.Font(None, config.FONT_SIZE_TINY)
        version_surface = font.render(
            self.version_label.text,
            True,
            self.version_label.color
        )
        # bottomright= positions the bottom-right corner of the text
        version_rect = version_surface.get_rect(
            bottomright=(config.SCREEN_WIDTH - 20, config.SCREEN_HEIGHT - 20)
        )
        self.screen.blit(version_surface, version_rect)

    def run(self, clock: pygame.time.Clock) -> Optional[str]:
        """
        Main loop for the title screen

        This is the GAME LOOP for the title screen. It runs continuously
        until the user makes a choice (clicks a button or presses a key).

        Game Loop Pattern (standard for all Pygame games):
        1. Handle Events - Process user input
        2. Update - Update game state based on input/time
        3. Draw - Render everything to the screen
        4. Display - Show what we drew (flip buffers)
        5. Tick - Wait to maintain consistent framerate

        Args:
            clock: pygame.time.Clock object for FPS control

        Returns:
            The user's choice as a string:
            - "new_game" if New Game was clicked
            - "continue" if Continue was clicked
            - "settings" if Settings was clicked
            - "exit" if Exit was clicked or window closed
            - None shouldn't happen, but type system allows it
        """
        while self.running:
            # ---- 1. Handle Events ----
            self.handle_events()  # Process keyboard and mouse input

            # ---- 2. Update ----
            self.update()  # Update button hover states

            # ---- 3. Draw ----
            self.draw()  # Render everything to hidden buffer

            # ---- 4. Display ----
            # Swap the hidden buffer to the visible screen
            # This is "double buffering" - prevents flickering
            pygame.display.flip()

            # ---- 5. Tick ----
            # Pause to maintain 60 FPS
            # If we drew the frame in 10ms, this waits ~6.67ms
            # to reach the target 16.67ms per frame (1000ms / 60fps)
            clock.tick(config.FPS)

        # ========================================================================
        # Loop has exited (self.running was set to False by a callback)
        # Return the user's choice to main.py
        # ========================================================================
        return self.next_screen
