# Week 6

This week I saved three static Plotly figures from Open Brewery DB data (same source and cleaning approach as Week 5, implemented in `W6/mp1_brewery_charts.py`). The images are committed as PNGs so they render on GitHub without running code. For context, the three analytical questions that I am focusing on for MP1 using the Open Brewery DB are:
1. What does the distribution of brewery types look like across different states?
2. Are certain types (micro, regional, brewpub) concentrated in particular regions?
3. Do cities with a higher number of breweries tend to have a more diverse mix of brewery types, or are they dominated by a single type?

---

## Chart 1 — `chart_q1_brewery_types_by_state.png`

**MP1 question:** What does the distribution of brewery types look like across different states?

### Which chart type, and why

I used a **stacked Plotly Express histogram** (`px.histogram`, `barmode="stack"`). Each row in the data is one brewery, so the histogram counts how many breweries fall into each state, and **color splits those counts by `brewery_type`**. That matches a “distribution of a categorical variable (brewery type) within another categorical bucket (state).” I limited the plot to the **14 states with the largest total brewery counts** so the x-axis stays readable; showing all states would compress labels and make comparison harder without a different layout (for example, small multiples or a table).

### What someone could misread

A reader might treat the **height of one colored segment** as if it were comparable to the same color’s height in another state. In a stacked bar, segment height is the count for that type in that state, which is valid to compare, but the **total bar height** is “all types in that state,” so a tall bar can mean “many breweries overall,” not necessarily “many of one type.” Someone might also assume the chart shows **all U.S. states**; it does not, so states not shown can still have different mixes. Finally, the API snapshot is **not a complete census** of every brewery in the country; it is “what this dataset lists,” so the chart shows **listed** distribution, not ground truth for every operating brewery.

### If the result were flat or null

A **flat** pattern (similar stacked proportions in every shown state) would still be a finding: it would suggest that, in this sample, brewery-type mix does not vary much by state, which would push follow-up questions toward data coverage (for example, whether the API catalogs some states more completely) or toward national branding or regulation that homogenizes what gets listed. A **null** outcome (no usable rows after cleaning) would mean the visualization cannot support geographic claims until data quality or filters are fixed; that is still a valid conclusion about what the pipeline can answer today.

---

## Chart 2 — `chart_q2_micro_regional_brewpub_by_region.png`

**MP1 question:** Are certain types (micro, regional, brewpub) concentrated in particular regions?

### Which chart type, and why

I used a **grouped bar chart** (`px.bar`, `barmode="group"`). After mapping each brewery’s state to a **U.S. Census region**, I filtered to the three types named in the question (**micro, regional, brewpub**) and plotted **raw counts** by region, with **one color per brewery type**. Grouped bars make it easy to compare, within the same region, whether one type is much larger than the others, and to scan across regions for the same type.

### What someone could misread

The chart shows **counts**, not **shares of all breweries in a region**. A region with more listed breweries overall will tend to have taller bars for every type, so a reader should not conclude “this region favors micros” only because the micro bar is tall; they should compare **micro vs regional vs brewpub within that region**, or normalize by total breweries if the goal is proportional concentration. Someone might also forget that **other brewery types** exist outside these three; those are omitted on purpose for this question but still matter for the full picture.

### If the result were flat or null

If the three types had **nearly identical counts in every region**, that would be a meaningful (if surprising) finding: in this listing, micro, regional, and brewpub would appear **evenly spread** across Census regions, and “concentration” would be weak. If one type dominated **every** region with the same gap, that would point to a **dataset or market structure** story (for example, one type being far more common in Open Brewery DB nationwide) rather than a regional story. If counts were **zero** for a type in all regions after filtering, that would indicate a data or labeling issue worth checking before drawing regional conclusions.

---

## Chart 3 — `chart_q3_city_brewery_count_vs_type_diversity.png`

**MP1 question:** Do cities with a higher number of breweries tend to have a more diverse mix of brewery types, or are they dominated by a single type?

### Which chart type, and why

I used a **scatter plot** (`px.scatter`). Each point is one **U.S. city** (defined by state + city in the data). The **horizontal axis** is how many breweries that city has in this sample, and the **vertical axis** is how many **distinct `brewery_type` values** appear in that city. **Color** encodes the **percentage of breweries in that city that belong to the single most common type** (higher means more dominated by one type). That directly supports the wording of the question: readers can see whether larger cities drift **upward** on the y-axis (more types) and whether they lean **green or red** on the color scale (more or less dominated by one type).

### What someone could misread

Readers might treat this as proof of **causation** (“building more breweries causes diversity”). The chart only shows **association** in a cross-sectional snapshot. They might also over-interpret **small cities** with one brewery: those points sit at low counts and low “unique types” by construction, which can pull intuition even though the interesting pattern is among cities with many listings. **Color** is the share of the largest type, not the identity of that type, so two cities with the same color could be dominated by **different** named types.

### If the result were flat or null

In my Week 5 analysis on the same pipeline, the correlation between `brewery_count` and `unique_types` across cities was **positive and fairly strong**, so the scatter is **not** flat in practice. If it **were** flat (no upward trend), that would still be informative: larger cities would not systematically show more distinct listed types, which could mean the database tags types narrowly, or that big cities repeat the same type labels. A **flat color** (every city with nearly the same dominant-type share) would suggest that scale does not change how “concentrated” the mix is in the listing. A **null** pattern (no variation in `unique_types` at all) would flag that `brewery_type` has too little variation in the cleaned data to support diversity comparisons. Those outcomes are still findings about what this dataset can say about diversity at the city level.

---

## Competency claim: C6 

**What C6 means to me:** Visualization is not simply for aesthetics; it is a way to **make a claim legible**, match **chart structure to the question and the shape of the data**, and leave enough context that someone else can **follow the reasoning** without guessing what you did.

**What these charts demonstrate about making findings visible and building an argument with data**

Together, the three figures turn the MP1 questions into **visible claims** instead of leaving them as abstract “we could look at that” ideas. Chart 1 makes **composition** (type mix within state buckets) something you can scan; Chart 2 makes **comparative concentration** (three named types across regions) something you can judge side by side; Chart 3 makes **two parts of one hypothesis** (scale vs diversity, and dominance vs diversity) visible on shared axes so the argument is explicit rather than implied. Titles and axis labels state what is being measured; color and grouping encode **which comparisons are valid** (for example, within-region comparisons vs across-region totals). The sections above on **misreadings** and **flat or null results** are part of the same argument-building habit: a chart should not only show a pattern but also **anticipate how a reader could over-interpret it**, which is how visualization supports honest inference rather than “pretty but misleading” storytelling.

**Evidence mapped to the C6 description**

- **Charts generated in Python:** All three figures are produced in `W6/mp1_brewery_charts.py` using **Plotly Express** (`px.histogram`, `px.bar`, `px.scatter`). 
- **Written justification for chart choice:** This file includes, for each chart, **which type I chose and why**, **which question it answers**, **what could be misread**, and **how a boring or null pattern would still count as a finding**.
- **Publishing so someone else can follow the reasoning:** On GitHub, a reader can open **`week6.md`** (narrative and interpretation), the **committed `.png` outputs** (what the code produced), and **`mp1_brewery_charts.py`** (exact steps from API pull to `fig.write_image`). The C6 rubric also mentions a **Jupyter notebook** with code, outputs, and markdown; I have not yet added my work to the MP1 Jupyter notebook, but plan on doing that as my next step. 
