# Mini Project 1 — Competency Claims

**Student:** Riya Chaudhari  
**Project:** Open Brewery DB analysis (`W7/week6_mp1_starter.ipynb`)

---

## C3 — Data cleaning and file handling

I demonstrated C3 by turning messy API JSON into a repeatable analysis-ready table. In the notebook’s load cell, I paginate Open Brewery DB, keep only `United States` rows, drop records missing `state`, `city`, or `brewery_type`, and normalize text with `.str.strip()` so groupings are consistent—the same cleaning pipeline I built in `W4/open_brewery_to_csv.py` and `W5/brewery_type_analysis.py`. In Week 4 I also handled real acquisition errors (HTTP 403) by adding request headers, which is part of making file and API workflows reliable.

---

## C5 — Data analysis with pandas

I used pandas intentionally to answer three research questions, not just to display rows. In Section 3 of the notebook I used `groupby`, `size`, `agg`, `nunique`, filtering (`isin` for focus types), and `corr()` to compare brewery-type mix by state, micro/regional/brewpub counts by Census region (with percent-within-type), and city-level brewery count vs type diversity. I interpreted outputs in markdown—for example noting that a positive correlation between `brewery_count` and `unique_types` shows association, not causation.

---

## C6 — Data visualization

I created three Plotly Express charts in Section 4 that match each analytical question: a **stacked histogram** for type composition across states (Q1), a **grouped bar chart** for regional concentration of three types (Q2), and a **scatter plot** with color for dominant-type share (Q3). Each chart has a title that states a finding, labeled axes, and a chart type chosen for the data shape. The rationale cell explains what readers should take away and which comparisons are valid (for example within-region vs across-region).

---

## C7 — Critical evaluation and professional judgment

I showed professional judgment by stating limitations and likely misreadings alongside results. In the notebook I note that Open Brewery DB is not a complete census, that raw regional counts reflect listing volume as well as preference, and that city-level correlation does not prove why larger cities diversify. Section 5 summarizes what surprised me, what I would investigate next (normalization, separating operational statuses), and what conclusions this dataset cannot support—matching the careful interpretation I documented in `W6/week6.md` for each chart.
