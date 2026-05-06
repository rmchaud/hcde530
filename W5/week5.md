# Week 5

The three analytical questions that I am focusing on for MP1 using the Open Brewery DB are:
1. What does the distribution of brewery types look like across different states?
2. Are certain types (micro, regional, brewpub) concentrated in particular regions?
3. Do cities with a higher number of breweries tend to have a more diverse mix of brewery types, or are they dominated by a single type?

## C3 — Data Cleaning and File Handling

### What it means
To me, C3 means loading real CSV data that may be incomplete or inconsistent, diagnosing failures from tracebacks, and writing code that still produces clean and repeatable output.

### Evidence from my work
- **File handling in W5 script:** In `W5/brewery_type_analysis.py`, I generate a consistent analysis report and save it to `W5/brewery_type_analysis_output.txt` every run.
- **Handles messy/invalid entries:** In `build_dataframe(...)`, I clean records by dropping rows with missing `state`, `city`, or `brewery_type`, then normalize text with `.str.strip()` so grouping is consistent.
- **Traceback diagnosis in W5 workflow:** While running this script, I hit a `ModuleNotFoundError: No module named 'pandas'` and fixed it by creating a local virtual environment (`.venv`) and installing pandas there.
- **Additional runtime error diagnosis:** I also hit a network `URLError` (`Tunnel connection failed: 403 Forbidden`) and resolved it by rerunning with full network access, confirming the script logic itself was correct.
- **Repeatable output:** `W5/brewery_type_analysis_output.txt` is regenerated with the same report structure each run, which makes results reproducible.

---

## C4 — APIs and Data Acquisition

### What it means
C4 means finding and using an API, understanding endpoint behavior from documentation, making requests, parsing responses, and handling errors safely.

### Evidence from my work
- **HTTP request + JSON parsing:** `W5/brewery_type_analysis.py` calls Open Brewery DB with `urllib.request`, then parses the response with `json.loads(...)`.
- **API chosen by me:** I used Open Brewery DB (`https://api.openbrewerydb.org/v1/breweries`) which I found using the class resource list.
- **Endpoint understanding:** The endpoint returns a list of brewery objects. I use fields such as `id`, `name`, `city`, `state`, `country`, and `brewery_type`.
- **What I did with response data:** In Week 5, I analyze the API data directly with pandas and save the final report to `W5/brewery_type_analysis_output.txt`.
- **API key safety:** This Open Brewery DB endpoint does not require an API key. For APIs that do require keys, I would keep secrets in environment variables and exclude local secret files in `.gitignore`.

---

## C5 — Data Analysis with Pandas

### What it means
C5 means using pandas operations intentionally to answer the three specific analytical questions that I detailed above, and then interpreting what the output says about the data.

### Evidence from my work
- **Script that answers real questions:** `W5/brewery_type_analysis.py` loads Open Brewery DB data into a DataFrame and answers:
  1) distribution of brewery types by state,  
  2) concentration of `micro`, `regional`, and `brewpub` by region,  
  3) whether cities with more breweries show more type diversity.
- **Pandas operations used:** I use multiple operations, including `head()`, `info()`, `value_counts()`, filtering (`df[df["column"] > value]` pattern), `groupby()`, `agg()`, `nunique()`, `corr()`, and sorting.
- **Missing value/data cleaning handling:** In `build_dataframe(...)`, I drop rows missing `state`, `city`, or `brewery_type` and standardize text with `.str.strip()` before grouping.
- **Interpretation of results (not just output):** From the generated report, the Pearson correlation between city brewery count and unique type count is positive (`0.782`), suggesting higher-brewery cities tend to have more diverse brewery-type mixes.
- **Repeatable output file:** Running the script saves a consistent report to `W5/brewery_type_analysis_output.txt`, making the analysis easy to re-check.
