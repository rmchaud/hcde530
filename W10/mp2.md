# Mini Project 2 — Competency Claims 

**Student:** Riya Chaudhari
**Project:** Open-ended survey theme report

---

## How this project maps to competency claims

Below are the claims I can support with **concrete evidence in this repo**. 

### C2 — Code literacy and documentation

**What this means to me:** Comments that explain *why*, docstrings, README, and a markdown explanation for non-technical readers. Code literacy means I can read my own Python script, explain the purpose of each section, and make updates without breaking it. Documentation means writing comments and explanations so another person (or future me) can quickly understand the logic and decisions. It is meant to support and facilitate that understanding.

**Evidence:**

- **`survey_theme_report.py`** — Inline comments explain design choices (for example, why the CSV loader tries multiple encodings and line endings; why numeric-heavy columns are filtered out; how cluster labels map back to real quotes). Functions such as `detect_open_ended_columns` include a **docstring** describing the heuristic intent, and helpers like `_numeric_fraction` document what they return.
- **`README.md`** — How to install, run the CLI, interpret output columns, and understand limitations.
- **`PROBLEM_AND_PUBLISHING.md`** — Problem framing, verification checklist, and how someone might share the work publicly later.
- **This file (`mp2.md`)** — Plain-language explanation of the tool for readers who will not read Python first.

---

### C3 — Data cleaning and file handling

**What this means to me:** Load messy real-world data; handle missing or inconsistent values; read errors diagnostically; repeatable output. This competency is about reading messy CSV data from the real world, identifying problems, fixing them in code, and producing repeatable output every time the script runs.

**Evidence:**

- **Reads from CSV, not hardcoded rows** — `read_survey_csv()` uses `pandas.read_csv` on a path you pass in (`--input`).
- **Inconsistent formatting** — The loader loops over encodings (`utf-8`, `latin-1`, `cp1252`) and line terminators (`\r`, `\n`, `\r\n`) because real files differ by platform and export settings.
- **Missing / placeholder text** — `_cell_as_text()` treats empty strings, stringified `"nan"`, `"none"`, and actual `NaN` as “no answer” so empty cells do not pollute clustering.
- **Mixed numeric + text survey grids** — `_numeric_fraction()` plus length/uniqueness rules in `detect_open_ended_columns()` reduce the chance that Likert-style numeric columns are mistaken for prose fields.
- **Repeatable output** — Same flags and `--random-state` yield the same theme table for the same CSV, which matters when you want to compare runs after changing survey wording.

**Traceback / diagnosis (example):** While wiring the Jupyter demo, passing a full synthetic `sys.argv` list that **included the script name** as the first token caused `argparse` to report an **“unrecognized arguments”** error. The error pointed at the extra first token. The fix was to pass only the flag tokens (`["--input", …, "--output", …]`) into `parse_args`, which matches how `argparse` expects an explicit argument list. That is a small example of **reading the error literally** and aligning the call pattern with the library contract.

---

### C5 — Data analysis with pandas

**What this means to me:** Use pandas to answer a question; at least two operations; interpret results in words. C5 means using pandas operations intentionally to answer the three specific analytical questions that I detailed above, and then interpreting what the output says about the data.

**Analytical question this tool supports:** *“Across my open-ended survey columns, what recurring themes show up most often, and what language do participants actually use?”*

**Pandas operations (examples from the script):**

1. **`pd.read_csv`** — Loads the survey table into a `DataFrame`.
2. **`pd.DataFrame(...)` / `sort_values` / column selection** — Assembles cluster results into a single report table, sorts themes by frequency (with tie-breakers), assigns `rank`, and exports a consistent column set.

**Interpretation (not just output):** The exported `theme_report.csv` is meant to be read as **relative emphasis**, not ground truth. High `frequency` with coherent `keywords` and `representative_quotes` suggests a cluster worth discussing in a readout; low-frequency clusters may be noise or long-tail opinions that still matter qualitatively even if they are rare.

---

### C7 — Critical evaluation and professional judgment

**What this means to me:** Evaluate automated output; say what you would verify before showing a client.

**What I would not ship unchecked:** Theme labels are **keyword summaries** derived from cluster centroids. They can look convincing while **flattening nuance** (sarcasm, cultural context, multilingual responses, or harm-related content that should be handled with care). I would not present the CSV alone as “what users believe” without spot-checking quotes and, where stakes are high, doing proper coding with a defined codebook.

**Override / supplement decisions built into the tool:**

- **`--columns`** lets a researcher **override** auto-detection when they know which headers are truly open-ended.
- **`--min-rows`**, **`--n-clusters`**, **`--random-state`** exist because I judged that a one-size-fits-all clustering setting would mislead users with very small *n* or very different survey designs.

**Confidence I would state to a stakeholder:** “This is a **fast exploratory** pass that highlights repetition and language patterns. Treat it as **prioritized reading homework**, not a decision engine.”

---

### C8 — Building and shipping a complete tool (scoped honestly)

**What I built:** A **CLI** (`survey_theme_report.py`) plus **`requirements.txt`**, **`README.md`**, a **demo notebook** (`survey_theme_report_demo.ipynb`), and supporting notes (`PROBLEM_AND_PUBLISHING.md`). Together these are a **complete, runnable mini-product** for the stated HCD use case: CSV in → ranked theme report out.

**One thing that went wrong and how I handled it:** Early clustering runs on messy exports made it obvious that **“works on my machine” CSV assumptions break quickly**. Rather than only documenting “use UTF-8,” I changed the loader to **try realistic combinations** and to treat placeholder text as missing. That aligns with real file-handling practice: **assume less, validate more**.

