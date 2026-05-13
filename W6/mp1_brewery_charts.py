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

BASE_API_URL = "https://api.openbrewerydb.org/v1/breweries"
PAGE_SIZE = 200
MAX_PAGES = 25

OUT_Q1 = "W6/chart_q1_brewery_types_by_state.png"
OUT_Q2 = "W6/chart_q2_micro_regional_brewpub_by_region.png"
OUT_Q3 = "W6/chart_q3_city_brewery_count_vs_type_diversity.png"

REGION_ORDER = ["Northeast", "Midwest", "South", "West", "Other/Unknown"]


def fetch_page(page: int, per_page: int = PAGE_SIZE) -> list[dict]:
    url = f"{BASE_API_URL}?per_page={per_page}&page={page}"
    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; HCDE530-Assignment/1.0)",
            "Accept": "application/json",
        },
    )
    with urlopen(request, timeout=20) as response:
        data = json.loads(response.read().decode("utf-8"))
    if not isinstance(data, list):
        raise RuntimeError("Unexpected API response format: expected a list.")
    return data


def fetch_breweries(max_pages: int = MAX_PAGES) -> list[dict]:
    all_records: list[dict] = []
    for page in range(1, max_pages + 1):
        page_records = fetch_page(page=page)
        if not page_records:
            break
        all_records.extend(page_records)
    return all_records


def build_dataframe(records: list[dict]) -> pd.DataFrame:
    columns = ["id", "name", "city", "state", "country", "brewery_type"]
    df = pd.DataFrame(records)
    df = df.loc[:, [c for c in columns if c in df.columns]].copy()
    df = df[df["country"] == "United States"].copy()
    df = df.dropna(subset=["state", "city", "brewery_type"])
    for col in ["state", "city", "brewery_type"]:
        df[col] = df[col].astype(str).str.strip()
    return df


def map_us_region(state: str) -> str:
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
    top_states = state_totals.head(14).index.tolist()
    sub = df[df["state"].isin(top_states)].copy()
    sub["state"] = pd.Categorical(sub["state"], categories=top_states, ordered=True)

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
        barmode="stack",
        xaxis_tickangle=-35,
        legend_title_text="Brewery type",
        yaxis_title="Number of breweries",
        margin=dict(b=120, l=60, r=40, t=60),
        height=520,
        width=960,
    )
    fig.write_image(OUT_Q1, scale=2)
    print(f"Wrote {OUT_Q1}")


def chart_q2_type_concentration_by_region(df: pd.DataFrame) -> None:
    """Q2: Are micro, regional, and brewpub breweries concentrated in particular regions?"""
    focus_types = ["micro", "regional", "brewpub"]
    regional = df.copy()
    regional["region"] = regional["state"].map(map_us_region)
    regional = regional[regional["brewery_type"].isin(focus_types)]
    plot_df = (
        regional.groupby(["region", "brewery_type"], observed=True)
        .size()
        .reset_index(name="brewery_count")
    )
    plot_df["region"] = pd.Categorical(plot_df["region"], categories=REGION_ORDER, ordered=True)
    plot_df = plot_df.sort_values(["region", "brewery_type"])

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
    type_counts = (
        df.groupby(["state", "city", "brewery_type"], observed=True)
        .size()
        .reset_index(name="n_per_type")
    )
    city_totals = type_counts.groupby(["state", "city"], observed=True)["n_per_type"].transform("sum")
    type_counts["pct_of_city"] = (type_counts["n_per_type"] / city_totals * 100).round(2)
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
    chart_q1_state_type_distribution(df)
    chart_q2_type_concentration_by_region(df)
    chart_q3_city_diversity(df)


if __name__ == "__main__":
    main()
