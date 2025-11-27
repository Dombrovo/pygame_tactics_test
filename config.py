"""
Game configuration and constants for Eldritch Tactics

This file serves as a CENTRALIZED CONFIGURATION SYSTEM.
Instead of scattering magic numbers throughout the codebase, we define
all constants here. This makes the game easy to balance and modify.

Benefits:
- Change button width once, affects all buttons everywhere
- Easy to test different resolutions or color schemes
- No hunting through code to find hardcoded values
- Clear documentation of all game parameters
"""

# ============================================================================
# DISPLAY SETTINGS
# ============================================================================
# These control the game window and rendering

# Resolution settings
SCREEN_WIDTH = 1920   # Horizontal resolution in pixels
SCREEN_HEIGHT = 1080  # Vertical resolution in pixels

# Available resolutions (width, height) tuples
AVAILABLE_RESOLUTIONS = [
    (1280, 720),   # 720p HD
    (1920, 1080),  # 1080p Full HD (default)
    (2560, 1440),  # 1440p 2K
]

FULLSCREEN = True     # True = fullscreen, False = windowed mode
FPS = 60              # Target frames per second (60 is standard for smooth gameplay)
SHOW_FPS = False      # Display FPS counter in battles (for debugging/performance monitoring)

# Visual style setting
# Options: "ascii", "emoji", "image" (image sprites not yet implemented)
VISUAL_STYLE = "emoji"  # Default to emoji if available

# ============================================================================
# GRID SETTINGS (for tactical combat - Phase 1)
# ============================================================================
# The tactical battlefield will be a grid of tiles

GRID_SIZE = 10   # 10x10 grid (100 tiles total)
TILE_SIZE = 80   # Each tile is 80x80 pixels (adjusted for 1920x1080)

# ============================================================================
# COLORS - Dark, Moody Palette for Lovecraftian Theme
# ============================================================================
# Colors in Pygame use RGB tuples: (Red, Green, Blue)
# Each value ranges from 0-255, where 0 is darkest and 255 is brightest
# Examples:
#   (255, 0, 0) = Pure red
#   (0, 255, 0) = Pure green
#   (0, 0, 255) = Pure blue
#   (255, 255, 255) = White
#   (0, 0, 0) = Black
#   (128, 128, 128) = Medium gray

# Background Colors
COLOR_BG = (15, 15, 25)         # Very dark blue-black (main background)
COLOR_UI_BG = (25, 25, 35)      # Slightly lighter for UI panels

# Text Colors
COLOR_TEXT = (220, 220, 230)              # Off-white for readability
COLOR_TEXT_HIGHLIGHT = (255, 200, 100)    # Golden highlight for selected/hovered items
COLOR_TEXT_DIM = (120, 120, 130)          # Dimmed text for less important info

# Menu Button Colors (creates hover effect through color transitions)
COLOR_MENU_BUTTON = (40, 40, 60)          # Normal state - dark blue-gray
COLOR_MENU_BUTTON_HOVER = (60, 60, 90)    # Hovered state - lighter blue-gray
COLOR_MENU_BUTTON_ACTIVE = (80, 80, 120)  # Pressed state - brightest blue-gray
COLOR_MENU_BORDER = (100, 100, 140)       # Border color for all buttons

# Game Colors (for tactical combat - Phase 1 and beyond)
COLOR_GRID = (50, 50, 60)             # Grid lines on battlefield
COLOR_PLAYER = (100, 150, 255)        # Player unit highlight (blue)
COLOR_ENEMY = (255, 100, 100)         # Enemy unit highlight (red)
COLOR_SELECTED = (255, 255, 100)      # Currently selected unit (yellow)
COLOR_VALID_MOVE = (100, 255, 100)    # Valid movement tiles (green)
COLOR_ATTACK_RANGE = (255, 100, 100)  # Attack range indicator (red)

# ============================================================================
# COMBAT CONSTANTS (for tactical battle system - Phase 1)
# ============================================================================
# These define the combat math for hit chances and damage

BASE_HIT_CHANCE = 75           # Starting accuracy % before modifiers
DISTANCE_PENALTY_PER_TILE = 10 # Lose 10% accuracy per tile of distance
HALF_COVER_BONUS = 20          # Half cover gives -20% hit chance to attacker
FULL_COVER_BONUS = 40          # Full cover gives -40% hit chance to attacker
MIN_HIT_CHANCE = 5             # Minimum possible hit chance (always some chance to miss)
MAX_HIT_CHANCE = 95            # Maximum possible hit chance (always some chance to hit)

# ============================================================================
# BALANCE CONSTANTS (for campaign meta-layer - Phase 2+)
# ============================================================================
# These control squad sizes, resources, and campaign progression

PLAYER_STARTING_SQUAD_SIZE = 4  # How many investigators in a mission
PLAYER_MAX_ROSTER = 12          # Total investigators you can recruit
STARTING_FUNDS = 1000           # Starting money for buying equipment
MISSION_REWARD_BASE = 200       # Base reward for completing a mission

# ============================================================================
# FONT SIZES
# ============================================================================
# Consistent font sizes throughout the UI
# Larger number = bigger text

FONT_SIZE_TITLE = 120   # Main title screen heading
FONT_SIZE_LARGE = 72    # Section headings
FONT_SIZE_MEDIUM = 48   # Buttons and important text
FONT_SIZE_SMALL = 36    # Body text
FONT_SIZE_TINY = 24     # Version numbers, fine print

# ============================================================================
# UI CONSTANTS
# ============================================================================
# Standard dimensions for UI elements (ensures consistency)

MENU_BUTTON_WIDTH = 400    # All menu buttons are this wide
MENU_BUTTON_HEIGHT = 80    # All menu buttons are this tall
MENU_BUTTON_SPACING = 30   # Vertical gap between buttons
