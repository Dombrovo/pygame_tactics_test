"""
UI Elements for Eldritch Tactics
Buttons, panels, and interactive components

This module provides REUSABLE UI COMPONENTS that can be used throughout the game.
Instead of recreating button logic in every screen, we define it once here.

Key Concepts Demonstrated:
- Object-Oriented Design: Encapsulation of UI logic
- Callback Pattern: Functions passed as parameters to customize behavior
- Inheritance: MenuButton extends Button to add new features
- Game Loop Integration: update() and draw() methods called every frame
"""

import pygame
from typing import Callable, Optional, Tuple
import config


class Button:
    """
    Base button class with hover and click detection

    This is a SELF-CONTAINED interactive button that manages its own:
    - Visual appearance (colors, text, borders)
    - State (hovered, pressed)
    - Event handling (mouse clicks)
    - Callback execution (runs a function when clicked)

    The button integrates with Pygame's game loop:
    - update() is called every frame to check hover state
    - handle_event() is called for each input event
    - draw() is called every frame to render the button
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        font_size: int = config.FONT_SIZE_MEDIUM,
        on_click: Optional[Callable] = None
    ):
        """
        Initialize a button

        Args:
            x, y: Top-left corner position in pixels
            width, height: Button dimensions in pixels
            text: Text displayed on the button
            font_size: Size of the button text (from config.py)
            on_click: CALLBACK FUNCTION - runs when button is clicked
                     Example: on_click=self.start_game
                     The function is NOT called here (no parentheses!)
        """
        # pygame.Rect provides built-in collision detection (collidepoint method)
        # and easy positioning/centering
        self.rect = pygame.Rect(x, y, width, height)

        self.text = text
        self.font_size = font_size
        self.on_click = on_click  # Store the callback function to call later

        # State flags (updated every frame)
        self.is_hovered = False  # Is mouse currently over this button?
        self.is_pressed = False  # Is button currently being clicked?

        # Colors for different button states (creates visual feedback)
        self.color_normal = config.COLOR_MENU_BUTTON        # Default appearance
        self.color_hover = config.COLOR_MENU_BUTTON_HOVER   # Mouse over button
        self.color_active = config.COLOR_MENU_BUTTON_ACTIVE # Button being pressed
        self.color_border = config.COLOR_MENU_BORDER
        self.color_text = config.COLOR_TEXT
        self.color_text_hover = config.COLOR_TEXT_HIGHLIGHT # Golden text when hovered

    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """
        Update button state based on mouse position

        CALLED EVERY FRAME (60 times per second) by the game loop

        Args:
            mouse_pos: Current (x, y) mouse coordinates from pygame.mouse.get_pos()

        This method checks if the mouse is inside the button's rectangle.
        rect.collidepoint() is a Pygame built-in that returns True if the
        point (mouse position) is inside the rectangle.
        """
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle mouse events for the button

        CALLED FOR EACH INPUT EVENT from pygame.event.get()

        This implements the FULL CLICK CYCLE:
        1. User presses mouse button down (MOUSEBUTTONDOWN)
        2. User releases mouse button (MOUSEBUTTONUP)
        3. Only counts as a click if both happened over the button

        This two-step approach allows users to change their mind:
        - Press down on button
        - Drag mouse away
        - Release mouse
        - Does NOT count as a click!

        Args:
            event: Pygame event object (contains type, button number, etc.)

        Returns:
            True if button was successfully clicked, False otherwise
        """
        # STEP 1: Detect mouse button press
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # event.button: 1 = left click, 2 = middle click, 3 = right click
            if self.is_hovered:
                self.is_pressed = True  # Mark button as being pressed
                return False  # Not a complete click yet

        # STEP 2: Detect mouse button release
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # Only count as a click if:
            # 1. Mouse is still over the button (didn't drag away)
            # 2. Button was previously pressed down
            if self.is_hovered and self.is_pressed:
                self.is_pressed = False

                # EXECUTE THE CALLBACK if one was provided
                if self.on_click:
                    self.on_click()  # Call the function!

                return True  # Signal that a complete click occurred

            # Reset pressed state even if click was invalid
            self.is_pressed = False

        return False  # No click occurred

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the button to the screen

        CALLED EVERY FRAME (60 times per second) by the game loop

        Drawing order matters! Later draws appear on top of earlier draws.
        We draw in layers:
        1. Filled background rectangle (button color)
        2. Border outline (slightly thicker when hovered)
        3. Text centered on the button

        Args:
            screen: The pygame Surface to draw on (usually the main screen)
        """
        # LAYER 1: Determine background color based on current state
        if self.is_pressed:
            bg_color = self.color_active      # Brightest when pressed
        elif self.is_hovered:
            bg_color = self.color_hover       # Lighter when hovered
        else:
            bg_color = self.color_normal      # Normal when idle

        # Draw filled rectangle (the button background)
        pygame.draw.rect(screen, bg_color, self.rect)

        # LAYER 2: Draw border (outline only, no fill)
        # The last parameter is border width (thicker when hovered for emphasis)
        border_width = 3 if self.is_hovered else 2
        pygame.draw.rect(screen, self.color_border, self.rect, border_width)

        # LAYER 3: Render and draw text
        # font.render() converts text string into a Surface (image)
        font = pygame.font.Font(None, self.font_size)  # None = default font
        text_color = self.color_text_hover if self.is_hovered else self.color_text
        text_surface = font.render(self.text, True, text_color)

        # Center the text on the button
        # get_rect() gets the text's bounding rectangle
        # center= positions it at the button's center point
        text_rect = text_surface.get_rect(center=self.rect.center)

        # blit() = "Block Image Transfer" - draws one surface onto another
        screen.blit(text_surface, text_rect)


class MenuButton(Button):
    """
    Specialized button for menu screens with enhanced styling

    DEMONSTRATES INHERITANCE:
    - MenuButton IS-A Button (has all Button features)
    - Adds new feature: enabled/disabled state
    - Overrides methods to check enabled state

    Use this for menu screens where some options might be unavailable
    (e.g., "Continue" button when there's no save file).
    """

    def __init__(
        self,
        x: int,
        y: int,
        text: str,
        on_click: Optional[Callable] = None,
        width: int = config.MENU_BUTTON_WIDTH,
        height: int = config.MENU_BUTTON_HEIGHT,
        enabled: bool = True
    ):
        """
        Initialize a menu button

        Note the parameter order is different from Button (simplified for menus).
        Width and height have DEFAULT VALUES from config, so you don't need
        to specify them every time.

        Args:
            x, y: Top-left corner position
            text: Button label
            on_click: Callback function to run when clicked
            width: Button width (defaults to config value)
            height: Button height (defaults to config value)
            enabled: Whether button can be clicked
        """
        # Call the parent class (Button) constructor using super()
        # This sets up all the basic button functionality
        super().__init__(x, y, width, height, text, config.FONT_SIZE_MEDIUM, on_click)

        # Add MenuButton-specific feature: enabled state
        self.enabled = enabled

        # Colors for disabled state (grayed out)
        self.color_disabled = (30, 30, 40)      # Very dark gray
        self.color_text_disabled = (80, 80, 90) # Dim text

    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """
        Update only if button is enabled

        OVERRIDES Button.update() to add enabled check
        If disabled, button can't be hovered
        """
        if self.enabled:
            super().update(mouse_pos)  # Call Button's update method
        else:
            self.is_hovered = False  # Disabled buttons never show hover

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle events only if button is enabled

        OVERRIDES Button.handle_event() to add enabled check
        If disabled, clicks are completely ignored
        """
        if self.enabled:
            return super().handle_event(event)  # Call Button's handle_event
        return False  # Disabled buttons don't respond to clicks

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw with disabled state if not enabled

        OVERRIDES Button.draw() to add disabled appearance
        Disabled buttons are grayed out with dimmed text
        """
        if not self.enabled:
            # Draw disabled appearance (no hover effects, dim colors)
            pygame.draw.rect(screen, self.color_disabled, self.rect)
            pygame.draw.rect(screen, self.color_border, self.rect, 1)

            font = pygame.font.Font(None, self.font_size)
            text_surface = font.render(self.text, True, self.color_text_disabled)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)
        else:
            # Enabled: use normal Button drawing logic
            super().draw(screen)


class TextLabel:
    """
    Simple text label for displaying information

    Unlike Button, this is NOT interactive. It just displays text.
    Useful for titles, subtitles, instructions, version numbers, etc.
    """

    def __init__(
        self,
        x: int,
        y: int,
        text: str,
        font_size: int = config.FONT_SIZE_MEDIUM,
        color: Tuple[int, int, int] = config.COLOR_TEXT,
        center: bool = False
    ):
        """
        Initialize a text label

        Args:
            x, y: Position (either top-left or center based on 'center' flag)
            text: The text to display
            font_size: Size of the text
            color: RGB color tuple
            center: If True, (x,y) is the center; if False, (x,y) is top-left
        """
        self.x = x
        self.y = y
        self.text = text
        self.font_size = font_size
        self.color = color
        self.center = center

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the text label

        CALLED EVERY FRAME by the game loop
        """
        font = pygame.font.Font(None, self.font_size)
        text_surface = font.render(self.text, True, self.color)

        # Position based on alignment mode
        if self.center:
            # (x, y) represents the center of the text
            text_rect = text_surface.get_rect(center=(self.x, self.y))
        else:
            # (x, y) represents the top-left corner
            text_rect = text_surface.get_rect(topleft=(self.x, self.y))

        screen.blit(text_surface, text_rect)

    def update_text(self, new_text: str) -> None:
        """
        Update the label text

        Useful for dynamic labels (e.g., health counters, score displays)
        """
        self.text = new_text


class RadioButton:
    """
    Radio button for selecting one option from a group.

    Radio buttons work in groups where only one can be selected at a time.
    When you click a radio button, it selects that one and deselects others
    in the same group.
    """

    def __init__(
        self,
        x: int,
        y: int,
        text: str,
        value: any,
        group: list,
        selected: bool = False,
        on_select: Optional[Callable] = None
    ):
        """
        Initialize a radio button.

        Args:
            x, y: Position of the radio button
            text: Label text displayed next to the button
            value: The value this radio button represents
            group: List that holds all radio buttons in this group
            selected: Whether this button starts selected
            on_select: Callback function when this button is selected
        """
        self.x = x
        self.y = y
        self.text = text
        self.value = value
        self.selected = selected
        self.on_select = on_select

        # Radio button circle dimensions
        self.circle_radius = 12
        self.circle_center = (x + self.circle_radius + 5, y + 20)

        # Clickable area (circle + text)
        text_width = len(text) * 12  # Approximate text width
        self.rect = pygame.Rect(x, y, text_width + 100, 40)

        # Visual state
        self.is_hovered = False

        # Add self to group
        group.append(self)
        self.group = group

    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """Update hover state based on mouse position."""
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle mouse clicks.

        When clicked, deselect all other radio buttons in the group
        and select this one.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                # Deselect all buttons in group
                for button in self.group:
                    button.selected = False

                # Select this button
                self.selected = True

                # Call callback if provided
                if self.on_select:
                    self.on_select(self.value)

                return True
        return False

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the radio button.

        Shows a circle (filled if selected, empty if not) and label text.
        """
        # Determine colors based on state
        if self.is_hovered:
            circle_color = config.COLOR_TEXT_HIGHLIGHT
            text_color = config.COLOR_TEXT_HIGHLIGHT
        else:
            circle_color = config.COLOR_MENU_BORDER
            text_color = config.COLOR_TEXT

        # Draw outer circle
        pygame.draw.circle(screen, circle_color, self.circle_center, self.circle_radius, 2)

        # Draw filled inner circle if selected
        if self.selected:
            pygame.draw.circle(screen, circle_color, self.circle_center, self.circle_radius - 4)

        # Draw label text
        font = pygame.font.Font(None, config.FONT_SIZE_SMALL)
        text_surface = font.render(self.text, True, text_color)
        text_x = self.circle_center[0] + self.circle_radius + 15
        text_y = self.circle_center[1] - (config.FONT_SIZE_SMALL // 2)
        screen.blit(text_surface, (text_x, text_y))


class Separator:
    """
    Visual separator line for dividing UI sections.

    A simple horizontal line to visually separate different groups
    of UI elements.
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        thickness: int = 2,
        color: Tuple[int, int, int] = None
    ):
        """
        Initialize a separator line.

        Args:
            x, y: Top-left position of the line
            width: Width of the separator line
            thickness: Thickness of the line in pixels
            color: RGB color tuple (defaults to border color)
        """
        self.x = x
        self.y = y
        self.width = width
        self.thickness = thickness
        self.color = color if color else config.COLOR_MENU_BORDER

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the separator line.

        CALLED EVERY FRAME by the game loop.
        """
        pygame.draw.line(
            screen,
            self.color,
            (self.x, self.y),
            (self.x + self.width, self.y),
            self.thickness
        )


class Dropdown:
    """
    Dropdown menu for selecting one option from multiple choices.

    Shows current selection, expands when clicked to show all options,
    and collapses after selection.
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        options: list,
        selected_index: int = 0,
        on_select: Optional[Callable] = None
    ):
        """
        Initialize a dropdown menu.

        Args:
            x, y: Top-left position
            width: Width of the dropdown
            options: List of (display_text, value) tuples
            selected_index: Index of initially selected option
            on_select: Callback function when option is selected
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = 60
        self.options = options  # List of (text, value) tuples
        self.selected_index = selected_index
        self.on_select = on_select

        # State
        self.is_expanded = False
        self.is_hovered = False
        self.hovered_option = -1  # Which option in dropdown is hovered

        # Main button rect (always visible)
        self.main_rect = pygame.Rect(x, y, width, self.height)

        # Option rects (only when expanded)
        self.option_rects = []
        self._update_option_rects()

    def _update_option_rects(self) -> None:
        """Update the rectangles for each dropdown option."""
        self.option_rects = []
        for i in range(len(self.options)):
            rect = pygame.Rect(
                self.x,
                self.y + self.height + (i * self.height),
                self.width,
                self.height
            )
            self.option_rects.append(rect)

    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """Update hover states."""
        self.is_hovered = self.main_rect.collidepoint(mouse_pos)

        # Check which option is hovered (if expanded)
        self.hovered_option = -1
        if self.is_expanded:
            for i, rect in enumerate(self.option_rects):
                if rect.collidepoint(mouse_pos):
                    self.hovered_option = i
                    break

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle mouse clicks.

        Click on main button toggles expansion.
        Click on option selects it and collapses.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Click on main button
            if self.is_hovered and not self.is_expanded:
                self.is_expanded = True
                return True

            # Click on an option
            if self.is_expanded and self.hovered_option != -1:
                self.selected_index = self.hovered_option
                self.is_expanded = False

                # Call callback with selected value
                if self.on_select:
                    _, value = self.options[self.selected_index]
                    self.on_select(value)

                return True

            # Click outside dropdown when expanded - collapse it
            if self.is_expanded:
                self.is_expanded = False
                return True

        return False

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the dropdown menu.

        Shows the main button with current selection.
        If expanded, shows all options below.
        """
        # Draw main button
        bg_color = config.COLOR_MENU_BUTTON_HOVER if self.is_hovered else config.COLOR_MENU_BUTTON
        pygame.draw.rect(screen, bg_color, self.main_rect)
        pygame.draw.rect(screen, config.COLOR_MENU_BORDER, self.main_rect, 2)

        # Draw current selection text
        font = pygame.font.Font(None, config.FONT_SIZE_MEDIUM)
        selected_text, _ = self.options[self.selected_index]
        text_surface = font.render(selected_text, True, config.COLOR_TEXT)
        text_rect = text_surface.get_rect(center=self.main_rect.center)
        screen.blit(text_surface, text_rect)

        # Draw dropdown arrow
        arrow_x = self.x + self.width - 30
        arrow_y = self.y + self.height // 2
        if self.is_expanded:
            # Up arrow
            points = [(arrow_x, arrow_y + 5), (arrow_x - 8, arrow_y - 5), (arrow_x + 8, arrow_y - 5)]
        else:
            # Down arrow
            points = [(arrow_x, arrow_y + 5), (arrow_x - 8, arrow_y - 5), (arrow_x + 8, arrow_y - 5)]
            points = [(arrow_x, arrow_y - 5), (arrow_x - 8, arrow_y + 5), (arrow_x + 8, arrow_y + 5)]
        pygame.draw.polygon(screen, config.COLOR_TEXT, points)

        # Draw options if expanded
        if self.is_expanded:
            for i, (option_text, _) in enumerate(self.options):
                rect = self.option_rects[i]

                # Background color (highlight if hovered)
                if i == self.hovered_option:
                    bg_color = config.COLOR_MENU_BUTTON_HOVER
                else:
                    bg_color = config.COLOR_MENU_BUTTON

                pygame.draw.rect(screen, bg_color, rect)
                pygame.draw.rect(screen, config.COLOR_MENU_BORDER, rect, 2)

                # Option text
                text_surface = font.render(option_text, True, config.COLOR_TEXT)
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)


class InvestigatorTile:
    """
    UI tile for displaying investigator stats in battle.

    Shows:
    - Portrait or symbol
    - Name
    - Health bar
    - Sanity bar
    - Key stats (accuracy, movement, will)
    - Selection indicator (yellow border when selected)

    Clickable to select the investigator.
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        investigator,
        on_click: Optional[Callable] = None
    ):
        """
        Initialize an investigator tile.

        Args:
            x, y: Top-left position
            width: Tile width
            height: Tile height
            investigator: Reference to Investigator object
            on_click: Callback when tile is clicked
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.investigator = investigator
        self.on_click = on_click

        # Visual state
        self.is_hovered = False
        self.is_selected = False

        # Portrait area (left side of tile)
        portrait_size = min(width // 3, height - 10)
        self.portrait_rect = pygame.Rect(
            x + 5,
            y + 5,
            portrait_size,
            portrait_size
        )

        # Portrait image (will try to load from investigator.image_path)
        self.portrait_image = None
        if hasattr(investigator, 'image_path') and investigator.image_path:
            try:
                # Try to load the portrait image
                from pathlib import Path
                image_path = Path(investigator.image_path)
                if image_path.exists():
                    self.portrait_image = pygame.image.load(str(image_path))
                    # Scale to fit portrait area
                    self.portrait_image = pygame.transform.scale(
                        self.portrait_image,
                        (portrait_size, portrait_size)
                    )
            except Exception as e:
                print(f"Failed to load portrait for {investigator.name}: {e}")
                self.portrait_image = None

        # Stats area (right side of tile)
        self.stats_x = x + portrait_size + 15
        self.stats_y = y + 10

        # Bar dimensions
        self.bar_width = width - portrait_size - 25
        self.bar_height = 12

    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """Update hover state based on mouse position."""
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle mouse clicks on the tile.

        Returns:
            True if tile was clicked, False otherwise
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                # Execute callback if provided
                if self.on_click:
                    self.on_click(self.investigator)
                return True
        return False

    def set_selected(self, selected: bool) -> None:
        """Set the selection state of this tile."""
        self.is_selected = selected

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the investigator tile.

        Shows portrait, name, health/sanity bars, and stats.
        """
        # Background color (darker if incapacitated)
        if self.investigator.is_incapacitated:
            bg_color = (20, 20, 25)
        elif self.is_hovered:
            bg_color = config.COLOR_MENU_BUTTON_HOVER
        else:
            bg_color = config.COLOR_UI_BG

        # Draw background
        pygame.draw.rect(screen, bg_color, self.rect)

        # Draw border (yellow if selected, red if incapacitated, normal otherwise)
        if self.is_selected:
            border_color = config.COLOR_SELECTED
            border_width = 4
        elif self.investigator.is_incapacitated:
            border_color = (100, 30, 30)  # Dark red
            border_width = 2
        else:
            border_color = config.COLOR_MENU_BORDER
            border_width = 2

        pygame.draw.rect(screen, border_color, self.rect, border_width)

        # Draw portrait or symbol
        if self.portrait_image:
            # Draw the loaded portrait image
            screen.blit(self.portrait_image, self.portrait_rect)
            # Draw border around portrait
            pygame.draw.rect(screen, config.COLOR_MENU_BORDER, self.portrait_rect, 1)
        else:
            # Draw symbol as fallback
            # Fill portrait area with dark background
            pygame.draw.rect(screen, (30, 30, 40), self.portrait_rect)
            pygame.draw.rect(screen, config.COLOR_MENU_BORDER, self.portrait_rect, 1)

            # Draw emoji symbol centered
            symbol_font = pygame.font.Font(None, 48)
            symbol_surface = symbol_font.render(
                self.investigator.symbol,
                True,
                config.COLOR_PLAYER
            )
            symbol_rect = symbol_surface.get_rect(center=self.portrait_rect.center)
            screen.blit(symbol_surface, symbol_rect)

        # Draw name split over two lines (larger font for bigger tiles)
        # Line 1: First name + nickname (if present)
        # Line 2: Last name
        name_font = pygame.font.Font(None, 38)  # Slightly smaller to fit 2 lines
        name_color = config.COLOR_TEXT_DIM if self.investigator.is_incapacitated else config.COLOR_TEXT

        # Parse name into first name (+ nickname) and last name
        # Format can be "First Last" or "First 'Nick' Last"
        full_name = self.investigator.name
        name_parts = full_name.split()

        # Check if there's a nickname (indicated by quotes)
        has_nickname = any("'" in part for part in name_parts)

        if has_nickname:
            # Find the last name (everything after the closing quote)
            # Example: "Arthur 'Bones' Blackwood" -> ["Arthur", "'Bones'", "Blackwood"]
            quote_end_idx = None
            for i, part in enumerate(name_parts):
                if part.endswith("'"):
                    quote_end_idx = i
                    break

            if quote_end_idx is not None and quote_end_idx + 1 < len(name_parts):
                # Line 1: First name + nickname
                first_line = " ".join(name_parts[:quote_end_idx + 1])
                # Line 2: Last name (everything after nickname)
                second_line = " ".join(name_parts[quote_end_idx + 1:])
            else:
                # Fallback: just split in half
                mid = len(name_parts) // 2
                first_line = " ".join(name_parts[:mid])
                second_line = " ".join(name_parts[mid:])
        else:
            # No nickname: "First Last" or "First Middle Last"
            if len(name_parts) >= 2:
                # First name on line 1, last name on line 2
                first_line = " ".join(name_parts[:-1])  # Everything except last word
                second_line = name_parts[-1]  # Last word
            else:
                # Single word name (shouldn't happen, but handle it)
                first_line = full_name
                second_line = ""

        # Draw first line (first name + optional nickname)
        first_line_surface = name_font.render(first_line, True, name_color)
        screen.blit(first_line_surface, (self.stats_x, self.stats_y))

        # Draw second line (last name) slightly below
        if second_line:
            second_line_surface = name_font.render(second_line, True, name_color)
            screen.blit(second_line_surface, (self.stats_x, self.stats_y + 32))  # 32px below first line

        # Draw health bar (larger bars for bigger tiles)
        # Adjusted to account for two-line name
        hp_y = self.stats_y + 70  # More spacing to fit 2 lines of text (was 50)
        # Bar dimensions will be larger due to increased tile size
        self._draw_resource_bar(
            screen,
            self.stats_x,
            hp_y,
            self.bar_width,
            int(self.bar_height * 1.3),  # Slightly taller bars
            self.investigator.current_health,
            self.investigator.max_health,
            (200, 50, 50),  # Red
            "HP"
        )

        # Draw sanity bar
        san_y = hp_y + int(self.bar_height * 1.3) + 12  # More spacing (was 8)
        self._draw_resource_bar(
            screen,
            self.stats_x,
            san_y,
            self.bar_width,
            int(self.bar_height * 1.3),  # Slightly taller bars
            self.investigator.current_sanity,
            self.investigator.max_sanity,
            (80, 120, 200),  # Blue
            "SAN"
        )

        # Draw compact stats (accuracy, movement, will) with larger font
        stats_y = san_y + int(self.bar_height * 1.3) + 18  # More spacing (was 12)
        stat_font = pygame.font.Font(None, 32)  # Increased from 24

        # Accuracy
        acc_text = f"ACC:{self.investigator.accuracy}%"
        acc_color = config.COLOR_TEXT_DIM if self.investigator.is_incapacitated else config.COLOR_TEXT
        acc_surface = stat_font.render(acc_text, True, acc_color)
        screen.blit(acc_surface, (self.stats_x, stats_y))

        # Movement (more spacing for larger tiles)
        move_text = f"MOV:{self.investigator.movement_range}"
        move_surface = stat_font.render(move_text, True, acc_color)
        screen.blit(move_surface, (self.stats_x + 105, stats_y))  # Increased from 75

        # Will
        will_text = f"WIL:{self.investigator.will}"
        will_surface = stat_font.render(will_text, True, acc_color)
        screen.blit(will_surface, (self.stats_x + 200, stats_y))  # Increased from 140

        # Draw incapacitated warning if needed (larger font)
        if self.investigator.is_incapacitated:
            warning_font = pygame.font.Font(None, 38)  # Increased from 28
            warning_surface = warning_font.render(
                "INCAPACITATED",
                True,
                (200, 50, 50)
            )
            warning_rect = warning_surface.get_rect(
                center=(self.rect.centerx, self.rect.bottom - 20)  # More margin
            )
            screen.blit(warning_surface, warning_rect)

    def _draw_resource_bar(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        current: int,
        maximum: int,
        bar_color: Tuple[int, int, int],
        label: str
    ) -> None:
        """
        Draw a resource bar (health or sanity).

        Args:
            screen: Surface to draw on
            x, y: Top-left position
            width, height: Bar dimensions
            current: Current value
            maximum: Maximum value
            bar_color: RGB color for filled portion
            label: Text label (e.g., "HP", "SAN")
        """
        # Background (empty bar)
        bg_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, (40, 40, 50), bg_rect)
        pygame.draw.rect(screen, (80, 80, 90), bg_rect, 1)

        # Filled portion (current value)
        if maximum > 0:
            fill_width = int((current / maximum) * width)
            fill_rect = pygame.Rect(x, y, fill_width, height)
            pygame.draw.rect(screen, bar_color, fill_rect)

        # Draw text (e.g., "HP: 12/15") with larger font for bigger tiles
        text_font = pygame.font.Font(None, 30)  # Increased from 22
        text = f"{label}: {current}/{maximum}"
        text_surface = text_font.render(text, True, config.COLOR_TEXT)
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(text_surface, text_rect)


class ActionButton:
    """
    Small action button for the action bar.

    Displays an ability/action icon or text with visual feedback.
    Can be in enabled, disabled, or cooldown states.
    """

    def __init__(
        self,
        x: int,
        y: int,
        size: int,
        text: str = "",
        icon: str = "",
        on_click: Optional[Callable] = None,
        enabled: bool = True,
        hotkey: str = ""
    ):
        """
        Initialize an action button.

        Args:
            x, y: Top-left position
            size: Width and height (square button)
            text: Text label for the action
            icon: Icon/emoji symbol (if available)
            on_click: Callback when button is clicked
            enabled: Whether button can be clicked
            hotkey: Keyboard shortcut (e.g., "1", "2", etc.)
        """
        self.rect = pygame.Rect(x, y, size, size)
        self.text = text
        self.icon = icon
        self.on_click = on_click
        self.enabled = enabled
        self.hotkey = hotkey

        # Visual state
        self.is_hovered = False
        self.is_pressed = False

        # Colors
        self.color_normal = (40, 40, 55)
        self.color_hover = (60, 60, 80)
        self.color_active = (80, 80, 110)
        self.color_disabled = (25, 25, 35)
        self.color_border = config.COLOR_MENU_BORDER
        self.color_border_hover = config.COLOR_TEXT_HIGHLIGHT

    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """Update hover state based on mouse position."""
        if self.enabled:
            self.is_hovered = self.rect.collidepoint(mouse_pos)
        else:
            self.is_hovered = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle mouse clicks on the action button.

        Returns:
            True if button was clicked, False otherwise
        """
        if not self.enabled:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.is_pressed = True
                return False

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_hovered and self.is_pressed:
                self.is_pressed = False
                if self.on_click:
                    self.on_click()
                return True
            self.is_pressed = False

        return False

    def set_enabled(self, enabled: bool) -> None:
        """Set whether the button is enabled."""
        self.enabled = enabled

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the action button.

        Shows icon/text, hotkey number, and visual state.
        """
        # Background color based on state
        if not self.enabled:
            bg_color = self.color_disabled
        elif self.is_pressed:
            bg_color = self.color_active
        elif self.is_hovered:
            bg_color = self.color_hover
        else:
            bg_color = self.color_normal

        # Draw background
        pygame.draw.rect(screen, bg_color, self.rect)

        # Draw border
        if self.is_hovered and self.enabled:
            border_color = self.color_border_hover
            border_width = 3
        else:
            border_color = self.color_border
            border_width = 2

        pygame.draw.rect(screen, border_color, self.rect, border_width)

        # Draw icon if available
        if self.icon:
            icon_font = pygame.font.Font(None, self.rect.height // 2)
            text_color = config.COLOR_TEXT if self.enabled else config.COLOR_TEXT_DIM
            icon_surface = icon_font.render(self.icon, True, text_color)
            icon_rect = icon_surface.get_rect(center=self.rect.center)
            screen.blit(icon_surface, icon_rect)

        # Draw text label (below icon or centered if no icon)
        if self.text:
            text_font = pygame.font.Font(None, 22)
            text_color = config.COLOR_TEXT if self.enabled else config.COLOR_TEXT_DIM
            text_surface = text_font.render(self.text, True, text_color)

            if self.icon:
                # Position below icon
                text_rect = text_surface.get_rect(
                    centerx=self.rect.centerx,
                    bottom=self.rect.bottom - 5
                )
            else:
                # Center in button
                text_rect = text_surface.get_rect(center=self.rect.center)

            screen.blit(text_surface, text_rect)

        # Draw hotkey number in top-left corner
        if self.hotkey:
            hotkey_font = pygame.font.Font(None, 18)
            hotkey_color = config.COLOR_TEXT_HIGHLIGHT if self.enabled else config.COLOR_TEXT_DIM
            hotkey_surface = hotkey_font.render(self.hotkey, True, hotkey_color)
            screen.blit(hotkey_surface, (self.rect.x + 3, self.rect.y + 2))


class ActionBar:
    """
    Action bar displaying 10 ability/action slots.

    Updates based on the currently selected investigator,
    showing available actions and their states.
    """

    def __init__(self, x: int, y: int, button_size: int = 70, spacing: int = 10):
        """
        Initialize the action bar.

        Args:
            x, y: Top-left position of the action bar
            button_size: Size of each action button (square)
            spacing: Space between buttons
        """
        self.x = x
        self.y = y
        self.button_size = button_size
        self.spacing = spacing

        # Create 10 action button slots
        self.action_buttons: List[ActionButton] = []
        for i in range(10):
            button_x = x + (i * (button_size + spacing))
            button_y = y

            # Create empty slot with hotkey number
            hotkey = str((i + 1) % 10)  # 1-9, then 0
            button = ActionButton(
                x=button_x,
                y=button_y,
                size=button_size,
                text="",
                on_click=lambda idx=i: self._on_action_click(idx),
                enabled=False,
                hotkey=hotkey
            )
            self.action_buttons.append(button)

        # Current investigator
        self.current_investigator = None

    def update_for_investigator(self, investigator) -> None:
        """
        Update action bar to show actions for the given investigator.

        Args:
            investigator: Investigator object whose actions to display
        """
        self.current_investigator = investigator

        # For now, show placeholder actions
        # In the future, this will be populated from investigator.abilities

        if investigator and not investigator.is_incapacitated:
            # Enable Move button (slot 0)
            self.action_buttons[0].text = "Move"
            self.action_buttons[0].icon = "↗"
            self.action_buttons[0].enabled = True

            # Enable Attack button (slot 1)
            self.action_buttons[1].text = "Attack"
            self.action_buttons[1].icon = "⚔"
            self.action_buttons[1].enabled = True

            # Disable remaining slots (no abilities yet)
            for i in range(2, 10):
                self.action_buttons[i].text = ""
                self.action_buttons[i].icon = ""
                self.action_buttons[i].enabled = False
        else:
            # No investigator selected or incapacitated - disable all
            for button in self.action_buttons:
                button.text = ""
                button.icon = ""
                button.enabled = False

    def clear(self) -> None:
        """Clear the action bar (no investigator selected)."""
        self.update_for_investigator(None)

    def _on_action_click(self, slot_index: int) -> None:
        """
        Handle click on an action button.

        Args:
            slot_index: Index of the clicked button (0-9)
        """
        print(f"Action slot {slot_index} clicked")
        # TODO: Execute the corresponding action
        # This will trigger movement/attack/ability logic

    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """Update hover states for all action buttons."""
        for button in self.action_buttons:
            button.update(mouse_pos)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle events for all action buttons.

        Returns:
            True if any button consumed the event, False otherwise
        """
        for button in self.action_buttons:
            if button.handle_event(event):
                return True

        # Handle hotkey presses (1-0 keys)
        if event.type == pygame.KEYDOWN:
            # Number keys 1-0 (SDLK keys 49-57 for 1-9, 48 for 0)
            if pygame.K_1 <= event.key <= pygame.K_9:
                slot_index = event.key - pygame.K_1  # 0-8
                if self.action_buttons[slot_index].enabled:
                    self._on_action_click(slot_index)
                    return True
            elif event.key == pygame.K_0:
                if self.action_buttons[9].enabled:
                    self._on_action_click(9)
                    return True

        return False

    def draw(self, screen: pygame.Surface) -> None:
        """Draw all action buttons."""
        for button in self.action_buttons:
            button.draw(screen)
