# Week 3 — Competency claims: C2 and C3

This week’s work uses **`week3_survey_messy.csv`** and **`week3_analysis_buggy.py`**. Together they support **code literacy (C2)** and **data cleaning and file handling (C3)**. The important shift from my earlier draft is that **C3 is not only “reading a traceback”**—it is recognizing when **messy real-world fields** make code that *runs* still produce **wrong summaries**, and cleaning or branching so results match what the column actually contains.

---

## C3 — Data cleaning and file handling

**What it means:** Loading messy real-world data with Python, finding what is broken, and fixing it so the script runs cleanly on any valid input. Reading error messages as diagnostic information. Writing scripts that produce consistent, repeatable output.

**What counts as evidence:**

| Requirement | Where it shows up |
|-------------|-------------------|
| Script reads a CSV | `week3_analysis_buggy.py` loads `week3_survey_messy.csv` with `csv.DictReader` (each row is a dictionary keyed by header names). |
| Real messy data | The survey mixes **role** capitalization (`ux designer`, `UX DESIGNER`, …), **experience_years** as mostly digits but also a **word** (`fifteen` for one row), **missing labels** (one row has empty `participant_name` and `role` but still has scores and text), and **sparse fields** generally. The script buckets an empty role as `(missing role)` so counts stay readable. |
| Traceback → diagnosis | **Bug 1:** A `ValueError` during experience parsing pointed at **non-numeric text** in `experience_years`. The error did not mean “Python is broken”; it meant **the column’s encoding of years did not match a single `int(...)` assumption**. |
| Repeatable output | After fixes, rerunning the script prints the same role counts, average experience, and **correct “top 5” satisfaction list** for the same CSV. |

### C3 framing: two different failure modes

**Bug 1 (experience years) — messy *values* vs the parser**

The `experience_years` column mostly contains digits (`3`, `8`, …) but also includes at least one **English word** (`fifteen`). Code that does `int(row["experience_years"])` assumes every cell is already an integer string. That assumption collides with the CSV: the traceback names the failing line and the **value that could not be coerced**, which is how I knew the fix belonged in **data handling** (normalize, branch, or map words to numbers), not in “trying again until it runs.”

If the script had instead **silently skipped** every non-digit without mapping words, it could have **run to completion** while **dropping a real participant’s years** from the average—still a **wrong result** driven by messy data. The point of the fix is to align the parser with **how respondents actually filled the field**.

**Bug 2 (top satisfaction) — messy *interpretation* even when digits look fine**

`satisfaction_score` values are numeric strings, so converting them with `int(...)` is straightforward. The bug was **logic**, not string shape: sorting **ascending** and then slicing the first five rows printed the **lowest** scores under a label that said **“Top 5.”** The script still “worked”; the output was **misleading for a stakeholder**. That is another C3 lesson: after data loads cleanly, **check that aggregates match the question** (here: “top” implies **descending** order, so `reverse=True`).

### Commit history as evidence

Git history for `W3/` records the sequence of understanding and repair, for example:

- **`1503aae`** — documents both bugs in one message: Bug 1 crash on parsing `experience_years` (non-numeric text / `ValueError`); Bug 2 reversed ranking logic fixed with **descending** sort (`reverse=True`).
- Follow-up commits add documentation and the competency write-up (`3d5a8ea`, `de32a2f`).

That trail is intentional: each message ties **symptom → cause → fix**, which is how I want future me (or a grader) to see that the fixes were **reasoned**, not random edits.

---

## C2 — Code literacy and documentation (still part of this week)

C2 here means I can **read** the script in order, **run** it to observe failures, **map** a traceback to the line and assumption that broke, and **document** why a change matches the data. Inline comments in `week3_analysis_buggy.py` call out decisions that matter for literacy—for example **role normalization** (`strip` + `title`) so differently capitalized titles aggregate correctly, and the **explicit branch** for digit vs word experience before averaging.

The **steepest debugging skill** this week was still **connecting runtime errors to code decisions** (Bug 1). C3 adds the complementary habit: **connecting output that “looks fine” back to the real survey fields** so we catch wrong rankings or biased averages (Bug 2 and the “silent skip” risk above).

---

## Related files (Week 3)

- `week3_survey_messy.csv` — messy survey-style input  
- `week3_analysis_buggy.py` — analysis script (reads CSV, prints summaries)  
