from unittest.mock import Mock
import pytest
from src import extract

def test_build_request_returns_expected_url_and_params(monkeypatch):
    """ Test that the build_request function returns the expected URL and parameters for a given page number. """
    # Set up test values for the API ID and API KEY
    monkeypatch.setattr(extract, "APP_ID", "test_id")
    monkeypatch.setattr(extract, "APP_KEY", "test_key")

    url, params = extract.build_request(3)

    # Check that the returned URL and parameters match the expected values
    assert url == "https://api.adzuna.com/v1/api/jobs/gb/search/3"
    assert params == {
        "app_id": "test_id",
        "app_key": "test_key",
        "results_per_page": 50,
        "what": "junior data engineer"
    }

@pytest.mark.parametrize("page", [-1, 0, "a", None])
def test_build_request_rejects_invalid_page_numbers(page):
    """ Test that the build_request function raises a ValueError for invalid page numbers. """

    with pytest.raises(ValueError):
        extract.build_request(page)

def test_fetch_page_uses_timeout_and_returns_json(monkeypatch):
    """ Test that the fetch_page function uses a timeout and returns the expected JSON response. """

    # Mock the requests.get method to return a mock response with a JSON method
    response = Mock()
    response.json.return_value = {"count": 100, "results": [{"id": "2"}]}
    request_get = Mock(return_value=response)
    monkeypatch.setattr(extract.requests, "get", request_get)

    result = extract.fetch_page(1)

    # Check that the request and response methods were called the correct number of times with the expected arguments 
    # and that the result matches the mock JSON response
    request_get.assert_called_once()
    assert request_get.call_args[1]["timeout"] == 10
    response.raise_for_status.assert_called_once_with()
    assert result == {"count": 100, "results": [{"id": "2"}]}

def test_fetch_all_jobs_fetches_result_count_for_pagination(monkeypatch):
    """ Test that the fetch_all_jobs function correctly fetches multiple pages of job results based on the total count. """

    # Mock fetch_page function to return a fake response with a count of 120 results
    requested_pages = []

    def fake_fetch_page(page):
        requested_pages.append(page)
        return {"count": 120, "results": [{"id": page}]}

    # Patch fetch_page function in the extract module with the fake_fetch_page function
    monkeypatch.setattr(extract, "fetch_page", fake_fetch_page)

    pages = extract.fetch_all_jobs()

    # Assert that correct number of pages were requested and appended to the pages list
    assert requested_pages == [1, 2, 3]
    assert len(pages) == 3

def test_fetch_all_jobs_limits_to_maximum_pages(monkeypatch):
    """ Test that the fetch_all_jobs function limits the number of pages fetched to a maximum of 5, even if total count exceeds that number. """
    requested_pages = []

    def fake_fetch_page(page):
        requested_pages.append(page)
        return {"count": 1_000, "results": [{"id": page}]}

    monkeypatch.setattr(extract, "fetch_page", fake_fetch_page)

    pages = extract.fetch_all_jobs()

    # Assert that the function only fetched a maximum of 5 pages
    assert requested_pages == [1, 2, 3, 4, 5]
    assert len(pages) == 5

def  test_fetch_all_jobs_handles_zero_results(monkeypatch):
    """ Test that the fetch_all_jobs function handles the case where the API returns zero results. """
    fetch_page = Mock(return_value={"count": 0, "results": []})
    monkeypatch.setattr(extract, "fetch_page", fetch_page)

    pages = extract.fetch_all_jobs()

    # Assert fetch_page function was called once with page number 1 and returned pages list contains the expected empty results
    fetch_page.assert_called_once_with(1)
    assert pages == [{"count": 0, "results": []}]