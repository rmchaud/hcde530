"""
Week 2 demo: load survey-style CSV rows, derive a simple quantitative signal
(word count per response), and print both row-level and aggregate views.

Comments in this file focus on *decisions* (why this API, why this default),
not on restating column names—so a reader (or an AI assistant using the repo
as context) can see what must stay true if the script changes.
"""

import csv
from pathlib import Path

# ---------------------------------------------------------------------------
# 1) Load CSV into memory as structured rows
# ---------------------------------------------------------------------------
# Resolve CSV next to this script so `python3 W2/demo_word_count.py` works from
# repo root (as documented in context.md), not only after `cd W2`.
_DATA_DIR = Path(__file__).resolve().parent
filename = _DATA_DIR / "demo_responses.csv"
responses = []

with open(filename, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        responses.append(row)

# Why DictReader (not plain reader): keys come from the header row, so code
# below can use stable names like row["response"] instead of brittle column
# indices if column order in the CSV ever changes.


# ---------------------------------------------------------------------------
# 2) One helper: define what "word" means for this analysis
# ---------------------------------------------------------------------------
def count_words(response: str) -> int:
    """Count words using whitespace splits (same rule as Week 2 write-up).

    This is a deliberate, simple definition: punctuation attached to a token
    counts as part of the "word." If the research question later needs
    linguistic tokenization, this function is the single place to swap rules.
    """
    return len(response.split())


# ---------------------------------------------------------------------------
# 3) Per-row table: mix numeric summary with a short text preview
# ---------------------------------------------------------------------------
# Fixed column widths trade a little flexibility for scanability in a plain
# terminal—aligned columns are easier to skim than comma-separated prints.
print(f"{'ID':<6} {'Role':<22} {'Words':<6} {'Response (first 60 chars)'}")
print("-" * 75)

word_counts = []  # accumulate counts in loop order for summary stats below

for row in responses:
    participant = row["participant_id"]
    role = row["role"]
    response = row["response"]

    count = count_words(response)
    word_counts.append(count)

    # Preview cap: long strings dominate the terminal; 60 chars keeps context
    # visible while still signaling that more text exists (ellipsis).
    if len(response) > 60:
        preview = response[:60] + "..."
    else:
        preview = response

    print(f"{participant:<6} {role:<22} {count:<6} {preview}")

# ---------------------------------------------------------------------------
# 4) Dataset-level view: cheap sanity check after the pass over all rows
# ---------------------------------------------------------------------------
# These aggregates catch odd loads (e.g., all zeros) before deeper analysis.
# Average uses floating division; script assumes ≥1 row so len is non-zero.
print()
print("── Summary ─────────────────────────────────")
print(f"  Total responses : {len(word_counts)}")
print(f"  Shortest        : {min(word_counts)} words")
print(f"  Longest         : {max(word_counts)} words")
print(f"  Average         : {sum(word_counts) / len(word_counts):.1f} words")
