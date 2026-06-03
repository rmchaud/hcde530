# MP2: Open-ended survey theme report

**Student:** Riya Chaudhari

---

## What it does

Many teams collect feedback with surveys, then export results as a **CSV spreadsheet** (the same kind of file you open in Excel or Google Sheets). **Open-ended** questions produce useful answers, but reading every row and grouping similar ideas by hand takes a long time. For example, after finishing data collection, a UX researcher might spend hours coding and grouping open-ended responses by hand before synthesis can begin. 

This tool **automates a first pass**:

1. **Reads** your survey CSV.
2. **Finds** columns that look like long written answers—or you can name specific columns.
3. **Groups** similar answers into **themes** using a standard text-mining approach (see **Method** below).
4. **Writes** a new CSV report: each row is one theme, **ranked by how often it appears**, with **keywords** and a few **example quotes** so you can skim “what keeps showing up” before deeper synthesis.

It does **not** replace careful reading or a proper qualitative codebook for high-stakes decisions. It **compresses repetition** and gives you a structured table you can sort, filter, and bring into a workshop or design review.

---

## Who it is for

**Primary audience:** UX researchers, designers, and students who:

- Run surveys to learn from participants,
- Export data as **CSV**,
- Want a **repeatable** way to summarize open-ended text **before** spending hours hand-tagging every response.

**Inputs:** Any survey-style CSV where at least some columns contain free-text answers.

**Outputs:** A single `theme_report.csv` (or any filename you choose) suitable for Excel, Google Sheets, or further analysis.

---

## Where to use it (public link — no install on your laptop)

The easiest way for others to run it **in a browser** is **Google Colab**: Colab provides a Python environment in the cloud; the demo notebook’s first cell installs the needed libraries for that session.

| What | Link (after you push) |
|------|------------------------|
| **Run in Google Colab** (recommended “live” use) | `https://colab.research.google.com/github/rmchaud/hcde530/blob/main/W10/survey_theme_report_demo.ipynb` |
| **View the notebook on GitHub** (read code + outputs if you commit them; running still uses Colab or local Jupyter) | `https://github.com/rmchaud/hcde530/blob/main/W10/survey_theme_report_demo.ipynb` |

**Open in Colab** button:

https://colab.research.google.com/github/rmchaud/hcde530/blob/main/W10/survey_theme_report_demo.ipynb

**What to do in Colab:** open the link → **Runtime → Run all** (or run cells top to bottom). Upload your own CSV if you are not using the sample file included in the repo. The notebook writes a theme report CSV you can download from the file browser.

---

## How to run it on your computer (command line)

Use this if you prefer a local Python install or are automating runs from a script.

### 1. Install

```bash
cd W10
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run

```bash
python survey_theme_report.py --input your_survey.csv --output theme_report.csv
```

Example with the included sample file:

```bash
python survey_theme_report.py --input food_coded.csv --output theme_report.csv
```

### Optional flags

| Flag | Meaning |
|------|--------|
| `--columns a,b,c` | Only these CSV headers (skip automatic detection of text columns) |
| `--n-clusters N` | Fixed number of themes (*K*) per column (default: chosen from row count) |
| `--min-rows N` | Ignore a column if it has fewer than *N* non-empty text cells (default: 10) |
| `--random-state INT` | Same number → same clustering result for the same data (default: 42) |

---

## What you get: output columns

The report is a CSV with these columns:

| Column | Meaning |
|--------|--------|
| `theme_label` | Short label, usually `[column name]` plus top keywords |
| `frequency` | How many responses fell in this theme |
| `percent_of_total` | Percent of **non-empty answers in that survey column** |
| `representative_quotes` | Up to three short example answers (separated by ` \| `) |
| `keywords` | Words/phrases that characterize the theme |
| `rank` | 1 = most frequent theme in the full report (ties broken in a stable way) |

---

## Method

The pipeline uses **TF–IDF** (word and two-word phrases) to turn text into numbers, then **K-means clustering** (in [scikit-learn](https://scikit-learn.org/)) to split answers into groups. Theme labels and keywords come from the strongest dimensions of each cluster; **representative quotes** are real answers closest to the cluster center in that numeric space. English **stop words** are removed by default.

---

## Sample data (Food Choices)

`food_coded.csv` is a public **Food Choices** survey-style export (125 rows) used to test the tool. It is not a UX product survey, but it has the same **shape** as many real files: mostly coded fields plus several long text columns.

- **Source:** [Food Choices on Kaggle](https://www.kaggle.com/datasets/borapajo/food-choices/data?select=food_coded.csv) 

On a typical run, the tool **auto-detects** text-heavy columns such as `comfort_food`, `diet_current`, and `ideal_diet`. Very short text columns may be skipped unless you pass `--columns`.

---

## Other files in this folder

| File | Purpose |
|------|--------|
| `survey_theme_report.py` | Main command-line program |
| `survey_theme_report_demo.ipynb` | Jupyter / Colab demo (same logic) |
| `requirements.txt` | Python dependencies |
| `PROBLEM_AND_PUBLISHING.md` | Extra notes on verification and sharing |
| `mp2.md` | Author’s competency claims reflection |
| `reflection.md` | Specification engineering documentation of the build |


---

## Limitations 

- Themes are **statistical clusters**, not the research codebook; labels are **keyword summaries** and can miss nuance (sarcasm, context, multilingual text).
- Auto-detection is a **heuristic**. If the wrong columns are picked up, use `--columns` with your exact header names.
- There is **no** built-in charting in v1 — the “visualization” is the **sorted table** you open in a spreadsheet.

If something breaks on a real export (encoding, odd line endings), the script tries several common CSV settings; if it still fails, try re-exporting UTF-8 CSV from your survey tool or open an issue with a **small** sample file (no personal data).
