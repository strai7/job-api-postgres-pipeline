import pytest

from src import config


def test_validate_config_lists_missing_values(monkeypatch):
    monkeypatch.setattr(config, "APP_ID", None)
    monkeypatch.setattr(config, "APP_KEY", "key")
    monkeypatch.setattr(
        config,
        "DB_CONFIG",
        {
            "host": "localhost",
            "port": "5432",
            "dbname": None,
            "user": "jobs_user",
            "password": "password",
        },
    )

    with pytest.raises(ValueError) as error:
        config.validate_config()

    assert "ADZUNA_APP_ID" in str(error.value)
    assert "DB_NAME" in str(error.value)


def test_validate_config_accepts_complete_configuration(monkeypatch):
    monkeypatch.setattr(config, "APP_ID", "id")
    monkeypatch.setattr(config, "APP_KEY", "key")
    monkeypatch.setattr(
        config,
        "DB_CONFIG",
        {
            "host": "localhost",
            "port": "5432",
            "dbname": "jobs",
            "user": "jobs_user",
            "password": "password",
        },
    )

    config.validate_config()
