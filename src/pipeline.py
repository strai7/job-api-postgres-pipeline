from .config import validate_config
from .database import validate_sql_files
from .extract import fetch_all_jobs
from .load import load_raw_pages


# SQL Pipeline Stages

TRANSFORMATION_FILES = [
    "01_stg_adzuna_jobs_json.sql",
    "02_stg_adzuna_jobs_extracted.sql",
    "03_stg_adzuna_jobs_typed.sql",
]

UPSERT_FILES = [
    "04_create_jobs_table.sql",
    "05_upsert_core_jobs_table.sql",
]


# Pipeline task definitions

def validate_prerequisites():
    sql_files = TRANSFORMATION_FILES + UPSERT_FILES
    validate_config()
    validate_sql_files(sql_files)


def ingest_raw_jobs():
    pages = fetch_all_jobs()
    load_raw_pages(pages)
