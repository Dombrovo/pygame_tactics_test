"""
Battle Screen - Tactical combat interface.

This module implements the tactical battle screen where grid-based
combat takes place.
"""

import pygame
import random
from typing import Optional, List, Tuple
import config
from combat.grid import Grid
from entities.unit import Unit
from entities.investigator import Investigator, create_test_squad
from entities.enemy import Enemy, create_test_enemies
from ui.ui_elements import InvestigatorTile, ActionBar, Button, TurnOrderTracker


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

        This constructor sets up everything needed for tactical combat:
        1. Creates a 10x10 grid battlefield
        2. Spawns player investigators and enemy units
        3. Places units at starting positions
        4. Initializes battle state (turn tracking, phase management)
        5. Sets up rendering (fonts, grid positioning)

        Args:
            screen: Pygame display surface (the main window to draw on)
        """
        self.screen = screen
        self.running = True
        # Navigation: which screen to show next (title, victory, defeat)
        self.next_screen = None

        # Create grid
        self.grid = Grid(config.GRID_SIZE)
        self.grid.setup_test_cover()  # Add some test cover

        # Create units
        self.player_units: List[Investigator] = create_test_squad()
        self.enemy_units: List[Enemy] = create_test_enemies()

        # Place units on grid
        self._setup_unit_positions()

        # ====================================================================
        # Turn Order System
        # ====================================================================
        # Individual unit turns instead of phase-based (all players then all enemies)
        # For now: random order; future: initiative stat-based

        # Combine all units into turn order and shuffle randomly
        all_units = self.player_units + self.enemy_units
        random.shuffle(all_units)
        self.turn_order: List[Unit] = all_units

        # Track which unit's turn it is
        self.current_turn_index = 0
        self.current_turn_unit: Optional[Unit] = self.turn_order[0] if self.turn_order else None

        # Battle state
        self.current_phase = "player_turn"  # Deprecated: kept for compatibility, will be removed
        self.selected_unit: Optional[Unit] = None  # Unit being viewed (not necessarily whose turn it is)
        self.turn_number = 1
        self.round_number = 1  # A round = all units have taken one turn

        # Calculate grid rendering offset (center on screen)
        self.grid_pixel_size = config.GRID_SIZE * config.TILE_SIZE
        self.grid_offset_x = (config.SCREEN_WIDTH - self.grid_pixel_size) // 2
        # grid_offset_y will be set after turn order tracker is created

        # ====================================================================
        # Font system with emoji support
        # ====================================================================
        # We want to use emoji symbols (👤, 🔫, 🐺) to represent units,
        # but not all systems have fonts that can render emoji.
        #
        # Strategy:
        # 1. Try to load a system font that supports emoji
        # 2. If no emoji font found, fall back to ASCII symbols ([I], [C], [H])
        #
        # Platform-specific emoji fonts:
        # - Windows: Segoe UI Emoji (built-in since Windows 8)
        # - macOS: Apple Color Emoji (built-in)
        # - Linux: Noto Color Emoji or Symbola (may need to be installed)

        emoji_font_names = ["Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji", "Symbola"]
        self.font_large = None

        # Loop through each font name and try to load it
        # pygame.font.SysFont() searches system fonts by name
        # If found, we break out of the loop immediately
        for font_name in emoji_font_names:
            try:
                self.font_large = pygame.font.SysFont(font_name, 60)
                print(f"Loaded emoji font: {font_name}")
                break  # Success! Stop searching
            except:
                continue  # This font not found, try next one

        # Fallback: If no emoji font was found, use default font with ASCII symbols
        if self.font_large is None:
            print("No emoji font found, using default font with text symbols")
            self.font_large = pygame.font.Font(None, 72)  # None = Pygame's default font
            self.emoji_font_available = False

            # Replace emoji symbols with ASCII equivalents
            # e.g., 👤 becomes [I], 🔫 becomes [C], etc.
            self._use_text_symbols()
        else:
            self.emoji_font_available = True

        # Medium font for UI text (turn counter, phase display)
        self.font_medium = pygame.font.Font(None, 48)

        # Small font for cover symbols and controls help
        # Use emoji font if available, otherwise use default
        if self.emoji_font_available:
            self.font_small = pygame.font.SysFont(emoji_font_names[0], 36)
        else:
            self.font_small = pygame.font.Font(None, 36)
            # Replace cover emoji (⬛, ▪️) with ASCII (##, ::)
            self._use_text_cover_symbols()

        # ====================================================================
        # Turn Order Tracker (Top of Screen)
        # ====================================================================
        # Visual display of the turn order, showing all units in sequence
        # with the current turn unit highlighted
        # MUST be created before investigator tiles and grid positioning
        tracker_height = 70
        tracker_width = 1200  # Wide enough to fit 8 unit icons with spacing
        tracker_x = (config.SCREEN_WIDTH - tracker_width) // 2  # Centered
        tracker_y = 10  # 10px from top

        self.turn_order_tracker = TurnOrderTracker(
            x=tracker_x,
            y=tracker_y,
            width=tracker_width,
            height=tracker_height
        )
        # Will be populated with turn order after units are created

        # Update grid offset to make room for turn order tracker
        # This affects both the grid and investigator tiles positioning
        self.grid_offset_y = tracker_y + tracker_height + 15  # 15px gap below tracker

        # ====================================================================
        # Investigator Tiles Panel (Left Side)
        # ====================================================================
        # Create UI tiles for each investigator, displayed vertically on left
        # Each tile shows: portrait, name, HP bar, sanity bar, stats
        # Tiles are clickable for selection
        self.investigator_tiles: List[InvestigatorTile] = []

        # Panel layout (left side of screen)
        # Tiles increased by 50% and spacing widened to use full vertical space
        tile_panel_x = 20  # 20px from left edge
        tile_panel_y = self.grid_offset_y  # Align with grid top
        tile_width = 510   # 50% larger (340 * 1.5)
        tile_height = 180  # 50% larger (120 * 1.5)
        tile_spacing = 25  # Widened gap (distributes 4 tiles across ~800px vertical space)

        # Create one tile for each investigator
        for i, investigator in enumerate(self.player_units):
            tile_y = tile_panel_y + (i * (tile_height + tile_spacing))

            tile = InvestigatorTile(
                x=tile_panel_x,
                y=tile_y,
                width=tile_width,
                height=tile_height,
                investigator=investigator,
                on_click=self._on_investigator_tile_click
            )
            self.investigator_tiles.append(tile)

        # ====================================================================
        # Action Bar (Bottom Center)
        # ====================================================================
        # Position the action bar below the grid, centered
        # 10 buttons × 70px + 9 gaps × 10px = 700 + 90 = 790px total width
        action_bar_width = 10 * 70 + 9 * 10  # 790px
        action_bar_x = (config.SCREEN_WIDTH - action_bar_width) // 2
        action_bar_y = self.grid_offset_y + self.grid_pixel_size + 20  # 20px below grid

        self.action_bar = ActionBar(
            x=action_bar_x,
            y=action_bar_y,
            button_size=70,
            spacing=10
        )

        # ====================================================================
        # End Turn Button (Right of Action Bar)
        # ====================================================================
        # Position end turn button to the right of action bar with 20px gap
        end_turn_button_width = 150
        end_turn_button_height = 70
        end_turn_button_x = action_bar_x + action_bar_width + 20  # 20px gap
        end_turn_button_y = action_bar_y

        self.end_turn_button = Button(
            x=end_turn_button_x,
            y=end_turn_button_y,
            width=end_turn_button_width,
            height=end_turn_button_height,
            text="End Turn",
            on_click=self._advance_turn
        )

        # ====================================================================
        # Initialize Turn Order Tracker Data
        # ====================================================================
        # Now that turn order is established, populate the tracker
        self.turn_order_tracker.update_turn_order(self.turn_order, self.current_turn_index)

        # ====================================================================
        # Initialize First Turn
        # ====================================================================
        # Set up the initial turn state
        # Auto-select the first unit in turn order
        self.selected_unit = self.current_turn_unit
        self._update_tile_selection()
        self._update_action_bar()

        # Print initial turn information
        if self.current_turn_unit:
            team_str = "Player" if self.current_turn_unit.team == "player" else "Enemy"
            print(f"\n=== BATTLE START ===")
            print(f"Turn order ({len(self.turn_order)} units):")
            for i, unit in enumerate(self.turn_order):
                current_marker = " <-- CURRENT" if i == 0 else ""
                team_marker = "P" if unit.team == "player" else "E"
                print(f"  {i+1}. [{team_marker}] {unit.name}{current_marker}")
            print(f"\n{team_str} Turn: {self.current_turn_unit.name}")

    def _use_text_symbols(self):
        """
        Replace emoji symbols with ASCII text symbols.

        Called when no emoji font is available on the system.
        This ensures units are always distinguishable even without
        emoji support.

        Symbol mapping:
        - 👤 (Investigator) → [I]
        - 🔫 (Cultist)      → [C]
        - 🐺 (Hound)        → [H]
        """
        # Change investigator symbols
        for inv in self.player_units:
            inv.symbol = "[I]"  # I for Investigator

        # Change enemy symbols based on their attack type
        # This works for any enemy class (Cultist, Hound, etc.)
        for enemy in self.enemy_units:
            if hasattr(enemy, 'attack_type'):
                if enemy.attack_type == "ranged":
                    enemy.symbol = "[C]"  # C for Cultist (ranged)
                elif enemy.attack_type == "melee":
                    enemy.symbol = "[H]"  # H for Hound (melee)
            else:
                enemy.symbol = "[E]"  # E for Enemy (generic fallback)

    def _use_text_cover_symbols(self):
        """
        Replace Unicode cover symbols with ASCII equivalents.

        Called when emoji font is not available. Iterates through
        every tile on the grid and replaces emoji terrain symbols
        with ASCII characters.

        Symbol mapping:
        - ⬛ (Full cover)  → ##
        - ▪️ (Half cover)  → ::
        - ⬜ (Empty tile)  → ..
        """
        # Loop through every tile in the grid
        for y in range(self.grid.size):
            for x in range(self.grid.size):
                tile = self.grid.get_tile(x, y)
                if tile:
                    # Replace symbol based on terrain type
                    if tile.terrain_type == "full_cover":
                        tile.symbol = "##"  # Double hash = solid cover
                    elif tile.terrain_type == "half_cover":
                        tile.symbol = "::"  # Double colon = partial cover
                    else:
                        tile.symbol = ".."  # Dots = empty/open ground

    def _setup_unit_positions(self):
        """
        Place units on the grid at starting positions.

        Tactical deployment:
        - Investigators start on the LEFT side (x = 0-1)
          Positioned at corners: (0,2), (1,2), (0,7), (1,7)
        - Enemies start on the RIGHT side (x = 8-9)
          Mirrored positions: (9,2), (8,2), (9,7), (8,7)

        This creates a symmetrical battlefield with units facing
        each other across the grid, separated by ~7-8 tiles of
        open ground.

        The grid.place_unit() method:
        1. Sets the unit's position attribute
        2. Updates the tile's occupied_by attribute
        3. Handles any existing unit at that position
        """
        # Place investigators on left side (x=0-1)
        # Corners provide tactical flexibility - can move forward or sideways
        investigator_positions = [
            (0, 2),   # Top-left corner area
            (1, 2),   # Second column, top
            (0, 7),   # Bottom-left corner area
            (1, 7)    # Second column, bottom
        ]
        for inv, pos in zip(self.player_units, investigator_positions):
            self.grid.place_unit(inv, pos[0], pos[1])

        # Place enemies on right side (x=8-9)
        # Mirrored deployment for balanced start
        enemy_positions = [
            (9, 2),   # Top-right corner area
            (8, 2),   # Second-to-last column, top
            (9, 7),   # Bottom-right corner area
            (8, 7)    # Second-to-last column, bottom
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

            # Handle action bar events (before other UI)
            # This includes both mouse clicks and hotkey presses (1-0 keys)
            if self.action_bar.handle_event(event):
                # Action bar consumed the event
                continue

            # Handle end turn button events
            if self.end_turn_button.handle_event(event):
                # End turn button was clicked, event consumed
                continue

            # Handle investigator tile events (must be before grid clicks)
            # This allows clicking on tiles to select investigators
            for tile in self.investigator_tiles:
                if tile.handle_event(event):
                    # Tile was clicked, event consumed
                    # Selection is handled in _on_investigator_tile_click callback
                    continue

            # Mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self._handle_left_click(event.pos)

    def _handle_left_click(self, mouse_pos: Tuple[int, int]):
        """
        Handle left mouse click on the battlefield.

        Click handling process:
        1. Convert pixel coordinates to grid coordinates
        2. Check if click was inside the grid
        3. Get the tile at that grid position
        4. If tile has a unit, select it (any unit can be selected for viewing stats)

        Selection behavior:
        - ANY unit can be selected to view stats in the right panel
        - Player units show actions in the action bar
        - Enemy units clear the action bar (can't control enemies)
        - Investigator tiles highlight which player unit is "active"

        Future expansion (Phase 1.5):
        - If unit selected and click is empty tile: Move to that tile
        - If unit selected and click is enemy: Attack that enemy

        Args:
            mouse_pos: (x, y) pixel coordinates of where user clicked
        """
        # Convert pixel position (e.g., 850, 300) to grid coordinates (e.g., 5, 3)
        grid_x, grid_y = self._pixel_to_grid(mouse_pos)

        # Check if click was outside the grid
        if grid_x is None or grid_y is None:
            # Click was outside the battlefield, ignore it
            return

        # Get the tile object at this grid position
        tile = self.grid.get_tile(grid_x, grid_y)
        if not tile:
            # Shouldn't happen, but safety check
            return

        # Check if the clicked tile has a unit on it
        if tile.is_occupied():
            unit = tile.occupied_by

            # Select any unit (player or enemy) to view stats
            self.selected_unit = unit

            # Update investigator tile selection (only highlights if player unit)
            self._update_tile_selection()

            # Update action bar (only populates if player unit)
            self._update_action_bar()

            # Print team indicator for clarity
            team_indicator = "Player" if unit.team == "player" else "Enemy"
            print(f"Selected: {unit.name} ({team_indicator})")

    def _on_investigator_tile_click(self, investigator: Investigator):
        """
        Callback when an investigator tile is clicked.

        This is called by InvestigatorTile when the user clicks on it.
        Investigator tiles are for selecting units to command, so they
        only work during player turn. To view stats at any time, click
        units directly on the grid.

        Args:
            investigator: The investigator whose tile was clicked
        """
        # Only allow selection during player turn (tiles are for commanding units)
        if self.current_phase != "player_turn":
            return

        # Select the investigator
        self.selected_unit = investigator
        self._update_tile_selection()
        self._update_action_bar()
        print(f"Selected: {investigator.name} (Player)")

    def _update_tile_selection(self):
        """
        Update visual selection state of all investigator tiles.

        Called when selection changes (either from tile click or grid click).
        Ensures only the selected investigator's tile shows as selected.
        """
        for tile in self.investigator_tiles:
            if tile.investigator == self.selected_unit:
                tile.set_selected(True)
            else:
                tile.set_selected(False)

    def _update_action_bar(self):
        """
        Update action bar to show actions for current turn unit (not selected unit).

        The action bar displays actions only for the unit whose turn it is.
        Selecting other units for viewing does NOT change the action bar.

        Called whenever turn advances or turn unit changes.
        """
        if self.current_turn_unit and isinstance(self.current_turn_unit, Investigator):
            self.action_bar.update_for_investigator(self.current_turn_unit)
        else:
            self.action_bar.clear()

    def _pixel_to_grid(self, pixel_pos: Tuple[int, int]) -> Tuple[Optional[int], Optional[int]]:
        """
        Convert pixel coordinates (mouse position) to grid coordinates.

        Coordinate system explanation:
        - Screen coordinates: (0, 0) is top-left of entire window
        - Grid coordinates: (0, 0) is top-left of the grid
        - The grid is OFFSET from screen edges (centered horizontally, 100px from top)

        Example calculation:
        - Mouse at pixel (960, 300) on screen
        - Grid offset is (460, 100)
        - Grid-relative: (500, 200)
        - Tile size is 80px
        - Grid coordinate: (500//80, 200//80) = (6, 2)

        This method handles:
        1. Subtracting grid offset to get grid-relative position
        2. Bounds checking (is click inside grid?)
        3. Integer division to get tile indices

        Args:
            pixel_pos: (x, y) in screen pixel coordinates

        Returns:
            (grid_x, grid_y) if click is inside grid, or (None, None) if outside
        """
        px, py = pixel_pos

        # Step 1: Convert from screen coordinates to grid-relative coordinates
        # Subtract the grid's offset to get position relative to grid's top-left corner
        grid_px = px - self.grid_offset_x
        grid_py = py - self.grid_offset_y

        # Step 2: Bounds checking - is the click inside the grid?
        # Check if position is negative (click was to the left/above grid)
        if grid_px < 0 or grid_py < 0:
            return (None, None)

        # Check if position exceeds grid size (click was to the right/below grid)
        # grid_pixel_size = GRID_SIZE * TILE_SIZE = 10 * 80 = 800 pixels
        if grid_px >= self.grid_pixel_size or grid_py >= self.grid_pixel_size:
            return (None, None)

        # Step 3: Convert pixel position to tile index
        # Integer division: 150 pixels // 80 pixels_per_tile = tile 1
        grid_x = grid_px // config.TILE_SIZE
        grid_y = grid_py // config.TILE_SIZE

        return (grid_x, grid_y)

    def _grid_to_pixel(self, grid_x: int, grid_y: int) -> Tuple[int, int]:
        """
        Convert grid coordinates to pixel coordinates (top-left of tile).

        Reverse of _pixel_to_grid(). Used for rendering units and tiles.

        Example calculation:
        - Grid coordinate: (5, 3)
        - Tile size: 80px
        - Grid offset: (460, 100)
        - Pixel position: (460 + 5*80, 100 + 3*80) = (860, 340)

        This gives us the screen position to draw the tile at.
        For centered drawing (like unit symbols), we add TILE_SIZE//2
        to get the center of the tile.

        Args:
            grid_x: Grid X coordinate (0-9 for a 10x10 grid)
            grid_y: Grid Y coordinate (0-9 for a 10x10 grid)

        Returns:
            (pixel_x, pixel_y) of tile's top-left corner in screen coordinates
        """
        # Multiply grid position by tile size, then add grid offset
        pixel_x = self.grid_offset_x + (grid_x * config.TILE_SIZE)
        pixel_y = self.grid_offset_y + (grid_y * config.TILE_SIZE)
        return (pixel_x, pixel_y)

    def _cycle_unit_selection(self):
        """
        Cycle through player units with Tab key.

        Pressing Tab repeatedly cycles through all active (non-incapacitated)
        player units in order. When reaching the end of the list, wraps
        around to the first unit.

        Cycle behavior:
        - If no unit selected: Select first active unit
        - If unit selected: Select next active unit in list
        - If at end of list: Wrap to first unit (using modulo operator)

        Only works during player turn - can't cycle units during enemy phase.
        """
        # Only allow during player turn
        if self.current_phase != "player_turn":
            return

        # Get list of units that can still act (not incapacitated)
        # List comprehension filters out any units with can_act() == False
        active_units = [u for u in self.player_units if u.can_act()]

        if not active_units:
            # No units available to select (all incapacitated)
            return

        # Find which unit is currently selected and select the next one
        if self.selected_unit in active_units:
            # Get index of currently selected unit
            current_index = active_units.index(self.selected_unit)

            # Calculate next index with wrap-around using modulo
            # If current_index = 3 and len = 4: (3+1) % 4 = 0 (wraps to start)
            next_index = (current_index + 1) % len(active_units)

            # Select the next unit
            self.selected_unit = active_units[next_index]
        else:
            # No unit selected, or selected unit is incapacitated
            # Select first active unit
            self.selected_unit = active_units[0]

        # Update tile selection and action bar to match
        self._update_tile_selection()
        self._update_action_bar()

        print(f"Selected: {self.selected_unit.name}")

    def _advance_turn(self):
        """
        Advance to the next unit in turn order.

        Turn advancement process:
        1. Reset current unit's turn flags
        2. Move to next unit in turn order (skip incapacitated units)
        3. If end of turn order reached, increment round and wrap to start
        4. Update action bar to show current unit's actions
        5. Auto-select current turn unit

        If current unit is enemy, execute AI (future implementation).
        """
        if not self.turn_order:
            return

        # Reset current unit's turn flags
        if self.current_turn_unit:
            self.current_turn_unit.reset_turn_flags()

        # Find next active unit (skip incapacitated units)
        original_index = self.current_turn_index
        found_active_unit = False

        # Loop through all units to find next active one
        for i in range(len(self.turn_order)):
            # Calculate next index with wrap-around
            self.current_turn_index = (original_index + 1 + i) % len(self.turn_order)
            next_unit = self.turn_order[self.current_turn_index]

            # Check if unit can act (not incapacitated)
            if next_unit.can_act():
                self.current_turn_unit = next_unit
                found_active_unit = True
                break

        # If we wrapped around to the start, increment round
        if self.current_turn_index < original_index or (self.current_turn_index == 0 and original_index > 0):
            self.round_number += 1
            print(f"\n=== ROUND {self.round_number} ===")

        if not found_active_unit:
            # No active units remaining - battle should end
            print("No active units remaining")
            return

        # Auto-select the current turn unit for viewing
        self.selected_unit = self.current_turn_unit

        # Update UI
        self._update_tile_selection()
        self._update_action_bar()

        # Update turn order tracker with new current turn index
        self.turn_order_tracker.update_turn_order(self.turn_order, self.current_turn_index)

        # Update current_phase for compatibility (deprecated)
        self.current_phase = "player_turn" if self.current_turn_unit.team == "player" else "enemy_turn"

        # Print turn information
        team_str = "Player" if self.current_turn_unit.team == "player" else "Enemy"
        print(f"\n{team_str} Turn: {self.current_turn_unit.name}")

        # If enemy turn, execute AI (future implementation)
        if self.current_turn_unit.team == "enemy":
            # TODO: Execute enemy AI
            # For now, immediately skip to next turn
            print("  [AI not yet implemented - skipping enemy turn]")
            self._advance_turn()

    def _end_turn(self):
        """
        End current phase and switch to next phase.

        Turn structure:
        Player Turn → Enemy Turn → Player Turn (turn counter++) → ...

        Phase transition process:
        1. Reset all units' turn flags (has_moved, has_attacked)
        2. Switch phase
        3. Clear selection (for player → enemy transition)
        4. Increment turn counter (for enemy → player transition)
        5. Execute AI if enemy turn (Phase 1.5+)

        Currently (MVP):
        - Player turn: User can select and view units, but can't move/attack yet
        - Enemy turn: Immediately switches back (no AI implemented yet)

        Turn flags (reset each phase):
        - has_moved: Unit has used their movement action
        - has_attacked: Unit has used their attack action
        """
        if self.current_phase == "player_turn":
            # Ending player turn, switching to enemy turn

            # Reset all player unit action flags
            # This allows them to move and attack again next turn
            for unit in self.player_units:
                unit.reset_turn_flags()  # Sets has_moved = False, has_attacked = False

            # Switch to enemy turn
            self.current_phase = "enemy_turn"
            self.selected_unit = None  # Clear selection (enemies can't be selected by player)
            print("Enemy Turn")

            # TODO: Enemy AI actions in Phase 1.5
            # The AI will:
            # 1. For each active enemy unit:
            #    a. Calculate best move (toward nearest investigator)
            #    b. Move if possible
            #    c. Attack if in range
            # 2. Then call _end_turn() again to return to player

            # For now, immediately switch back to player turn (no AI yet)
            self._end_turn()

        elif self.current_phase == "enemy_turn":
            # Ending enemy turn, switching back to player turn

            # Reset all enemy unit action flags
            for unit in self.enemy_units:
                unit.reset_turn_flags()

            # Increment turn counter (only when full round completes)
            # Turn 1 = Player 1 + Enemy 1, Turn 2 = Player 2 + Enemy 2, etc.
            self.turn_number += 1

            # Switch back to player turn
            self.current_phase = "player_turn"
            print(f"Player Turn {self.turn_number}")

    def update(self) -> None:
        """Update battle state."""
        # Check win/lose conditions
        self._check_win_lose()

        # Get mouse position for hover effects
        self.mouse_pos = pygame.mouse.get_pos()

        # Update turn order tracker (hover effects for tooltips)
        self.turn_order_tracker.update(self.mouse_pos)

        # Update investigator tiles (hover effects)
        for tile in self.investigator_tiles:
            tile.update(self.mouse_pos)

        # Update action bar (hover effects)
        self.action_bar.update(self.mouse_pos)

        # Update end turn button (hover effects)
        self.end_turn_button.update(self.mouse_pos)

    def _check_win_lose(self):
        """
        Check if battle is won or lost.

        Win condition: All enemies incapacitated (health or sanity = 0)
        Lose condition: All investigators incapacitated

        Called every frame in update() to detect when battle ends.
        When a condition is met:
        1. Stop the game loop (self.running = False)
        2. Set next_screen to indicate result ("victory" or "defeat")
        3. main.py will detect this and show appropriate screen

        Phase 2+ may add more complex conditions:
        - Objective-based missions (reach extraction point, survive X turns)
        - Partial victory (some investigators survive)
        - Retreat option (voluntary withdrawal)
        """
        # Count active (non-incapacitated) units on each side
        # can_act() returns False if unit.is_incapacitated == True
        # sum() with generator expression counts how many units return True
        active_investigators = sum(1 for u in self.player_units if u.can_act())
        active_enemies = sum(1 for u in self.enemy_units if u.can_act())

        # Check victory condition
        if active_enemies == 0:
            # All enemies defeated - player wins!
            print("VICTORY! All enemies defeated.")
            self.running = False
            self.next_screen = "victory"

        # Check defeat condition
        elif active_investigators == 0:
            # All investigators down - player loses!
            print("DEFEAT! All investigators incapacitated.")
            self.running = False
            self.next_screen = "defeat"

        # If both have active units, battle continues

    def draw(self) -> None:
        """Render the battle screen."""
        # Clear screen
        self.screen.fill(config.COLOR_BG)

        # Draw turn order tracker (top of screen)
        # This now displays current turn info, so no separate header needed
        self.turn_order_tracker.draw(self.screen)

        # Draw investigator tiles panel (left side)
        for tile in self.investigator_tiles:
            tile.draw(self.screen)

        # Draw grid
        self._draw_grid()

        # Draw units
        self._draw_units()

        # Draw selection highlights
        # 1. Current turn unit (green) - always shown
        if self.current_turn_unit and self.current_turn_unit.position:
            self._draw_selection_highlight(self.current_turn_unit.position, is_current_turn=True)

        # 2. Selected unit for viewing (yellow) - only if different from current turn unit
        if self.selected_unit and self.selected_unit.position:
            if self.selected_unit != self.current_turn_unit:
                self._draw_selection_highlight(self.selected_unit.position, is_current_turn=False)

        # Draw unit info panel
        self._draw_unit_info_panel()

        # Draw action bar (bottom center)
        self.action_bar.draw(self.screen)

        # Draw end turn button
        self.end_turn_button.draw(self.screen)

        # Controls help disabled - action bar replaces it
        # self._draw_controls_help()

    def _draw_header(self):
        """Draw battle status header."""
        # Show current unit's turn
        if self.current_turn_unit:
            team_text = "Player" if self.current_turn_unit.team == "player" else "Enemy"
            turn_text = f"ROUND {self.round_number} | {team_text} Turn: {self.current_turn_unit.name}"
        else:
            turn_text = f"ROUND {self.round_number}"

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

            # Choose color based on team
            if unit.team == "player":
                symbol_color = config.COLOR_PLAYER  # Blue for investigators
            else:
                symbol_color = config.COLOR_ENEMY   # Red for enemies

            # Draw unit symbol with team color
            symbol_surface = self.font_large.render(unit.symbol, True, symbol_color)
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

    def _draw_selection_highlight(self, grid_pos: Tuple[int, int], is_current_turn: bool = False):
        """
        Draw highlight around selected/current turn unit.

        Highlights use different colors to indicate different states:
        - Green: Current turn unit (can act now)
        - Yellow: Selected for viewing (not their turn)

        Args:
            grid_pos: (x, y) grid coordinates
            is_current_turn: True if this is the current turn unit's highlight
        """
        x, y = grid_pos
        pixel_x, pixel_y = self._grid_to_pixel(x, y)

        # Choose color based on whether it's current turn or just viewing
        if is_current_turn:
            color = config.COLOR_CURRENT_TURN  # Green
        else:
            color = config.COLOR_SELECTED  # Yellow

        # Draw border
        highlight_rect = pygame.Rect(pixel_x, pixel_y, config.TILE_SIZE, config.TILE_SIZE)
        pygame.draw.rect(self.screen, color, highlight_rect, 3)

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
