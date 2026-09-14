from contextlib import contextmanager
from src import load

class FakeCursor:
    """A fake cursor class for testing purposes."""

    def __init__(self):
        self.executed_queries = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False  # Don't suppress exceptions

    def execute(self, query, json_data):
        """Store the executed query and parameters for later inspection."""
        self.executed_queries.append((query, json_data))

class FakeConnection:
    """A fake database connection class for testing purposes."""

    def __init__(self, cursor):
        self._cursor = cursor

    def cursor(self):
        return self._cursor

def test_load_raw_pages_insert_each_page(monkeypatch):
    """Test that load_raw_pages executes once per page with the expected data."""

    # Set up a fake cursor and connection to simulate database interactions
    cursor = FakeCursor()
    connection = FakeConnection(cursor)

    # Replace the get_connection function in the load module to return the fake connection
    @contextmanager
    def fake_get_connection():
        yield connection

    monkeypatch.setattr(load, "get_connection", fake_get_connection)

    # Raw pages to be loaded into the database
    raw_pages = [
        {"count": 100, "results": [{"id": 1}]},
        {"count": 100, "results": [{"id": 2}]},
    ]

    load.load_raw_pages(raw_pages)

    # Assert that the correct number of queries were executed and that the data matches the raw pages
    assert len(cursor.executed_queries) == 2
    # Note: comparison is made with the original dictionaries held by the Json adapters.
    assert cursor.executed_queries[0][1][0].adapted == raw_pages[0]
    assert cursor.executed_queries[1][1][0].adapted == raw_pages[1]
