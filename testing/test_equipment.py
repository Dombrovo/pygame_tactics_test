"""
Test suite for the equipment system.

Tests:
- Equipment creation and properties
- Weapon equipping/unequipping
- Weapon stat delegation (damage, range, accuracy modifiers)
- Investigator default weapon assignment
- Enemy weapon assignment
- Unarmed combat (no weapon equipped)
"""

from entities.unit import Unit
from entities.investigator import Investigator, create_test_squad
from entities.enemy import Cultist, HoundOfTindalos
from entities import equipment


def test_equipment_creation():
    """Test creating equipment items."""
    print("\n=== Test: Equipment Creation ===")

    # Test weapon creation
    revolver = equipment.REVOLVER
    print(f"Weapon: {revolver.name}")
    print(f"  Damage: {revolver.damage}")
    print(f"  Range: {revolver.weapon_range}")
    print(f"  Type: {revolver.attack_type}")
    print(f"  Accuracy Modifier: {revolver.accuracy_modifier}")

    assert revolver.name == "Revolver"
    assert revolver.damage == 5
    assert revolver.weapon_range == 3
    assert revolver.attack_type == "ranged"
    assert revolver.accuracy_modifier == 0

    print("[OK] Equipment creation test passed")


def test_weapon_equipping():
    """Test equipping and unequipping weapons."""
    print("\n=== Test: Weapon Equipping ===")

    # Create a basic unit
    unit = Unit(
        name="Test Unit",
        max_health=15,
        max_sanity=10,
        accuracy=75,
        will=5,
        movement_range=4,
        team="player"
    )

    # Check unarmed stats
    print(f"\nUnarmed Stats:")
    print(f"  Damage: {unit.weapon_damage} (expected: 2)")
    print(f"  Range: {unit.weapon_range} (expected: 1)")
    print(f"  Type: {unit.attack_type} (expected: melee)")
    print(f"  Accuracy: {unit.accuracy}% (expected: 75)")

    assert unit.weapon_damage == 2
    assert unit.weapon_range == 1
    assert unit.attack_type == "melee"
    assert unit.accuracy == 75
    assert not unit.has_weapon()

    # Equip revolver
    unit.equip_weapon(equipment.REVOLVER)
    print(f"\nEquipped Revolver:")
    print(f"  Damage: {unit.weapon_damage} (expected: 5)")
    print(f"  Range: {unit.weapon_range} (expected: 3)")
    print(f"  Type: {unit.attack_type} (expected: ranged)")
    print(f"  Accuracy: {unit.accuracy}% (expected: 75)")

    assert unit.weapon_damage == 5
    assert unit.weapon_range == 3
    assert unit.attack_type == "ranged"
    assert unit.accuracy == 75
    assert unit.has_weapon()

    # Unequip weapon
    old_weapon = unit.unequip_weapon()
    print(f"\nUnequipped Weapon: {old_weapon.name}")
    print(f"  Back to unarmed damage: {unit.weapon_damage} (expected: 2)")

    assert old_weapon == equipment.REVOLVER
    assert unit.weapon_damage == 2
    assert not unit.has_weapon()

    print("[OK] Weapon equipping test passed")


def test_weapon_accuracy_modifiers():
    """Test that weapon accuracy modifiers affect total accuracy."""
    print("\n=== Test: Weapon Accuracy Modifiers ===")

    # Create investigator with 75 base accuracy
    inv = Investigator(
        name="Test Investigator",
        accuracy=75
    )

    # Test rifle (+10% accuracy)
    inv.equip_weapon(equipment.RIFLE)
    print(f"Rifle accuracy: {inv.accuracy}% (expected: 85)")
    print(f"  Base: 75, Rifle bonus: +10")
    assert inv.accuracy == 85

    # Test shotgun (-10% accuracy)
    inv.equip_weapon(equipment.SHOTGUN)
    print(f"Shotgun accuracy: {inv.accuracy}% (expected: 65)")
    print(f"  Base: 75, Shotgun penalty: -10")
    assert inv.accuracy == 65

    # Test tommy gun (-5% accuracy)
    inv.equip_weapon(equipment.TOMMY_GUN)
    print(f"Tommy Gun accuracy: {inv.accuracy}% (expected: 70)")
    print(f"  Base: 75, Tommy Gun penalty: -5")
    assert inv.accuracy == 70

    # Test accuracy clamping (5-95%)
    inv.base_accuracy = 100  # Try to exceed max
    inv.equip_weapon(equipment.RIFLE)  # +10
    print(f"Clamped accuracy: {inv.accuracy}% (expected: 95, not 110)")
    assert inv.accuracy == 95  # Clamped to 95%

    inv.base_accuracy = 0  # Try to go below min
    inv.equip_weapon(equipment.SHOTGUN)  # -10
    print(f"Clamped accuracy: {inv.accuracy}% (expected: 5, not -10)")
    assert inv.accuracy == 5  # Clamped to 5%

    print("[OK] Weapon accuracy modifier test passed")


def test_investigator_default_weapons():
    """Test that investigators spawn with weapons equipped."""
    print("\n=== Test: Investigator Default Weapons ===")

    squad = create_test_squad()

    # Expected weapons per role
    expected_weapons = [
        ("Revolver", 5, 3),     # Balanced
        ("Hunting Rifle", 6, 5), # Sniper
        ("Shotgun", 8, 2),       # Tank
        ("Revolver", 5, 3),      # Scout
    ]

    for i, inv in enumerate(squad):
        expected_name, expected_damage, expected_range = expected_weapons[i]
        print(f"\n{inv.name}:")
        print(f"  Weapon: {inv.equipped_weapon.name if inv.has_weapon() else 'None'}")
        print(f"  Damage: {inv.weapon_damage} (expected: {expected_damage})")
        print(f"  Range: {inv.weapon_range} (expected: {expected_range})")

        assert inv.has_weapon(), f"Investigator {i+1} has no weapon!"
        assert inv.equipped_weapon.name == expected_name
        assert inv.weapon_damage == expected_damage
        assert inv.weapon_range == expected_range

    print("[OK] Investigator default weapons test passed")


def test_enemy_weapons():
    """Test that enemies have weapons equipped."""
    print("\n=== Test: Enemy Weapons ===")

    # Test Cultist
    cultist = Cultist("Test Cultist")
    print(f"\nCultist:")
    print(f"  Weapon: {cultist.equipped_weapon.name}")
    print(f"  Damage: {cultist.weapon_damage} (expected: 4)")
    print(f"  Range: {cultist.weapon_range} (expected: 3)")
    print(f"  Type: {cultist.attack_type} (expected: ranged)")
    print(f"  Sanity Damage: {cultist.weapon_sanity_damage} (expected: 0)")

    assert cultist.has_weapon()
    assert cultist.equipped_weapon.name == "Cultist Pistol"
    assert cultist.weapon_damage == 4
    assert cultist.weapon_range == 3
    assert cultist.attack_type == "ranged"
    assert cultist.weapon_sanity_damage == 0

    # Test Hound
    hound = HoundOfTindalos("Test Hound")
    print(f"\nHound of Tindalos:")
    print(f"  Weapon: {hound.equipped_weapon.name}")
    print(f"  Damage: {hound.weapon_damage} (expected: 6)")
    print(f"  Range: {hound.weapon_range} (expected: 1)")
    print(f"  Type: {hound.attack_type} (expected: melee)")
    print(f"  Sanity Damage: {hound.weapon_sanity_damage} (expected: 5)")

    assert hound.has_weapon()
    assert hound.equipped_weapon.name == "Eldritch Claws"
    assert hound.weapon_damage == 6
    assert hound.weapon_range == 1
    assert hound.attack_type == "melee"
    assert hound.weapon_sanity_damage == 5

    print("[OK] Enemy weapons test passed")


def test_sanity_damage_weapons():
    """Test weapons that deal sanity damage."""
    print("\n=== Test: Sanity Damage Weapons ===")

    inv = Investigator(name="Test Investigator")

    # Test blessed blade (melee, sanity damage)
    inv.equip_weapon(equipment.BLESSED_BLADE)
    print(f"\nBlessed Blade:")
    print(f"  Health Damage: {inv.weapon_damage} (expected: 5)")
    print(f"  Sanity Damage: {inv.weapon_sanity_damage} (expected: 3)")
    print(f"  Range: {inv.weapon_range} (expected: 1)")
    print(f"  Type: {inv.attack_type} (expected: melee)")

    assert inv.weapon_damage == 5
    assert inv.weapon_sanity_damage == 3
    assert inv.weapon_range == 1
    assert inv.attack_type == "melee"

    # Test elder sign amulet (ranged, high sanity damage)
    inv.equip_weapon(equipment.ELDER_SIGN_AMULET)
    print(f"\nElder Sign Amulet:")
    print(f"  Health Damage: {inv.weapon_damage} (expected: 3)")
    print(f"  Sanity Damage: {inv.weapon_sanity_damage} (expected: 5)")
    print(f"  Range: {inv.weapon_range} (expected: 4)")
    print(f"  Type: {inv.attack_type} (expected: ranged)")
    print(f"  Accuracy: {inv.accuracy}% (expected: 65 = 75 base - 10 penalty)")

    assert inv.weapon_damage == 3
    assert inv.weapon_sanity_damage == 5
    assert inv.weapon_range == 4
    assert inv.attack_type == "ranged"
    assert inv.accuracy == 65  # 75 base - 10 penalty

    print("[OK] Sanity damage weapons test passed")


def test_weapon_library():
    """Test the weapon library helper functions."""
    print("\n=== Test: Weapon Library Functions ===")

    # Test get_weapon_by_name
    shotgun = equipment.get_weapon_by_name("Shotgun")
    print(f"Found weapon: {shotgun.name}")
    assert shotgun == equipment.SHOTGUN

    # Test case-insensitive lookup
    rifle = equipment.get_weapon_by_name("HUNTING RIFLE")
    print(f"Case-insensitive lookup: {rifle.name}")
    assert rifle == equipment.RIFLE

    # Test non-existent weapon
    nonexistent = equipment.get_weapon_by_name("Laser Gun")
    print(f"Non-existent weapon: {nonexistent}")
    assert nonexistent is None

    # Test get_all_investigator_weapons
    inv_weapons = equipment.get_all_investigator_weapons()
    print(f"Total investigator weapons: {len(inv_weapons)}")
    assert len(inv_weapons) >= 5  # At least 5 weapons

    # Test get_all_enemy_weapons
    enemy_weapons = equipment.get_all_enemy_weapons()
    print(f"Total enemy weapons: {len(enemy_weapons)}")
    assert len(enemy_weapons) >= 2  # At least 2 weapons

    print("[OK] Weapon library test passed")


def run_all_tests():
    """Run all equipment system tests."""
    print("=" * 60)
    print("EQUIPMENT SYSTEM TEST SUITE")
    print("=" * 60)

    test_equipment_creation()
    test_weapon_equipping()
    test_weapon_accuracy_modifiers()
    test_investigator_default_weapons()
    test_enemy_weapons()
    test_sanity_damage_weapons()
    test_weapon_library()

    print("\n" + "=" * 60)
    print("[OK] ALL EQUIPMENT TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
