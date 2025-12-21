"""
Test the new attack resolution popup display.

This script tests various attack scenarios to ensure the popup
shows all tactical information correctly.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pygame
import config
from ui.ui_elements import Popup


def test_attack_popup():
    """
    Test the new attack resolution popup with various scenarios.
    """
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Attack Popup Test")

    # Test scenarios
    scenarios = [
        {
            "name": "HIT - Normal damage with +2 card",
            "result": {
                "valid": True,
                "hit": True,
                "hit_chance": 65,
                "roll": 42,
                "card_drawn": "+2",
                "damage_dealt": 7,
                "sanity_damage": 0
            }
        },
        {
            "name": "HIT - Critical x2 card",
            "result": {
                "valid": True,
                "hit": True,
                "hit_chance": 75,
                "roll": 15,
                "card_drawn": "x2",
                "damage_dealt": 12,
                "sanity_damage": 0
            }
        },
        {
            "name": "HIT - With sanity damage (Hound attack)",
            "result": {
                "valid": True,
                "hit": True,
                "hit_chance": 85,
                "roll": 55,
                "card_drawn": "+1",
                "damage_dealt": 7,
                "sanity_damage": 5
            }
        },
        {
            "name": "HIT - NULL card (should still show as hit but 0 damage)",
            "result": {
                "valid": True,
                "hit": True,
                "hit_chance": 55,
                "roll": 30,
                "card_drawn": "NULL",
                "damage_dealt": 0,
                "sanity_damage": 0
            }
        },
        {
            "name": "MISS - Failed roll",
            "result": {
                "valid": True,
                "hit": False,
                "hit_chance": 45,
                "roll": 88,
                "card_drawn": "",
                "damage_dealt": 0,
                "sanity_damage": 0
            }
        },
        {
            "name": "MISS - Low hit chance",
            "result": {
                "valid": True,
                "hit": False,
                "hit_chance": 15,
                "roll": 67,
                "card_drawn": "",
                "damage_dealt": 0,
                "sanity_damage": 0
            }
        },
        {
            "name": "HIT - Enemy attack (no card)",
            "result": {
                "valid": True,
                "hit": True,
                "hit_chance": 50,
                "roll": 35,
                "card_drawn": "",
                "damage_dealt": 4,
                "sanity_damage": 0
            }
        }
    ]

    print("=" * 70)
    print("ATTACK POPUP TEST")
    print("=" * 70)
    print("\nThis test will display different attack result popups.")
    print("Press SPACE to advance to the next scenario.")
    print("Press ESC to quit.\n")

    scenario_index = 0
    running = True
    show_popup = True

    while running and scenario_index < len(scenarios):
        scenario = scenarios[scenario_index]

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    scenario_index += 1
                    show_popup = True

        # Clear screen
        screen.fill(config.COLOR_BG)

        # Draw scenario info at top
        font = pygame.font.Font(None, 36)
        title_text = f"Scenario {scenario_index + 1}/{len(scenarios)}: {scenario['name']}"
        title_surface = font.render(title_text, True, config.COLOR_TEXT_HIGHLIGHT)
        title_rect = title_surface.get_rect(center=(config.SCREEN_WIDTH // 2, 50))
        screen.blit(title_surface, title_rect)

        instruction_text = "Press SPACE for next scenario | ESC to quit"
        instruction_surface = font.render(instruction_text, True, config.COLOR_TEXT_DIM)
        instruction_rect = instruction_surface.get_rect(center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT - 50))
        screen.blit(instruction_surface, instruction_rect)

        # Show popup (non-blocking version for testing)
        if show_popup:
            # Draw the popup without blocking
            attack_result = scenario["result"]
            hit_chance = attack_result.get("hit_chance", 0)
            hit = attack_result.get("hit", False)
            roll = attack_result.get("roll", 0)
            card_drawn = attack_result.get("card_drawn", "")
            damage = attack_result.get("damage_dealt", 0)
            sanity_dmg = attack_result.get("sanity_damage", 0)

            # Build popup content
            lines = []
            lines.append(f"Hit Chance: {hit_chance}%")
            if hit:
                lines.append(f">>> HIT <<<")
                result_color = (100, 255, 100)
            else:
                lines.append(f">>> MISS <<<")
                result_color = (255, 100, 100)
            lines.append(f"Roll: {roll}/100")

            if hit:
                lines.append("")
                if card_drawn:
                    lines.append(f"Card: {card_drawn}")
                damage_text = f"Damage: {damage} HP"
                if sanity_dmg > 0:
                    damage_text += f" + {sanity_dmg} SAN"
                lines.append(damage_text)

            # Determine border color
            if not hit:
                border_color = (150, 50, 50)
            elif card_drawn and ("x2" in card_drawn.upper() or "X2" in card_drawn):
                border_color = (255, 200, 0)
            elif card_drawn and "NULL" in card_drawn.upper():
                border_color = (150, 50, 50)
            else:
                border_color = (100, 200, 100)

            # Draw popup
            popup_width = 600
            popup_height = 400
            popup_bg = (15, 15, 25)

            popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
            popup_surface.fill((*popup_bg, 220))
            pygame.draw.rect(popup_surface, border_color,
                           pygame.Rect(0, 0, popup_width, popup_height), 4)

            font_large = pygame.font.Font(None, 56)
            font_medium = pygame.font.Font(None, 44)
            font_small = pygame.font.Font(None, 36)

            y_offset = 30

            for i, line in enumerate(lines):
                if i == 0:
                    text_surface = font_medium.render(line, True, (200, 200, 220))
                elif i == 1:
                    text_surface = font_large.render(line, True, result_color)
                elif i == 2:
                    text_surface = font_medium.render(line, True, (200, 200, 220))
                elif line.startswith("Card:"):
                    text_surface = font_medium.render(line, True, (255, 200, 100))
                elif line.startswith("Damage:"):
                    text_surface = font_large.render(line, True, (255, 100, 100))
                elif line == "":
                    y_offset += 20
                    continue
                else:
                    text_surface = font_small.render(line, True, (220, 220, 230))

                text_rect = text_surface.get_rect(center=(popup_width // 2, y_offset + text_surface.get_height() // 2))
                popup_surface.blit(text_surface, text_rect)
                y_offset += text_surface.get_height() + 10

            popup_x = (screen.get_width() - popup_width) // 2
            popup_y = (screen.get_height() - popup_height) // 2
            screen.blit(popup_surface, (popup_x, popup_y))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()

    print("\nTest completed!")
    print("=" * 70)


if __name__ == "__main__":
    test_attack_popup()
