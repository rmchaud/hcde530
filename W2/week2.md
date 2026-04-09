# Week 2 — Competency 2: Code Literacy & Documentation

This note captures observations about **competency 2** (code literacy and documentation) for HCDE 530. It mixes **personal reflection** with **evidence** of what I practiced this week.

## What competency 2 means to me here

Code literacy is not about writing large programs—it is about **reading and shaping code enough to process data responsibly**, and **documenting** choices so someone else (or future me) can follow the logic. Documentation belongs both **in** the script (where it helps) and **beside** it (when explanations would clutter the code).

## Evidence from this week’s work

| Practice | How it showed up |
|----------|------------------|
| Explain code in plain language | `context.md` walks through `demo_word_count.py` by section, in beginner-friendly language, with short snippets only where they clarify the flow. |
| Useful comments, not comment overload | `demo_word_count.py` uses targeted comments (e.g., data loading, counting helper, key fields) without turning the file into a wall of text. |
| Document script logic outside the `.py` | `context.md` holds the narrative: purpose, run instructions, walkthrough, UX-relevant interpretation, common errors, optional extensions. |
| Readability of variables and output | Clear field names from the CSV, aligned table output, and truncated previews so terminal output stays scannable. |
| Run and validate behavior | Script executed from the correct working directory; output (per-row counts and summary stats) checked against expectations. |

## Reflection: what was hardest

The **steepest learning curve this week was setting up Cursor and Git**—initializing the repository, connecting to GitHub, handling a remote that already had commits, and learning when to run commands from the repo root versus inside `W2/`. That work is not “the assignment,” but it **unblocks** everything else: version history, sharing, and a stable place for documentation and code to live together.

## What I want to carry forward

- Keep **documentation split**: tight comments in code, fuller explanation in a companion file like `context.md`.
- Continue **validating** by running the script after changes and checking that paths and outputs still make sense.
- Treat **repo setup** as a repeatable skill—less scary each time.

## Related files (Week 2)

- `demo_word_count.py` — processing script  
- `demo_responses.csv` — sample data  
- `context.md` — section-by-section explanation and student-facing guidance  

---

*Written from interview responses: purpose (reflection + assignment evidence), competency 2 practices listed above, hardest part (Cursor/Git setup), location `W2/week2.md`.*
