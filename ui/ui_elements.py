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
