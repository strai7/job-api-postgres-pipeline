from src.config import TRANSFORMATION_FILES
from src.database import apply_transformations, validate_config, validate_sql_files
from src.extract import fetch_all_jobs
from src.load import load_raw_pages
from src.database import get_connection

import datetime
import json
from pathlib import Path
from psycopg2 import sql

ORC_SQL_DIR = Path(__file__).resolve().parent /  "sql"
CREATE_LANDING_TABLE_FILE = ORC_SQL_DIR / "01_create_landing_tables.sql"
UPSERT_FILE = ORC_SQL_DIR / "06_upsert_core_jobs_table.sql"
DB_SCHEMA = "raw"

# Pipeline task definitions

def create_landing_table():
    """Create the landing table for storing raw API response pages."""

    now = datetime.datetime.now()
    db_table = now.strftime("adzuna_jobs_%Y%m%d_%H%M%S")
    ingestion_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    print(f"Creating landing table: {DB_SCHEMA}.{db_table} for ingestion timestamp: {ingestion_timestamp}")
    with get_connection() as conn:
        with conn.cursor() as cur:
            statement = sql.SQL(CREATE_LANDING_TABLE_FILE.read_text(encoding="utf-8")).format(
                raw_landing_table=sql.SQL("{}.{}").format(
                    sql.Identifier(DB_SCHEMA),
                    sql.Identifier(db_table),
                )
            )
            cur.execute(statement)
            print("Landing table created successfully.")

    landing_table = {"schema": DB_SCHEMA, "table": db_table, "ingestion_timestamp": ingestion_timestamp}
    return json.loads(json.dumps(landing_table))


def ingest_raw(landing_table):
    """Fetch all jobs from the API and load them into the landing table."""
    db_schema = landing_table["schema"]
    db_table = landing_table["table"]

    print(f"Fetching pages of jobs from API")
    pages = fetch_all_jobs()

    print(f"Loading {len(pages)} pages of jobs into landing table: {db_schema}.{db_table}")
    load_raw_pages(pages, db_schema, db_table)
    print("Raw jobs loaded successfully.")


def stage_jobs(landing_table):
    """Apply transformations to create staging schemas and views."""

    db_schema = landing_table["schema"]
    db_table = landing_table["table"]
    ingestion_timestamp = landing_table["ingestion_timestamp"]

    print(f"Applying transformations and staging new set of jobs from landing table: {db_schema}.{db_table} for ingestion timestamp: {ingestion_timestamp}")
    apply_transformations(TRANSFORMATION_FILES, db_schema, db_table, ingestion_timestamp)
    print("Staging of jobs completed successfully.")


def upsert_jobs():
    """Upsert staged jobs into the core jobs table."""

    print("Upserting staged jobs into the core jobs table.")
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql.SQL(UPSERT_FILE.read_text(encoding="utf-8")))
            print("Upsert of staged jobs into core jobs table completed successfully.")


def validate_prerequisites():
    """Validate that all required SQL files exist in the sql directory."""
    sql_files = TRANSFORMATION_FILES + [CREATE_LANDING_TABLE_FILE.name] + [UPSERT_FILE.name]

    print("Validating prerequisite configurations for the pipeline.")
    validate_config()
    print("Prerequisite configurations validated successfully.")

    print(f"Validating existence of required SQL files in directory: {ORC_SQL_DIR}")
    validate_sql_files(TRANSFORMATION_FILES)
    print("Required SQL files validated successfully.")
