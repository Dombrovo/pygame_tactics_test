"""
Quick test script to verify random name generation with nicknames.
"""

from entities.investigator import generate_random_name

print("Testing random name generation (50 samples):")
print("=" * 60)

nickname_count = 0
male_count = 0
female_count = 0

# Generate 50 names to see distribution
for i in range(50):
    name, gender = generate_random_name()

    # Count nicknames (they have single quotes)
    if "'" in name:
        nickname_count += 1
        print(f"{i+1:2d}. {name:40s} ({gender}) [NICKNAME]")
    else:
        print(f"{i+1:2d}. {name:40s} ({gender})")

    # Count gender
    if gender == "male":
        male_count += 1
    else:
        female_count += 1

print("=" * 60)
print(f"Statistics:")
print(f"  Male:     {male_count}/50 ({male_count/50*100:.1f}%)")
print(f"  Female:   {female_count}/50 ({female_count/50*100:.1f}%)")
print(f"  Nickname: {nickname_count}/50 ({nickname_count/50*100:.1f}%) [Expected ~30%]")
