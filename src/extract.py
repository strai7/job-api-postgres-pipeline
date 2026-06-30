import requests
from math import ceil

from config import BASE_URL, SEARCH_URL, APP_ID, APP_KEY, QUERY, RESULTS_PER_PAGE

def build_request(page):
    """Build the ADzuna API URL and query parameters for a single results page."""
    url = f"{BASE_URL}{SEARCH_URL}{page}"

    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": RESULTS_PER_PAGE,
        "what": QUERY
    }

    return url, params

def fetch_page(page):
    """Fetch a single page of job results from ther Adzuna API."""
    url, params = build_request(page)

    response =  requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    return response.json()

def fetch_all_jobs():
    """Fetch all available job result pages, up to a min of 5 pages, for the configured search query."""
    print(f"Fetching page 1")
    first_page = fetch_page(1)

    total_count = int(first_page.get("count", 0))
    total_pages = ceil(total_count/RESULTS_PER_PAGE)
    total_pages = min(total_pages, 5)

    pages = [first_page]

    for page_number in range(2, total_pages+1):
        print(f"Fetching page {page_number} of {total_pages}")
        pages.append(fetch_page(page_number))

    return pages
