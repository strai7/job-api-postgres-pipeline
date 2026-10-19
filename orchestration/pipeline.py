from src.config import validate_config, TRANSFORMATION_FILES, UPSERT_FILES
from src.database import apply_transformations, validate_sql_files
from src.extract import fetch_all_jobs
from src.load import load_raw_pages
from src.database import get_connection

from psycopg2 import sql
from pathlib import Path
import datetime
import json

ORC_SQL_DIR = Path(__file__).resolve().parent /  "sql"
CREATE_LANDING_TABLE_FILE = ORC_SQL_DIR / "01_create_landing_tables.sql"
UPSERT_FILE = ORC_SQL_DIR / "06_upsert_core_jobs_table.sql"
DB_SCHEMA = "raw"

# Pipeline task definitions

def create_landing_table():
    """Create the landing table for storing raw API response pages."""
    DB_TABLE = datetime.datetime.now().strftime("adzuna_jobs_%Y%m%d_%H%M%S")
    INGESTION_TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as conn:
        with conn.cursor() as cur:
            statement = sql.SQL(CREATE_LANDING_TABLE_FILE.read_text(encoding="utf-8")).format(
                raw_landing_table=sql.SQL("{}.{}").format(
                    sql.Identifier(DB_SCHEMA),
                    sql.Identifier(DB_TABLE),
                )
            )
            cur.execute(statement)

    landing_table = {"schema": DB_SCHEMA, "table": DB_TABLE, "ingestion_timestamp": INGESTION_TIMESTAMP}
    return json.loads(json.dumps(landing_table))


def ingest_raw(landing_table):
    """Fetch all jobs from the API and load them into the landing table."""
    DB_SCHEMA = landing_table["schema"]
    DB_TABLE = landing_table["table"]

    pages = fetch_all_jobs()

    load_raw_pages(pages, DB_SCHEMA, DB_TABLE)


def stage_jobs(landing_table):
    """Apply transformations to create staging schemas and views."""
    DB_SCHEMA = landing_table["schema"]
    DB_TABLE = landing_table["table"]
    INGESTION_TIMESTAMP = landing_table["ingestion_timestamp"]

    apply_transformations(TRANSFORMATION_FILES, DB_SCHEMA, DB_TABLE, INGESTION_TIMESTAMP)


def upsert_jobs():
    """Upsert staged jobs into the core jobs table."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql.SQL(UPSERT_FILE.read_text(encoding="utf-8")))


def validate_prerequisites():
    """Validate that all required SQL files exist in the sql directory."""
    sql_files = TRANSFORMATION_FILES + UPSERT_FILES
    validate_config()
    validate_sql_files(sql_files)