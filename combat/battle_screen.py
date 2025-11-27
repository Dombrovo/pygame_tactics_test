"""
Battle Screen - Tactical combat interface.

This module implements the tactical battle screen where grid-based
combat takes place.
"""

import pygame
from typing import Optional, List, Tuple
import config
from combat.grid import Grid
from entities.unit import Unit
from entities.investigator import Investigator, create_test_squad
from entities.enemy import Enemy, create_test_enemies


class BattleScreen:
    """
    Battle screen for tactical combat.

    Manages:
    - Grid rendering
    - Unit rendering and selection
    - Turn-based gameplay (player/enemy phases)
    - Win/lose conditions
    """

    def __init__(self, screen: pygame.Surface):
        """
        Initialize the battle screen.

        Args:
            screen: Pygame display surface
        """
        self.screen = screen
        self.running = True
        self.next_screen = None

        # Create grid
        self.grid = Grid(config.GRID_SIZE)
        self.grid.setup_test_cover()  # Add some test cover

        # Create units
        self.player_units: List[Investigator] = create_test_squad()
        self.enemy_units: List[Enemy] = create_test_enemies()

        # Place units on grid
        self._setup_unit_positions()

        # Battle state
        self.current_phase = "player_turn"  # "player_turn" or "enemy_turn"
        self.selected_unit: Optional[Unit] = None
        self.turn_number = 1

        # Calculate grid rendering offset (center on screen)
        self.grid_pixel_size = config.GRID_SIZE * config.TILE_SIZE
        self.grid_offset_x = (config.SCREEN_WIDTH - self.grid_pixel_size) // 2
        self.grid_offset_y = 100  # Leave space at top for UI

        # Fonts
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)

    def _setup_unit_positions(self):
        """Place units on the grid at starting positions."""
        # Place investigators on left side (x=0-1)
        investigator_positions = [
            (0, 2), (1, 2), (0, 7), (1, 7)
        ]
        for inv, pos in zip(self.player_units, investigator_positions):
            self.grid.place_unit(inv, pos[0], pos[1])

        # Place enemies on right side (x=8-9)
        enemy_positions = [
            (9, 2), (8, 2), (9, 7), (8, 7)
        ]
        for enemy, pos in zip(self.enemy_units, enemy_positions):
            self.grid.place_unit(enemy, pos[0], pos[1])

    def handle_events(self) -> None:
        """Process input events."""
        for event in pygame.event.get():
            # Quit events
            if event.type == pygame.QUIT:
                self.running = False
                self.next_screen = "quit"

            # Keyboard events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.next_screen = "title"
                elif event.key == pygame.K_SPACE:
                    self._end_turn()
                elif event.key == pygame.K_TAB:
                    self._cycle_unit_selection()

            # Mouse events
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self._handle_left_click(event.pos)

    def _handle_left_click(self, mouse_pos: Tuple[int, int]):
        """
        Handle left mouse click.

        Args:
            mouse_pos: (x, y) pixel coordinates of click
        """
        # Convert mouse position to grid coordinates
        grid_x, grid_y = self._pixel_to_grid(mouse_pos)

        if grid_x is None or grid_y is None:
            return

        # Get tile at clicked position
        tile = self.grid.get_tile(grid_x, grid_y)
        if not tile:
            return

        # If tile has a unit, select it
        if tile.is_occupied():
            unit = tile.occupied_by
            # Only select player units during player turn
            if self.current_phase == "player_turn" and unit.team == "player":
                self.selected_unit = unit
                print(f"Selected: {unit.name}")

    def _pixel_to_grid(self, pixel_pos: Tuple[int, int]) -> Tuple[Optional[int], Optional[int]]:
        """
        Convert pixel coordinates to grid coordinates.

        Args:
            pixel_pos: (x, y) in pixels

        Returns:
            (grid_x, grid_y) or (None, None) if outside grid
        """
        px, py = pixel_pos

        # Subtract grid offset
        grid_px = px - self.grid_offset_x
        grid_py = py - self.grid_offset_y

        # Check if within grid bounds
        if grid_px < 0 or grid_py < 0:
            return (None, None)
        if grid_px >= self.grid_pixel_size or grid_py >= self.grid_pixel_size:
            return (None, None)

        # Calculate grid coordinates
        grid_x = grid_px // config.TILE_SIZE
        grid_y = grid_py // config.TILE_SIZE

        return (grid_x, grid_y)

    def _grid_to_pixel(self, grid_x: int, grid_y: int) -> Tuple[int, int]:
        """
        Convert grid coordinates to pixel coordinates (top-left of tile).

        Args:
            grid_x: Grid X coordinate
            grid_y: Grid Y coordinate

        Returns:
            (pixel_x, pixel_y) of tile's top-left corner
        """
        pixel_x = self.grid_offset_x + (grid_x * config.TILE_SIZE)
        pixel_y = self.grid_offset_y + (grid_y * config.TILE_SIZE)
        return (pixel_x, pixel_y)

    def _cycle_unit_selection(self):
        """Cycle through player units with Tab key."""
        if self.current_phase != "player_turn":
            return

        # Get list of active player units
        active_units = [u for u in self.player_units if u.can_act()]
        if not active_units:
            return

        # Find current selection index
        if self.selected_unit in active_units:
            current_index = active_units.index(self.selected_unit)
            next_index = (current_index + 1) % len(active_units)
            self.selected_unit = active_units[next_index]
        else:
            self.selected_unit = active_units[0]

        print(f"Selected: {self.selected_unit.name}")

    def _end_turn(self):
        """End current phase and switch to next phase."""
        if self.current_phase == "player_turn":
            # Reset player unit flags
            for unit in self.player_units:
                unit.reset_turn_flags()

            # Switch to enemy turn
            self.current_phase = "enemy_turn"
            self.selected_unit = None
            print("Enemy Turn")

            # TODO: Enemy AI actions in Phase 1.5

            # For now, immediately switch back to player turn
            self._end_turn()

        elif self.current_phase == "enemy_turn":
            # Reset enemy unit flags
            for unit in self.enemy_units:
                unit.reset_turn_flags()

            # Increment turn counter
            self.turn_number += 1

            # Switch to player turn
            self.current_phase = "player_turn"
            print(f"Player Turn {self.turn_number}")

    def update(self) -> None:
        """Update battle state."""
        # Check win/lose conditions
        self._check_win_lose()

        # Get mouse position for hover effects
        self.mouse_pos = pygame.mouse.get_pos()

    def _check_win_lose(self):
        """Check if battle is won or lost."""
        # Count active units
        active_investigators = sum(1 for u in self.player_units if u.can_act())
        active_enemies = sum(1 for u in self.enemy_units if u.can_act())

        if active_enemies == 0:
            # Victory!
            print("VICTORY! All enemies defeated.")
            self.running = False
            self.next_screen = "victory"

        elif active_investigators == 0:
            # Defeat!
            print("DEFEAT! All investigators incapacitated.")
            self.running = False
            self.next_screen = "defeat"

    def draw(self) -> None:
        """Render the battle screen."""
        # Clear screen
        self.screen.fill(config.COLOR_BG)

        # Draw UI header
        self._draw_header()

        # Draw grid
        self._draw_grid()

        # Draw units
        self._draw_units()

        # Draw selection highlight
        if self.selected_unit and self.selected_unit.position:
            self._draw_selection_highlight(self.selected_unit.position)

        # Draw unit info panel
        self._draw_unit_info_panel()

        # Draw controls help
        self._draw_controls_help()

    def _draw_header(self):
        """Draw battle status header."""
        # Turn number and phase
        phase_text = "PLAYER PHASE" if self.current_phase == "player_turn" else "ENEMY PHASE"
        turn_text = f"TURN {self.turn_number} | {phase_text}"

        text_surface = self.font_medium.render(turn_text, True, config.COLOR_TEXT_HIGHLIGHT)
        text_rect = text_surface.get_rect(center=(config.SCREEN_WIDTH // 2, 50))
        self.screen.blit(text_surface, text_rect)

    def _draw_grid(self):
        """Draw the battlefield grid."""
        for y in range(self.grid.size):
            for x in range(self.grid.size):
                tile = self.grid.get_tile(x, y)
                if not tile:
                    continue

                # Calculate pixel position
                pixel_x, pixel_y = self._grid_to_pixel(x, y)

                # Tile background color based on terrain
                if tile.terrain_type == "full_cover":
                    color = (50, 50, 70)  # Darker for full cover
                elif tile.terrain_type == "half_cover":
                    color = (35, 35, 50)  # Medium for half cover
                else:
                    color = (25, 25, 35)  # Dark for empty

                # Draw tile background
                tile_rect = pygame.Rect(pixel_x, pixel_y, config.TILE_SIZE, config.TILE_SIZE)
                pygame.draw.rect(self.screen, color, tile_rect)

                # Draw grid lines
                pygame.draw.rect(self.screen, config.COLOR_GRID, tile_rect, 1)

                # Draw cover symbol
                if tile.terrain_type != "empty":
                    symbol_surface = self.font_small.render(tile.symbol, True, (100, 100, 120))
                    symbol_rect = symbol_surface.get_rect(
                        center=(pixel_x + config.TILE_SIZE // 2, pixel_y + config.TILE_SIZE // 2)
                    )
                    self.screen.blit(symbol_surface, symbol_rect)

    def _draw_units(self):
        """Draw all units on the grid."""
        all_units = self.player_units + self.enemy_units

        for unit in all_units:
            if not unit.position:
                continue

            x, y = unit.position
            pixel_x, pixel_y = self._grid_to_pixel(x, y)

            # Draw unit symbol
            symbol_surface = self.font_large.render(unit.symbol, True, config.COLOR_TEXT)
            symbol_rect = symbol_surface.get_rect(
                center=(pixel_x + config.TILE_SIZE // 2, pixel_y + config.TILE_SIZE // 2)
            )
            self.screen.blit(symbol_surface, symbol_rect)

            # Draw health bar
            self._draw_health_bar(unit, pixel_x, pixel_y)

    def _draw_health_bar(self, unit: Unit, pixel_x: int, pixel_y: int):
        """
        Draw health and sanity bars for a unit.

        Args:
            unit: Unit to draw bars for
            pixel_x: Pixel X position of tile
            pixel_y: Pixel Y position of tile
        """
        bar_width = config.TILE_SIZE - 10
        bar_height = 5
        bar_x = pixel_x + 5
        bar_y_health = pixel_y + config.TILE_SIZE - 15
        bar_y_sanity = pixel_y + config.TILE_SIZE - 8

        # Health bar (red)
        health_pct = unit.get_health_percentage()
        pygame.draw.rect(self.screen, (80, 30, 30), (bar_x, bar_y_health, bar_width, bar_height))
        if health_pct > 0:
            pygame.draw.rect(
                self.screen,
                (200, 50, 50),
                (bar_x, bar_y_health, int(bar_width * health_pct), bar_height)
            )

        # Sanity bar (blue)
        sanity_pct = unit.get_sanity_percentage()
        pygame.draw.rect(self.screen, (30, 30, 80), (bar_x, bar_y_sanity, bar_width, bar_height))
        if sanity_pct > 0:
            pygame.draw.rect(
                self.screen,
                (50, 100, 200),
                (bar_x, bar_y_sanity, int(bar_width * sanity_pct), bar_height)
            )

    def _draw_selection_highlight(self, grid_pos: Tuple[int, int]):
        """
        Draw highlight around selected unit.

        Args:
            grid_pos: (x, y) grid coordinates
        """
        x, y = grid_pos
        pixel_x, pixel_y = self._grid_to_pixel(x, y)

        # Draw yellow border
        highlight_rect = pygame.Rect(pixel_x, pixel_y, config.TILE_SIZE, config.TILE_SIZE)
        pygame.draw.rect(self.screen, (255, 255, 100), highlight_rect, 3)

    def _draw_unit_info_panel(self):
        """Draw info panel for selected unit."""
        if not self.selected_unit:
            return

        # Panel position (right side of screen)
        panel_x = self.grid_offset_x + self.grid_pixel_size + 40
        panel_y = self.grid_offset_y
        panel_width = config.SCREEN_WIDTH - panel_x - 40

        # Draw panel background
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, 400)
        pygame.draw.rect(self.screen, (30, 30, 45), panel_rect)
        pygame.draw.rect(self.screen, (100, 100, 130), panel_rect, 2)

        # Draw unit info text
        info_lines = self.selected_unit.get_info_text().split('\n')
        y_offset = panel_y + 20

        for line in info_lines:
            text_surface = self.font_small.render(line, True, config.COLOR_TEXT)
            self.screen.blit(text_surface, (panel_x + 20, y_offset))
            y_offset += 40

    def _draw_controls_help(self):
        """Draw controls help at bottom of screen."""
        controls = [
            "CONTROLS:",
            "Click: Select Unit",
            "Tab: Cycle Units",
            "Space: End Turn",
            "ESC: Return to Menu"
        ]

        y_offset = config.SCREEN_HEIGHT - 200

        for line in controls:
            text_surface = self.font_small.render(line, True, (150, 150, 170))
            text_rect = text_surface.get_rect(center=(config.SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += 35

    def run(self, clock: pygame.time.Clock) -> str:
        """
        Run the battle screen game loop.

        Args:
            clock: Pygame clock for timing

        Returns:
            Next screen to display
        """
        print(f"Battle Started! Turn {self.turn_number} - {self.current_phase}")

        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            pygame.display.flip()
            clock.tick(config.FPS)

        return self.next_screen if self.next_screen else "title"
