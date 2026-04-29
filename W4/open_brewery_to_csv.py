"""
Fetch brewery data from Open Brewery DB and save it to CSV.
"""

import csv
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


# API endpoint for breweries:
# - /v1/breweries is the resource
# - per_page=50 asks for 50 records in one response
# - page=1 gets the first "page" of results
API_URL = "https://api.openbrewerydb.org/v1/breweries?per_page=50&page=1"
OUTPUT_FILE = "W4/open_breweries.csv"


def fetch_breweries(url: str) -> list[dict]:
    """Call the API endpoint and return parsed JSON as a list of dicts."""
    try:
        # Some APIs reject anonymous clients; these headers identify the request
        # and explicitly ask for JSON in the response.
        request = Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; HCDE530-Assignment/1.0)",
                "Accept": "application/json",
            },
        )
        with urlopen(request, timeout=15) as response:
            # The API returns JSON text. Here we decode bytes to a string,
            # then parse that JSON into Python objects (usually a list of dicts).
            payload = response.read().decode("utf-8")
            data = json.loads(payload)
    except HTTPError as error:
        raise RuntimeError(f"HTTP error while calling API: {error.code}") from error
    except URLError as error:
        raise RuntimeError(f"Network error while calling API: {error.reason}") from error
    except json.JSONDecodeError as error:
        raise RuntimeError("Failed to parse API response as JSON.") from error

    # Validate expected structure before we try looping through records later.
    if not isinstance(data, list):
        raise RuntimeError("Unexpected API response format: expected a list.")

    return data


def save_to_csv(records: list[dict], output_path: str) -> None:
    """Save selected fields from brewery records into a CSV file."""
    # These fields are chosen to give a readable summary:
    # - id: unique identifier for each brewery
    # - name: brewery name
    # - city/state/country: location context
    # - brewery_type: category (micro, brewpub, etc.)
    fields = ["id", "name", "city", "state", "country", "brewery_type"]

    with open(output_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()

        for row in records:
            # Extract only the selected fields so the CSV stays focused and clean.
            writer.writerow({field: row.get(field, "") for field in fields})


def main() -> None:
    breweries = fetch_breweries(API_URL)

    # Assignment requirement: ensure we received at least 50 records.
    if len(breweries) < 50:
        raise RuntimeError(
            f"Expected at least 50 records, but received {len(breweries)}."
        )

    # Keep output size consistent by writing exactly the first 50 records.
    save_to_csv(breweries[:50], OUTPUT_FILE)
    print(f"Saved {50} brewery records to {OUTPUT_FILE}")


# Run main() only when this file is executed directly.
if __name__ == "__main__":
    main()
