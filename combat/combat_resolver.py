"""
Combat Resolution system for attack resolution.

This module handles the complete attack resolution process:
1. Calculate hit chance (accuracy - distance - cover)
2. Roll to hit
3. Draw combat card from deck (if attacker is investigator)
4. Apply card modifier to damage
5. Apply damage to target
6. Return detailed results for UI display

Integrates with:
- Line of sight system (combat/line_of_sight.py)
- Combat deck system (entities/combat_deck.py)
- Grid system (combat/grid.py)
- Unit stats (entities/unit.py)
"""

import random
from typing import Dict, Any, Optional, TYPE_CHECKING
from combat.grid import Grid
from combat.line_of_sight import has_line_of_sight, get_cover_between
from entities.unit import Unit
from entities.investigator import Investigator
import config

if TYPE_CHECKING:
    from entities.combat_deck import CombatDeck


def calculate_hit_chance(
    attacker: Unit,
    target: Unit,
    distance: float,
    cover_type: str
) -> int:
    """
    Calculate the final hit chance percentage.

    Formula:
    base_accuracy - distance_penalty - cover_penalty

    Args:
        attacker: The attacking unit
        target: The defending unit
        distance: Distance in tiles between attacker and target
        cover_type: Cover between them ("empty", "half_cover", "full_cover")

    Returns:
        Hit chance percentage (clamped between 5-95%)

    Example:
        >>> calculate_hit_chance(investigator, cultist, distance=3, cover="half_cover")
        45  # 75% base - 30% distance - 20% cover = 25% -> clamped to 45%
    """
    # Start with attacker's accuracy (already includes weapon modifier)
    base_chance = attacker.accuracy

    # Distance penalty: -10% per tile
    distance_penalty = int(distance) * config.DISTANCE_PENALTY_PER_TILE

    # Cover penalty
    cover_penalty = 0
    if cover_type == "half_cover":
        cover_penalty = config.HALF_COVER_BONUS
    elif cover_type == "full_cover":
        cover_penalty = config.FULL_COVER_BONUS

    # Calculate final chance
    final_chance = base_chance - distance_penalty - cover_penalty

    # Clamp between min and max (5-95%)
    final_chance = max(config.MIN_HIT_CHANCE, min(config.MAX_HIT_CHANCE, final_chance))

    return final_chance


def resolve_attack(
    attacker: Unit,
    target: Unit,
    grid: Grid,
    monster_deck: Optional["CombatDeck"] = None
) -> Dict[str, Any]:
    """
    Resolve a complete attack from attacker to target.

    This is the main entry point for combat resolution.

    Process:
    1. Verify attack is valid (range, LOS)
    2. Calculate hit chance
    3. Roll to hit (d100 vs hit chance)
    4. If miss: Return immediately (no card drawn)
    5. If hit: Draw combat card to modify damage
    6. Apply card modifier to damage (NULL sets damage to 0)
    7. Apply damage and return results

    Args:
        attacker: The attacking unit
        target: The defending unit
        grid: The battlefield grid (for LOS and distance)
        monster_deck: Optional universal monster deck (for enemy attacks)

    Returns:
        Dictionary with attack results:
        {
            "valid": bool,           # Was attack valid?
            "reason": str,           # If invalid, why?
            "hit": bool,             # Did attack hit?
            "hit_chance": int,       # Calculated hit chance %
            "roll": int,             # D100 roll (1-100)
            "distance": float,       # Distance in tiles
            "cover": str,            # Cover type
            "card_drawn": str,       # Card name (if using deck)
            "card_is_crit": bool,    # Was it a crit?
            "card_is_null": bool,    # Was it auto-miss?
            "base_damage": int,      # Weapon damage
            "final_damage": int,     # Damage after card modifier
            "damage_dealt": int,     # Actual damage dealt (clamped by HP)
            "sanity_damage": int,    # Sanity damage dealt
            "target_killed": bool,   # Did target die?
        }

    Example:
        >>> result = resolve_attack(investigator, cultist, grid)
        >>> if result["hit"]:
        >>>     print(f"Hit for {result['damage_dealt']} damage!")
    """
    # Validate positions
    if not attacker.position or not target.position:
        return {
            "valid": False,
            "reason": "attacker or target not on grid"
        }

    attacker_pos = attacker.position
    target_pos = target.position

    # Calculate distance
    distance = grid.get_distance(attacker_pos[0], attacker_pos[1],
                                 target_pos[0], target_pos[1])

    # Check range
    if distance > attacker.weapon_range:
        return {
            "valid": False,
            "reason": "out_of_range",
            "distance": distance,
            "weapon_range": attacker.weapon_range
        }

    # Check line of sight
    if not has_line_of_sight(attacker_pos, target_pos, grid):
        return {
            "valid": False,
            "reason": "no_line_of_sight"
        }

    # Determine cover
    cover_type = get_cover_between(attacker_pos, target_pos, grid)

    # Calculate hit chance
    hit_chance = calculate_hit_chance(attacker, target, distance, cover_type)

    # Roll to hit (1-100)
    roll = random.randint(1, 100)

    # Initialize result dictionary
    result = {
        "valid": True,
        "hit_chance": hit_chance,
        "roll": roll,
        "distance": distance,
        "cover": cover_type,
        "base_damage": attacker.weapon_damage,
        "sanity_damage": 0,
        "card_drawn": None,
        "card_is_crit": False,
        "card_is_null": False,
    }

    # Check if attack hit (d100 roll)
    hit = roll <= hit_chance

    if not hit:
        # Miss - no damage, no card drawn
        result["hit"] = False
        result["final_damage"] = 0
        result["damage_dealt"] = 0
        result["target_killed"] = False
        return result

    # Attack hit! Now draw combat card to determine damage modifier
    # - Investigators draw from their personal deck
    # - Enemies draw from the universal monster deck (if provided)
    card = None
    if isinstance(attacker, Investigator):
        # Investigator: draw from personal deck
        card = attacker.draw_combat_card()
        if card:
            result["card_drawn"] = card.name
            result["card_is_crit"] = card.is_multiply()
            result["card_is_null"] = card.is_null()
    elif monster_deck:
        # Enemy: draw from universal monster deck
        card = monster_deck.draw()
        if card:
            result["card_drawn"] = card.name
            result["card_is_crit"] = card.is_multiply()
            result["card_is_null"] = card.is_null()

    # Hit! Calculate damage
    base_damage = attacker.weapon_damage

    # Apply combat card modifier (if card was drawn)
    # NULL card will set damage to 0 via apply_to_damage()
    if card:
        final_damage = card.apply_to_damage(base_damage)
    else:
        final_damage = base_damage

    # Apply damage to target
    damage_dealt = target.take_damage(final_damage)

    # Apply sanity damage (if weapon has it)
    sanity_damage_dealt = 0
    if attacker.weapon_sanity_damage > 0:
        sanity_damage_dealt = target.take_sanity_damage(attacker.weapon_sanity_damage)

    # Check if target was killed
    target_killed = target.is_incapacitated

    # Update result
    result["hit"] = True
    result["final_damage"] = final_damage
    result["damage_dealt"] = damage_dealt
    result["sanity_damage"] = sanity_damage_dealt
    result["target_killed"] = target_killed

    return result


def format_attack_result(
    attacker: Unit,
    target: Unit,
    result: Dict[str, Any]
) -> str:
    """
    Format attack result as a human-readable string for console/UI display.

    Args:
        attacker: The attacking unit
        target: The defending unit
        result: Result dictionary from resolve_attack()

    Returns:
        Formatted string describing the attack outcome

    Example:
        >>> msg = format_attack_result(inv, cultist, result)
        >>> print(msg)
        "John Doe attacks Cultist Alpha (3 tiles, half cover)
         Drew +1 card - Hit! (Roll: 45 vs 55% chance)
         Dealt 6 damage (5 base +1 card)
         Cultist Alpha: 4/10 HP"
    """
    lines = []

    # Header: "Attacker attacks Target (distance, cover)"
    cover_str = result.get("cover", "no cover")
    distance_str = f"{result.get('distance', 0):.1f} tiles"
    lines.append(f"{attacker.name} attacks {target.name} ({distance_str}, {cover_str})")

    # Check if attack was invalid
    if not result.get("valid", False):
        reason = result.get("reason", "unknown")
        if reason == "out_of_range":
            weapon_range = result.get("weapon_range", 0)
            distance = result.get("distance", 0)
            lines.append(f"  [!] OUT OF RANGE (distance: {distance:.1f}, max: {weapon_range})")
        elif reason == "no_line_of_sight":
            lines.append(f"  [!] NO LINE OF SIGHT")
        else:
            lines.append(f"  [!] INVALID ATTACK ({reason})")
        return "\n".join(lines)

    # Card drawn (if investigator)
    if result.get("card_drawn"):
        card_name = result["card_drawn"]
        if result.get("card_is_null"):
            lines.append(f"  Drew {card_name} - NO DAMAGE!")
        elif result.get("card_is_crit"):
            lines.append(f"  Drew {card_name} - CRITICAL HIT!")
        else:
            lines.append(f"  Drew {card_name}")

    # Hit or miss
    hit = result.get("hit", False)
    roll = result.get("roll", 0)
    hit_chance = result.get("hit_chance", 0)

    if hit:
        lines.append(f"  HIT! (Roll: {roll} vs {hit_chance}% chance)")

        # Damage breakdown
        base_damage = result.get("base_damage", 0)
        final_damage = result.get("final_damage", 0)
        damage_dealt = result.get("damage_dealt", 0)

        if result.get("card_drawn") and not result.get("card_is_crit"):
            modifier = final_damage - base_damage
            modifier_str = f"{modifier:+d}" if modifier != 0 else ""
            lines.append(f"  Dealt {damage_dealt} damage ({base_damage} base {modifier_str} card)")
        else:
            lines.append(f"  Dealt {damage_dealt} damage")

        # Sanity damage
        sanity_damage = result.get("sanity_damage", 0)
        if sanity_damage > 0:
            lines.append(f"  + {sanity_damage} sanity damage!")

        # Target status
        if result.get("target_killed"):
            lines.append(f"  {target.name} INCAPACITATED!")
        else:
            lines.append(f"  {target.name}: {target.current_health}/{target.max_health} HP")

    else:
        lines.append(f"  MISS (Roll: {roll} vs {hit_chance}% chance)")

    return "\n".join(lines)


def get_attack_preview(
    attacker: Unit,
    target: Unit,
    grid: Grid
) -> Dict[str, Any]:
    """
    Get attack preview information without actually attacking.

    Useful for showing hit chance to player before confirming attack.

    Args:
        attacker: The attacking unit
        target: The target unit
        grid: The battlefield grid

    Returns:
        Dictionary with preview info:
        {
            "valid": bool,
            "reason": str,
            "hit_chance": int,
            "distance": float,
            "cover": str,
            "base_damage": int,
            "min_damage": int,  # With worst card (-1)
            "max_damage": int,  # With best card (x2)
        }
    """
    # Validate positions
    if not attacker.position or not target.position:
        return {
            "valid": False,
            "reason": "not on grid"
        }

    attacker_pos = attacker.position
    target_pos = target.position

    # Calculate distance
    distance = grid.get_distance(attacker_pos[0], attacker_pos[1],
                                 target_pos[0], target_pos[1])

    # Check range
    if distance > attacker.weapon_range:
        return {
            "valid": False,
            "reason": "out_of_range",
            "distance": distance,
            "weapon_range": attacker.weapon_range
        }

    # Check line of sight
    if not has_line_of_sight(attacker_pos, target_pos, grid):
        return {
            "valid": False,
            "reason": "no_line_of_sight"
        }

    # Determine cover
    cover_type = get_cover_between(attacker_pos, target_pos, grid)

    # Calculate hit chance
    hit_chance = calculate_hit_chance(attacker, target, distance, cover_type)

    # Calculate damage range
    base_damage = attacker.weapon_damage
    min_damage = max(0, base_damage - 1)  # Worst card: -1
    max_damage = base_damage * 2          # Best card: x2

    return {
        "valid": True,
        "hit_chance": hit_chance,
        "distance": distance,
        "cover": cover_type,
        "base_damage": base_damage,
        "min_damage": min_damage,
        "max_damage": max_damage,
    }
