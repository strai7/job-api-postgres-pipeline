from unittest.mock import Mock

import pytest

from src import extract


def test_build_request_returns_expected_url_and_parameters(monkeypatch):
    monkeypatch.setattr(extract, "APP_ID", "test-id")
    monkeypatch.setattr(extract, "APP_KEY", "test-key")

    url, params = extract.build_request(3)

    assert url == "https://api.adzuna.com/v1/api/jobs/gb/search/3"
    assert params == {
        "app_id": "test-id",
        "app_key": "test-key",
        "results_per_page": 50,
        "what": "junior data engineer",
    }


@pytest.mark.parametrize("page", [0, -1, 1.5, "1"])
def test_build_request_rejects_invalid_page_numbers(page):
    with pytest.raises(ValueError, match="positive integer"):
        extract.build_request(page)


def test_fetch_page_uses_timeout_and_returns_json(monkeypatch):
    response = Mock()
    response.json.return_value = {"count": 1, "results": [{"id": "123"}]}
    request_get = Mock(return_value=response)
    monkeypatch.setattr(extract.requests, "get", request_get)

    result = extract.fetch_page(1)

    request_get.assert_called_once()
    assert request_get.call_args.kwargs["timeout"] == 10
    response.raise_for_status.assert_called_once_with()
    assert result == {"count": 1, "results": [{"id": "123"}]}


def test_fetch_all_jobs_uses_result_count_for_pagination(monkeypatch):
    requested_pages = []

    def fake_fetch_page(page):
        requested_pages.append(page)
        return {"count": 120, "results": [{"page": page}]}

    monkeypatch.setattr(extract, "fetch_page", fake_fetch_page)

    pages = extract.fetch_all_jobs()

    assert requested_pages == [1, 2, 3]
    assert len(pages) == 3


def test_fetch_all_jobs_caps_requests_at_five_pages(monkeypatch):
    requested_pages = []

    def fake_fetch_page(page):
        requested_pages.append(page)
        return {"count": 10_000, "results": []}

    monkeypatch.setattr(extract, "fetch_page", fake_fetch_page)

    extract.fetch_all_jobs()

    assert requested_pages == [1, 2, 3, 4, 5]


def test_fetch_all_jobs_keeps_first_page_when_no_results(monkeypatch):
    fetch_page = Mock(return_value={"count": 0, "results": []})
    monkeypatch.setattr(extract, "fetch_page", fetch_page)

    pages = extract.fetch_all_jobs()

    fetch_page.assert_called_once_with(1)
    assert pages == [{"count": 0, "results": []}]
