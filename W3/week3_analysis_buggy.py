"""
Week 3 survey analysis: read messy CSV rows and print simple aggregates.

C3 focus: columns like experience_years mix formats (digits and words). Code
that assumes one shape can crash (ValueError) or, if it swallows errors,
produce plausible-looking but wrong averages. Satisfaction scores are numeric
but "top N" still depends on sort direction—wrong sort = wrong story, no crash.
"""

import csv
from pathlib import Path

# ---------------------------------------------------------------------------
# 1) Load CSV (path next to this file so runs work from repo root or W3/)
# ---------------------------------------------------------------------------
_DATA_DIR = Path(__file__).resolve().parent
filename = _DATA_DIR / "week3_survey_messy.csv"
rows = []

with open(filename, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

# ---------------------------------------------------------------------------
# 2) Count by role — inconsistent capitalization in the file is a data problem
# ---------------------------------------------------------------------------
role_counts = {}

for row in rows:
    # strip() removes stray spaces; title() merges "ux designer" with "UX Designer"
    raw_role = row["role"].strip()
    role = raw_role.title() if raw_role else "(missing role)"  # e.g. blank role but rest of row present
    if role in role_counts:
        role_counts[role] += 1
    else:
        role_counts[role] = 1

print("Responses by role:")
for role, count in sorted(role_counts.items()):
    print(f"  {role}: {count}")

# ---------------------------------------------------------------------------
# 3) Average experience — column mixes digits and at least one word ("fifteen")
# ---------------------------------------------------------------------------
total_experience = 0
valid_experience_count = 0
word_to_number = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
}

for row in rows:
    experience = row["experience_years"].strip().lower()
    if not experience:
        # Missing or blank: skip for average (explicit choice; document if policy changes)
        continue
    if experience.isdigit():
        total_experience += int(experience)
        valid_experience_count += 1
    elif experience in word_to_number:
        # Without this branch, int(experience) raises ValueError on words like "fifteen"
        total_experience += word_to_number[experience]
        valid_experience_count += 1

if valid_experience_count > 0:
    avg_experience = total_experience / valid_experience_count
    print(f"\nAverage years of experience: {avg_experience:.1f}")
else:
    print("\nAverage years of experience: N/A")

# ---------------------------------------------------------------------------
# 4) Top 5 satisfaction — scores are numeric; "top" means sort descending
# ---------------------------------------------------------------------------
scored_rows = []
for row in rows:
    if row["satisfaction_score"].strip():
        scored_rows.append((row["participant_name"], int(row["satisfaction_score"])))

# reverse=True: highest scores first; without it, "Top 5" would show the lowest scores
scored_rows.sort(key=lambda x: x[1], reverse=True)
top5 = scored_rows[:5]

print("\nTop 5 satisfaction scores:")
for name, score in top5:
    print(f"  {name}: {score}")
