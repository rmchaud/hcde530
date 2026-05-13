# Week 2 — Competency 2: Code Literacy & Documentation

This note captures observations about **competency 2** (code literacy and documentation) for HCDE 530. It mixes **personal reflection** with **evidence** of what I practiced this week.

## What competency 2 means to me here

Code literacy is not about memorizing syntax or writing large programs from scratch. For me it is closer to **evaluating and directing**: can I read enough of a script to judge whether it matches the question, spot fragile assumptions, and steer changes safely? **Documentation** is part of that control surface—it records *why* a choice was reasonable so I (or a collaborator, **including an AI tool working inside this repo**) do not have to reverse-engineer intent from behavior alone. Documentation belongs both **in** the script (where it anchors fragile or non-obvious decisions) and **beside** it in `context.md` (where narrative, run instructions, and UX framing belong without cluttering the code).

## Evidence from this week’s work

| Practice | How it showed up |
|----------|------------------|
| Explain code in plain language | `context.md` walks through `demo_word_count.py` by section, in beginner-friendly language, with short snippets only where they clarify the flow. |
| Useful comments, not comment overload | `demo_word_count.py` ties comments to **decisions**: why `DictReader` (stable field names if column order changes), why `newline=""` with the csv module, why the CSV path is anchored with `Path(__file__)` (matches documented runs from repo root), why word counting lives in one function (single place to change the definition of a “word”), why responses are truncated for display, and why summary stats close the loop as a quick data sanity check. |
| Document script logic outside the `.py` | `context.md` holds the narrative: purpose, run instructions, walkthrough, UX-relevant interpretation, common errors, optional extensions. |
| Readability of variables and output | Clear field names from the CSV, aligned table output, and truncated previews so terminal output stays scannable. |
| Run and validate behavior | Script executed from the correct working directory; output (per-row counts and summary stats) checked against expectations. |

## Connecting the reflection to the scripts (so the competency claim lands)

The table above is only convincing if it points to **concrete** places in the repo:

- **`demo_word_count.py` → “evaluate and direct.”** The module docstring states what must stay true if someone edits the file; section comments explain *why* each block exists (anchored CSV path via `Path(__file__)` so repo-root runs match `context.md`, dictionary-based access, preview length, summary as a sanity check). That is the kind of literacy I mean: you can **audit** the pipeline without running it blind.
- **`demo_word_count.py` → AI and documentation.** Instructor feedback noted that good documentation helps AI tools stay accurate in a project. Here, `context.md` carries goals and run paths, while in-file comments pin down ambiguous research choices—especially **what counts as a word** (`split()` rule called out in `count_words`). Together they reduce guesswork for any reader generating patches.
- **`context.md` → bridge between story and code.** It mirrors the same section structure as the script but in prose: purpose, walkthrough, UX link, errors. That file is the explicit evidence that I separated *narrative* from *implementation* on purpose, not only by default template wording.

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
