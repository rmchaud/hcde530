"""
Week 6: three Plotly charts for MP1 analytical questions (Open Brewery DB).
Saves PNGs via kaleido (fig.write_image).
"""

from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import pandas as pd
import plotly.express as px

# Open Brewery DB v1 returns JSON arrays; pagination is via per_page + page query params.
BASE_API_URL = "https://api.openbrewerydb.org/v1/breweries"
PAGE_SIZE = 200  # larger pages mean fewer HTTP round-trips up to the API limit
MAX_PAGES = 25  # safety cap so a bug or API change cannot loop forever

# Paths are relative to repo root when you run: python3 W6/mp1_brewery_charts.py
OUT_Q1 = "W6/chart_q1_brewery_types_by_state.png"
OUT_Q2 = "W6/chart_q2_micro_regional_brewpub_by_region.png"
OUT_Q3 = "W6/chart_q3_city_brewery_count_vs_type_diversity.png"

# Fixed region order keeps bars/lines on the x-axis in a sensible geographic grouping.
REGION_ORDER = ["Northeast", "Midwest", "South", "West", "Other/Unknown"]


def fetch_page(page: int, per_page: int = PAGE_SIZE) -> list[dict]:
    # Build the same URL shape documented for the v1 breweries collection.
    url = f"{BASE_API_URL}?per_page={per_page}&page={page}"
    request = Request(
        url,
        headers={
            # Some servers reject requests with no User-Agent; this identifies the script politely.
            "User-Agent": "Mozilla/5.0 (compatible; HCDE530-Assignment/1.0)",
            "Accept": "application/json",
        },
    )
    with urlopen(request, timeout=20) as response:
        # Body is UTF-8 JSON; loads() turns it into Python dicts/lists matching the API schema.
        data = json.loads(response.read().decode("utf-8"))
    if not isinstance(data, list):
        raise RuntimeError("Unexpected API response format: expected a list.")
    return data


def fetch_breweries(max_pages: int = MAX_PAGES) -> list[dict]:
    """Walk pages 1..max_pages until the API returns an empty list (no more data)."""
    all_records: list[dict] = []
    for page in range(1, max_pages + 1):
        page_records = fetch_page(page=page)
        if not page_records:
            break  # normal end-of-catalog signal from this API
        all_records.extend(page_records)
    return all_records


def build_dataframe(records: list[dict]) -> pd.DataFrame:
    # Only columns needed for charts and grouping; keeps the frame small and explicit.
    columns = ["id", "name", "city", "state", "country", "brewery_type"]
    df = pd.DataFrame(records)
    df = df.loc[:, [c for c in columns if c in df.columns]].copy()
    df = df[df["country"] == "United States"].copy()
    # Rows missing location or type would break groupbys or mislead maps; drop instead of guessing.
    df = df.dropna(subset=["state", "city", "brewery_type"])
    for col in ["state", "city", "brewery_type"]:
        # strip() merges labels that only differ by stray spaces so counts match intuition.
        df[col] = df[col].astype(str).str.strip()
    return df


def map_us_region(state: str) -> str:
    # U.S. Census Bureau-style regions; used so Q2 compares a few coarse buckets instead of 50 states.
    northeast = {
        "Connecticut", "Maine", "Massachusetts", "New Hampshire", "Rhode Island",
        "Vermont", "New Jersey", "New York", "Pennsylvania",
    }
    midwest = {
        "Illinois", "Indiana", "Michigan", "Ohio", "Wisconsin", "Iowa", "Kansas",
        "Minnesota", "Missouri", "Nebraska", "North Dakota", "South Dakota",
    }
    south = {
        "Delaware", "District of Columbia", "Florida", "Georgia", "Maryland",
        "North Carolina", "South Carolina", "Virginia", "West Virginia", "Alabama",
        "Kentucky", "Mississippi", "Tennessee", "Arkansas", "Louisiana", "Oklahoma", "Texas",
    }
    west = {
        "Arizona", "Colorado", "Idaho", "Montana", "Nevada", "New Mexico", "Utah",
        "Wyoming", "Alaska", "California", "Hawaii", "Oregon", "Washington",
    }
    # First match wins; anything else (territories, typos) rolls up so plots still have a bucket.
    if state in northeast:
        return "Northeast"
    if state in midwest:
        return "Midwest"
    if state in south:
        return "South"
    if state in west:
        return "West"
    return "Other/Unknown"


def chart_q1_state_type_distribution(df: pd.DataFrame) -> None:
    """Q1: How are brewery types distributed across states? (top states, stacked counts)."""
    state_totals = df.groupby("state").size().sort_values(ascending=False)
    # Focus on busiest states so labels stay readable; full US would need a different layout.
    top_states = state_totals.head(14).index.tolist()
    sub = df[df["state"].isin(top_states)].copy()
    # Categorical fixes bar order to total-descending, not alphabetical default.
    sub["state"] = pd.Categorical(sub["state"], categories=top_states, ordered=True)

    # One row per brewery: histogram bins are states; color stacks brewery_type counts.
    fig = px.histogram(
        sub,
        x="state",
        color="brewery_type",
        title="Distribution of brewery types across selected U.S. states",
        labels={
            "state": "State",
            "count": "Number of breweries",
            "brewery_type": "Brewery type",
        },
        category_orders={"state": top_states},
    )
    fig.update_layout(
        barmode="stack",  # each state's bar shows the mix of types, total height = all breweries
        xaxis_tickangle=-35,
        legend_title_text="Brewery type",
        yaxis_title="Number of breweries",
        margin=dict(b=120, l=60, r=40, t=60),
        height=520,
        width=960,
    )
    # kaleido (Plotly's image engine) rasterizes to PNG; scale=2 improves text sharpness.
    fig.write_image(OUT_Q1, scale=2)
    print(f"Wrote {OUT_Q1}")


def chart_q2_type_concentration_by_region(df: pd.DataFrame) -> None:
    """Q2: Are micro, regional, and brewpub breweries concentrated in particular regions?"""
    focus_types = ["micro", "regional", "brewpub"]
    regional = df.copy()
    regional["region"] = regional["state"].map(map_us_region)
    regional = regional[regional["brewery_type"].isin(focus_types)]
    # Aggregate to one count per (region, type) pair for plotting.
    plot_df = (
        regional.groupby(["region", "brewery_type"], observed=True)
        .size()
        .reset_index(name="brewery_count")
    )
    plot_df["region"] = pd.Categorical(plot_df["region"], categories=REGION_ORDER, ordered=True)
    plot_df = plot_df.sort_values(["region", "brewery_type"])

    # Grouped bars: within each region, compare the three types side by side (raw counts).
    fig = px.bar(
        plot_df,
        x="region",
        y="brewery_count",
        color="brewery_type",
        barmode="group",
        title="Micro, regional, and brewpub breweries by U.S. Census region",
        labels={
            "region": "Region",
            "brewery_count": "Number of breweries",
            "brewery_type": "Brewery type",
        },
        category_orders={"region": REGION_ORDER},
    )
    fig.update_layout(
        legend_title_text="Brewery type",
        margin=dict(b=80, l=60, r=40, t=60),
        height=480,
        width=800,
    )
    fig.write_image(OUT_Q2, scale=2)
    print(f"Wrote {OUT_Q2}")


def chart_q3_city_diversity(df: pd.DataFrame) -> None:
    """Q3: Do cities with more breweries show higher type diversity (vs single-type dominance)?"""
    # Per (state, city, type): how many breweries of that type in that city.
    type_counts = (
        df.groupby(["state", "city", "brewery_type"], observed=True)
        .size()
        .reset_index(name="n_per_type")
    )
    # Broadcast each city's total across its rows so we can turn counts into percentages.
    city_totals = type_counts.groupby(["state", "city"], observed=True)["n_per_type"].transform("sum")
    type_counts["pct_of_city"] = (type_counts["n_per_type"] / city_totals * 100).round(2)
    # Largest single-type share in each city: high means one label dominates the local scene.
    dominant = (
        type_counts.groupby(["state", "city"], observed=True)["pct_of_city"]
        .max()
        .reset_index(name="dominant_type_share_pct")
    )
    city_summary = (
        df.groupby(["state", "city"], observed=True)
        .agg(
            brewery_count=("id", "count"),
            unique_types=("brewery_type", "nunique"),
        )
        .reset_index()
        .merge(dominant, on=["state", "city"], how="left")
    )

    # Scatter: x = scale, y = diversity; color adds "dominance" without needing a third axis.
    fig = px.scatter(
        city_summary,
        x="brewery_count",
        y="unique_types",
        color="dominant_type_share_pct",
        title="City brewery count vs number of distinct brewery types (U.S. cities)",
        labels={
            "brewery_count": "Breweries in city",
            "unique_types": "Distinct brewery types",
            "dominant_type_share_pct": "Share of largest type (%)",
        },
        # Reversed diverging scale: warmer = more dominated by the top type in that city.
        color_continuous_scale="RdYlGn_r",
        opacity=0.65,
    )
    fig.update_layout(
        coloraxis_colorbar=dict(title="Largest type<br>% of city"),
        margin=dict(b=60, l=60, r=40, t=60),
        height=520,
        width=880,
    )
    fig.write_image(OUT_Q3, scale=2)
    print(f"Wrote {OUT_Q3}")


def main() -> None:
    # urllib raises typed exceptions; wrap so failures surface as clear messages for debugging.
    try:
        records = fetch_breweries()
    except HTTPError as e:
        raise RuntimeError(f"HTTP error while calling API: {e.code}") from e
    except URLError as e:
        raise RuntimeError(f"Network error while calling API: {e.reason}") from e
    except json.JSONDecodeError as e:
        raise RuntimeError("Failed to parse API response as JSON.") from e

    if not records:
        raise RuntimeError("No records were returned from Open Brewery DB.")

    df = build_dataframe(records)
    if df.empty:
        raise RuntimeError("No usable U.S. brewery records after cleaning.")

    print(f"Loaded {len(df)} U.S. brewery records.")
    # Each chart function mutates nothing global: it reads df and writes one PNG file.
    chart_q1_state_type_distribution(df)
    chart_q2_type_concentration_by_region(df)
    chart_q3_city_diversity(df)


if __name__ == "__main__":
    # Allows importing helpers elsewhere without running the full fetch + export pipeline.
    main()
