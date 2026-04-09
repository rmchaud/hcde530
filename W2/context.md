# W2 Context: Processing a CSV Data File

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
The script starts by reading `demo_responses.csv` with `csv.DictReader`, so each row is stored as a dictionary with column names as keys.

```python
filename = "demo_responses.csv"
responses = []

with open(filename, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        responses.append(row)
```

Why this matters:
- It converts raw file rows into structured Python objects.
- It makes fields like `row["participant_id"]` and `row["response"]` easy to access later.

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
- **"No such file or directory: demo_responses.csv"**
  - The script expects the CSV in the current working directory. Run from `W2`, or update the script to use a full/relative path intentionally.
- **Wrong Python command**
  - Use `python3` (not `python`) on systems where Python 2 might still be default.

## What to Try Next (Optional Extensions)
- Add median word count (in addition to average).
- Group by role and report average words per role.
- Export results to a new CSV or simple HTML report.
- Add basic error handling for missing or empty `response` values.
