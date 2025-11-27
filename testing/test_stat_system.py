"""
Test script for the new stat system with base stats + modifiers.
"""

from entities.investigator import Investigator, generate_random_name

print("=" * 70)
print("STAT SYSTEM TEST - Base Stats + Modifiers Pattern")
print("=" * 70)

# Create a test investigator
name, gender = generate_random_name()
inv = Investigator(
    name=name,
    gender=gender,
    max_health=15,
    max_sanity=10,
    accuracy=75,
    will=5,
    movement_range=4
)

print(f"\n1. INITIAL STATE")
print(f"   Name: {inv.name} ({gender})")
print(f"   Base Stats:")
print(f"     - Health:   {inv.base_max_health}")
print(f"     - Sanity:   {inv.base_max_sanity}")
print(f"     - Accuracy: {inv.base_accuracy}%")
print(f"     - Will:     {inv.base_will}")
print(f"     - Movement: {inv.base_movement_range}")
print(f"\n   Effective Stats (base + modifiers):")
print(f"     - Health:   {inv.max_health} (modifier: {inv.max_health_modifier:+d})")
print(f"     - Sanity:   {inv.max_sanity} (modifier: {inv.max_sanity_modifier:+d})")
print(f"     - Accuracy: {inv.accuracy}% (modifier: {inv.accuracy_modifier:+d})")
print(f"     - Will:     {inv.will} (modifier: {inv.will_modifier:+d})")
print(f"     - Movement: {inv.movement_range} (modifier: {inv.movement_modifier:+d})")

# Apply some modifiers (simulating a background)
print(f"\n2. APPLYING MODIFIERS (simulating 'Soldier' background)")
print(f"   Changes: +10 accuracy, -1 max_sanity")
inv.apply_stat_modifiers(accuracy=10, max_sanity=-1)

print(f"\n   Effective Stats After Modifiers:")
print(f"     - Health:   {inv.max_health} (modifier: {inv.max_health_modifier:+d})")
print(f"     - Sanity:   {inv.max_sanity} (modifier: {inv.max_sanity_modifier:+d})")
print(f"     - Accuracy: {inv.accuracy}% (modifier: {inv.accuracy_modifier:+d})")
print(f"     - Will:     {inv.will} (modifier: {inv.will_modifier:+d})")
print(f"     - Movement: {inv.movement_range} (modifier: {inv.movement_modifier:+d})")
print(f"\n   Has modifiers? {inv.has_modifiers()}")

# Apply more modifiers (simulating a trait)
print(f"\n3. APPLYING MORE MODIFIERS (simulating 'Veteran' trait)")
print(f"   Changes: +2 will, +1 movement")
inv.apply_stat_modifiers(will=2, movement=1)

print(f"\n   Effective Stats After Additional Modifiers:")
print(f"     - Health:   {inv.max_health} (modifier: {inv.max_health_modifier:+d})")
print(f"     - Sanity:   {inv.max_sanity} (modifier: {inv.max_sanity_modifier:+d})")
print(f"     - Accuracy: {inv.accuracy}% (modifier: {inv.accuracy_modifier:+d})")
print(f"     - Will:     {inv.will} (modifier: {inv.will_modifier:+d})")
print(f"     - Movement: {inv.movement_range} (modifier: {inv.movement_modifier:+d})")

# Test negative modifiers (injury)
print(f"\n4. APPLYING NEGATIVE MODIFIERS (simulating 'Leg Wound' injury)")
print(f"   Changes: -2 max_health, -1 movement")
inv.apply_stat_modifiers(max_health=-2, movement=-1)

print(f"\n   Effective Stats After Injury:")
print(f"     - Health:   {inv.max_health} (modifier: {inv.max_health_modifier:+d})")
print(f"     - Sanity:   {inv.max_sanity} (modifier: {inv.max_sanity_modifier:+d})")
print(f"     - Accuracy: {inv.accuracy}% (modifier: {inv.accuracy_modifier:+d})")
print(f"     - Will:     {inv.will} (modifier: {inv.will_modifier:+d})")
print(f"     - Movement: {inv.movement_range} (modifier: {inv.movement_modifier:+d})")

# Test clamping
print(f"\n5. TESTING STAT CLAMPING")
inv.apply_stat_modifiers(accuracy=50)  # Should clamp at 95%
inv.apply_stat_modifiers(max_health=-100)  # Should clamp at 1
inv.apply_stat_modifiers(will=-50)  # Should clamp at 0

print(f"   After extreme modifiers:")
print(f"     - Accuracy: {inv.accuracy}% (should be clamped to 95%)")
print(f"     - Health:   {inv.max_health} (should be clamped to 1)")
print(f"     - Will:     {inv.will} (should be clamped to 0)")

print(f"\n6. FINAL SUMMARY")
print(f"   Base -> Effective (Change)")
print(f"     - Health:   {inv.base_max_health} -> {inv.max_health} ({inv.max_health_modifier:+d})")
print(f"     - Sanity:   {inv.base_max_sanity} -> {inv.max_sanity} ({inv.max_sanity_modifier:+d})")
print(f"     - Accuracy: {inv.base_accuracy}% -> {inv.accuracy}% ({inv.accuracy_modifier:+d})")
print(f"     - Will:     {inv.base_will} -> {inv.will} ({inv.will_modifier:+d})")
print(f"     - Movement: {inv.base_movement_range} -> {inv.movement_range} ({inv.movement_modifier:+d})")

print("\n" + "=" * 70)
print("[SUCCESS] STAT SYSTEM TEST COMPLETE")
print("=" * 70)
