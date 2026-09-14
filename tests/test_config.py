import pytest
from src import config

def test_validate_config_lists_missing_values(monkeypatch):
    """ Test the validate_config function raises a ValueError with the correct message when required environment variables are missing. """

    # Set configuration values to simulate missing required settings
    monkeypatch.setattr(config, "APP_ID", None)
    monkeypatch.setattr(config, "APP_KEY", "key")
    monkeypatch.setattr(config, "DB_CONFIG", {
        "host": None,
        "port": "5432",
        "dbname": "db_name",
        "user": "test_user",
        "password": "test_password"
    })

    # Expect validation to raise ValueError
    with pytest.raises(ValueError) as error:
        config.validate_config()

    # Check that the error message contains the names of the missing environment variables
    assert "ADZUNA_APP_ID" in str(error.value)
    assert "DB_HOST" in str(error.value)

def test_validate_config_accepts_complete_config(monkeypatch):
    """ Test the validate_config function does not raise an error when all required configuration variables are set. """

    # Set configuration values to simulate all required settings being present
    monkeypatch.setattr(config, "APP_ID", "app_id")
    monkeypatch.setattr(config, "APP_KEY", "key")
    monkeypatch.setattr(config, "DB_CONFIG", {
        "host": "localhost",
        "port": "5432",
        "dbname": "db_name",
        "user": "test_user",
        "password": "test_password"
    })

    # Validation should complete without raising an exception
    config.validate_config()