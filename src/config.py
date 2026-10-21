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

# Logging and file path settings for the job API Postgres pipeline
LOGGING_ROOT = 'job_api_pipeline'
LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"
SQL_DIR = Path(__file__).resolve().parent.parent / "sql"

POSTGRES_ENV_FILES = [
    "00_init_schemas.sql",
    "05_create_jobs_table.sql"
]

TRANSFORMATION_FILES = [
    "02_stg_adzuna_jobs_json.sql",
    "03_stg_adzuna_jobs_extracted.sql",
    "04_stg_adzuna_jobs_typed.sql",
]
