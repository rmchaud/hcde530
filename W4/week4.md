# Week 4

## C2 — Code Literacy and Documentation

### What this means to me
Code literacy means I can read my own Python script, explain the purpose of each section, and make updates without breaking it. Documentation means writing comments and explanations so another person (or future me) can quickly understand the logic and decisions. It is meant to support and facilitate that understanding. 

### Evidence from my work
- **Inline comments that explain why:** In `W4/open_brewery_to_csv.py`, I added comments explaining:
  - why the API URL uses `per_page=50&page=1`
  - why headers like `User-Agent` and `Accept` are included
  - why I validate that the JSON response is a list
  - why I save exactly 50 records
- **Function docstring:** The function `fetch_breweries(url: str)` has a docstring that states what it does and what it returns (a list of dictionaries parsed from JSON).
- **Commit message quality target:** My commit message for Week 4 describes both what the script does and what API it uses. 

---

## C3 — Data Cleaning and File Handling

### What this means to me
This competency is about reading messy CSV data from the real world, identifying problems, fixing them in code, and producing repeatable output every time the script runs.

### Evidence from my work
- I already demonstrate **file output handling** by writing a consistent CSV from API data in `W4/open_brewery_to_csv.py`.
- In this assignment, I demonstrated error diagnosis when I got an HTTP 403 error while calling the API. I diagnosed that the request needed headers and fixed it by adding a `User-Agent` and `Accept` header.

---

## C4 — APIs and Data Acquisition

### What this means to me
C4 is about finding and using a public API, reading its documentation, requesting data correctly, and turning the response into useful output.

### Evidence from my work
- **HTTP request + JSON parsing:** `W4/open_brewery_to_csv.py` uses Python (`urllib`) to call Open Brewery DB and parse the JSON response.
- **Self-selected API:** I used Open Brewery DB (`https://api.openbrewerydb.org/v1/breweries`) as my data source.
- **Endpoint understanding:** The endpoint returns a list of brewery records (one object per brewery) with fields like name, type, and location.
- **Use of returned data:** I extracted six fields and saved them to CSV for a clean, readable dataset.
- **Documentation and Handling:** I made sure to read through the API documentation on Open Brewery DB, which states that it does not require an API key for this endpoint, so there is no secret key to store. If I use an API that requires a key later, I will keep it out of version control using environment variables and `.gitignore`.
