"""
Settings Screen for Eldritch Tactics
Configuration menu for game settings

This module implements a settings screen where players can adjust:
- Display settings (fullscreen toggle)
- UI preferences (FPS counter)
- Audio controls (Phase 2+)
- Controls/keybindings (Phase 2+)

Key Concepts:
- Toggle buttons for on/off settings
- Live preview of settings changes
- Persistent settings (saved to config for future sessions)
"""

import pygame
from typing import Optional
import config
from ui.ui_elements import MenuButton, TextLabel, RadioButton, Separator, Dropdown


class SettingsScreen:
    """
    Settings screen for game configuration.

    Allows players to adjust game settings like fullscreen mode,
    FPS display, and other preferences.

    The screen follows the same pattern as TitleScreen:
    - Initialize UI elements in __init__
    - Run game loop in run()
    - Return navigation choice when done
    """

    def __init__(self, screen: pygame.Surface):
        """
        Initialize the settings screen and create all UI elements.

        Args:
            screen: The pygame display Surface (from main.py)
        """
        self.screen = screen
        self.running = True
        self.next_screen = None

        # Track current settings (these will be applied when user exits)
        self.fullscreen_enabled = config.FULLSCREEN
        self.show_fps = getattr(config, 'SHOW_FPS', False)
        self.visual_style = getattr(config, 'VISUAL_STYLE', 'emoji')

        # Resolution - find current resolution in available resolutions
        current_res = (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        try:
            self.resolution_index = config.AVAILABLE_RESOLUTIONS.index(current_res)
        except ValueError:
            self.resolution_index = 1  # Default to 1920x1080 if not found

        # Calculate screen center for positioning
        center_x = config.SCREEN_WIDTH // 2

        # ====================================================================
        # UI elements lists
        # ====================================================================
        self.radio_buttons = []  # All radio buttons
        self.labels = []         # All labels
        self.separators = []     # Visual separators
        self.dropdowns = []      # Dropdown menus

        # Layout constants
        separator_width = 1520
        separator_x = (config.SCREEN_WIDTH - separator_width) // 2
        left_margin = 200

        # ====================================================================
        # TITLE
        # ====================================================================
        self.title = TextLabel(
            center_x,
            80,
            "SETTINGS",
            config.FONT_SIZE_TITLE,
            config.COLOR_TEXT_HIGHLIGHT,
            center=True
        )

        # Title separator
        title_separator = Separator(
            separator_x,
            160,
            separator_width,
            thickness=3,
            color=config.COLOR_TEXT_HIGHLIGHT
        )
        self.separators.append(title_separator)

        # ====================================================================
        # DISPLAY OPTIONS SECTION
        # ====================================================================
        section_y = 220

        # Section header
        display_header = TextLabel(
            left_margin,
            section_y,
            "DISPLAY OPTIONS",
            config.FONT_SIZE_LARGE,
            config.COLOR_TEXT_HIGHLIGHT,
            center=False
        )
        self.labels.append(display_header)

        # --- Resolution Dropdown ---
        resolution_y = section_y + 70

        resolution_label = TextLabel(
            left_margin,
            resolution_y,
            "Resolution:",
            config.FONT_SIZE_MEDIUM,
            config.COLOR_TEXT,
            center=False
        )
        self.labels.append(resolution_label)

        # Create resolution options for dropdown
        resolution_options = [
            (f"{w}x{h} ({self._get_resolution_name(w, h)})", (w, h))
            for w, h in config.AVAILABLE_RESOLUTIONS
        ]

        self.resolution_dropdown = Dropdown(
            left_margin,
            resolution_y + 45,
            450,
            resolution_options,
            selected_index=self.resolution_index,
            on_select=self._set_resolution
        )
        self.dropdowns.append(self.resolution_dropdown)

        # --- Fullscreen Setting ---
        fullscreen_y = resolution_y + 150

        fullscreen_label = TextLabel(
            left_margin,
            fullscreen_y,
            "Fullscreen Mode:",
            config.FONT_SIZE_MEDIUM,
            config.COLOR_TEXT,
            center=False
        )
        self.labels.append(fullscreen_label)

        self.fullscreen_group = []
        radio_y = fullscreen_y + 45

        fullscreen_on = RadioButton(
            left_margin,
            radio_y,
            "ON",
            True,
            self.fullscreen_group,
            selected=self.fullscreen_enabled,
            on_select=self._set_fullscreen
        )
        self.radio_buttons.append(fullscreen_on)

        fullscreen_off = RadioButton(
            left_margin + 150,
            radio_y,
            "OFF",
            False,
            self.fullscreen_group,
            selected=not self.fullscreen_enabled,
            on_select=self._set_fullscreen
        )
        self.radio_buttons.append(fullscreen_off)

        # --- FPS Display Setting ---
        fps_y = fullscreen_y + 120

        fps_label = TextLabel(
            left_margin,
            fps_y,
            "Show FPS Counter:",
            config.FONT_SIZE_MEDIUM,
            config.COLOR_TEXT,
            center=False
        )
        self.labels.append(fps_label)

        self.fps_group = []
        fps_radio_y = fps_y + 45

        fps_on = RadioButton(
            left_margin,
            fps_radio_y,
            "ON",
            True,
            self.fps_group,
            selected=self.show_fps,
            on_select=self._set_fps
        )
        self.radio_buttons.append(fps_on)

        fps_off = RadioButton(
            left_margin + 150,
            fps_radio_y,
            "OFF",
            False,
            self.fps_group,
            selected=not self.show_fps,
            on_select=self._set_fps
        )
        self.radio_buttons.append(fps_off)

        # ====================================================================
        # SECTION SEPARATOR - Between Display and Visual Style
        # ====================================================================
        section_separator = Separator(
            separator_x,
            fps_y + 100,
            separator_width,
            thickness=2,
            color=config.COLOR_MENU_BORDER
        )
        self.separators.append(section_separator)

        # ====================================================================
        # VISUAL STYLE SECTION
        # ====================================================================
        visual_section_y = fps_y + 140

        # Section header
        visual_header = TextLabel(
            left_margin,
            visual_section_y,
            "VISUAL STYLE",
            config.FONT_SIZE_LARGE,
            config.COLOR_TEXT_HIGHLIGHT,
            center=False
        )
        self.labels.append(visual_header)

        # --- Visual Style Setting ---
        visual_y = visual_section_y + 70

        visual_label = TextLabel(
            left_margin,
            visual_y,
            "Unit & Terrain Display:",
            config.FONT_SIZE_MEDIUM,
            config.COLOR_TEXT,
            center=False
        )
        self.labels.append(visual_label)

        self.visual_group = []
        visual_radio_y = visual_y + 45

        # ASCII option
        visual_ascii = RadioButton(
            left_margin,
            visual_radio_y,
            "ASCII Text",
            "ascii",
            self.visual_group,
            selected=self.visual_style == "ascii",
            on_select=self._set_visual_style
        )
        self.radio_buttons.append(visual_ascii)

        # Emoji option
        visual_emoji = RadioButton(
            left_margin + 250,
            visual_radio_y,
            "Emoji",
            "emoji",
            self.visual_group,
            selected=self.visual_style == "emoji",
            on_select=self._set_visual_style
        )
        self.radio_buttons.append(visual_emoji)

        # Image option (not yet implemented)
        visual_image = RadioButton(
            left_margin + 500,
            visual_radio_y,
            "Images (Coming Soon)",
            "image",
            self.visual_group,
            selected=self.visual_style == "image",
            on_select=self._set_visual_style
        )
        self.radio_buttons.append(visual_image)

        # ====================================================================
        # BOTTOM SEPARATOR - Before back button
        # ====================================================================
        bottom_separator = Separator(
            separator_x,
            config.SCREEN_HEIGHT - 280,
            separator_width,
            thickness=2,
            color=config.COLOR_MENU_BORDER
        )
        self.separators.append(bottom_separator)

        # ====================================================================
        # BACK BUTTON
        # ====================================================================
        self.buttons = []  # Keep for back button only

        back_button = MenuButton(
            center_x - (config.MENU_BUTTON_WIDTH // 2),
            config.SCREEN_HEIGHT - 200,
            "Back to Main Menu",
            on_click=self._on_back
        )
        self.buttons.append(back_button)

        # ====================================================================
        # Info text at bottom
        # ====================================================================
        self.info_label = TextLabel(
            center_x,
            config.SCREEN_HEIGHT - 100,
            "Settings are saved when you return to the main menu • Resolution changes require restart",
            config.FONT_SIZE_TINY,
            config.COLOR_TEXT_DIM,
            center=True
        )

    def _get_resolution_name(self, width: int, height: int) -> str:
        """Get a friendly name for a resolution."""
        if height == 720:
            return "HD"
        elif height == 1080:
            return "Full HD"
        elif height == 1440:
            return "2K"
        else:
            return ""

    # ========================================================================
    # Callback methods for settings changes
    # ========================================================================

    def _set_resolution(self, value: tuple) -> None:
        """
        Set resolution based on dropdown selection.

        Args:
            value: Tuple of (width, height)

        Note: Resolution changes require restarting the game.
        """
        width, height = value
        self.resolution_index = config.AVAILABLE_RESOLUTIONS.index(value)
        print(f"Resolution set to: {width}x{height}")
        print("NOTE: Resolution changes will apply on next game launch")

    def _set_fullscreen(self, value: bool) -> None:
        """
        Set fullscreen setting based on radio button selection.

        Args:
            value: True for fullscreen ON, False for fullscreen OFF

        Note: Fullscreen changes require restarting the game.
        """
        self.fullscreen_enabled = value
        print(f"Fullscreen set to: {'ON' if value else 'OFF'}")
        if value != config.FULLSCREEN:
            print("NOTE: Fullscreen changes will apply on next game launch")

    def _set_fps(self, value: bool) -> None:
        """
        Set FPS counter display based on radio button selection.

        Args:
            value: True for FPS display ON, False for FPS display OFF

        This setting can be applied immediately for new screens.
        """
        self.show_fps = value
        print(f"FPS display set to: {'ON' if value else 'OFF'}")

    def _set_visual_style(self, value: str) -> None:
        """
        Set visual style based on radio button selection.

        Args:
            value: Visual style - "ascii", "emoji", or "image"

        Note: Visual style changes will apply to new battles.
        """
        self.visual_style = value
        print(f"Visual style set to: {value}")
        if value == "image":
            print("NOTE: Image sprites are not yet implemented. Using emoji for now.")

    def _on_back(self) -> None:
        """
        Return to main menu.

        Saves settings to config before exiting.
        """
        # Save settings to config module
        # This makes them available for other screens
        selected_res = config.AVAILABLE_RESOLUTIONS[self.resolution_index]
        config.SCREEN_WIDTH, config.SCREEN_HEIGHT = selected_res
        config.FULLSCREEN = self.fullscreen_enabled
        config.SHOW_FPS = self.show_fps
        config.VISUAL_STYLE = self.visual_style

        print("Settings saved to config")
        print(f"  Resolution: {config.SCREEN_WIDTH}x{config.SCREEN_HEIGHT}")
        print(f"  Fullscreen: {config.FULLSCREEN}")
        print(f"  Show FPS: {config.SHOW_FPS}")
        print(f"  Visual Style: {config.VISUAL_STYLE}")

        self.running = False
        self.next_screen = "title"

    # ========================================================================
    # Game loop methods
    # ========================================================================

    def handle_events(self) -> None:
        """
        Process input events.

        CALLED EVERY FRAME (60 times per second)

        Handles:
        - Window close (X button)
        - ESC key to go back
        - Forward events to all buttons and radio buttons
        """
        for event in pygame.event.get():
            # Window close
            if event.type == pygame.QUIT:
                self._on_back()  # Save settings before exit

            # Keyboard shortcuts
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # ESC returns to main menu
                    self._on_back()

            # Forward event to all dropdowns
            for dropdown in self.dropdowns:
                dropdown.handle_event(event)

            # Forward event to all radio buttons
            for radio in self.radio_buttons:
                radio.handle_event(event)

            # Forward event to all buttons (back button)
            for button in self.buttons:
                button.handle_event(event)

    def update(self) -> None:
        """
        Update settings screen state.

        CALLED EVERY FRAME (60 times per second)

        Updates button and radio button hover states based on mouse position.
        """
        mouse_pos = pygame.mouse.get_pos()

        # Update dropdowns
        for dropdown in self.dropdowns:
            dropdown.update(mouse_pos)

        # Update radio buttons
        for radio in self.radio_buttons:
            radio.update(mouse_pos)

        # Update regular buttons
        for button in self.buttons:
            button.update(mouse_pos)

    def draw(self) -> None:
        """
        Render the settings screen.

        CALLED EVERY FRAME (60 times per second)

        Drawing layers:
        1. Background fill
        2. Title
        3. Setting labels
        4. Radio buttons
        5. Back button
        6. Info text
        """
        # Layer 1: Clear screen
        self.screen.fill(config.COLOR_BG)

        # Layer 2: Draw title
        self.title.draw(self.screen)

        # Layer 2.5: Draw separators
        for separator in self.separators:
            separator.draw(self.screen)

        # Layer 3: Draw all labels
        for label in self.labels:
            label.draw(self.screen)

        # Layer 4: Draw all dropdowns
        for dropdown in self.dropdowns:
            dropdown.draw(self.screen)

        # Layer 5: Draw all radio buttons
        for radio in self.radio_buttons:
            radio.draw(self.screen)

        # Layer 6: Draw buttons (back button)
        for button in self.buttons:
            button.draw(self.screen)

        # Layer 7: Draw info text
        self.info_label.draw(self.screen)

    def run(self, clock: pygame.time.Clock) -> Optional[str]:
        """
        Main loop for the settings screen.

        Standard game loop:
        1. Handle events
        2. Update state
        3. Draw
        4. Display
        5. Tick for FPS control

        Args:
            clock: Pygame clock for FPS control

        Returns:
            Next screen to navigate to ("title" when done)
        """
        while self.running:
            # 1. Handle Events
            self.handle_events()

            # 2. Update
            self.update()

            # 3. Draw
            self.draw()

            # 4. Display (flip buffers)
            pygame.display.flip()

            # 5. Tick (maintain FPS)
            clock.tick(config.FPS)

        # Return navigation choice
        return self.next_screen
