"""
Analyze Open Brewery DB data with pandas for Week 5 assignment.
"""

# Import necessary libraries
import json
from contextlib import redirect_stdout
from io import StringIO
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import pandas as pd # for data analysis


BASE_API_URL = "https://api.openbrewerydb.org/v1/breweries" # API endpoint
PAGE_SIZE = 200 # number of records per page
MAX_PAGES = 25 # maximum number of pages to fetch
OUTPUT_REPORT_FILE = "W5/brewery_type_analysis_output.txt" # text file for saved output

# Function to fetch one API page from Open Brewery DB and return JSON records
def fetch_page(page: int, per_page: int = PAGE_SIZE) -> list[dict]:
    """Fetch one API page from Open Brewery DB and return JSON records."""
    url = f"{BASE_API_URL}?per_page={per_page}&page={page}"
    try:
        request = Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; HCDE530-Assignment/1.0)",
                "Accept": "application/json",
            },
        )
        with urlopen(request, timeout=15) as response:
            payload = response.read().decode("utf-8")
            data = json.loads(payload)
    except HTTPError as error:
        raise RuntimeError(f"HTTP error while calling API: {error.code}") from error
    except URLError as error:
        raise RuntimeError(f"Network error while calling API: {error.reason}") from error
    except json.JSONDecodeError as error:
        raise RuntimeError("Failed to parse API response as JSON.") from error

    if not isinstance(data, list):
        raise RuntimeError("Unexpected API response format: expected a list.")

    return data


# Function to fetch all brewery records from Open Brewery DB
def fetch_breweries(max_pages: int = MAX_PAGES) -> list[dict]:
    """Fetch multiple pages until empty page or max page limit."""
    all_records: list[dict] = []
    for page in range(1, max_pages + 1):
        page_records = fetch_page(page=page)
        if not page_records:
            break
        all_records.extend(page_records)
    return all_records


# Function to build a cleaned DataFrame with the fields needed for analysis
def build_dataframe(records: list[dict]) -> pd.DataFrame:
    """Create a cleaned DataFrame with the fields needed for analysis."""
    columns = ["id", "name", "city", "state", "country", "brewery_type"]
    df = pd.DataFrame(records)
    df = df.loc[:, [col for col in columns if col in df.columns]].copy()

    # Keep U.S. records and remove rows missing core grouping fields.
    df = df[df["country"] == "United States"].copy()
    df = df.dropna(subset=["state", "city", "brewery_type"])

    # Normalize text fields to avoid duplicate groups caused by casing/spacing.
    for col in ["state", "city", "brewery_type"]:
        df[col] = df[col].astype(str).str.strip()

    return df


# Function to map U.S. state names to U.S. Census-style regions
def map_us_region(state: str) -> str:
    """Map U.S. state names to U.S. Census-style regions."""
    northeast = {
        "Connecticut",
        "Maine",
        "Massachusetts",
        "New Hampshire",
        "Rhode Island",
        "Vermont",
        "New Jersey",
        "New York",
        "Pennsylvania",
    }
    midwest = {
        "Illinois",
        "Indiana",
        "Michigan",
        "Ohio",
        "Wisconsin",
        "Iowa",
        "Kansas",
        "Minnesota",
        "Missouri",
        "Nebraska",
        "North Dakota",
        "South Dakota",
    }
    south = {
        "Delaware",
        "District of Columbia",
        "Florida",
        "Georgia",
        "Maryland",
        "North Carolina",
        "South Carolina",
        "Virginia",
        "West Virginia",
        "Alabama",
        "Kentucky",
        "Mississippi",
        "Tennessee",
        "Arkansas",
        "Louisiana",
        "Oklahoma",
        "Texas",
    }
    west = {
        "Arizona",
        "Colorado",
        "Idaho",
        "Montana",
        "Nevada",
        "New Mexico",
        "Utah",
        "Wyoming",
        "Alaska",
        "California",
        "Hawaii",
        "Oregon",
        "Washington",
    }

    if state in northeast:
        return "Northeast"
    if state in midwest:
        return "Midwest"
    if state in south:
        return "South"
    if state in west:
        return "West"
    return "Other/Unknown"

# Function to analyze the distribution of brewery types across states
def analyze_state_type_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Question 1: distribution of brewery types across states."""
    state_type = (
        df.groupby(["state", "brewery_type"])
        .size()
        .reset_index(name="count")
        .sort_values(["state", "count"], ascending=[True, False])
    )
    return state_type

# Function to analyze the concentration of selected types by region
def analyze_type_concentration_by_region(df: pd.DataFrame) -> pd.DataFrame:
    """Question 2: concentration of selected types by region."""
    focus_types = ["micro", "regional", "brewpub"]
    regional = df.copy()
    regional["region"] = regional["state"].map(map_us_region)
    regional = regional[regional["brewery_type"].isin(focus_types)].copy()

    concentration = (
        regional.groupby(["region", "brewery_type"])
        .size()
        .reset_index(name="count")
        .sort_values(["brewery_type", "count"], ascending=[True, False])
    )
    concentration["pct_within_type"] = concentration.groupby("brewery_type")["count"].transform(
        lambda s: (s / s.sum() * 100).round(2)
    )
    return concentration

# Function to analyze the relationship between city count and type diversity
def analyze_city_brewery_diversity(df: pd.DataFrame) -> pd.DataFrame:
    """Question 3: relationship between city count and type diversity."""
    city_summary = (
        df.groupby(["state", "city"])
        .agg(
            brewery_count=("id", "count"),
            unique_types=("brewery_type", "nunique"),
        )
        .reset_index()
    )
    city_summary["dominant_type_share"] = (
        df.groupby(["state", "city", "brewery_type"])
        .size()
        .groupby(level=[0, 1])
        .apply(lambda s: round((s.max() / s.sum()) * 100, 2))
        .values
    )
    return city_summary.sort_values("brewery_count", ascending=False)

# Function to show the required pandas operations
def show_required_operations(df: pd.DataFrame) -> None:
    """Print exactly three required pandas operations for the assignment."""
    print("\nRequired pandas operations (3 used):")

    # Question: "What does this dataset look like before I analyze patterns?"
    # Meaning: The first rows show the real values I will analyze (state/city/type),
    # and info() confirms row count, column types, and whether fields are populated
    # enough to trust later group comparisons.
    print("\n1) df.head() -> first 5 rows:")
    print(df.head().to_string(index=False))
    print("\n1) df.info() -> data structure summary:")
    info_buffer = StringIO()
    df.info(buf=info_buffer)
    print(info_buffer.getvalue().strip())

    # Question: "Which brewery types appear most often in this sample?"
    # Meaning: A high count for one type (like micro) tells me the dataset is
    # dominated by that category, which affects how I interpret state/region results.
    print("\n2) df['brewery_type'].value_counts() -> most common brewery types:")
    print(df["brewery_type"].value_counts().head(10).to_string())

    # Question: "Which cities have especially large brewery scenes?"
    # Meaning: Filtering to brewery_count > 20 highlights high-density brewery cities
    # that I can compare for diversity vs single-type dominance in Q3.
    city_counts = df.groupby(["state", "city"]).size().reset_index(name="brewery_count")
    cities_over_20 = city_counts[city_counts["brewery_count"] > 20]
    print("\n3) df[df['column'] > value] -> cities with brewery_count > 20:")
    if cities_over_20.empty:
        print("No cities found with brewery_count > 20.")
    else:
        print(cities_over_20.sort_values("brewery_count", ascending=False).to_string(index=False))

# Function to main function
def main() -> None:
    breweries = fetch_breweries()
    if not breweries:
        raise RuntimeError("No records were returned from Open Brewery DB.")

    df = build_dataframe(breweries)
    if df.empty:
        raise RuntimeError("No usable U.S. brewery records after cleaning.")

    report_buffer = StringIO()
    with redirect_stdout(report_buffer):
        print(f"Loaded {len(df)} U.S. brewery records from Open Brewery DB.")
        show_required_operations(df)

        # 1) Distribution of brewery types across states.
        state_distribution = analyze_state_type_distribution(df)
        print("\nQ1) Brewery type distribution across states (top 25 state-type rows):")
        print(state_distribution.head(25).to_string(index=False))

        # 2) Concentration of selected types by region.
        region_concentration = analyze_type_concentration_by_region(df)
        print("\nQ2) Regional concentration for micro, regional, and brewpub:")
        print(region_concentration.to_string(index=False))

        # 3) City count vs type diversity (plus dominant-type share).
        city_diversity = analyze_city_brewery_diversity(df)
        correlation = city_diversity["brewery_count"].corr(city_diversity["unique_types"])
        print("\nQ3) City brewery count vs diversity summary (top 20 cities):")
        print(city_diversity.head(20).to_string(index=False))
        print(
            "\nPearson correlation between brewery_count and unique_types "
            f"across cities: {correlation:.3f}"
        )
        print(
            "Higher unique_types and lower dominant_type_share indicate a more diverse city mix."
        )

# Function to save the analysis output to a text file
    report_text = report_buffer.getvalue()
    print(report_text, end="")
    with open(OUTPUT_REPORT_FILE, "w", encoding="utf-8") as output_file:
        output_file.write(report_text)
    print(f"\nSaved analysis output to {OUTPUT_REPORT_FILE}")


if __name__ == "__main__":
    main()
