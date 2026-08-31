from contextlib import contextmanager

from src import load


class RecordingCursor:
    def __init__(self):
        self.executions = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def execute(self, query, parameters):
        self.executions.append((query, parameters))


class FakeConnection:
    def __init__(self, cursor):
        self._cursor = cursor

    def cursor(self):
        return self._cursor


def test_load_raw_pages_inserts_each_page(monkeypatch):
    cursor = RecordingCursor()
    connection = FakeConnection(cursor)

    @contextmanager
    def fake_get_connection():
        yield connection

    monkeypatch.setattr(load, "get_connection", fake_get_connection)
    pages = [
        {"count": 2, "results": [{"id": "1"}]},
        {"count": 2, "results": [{"id": "2"}]},
    ]

    load.load_raw_pages(pages)

    assert len(cursor.executions) == 2
    assert cursor.executions[0][1][0].adapted == pages[0]
    assert cursor.executions[1][1][0].adapted == pages[1]
