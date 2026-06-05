# Problem fit, verification, and public sharing

## Problem space → what this tool does

| Pain Points | How this tool helps |
|---------------------|---------------------|
| Hours hand-coding and grouping open-ended survey answers before synthesis | **Automates a first pass:** turns each detected long-text column into **theme clusters** (TF–IDF + K-means) and a **frequency-ranked table** so you see what repeats *before* deep qualitative coding. |
| Need feedback that guides the **next design iteration** | Output highlights **dominant themes**, **keywords**, and **representative quotes** per cluster—useful for “what should we change / keep?” conversations, not a substitute for contextual inquiry. |
| Data comes from **your own** surveys (any CSV) | **Auto-detect** open-ended columns from length/uniqueness heuristics, or **pin exact columns** with `--columns` when you know the headers. |

**Honest limits:** clusters are **statistical**, not the codebook. Short answers, sarcasm, and multilingual text need tighter `--columns` choices or future method upgrades. The value is **compression and triage**, not automated “truth.”

## Verification checklist (expected behavior)

Run from `W10/` (after `pip install -r requirements.txt`):

```bash
python survey_theme_report.py --input food_coded.csv --output theme_report.csv
```

**Expected:**

1. **Exit code 0**; stderr lists **auto-detected** text-heavy columns (on Food Choices: e.g. `comfort_food`, `diet_current`, …).
2. **`theme_report.csv`** exists with **exactly these columns:**  
   `theme_label`, `frequency`, `percent_of_total`, `representative_quotes`, `keywords`, `rank`
3. **Rows:** one row per cluster per analyzed column (Food Choices sample: on the order of **dozens** of rows, e.g. ~80 with default heuristics—not fixed forever).
4. **`rank`** runs 1…N in **global frequency order** (highest `frequency` first; ties broken by column name then label).
5. **`percent_of_total`** is **within that source column** (non-empty cells in that question); values are between 0 and 100.

Re-run with `--random-state 42` (default) for reproducible cluster assignments given the same CSV and options.

## “No install” Jupyter in the browser — what is realistic?

| Option | Audience experience | Notes |
|--------|----------------------|--------|
| **Google Colab** | Open a URL → run cells; **first cell** usually `%pip install pandas scikit-learn numpy` once per session | This is the most common “public notebook, low friction” path. See `survey_theme_report_demo.ipynb`. |
| **Binder** | Open badge URL → waits for build → Jupyter in browser | Needs `requirements.txt` (you have it) and sometimes a `environment.yml`; cold starts can be slow. |
| **JupyterLite** (WASM) | Pure browser, no server | **scikit-learn is not trivial** in Pyodide; the current stack is easier on **Colab/Binder** than Lite unless you rework to lighter deps. |
| **GitHub / nbviewer** | **Read-only** render of the notebook | Good for **viewing** write-ups; **does not execute** Python. |
