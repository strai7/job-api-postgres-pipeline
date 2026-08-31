import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Configuration settings for the job API Postgres pipeline
BASE_URL = "https://api.adzuna.com/v1/api"
SEARCH_URL = "/jobs/gb/search/"
QUERY = "junior data engineer"
RESULTS_PER_PAGE = 50

# Environment variables for Adzuna API credentials
APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

# Database configuration settings for Postgres connection
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

# Database schema and table settings for storing raw API response pages
DB_SCHEMA = os.getenv("DB_SCHEMA", "raw")
DB_TABLE = os.getenv("DB_TABLE", "adzuna_jobs")

# Logging configuration settings
LOGGING_ROOT = 'job_api_pipeline'
LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"


def validate_config():
    """Fail early with a clear message when required configuration is missing."""

    required_values = {
        "ADZUNA_APP_ID": APP_ID,
        "ADZUNA_APP_KEY": APP_KEY,
        "DB_HOST": DB_CONFIG["host"],
        "DB_PORT": DB_CONFIG["port"],
        "DB_NAME": DB_CONFIG["dbname"],
        "DB_USER": DB_CONFIG["user"],
        "DB_PASSWORD": DB_CONFIG["password"],
    }
    missing = [name for name, value in required_values.items() if not value]

    if missing:
        raise ValueError(
            "Missing required environment variables: " + ", ".join(missing)
        )
