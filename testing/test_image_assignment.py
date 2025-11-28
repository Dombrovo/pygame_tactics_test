"""
Test script for character image assignment system.

This script verifies that:
1. Images are correctly assigned to investigators
2. No image is used twice
3. Pool tracking works correctly
4. Reset functionality works
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from entities.investigator import (
    create_test_squad,
    get_image_pool_status,
    reset_image_pool,
    get_random_unused_image
)


def test_basic_assignment():
    """Test that images are assigned to a squad."""
    print("=" * 70)
    print("TEST 1: Basic Image Assignment")
    print("=" * 70)

    # Reset pool to start fresh
    reset_image_pool()

    # Create a test squad
    squad = create_test_squad()

    print(f"\nCreated squad of {len(squad)} investigators:\n")

    for i, inv in enumerate(squad, 1):
        print(f"{i}. {inv.name} ({inv.gender})")
        print(f"   Image: {inv.image_path}")
        print(f"   Stats: {inv.current_health}/{inv.max_health} HP, "
              f"{inv.accuracy}% acc, {inv.movement_range} move")
        print()

    # Check pool status
    status = get_image_pool_status()
    print("\nImage Pool Status:")
    for gender, stats in status.items():
        print(f"  {gender.capitalize()}: {stats['used']}/{stats['total']} used, "
              f"{stats['available']} available")

    return squad


def test_no_duplicates():
    """Test that no image is used twice."""
    print("\n" + "=" * 70)
    print("TEST 2: No Duplicate Images")
    print("=" * 70)

    # Reset pool
    reset_image_pool()

    # Create multiple squads to use more images
    all_investigators = []
    num_squads = 3

    print(f"\nCreating {num_squads} squads ({num_squads * 4} investigators total)...\n")

    for squad_num in range(num_squads):
        squad = create_test_squad()
        all_investigators.extend(squad)
        print(f"Squad {squad_num + 1}: Created {len(squad)} investigators")

    # Check for duplicate images
    male_images = []
    female_images = []

    for inv in all_investigators:
        if inv.gender == "male":
            male_images.append(inv.image_path)
        else:
            female_images.append(inv.image_path)

    # Check for duplicates
    male_duplicates = len(male_images) - len(set(male_images))
    female_duplicates = len(female_images) - len(set(female_images))

    print(f"\nDuplicate Check:")
    print(f"  Male images: {len(male_images)} assigned, {male_duplicates} duplicates")
    print(f"  Female images: {len(female_images)} assigned, {female_duplicates} duplicates")

    if male_duplicates == 0 and female_duplicates == 0:
        print("\n  [PASS] No duplicate images found!")
    else:
        print("\n  [FAIL] Duplicate images detected!")

    # Show pool status
    status = get_image_pool_status()
    print("\nFinal Image Pool Status:")
    for gender, stats in status.items():
        print(f"  {gender.capitalize()}: {stats['used']}/{stats['total']} used, "
              f"{stats['available']} available")


def test_pool_exhaustion():
    """Test what happens when we run out of images."""
    print("\n" + "=" * 70)
    print("TEST 3: Pool Exhaustion Handling")
    print("=" * 70)

    # Reset pool
    reset_image_pool()

    print("\nAttempting to assign images until pool is exhausted...")

    # Try to get all male images
    male_count = 0
    while True:
        image = get_random_unused_image("male")
        if image is None:
            break
        male_count += 1

    print(f"  Assigned {male_count} male images before exhaustion")

    # Try one more (should return None)
    extra = get_random_unused_image("male")
    if extra is None:
        print("  [PASS] Correctly returns None when pool exhausted")
    else:
        print("  [FAIL] Should have returned None!")

    # Show final status
    status = get_image_pool_status()
    print(f"\nMale pool: {status['male']['used']}/{status['male']['total']} used")


def test_reset_functionality():
    """Test that reset_image_pool() works correctly."""
    print("\n" + "=" * 70)
    print("TEST 4: Reset Functionality")
    print("=" * 70)

    # Use some images
    print("\nUsing 10 images...")
    for _ in range(10):
        gender = "male" if _ % 2 == 0 else "female"
        get_random_unused_image(gender)

    status_before = get_image_pool_status()
    print(f"Before reset:")
    print(f"  Male: {status_before['male']['used']} used")
    print(f"  Female: {status_before['female']['used']} used")

    # Reset
    print("\nResetting pool...")
    reset_image_pool()

    status_after = get_image_pool_status()
    print(f"\nAfter reset:")
    print(f"  Male: {status_after['male']['used']} used")
    print(f"  Female: {status_after['female']['used']} used")

    if status_after['male']['used'] == 0 and status_after['female']['used'] == 0:
        print("\n  [PASS] Pool correctly reset!")
    else:
        print("\n  [FAIL] Pool not properly reset!")


def main():
    """Run all tests."""
    print("\n")
    print("=" * 70)
    print("CHARACTER IMAGE ASSIGNMENT TESTS".center(70))
    print("=" * 70)

    test_basic_assignment()
    test_no_duplicates()
    test_pool_exhaustion()
    test_reset_functionality()

    print("\n" + "=" * 70)
    print("ALL TESTS COMPLETE")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
