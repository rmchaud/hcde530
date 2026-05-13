# W2 Context: Processing a CSV Data File

For the **competency 2** narrative (code literacy and documentation), see `week2.md`, which ties this folder’s artifacts together. This file is the **long-form companion** to `demo_word_count.py`: it explains flow and UX in prose; the script keeps **decision-level** comments so the two stay aligned.

## Purpose
This project demonstrates a clean, beginner-friendly way to process a CSV data file in Python and summarize text responses.

The script:
- loads participant responses from a CSV file,
- calculates word counts per response,
- prints a readable row-by-row table, and
- reports overall summary statistics (shortest, longest, average).

## Audience and Goal
This is written for students who may be new to coding. The goal is to make the logic easy to follow without turning the Python file into a wall of comments.

## Files in This Week
- `demo_responses.csv`: source data (participant ID, role, response text)
- `demo_word_count.py`: processing script
- `context.md`: this explanation file

## How to Run
From the repo root (`HCDE 530`):

```bash
python3 W2/demo_word_count.py
```

Or from inside `W2`:

```bash
python3 demo_word_count.py
```

## Script Walkthrough (By Section)

### 1) Load data from CSV
The script resolves `demo_responses.csv` next to `demo_word_count.py` using `Path(__file__)`, so it runs correctly from the **repo root** (`python3 W2/demo_word_count.py`) or from inside `W2/`. It reads the file with `csv.DictReader`, so each row is stored as a dictionary with column names as keys.

```python
from pathlib import Path

_DATA_DIR = Path(__file__).resolve().parent
filename = _DATA_DIR / "demo_responses.csv"
responses = []

with open(filename, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        responses.append(row)
```

Why this matters:
- It converts raw file rows into structured Python objects.
- It makes fields like `row["participant_id"]` and `row["response"]` easy to access later.
- Anchoring the path to the script avoids “file not found” surprises when the shell’s working directory is not `W2/`.

### 2) Define one focused helper function
The script defines `count_words()` to keep word counting logic in one place.

```python
def count_words(response):
    return len(response.split())
```

Why this matters:
- Keeping logic in a function improves readability and reuse.
- If your definition of a "word" changes later, you update one place.

### 3) Process each response row
The script loops through every participant response, counts words, and stores counts for later summary stats.

```python
for row in responses:
    participant = row["participant_id"]
    role = row["role"]
    response = row["response"]

    count = count_words(response)
    word_counts.append(count)
```

Why this matters:
- This is the core transformation step: raw text -> measurable feature (word count).
- It supports both per-row output and overall aggregate metrics.

### 4) Keep output readable with a preview
Long responses are truncated to the first 60 characters in the table output.

```python
if len(response) > 60:
    preview = response[:60] + "..."
else:
    preview = response
```

Why this matters:
- It improves scanability in terminal output.
- You can quickly inspect many rows without flooding the screen.

### 5) Compute summary statistics
After processing all rows, the script prints total responses and basic descriptive statistics.

```python
print(f"  Total responses : {len(word_counts)}")
print(f"  Shortest        : {min(word_counts)} words")
print(f"  Longest         : {max(word_counts)} words")
print(f"  Average         : {sum(word_counts) / len(word_counts):.1f} words")
```

Why this matters:
- These metrics give a quick quality check of the dataset.
- They help compare response length distributions at a glance.

## What "Effective Processing" Looks Like Here
In this script, effective processing means:
- **clear data flow**: load -> transform -> display -> summarize
- **separation of concerns**: helper function for counting, loop for orchestration
- **readable output**: aligned table and concise previews
- **actionable summary**: statistics that immediately describe the dataset

## UX Workflow Connection
For UX research/design practice, this pattern maps to a common synthesis workflow:
- collect open-ended feedback,
- create simple quantitative signals (like response length),
- keep qualitative context via text preview, and
- summarize the set before deeper thematic analysis.

This does not replace qualitative interpretation, but it helps you quickly orient to the data before diving deeper.

## Common Errors and Quick Fixes
- **"can't open file ... demo_word_count.py"**
  - You are in the wrong directory. Run from repo root with `python3 W2/demo_word_count.py`, or `cd W2` first.
- **"No such file or directory: ... demo_responses.csv"**
  - The script looks for the CSV **next to** `demo_word_count.py`. If you moved or renamed the data file, update the path logic or restore the default layout (`W2/demo_responses.csv` beside `W2/demo_word_count.py`).
- **Wrong Python command**
  - Use `python3` (not `python`) on systems where Python 2 might still be default.

## What to Try Next (Optional Extensions)
- Add median word count (in addition to average).
- Group by role and report average words per role.
- Export results to a new CSV or simple HTML report.
- Add basic error handling for missing or empty `response` values.
