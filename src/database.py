import psycopg2
from psycopg2 import sql
import logging
from contextlib import contextmanager
from pathlib import Path

from .config import DB_CONFIG, DB_SCHEMA, DB_TABLE, LOGGING_ROOT
from .sql_pipeline_config import TRANSFORMATION_FILES, UPSERT_FILES

logger = logging.getLogger(f"{LOGGING_ROOT}.database")
SQL_DIR = Path(__file__).resolve().parent.parent / "sql"


@contextmanager
def get_connection():
    """Create a connection to the Postgres database."""

    # Set up logging
    logger.info("Establishing connection to the Postgres database")

    # Create a connection to the Postgres database using the provided configuration
    conn = psycopg2.connect(**DB_CONFIG)

    # Use a context manager to ensure the connection is closed after use
    try:
        with conn:
            yield conn

    finally:
        conn.close()
        logger.info("Connection to the Postgres database closed")


def reset_table():
    """Reset the table for storing raw API response pages."""

    # Set up logging
    logger.info(f"Resetting table {DB_SCHEMA}.{DB_TABLE} for storing raw API response pages")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(
                    sql.Identifier(DB_SCHEMA)
                )
            )
            cur.execute(
                sql.SQL("DROP TABLE IF EXISTS {}.{} CASCADE").format(
                    sql.Identifier(DB_SCHEMA),
                    sql.Identifier(DB_TABLE),
                )
            )
            cur.execute(
                sql.SQL("""
                    CREATE TABLE {}.{} (
                        page_results JSONB NOT NULL
                    )
                """).format(
                    sql.Identifier(DB_SCHEMA),
                    sql.Identifier(DB_TABLE),
                )
            )

    logger.info(f"Table {DB_SCHEMA}.{DB_TABLE} reset successfully")


def validate_sql_files():
    """Validate that all required SQL files exist in the sql directory."""

    logger.info(f"Validating existence of required SQL files in directory: {SQL_DIR}")
    for filename in TRANSFORMATION_FILES + UPSERT_FILES:
        sql_file = SQL_DIR / filename
        if not sql_file.is_file():
            raise FileNotFoundError(f"Required SQL file not found: {sql_file}")

def apply_transformations():
    """Creates the staging schemas and views from this versioned SQL files."""

    # Get a list of all SQL files in the sql directory and sort them by name
    transform_files = [SQL_DIR / file_name for file_name in TRANSFORMATION_FILES]
    logger.info(f"Applying {len(transform_files)} SQL transformation files")

    if not transform_files:
        raise ValueError(f"No sql transformation files configured. Directory:{SQL_DIR}. Files: {TRANSFORMATION_FILES}")

    with get_connection() as conn:
        with conn.cursor() as cur:

            # Apply each transformation SQL file in order, formatting the raw table name into the SQL statement
            for sql_file in transform_files:
                logger.info(f"Applying SQL file {sql_file.name}")
                statement = sql.SQL(sql_file.read_text(encoding="utf-8")).format(
                    raw_table=sql.SQL("{}.{}").format(
                        sql.Identifier(DB_SCHEMA),
                        sql.Identifier(DB_TABLE),
                    )
                )
                cur.execute(statement)

    logger.info("SQL transformations applied successfully")


def validate_staged_jobs():
    """ Validate staged job ids before upserting into core jobs table."""

    logger.info("Validating staged jobs for NULL, blank, or duplicate job IDs")

    with get_connection() as conn:
        with conn.cursor() as cur:

            # Count NULL job ids
            cur.execute("""
                SELECT COUNT(*)
                FROM stg.adzuna_jobs_typed
                WHERE job_id IS NULL
                   OR TRIM(job_id) = '';
            """)

            invalid_job_ids = cur.fetchone()[0]

            if invalid_job_ids > 0:
                raise ValueError(
                    f"Staged data contains {invalid_job_ids} NULL or blank job IDs"
                )

            # Count duplicate job ids
            cur.execute("""
                SELECT COUNT(*)
                FROM (
                    SELECT job_id
                    FROM stg.adzuna_jobs_typed
                    GROUP BY job_id
                    HAVING COUNT(*) > 1
                ) AS duplicate_ids;
            """)

            duplicate_job_ids = cur.fetchone()[0]

            if duplicate_job_ids > 0:
                raise ValueError(
                    f"Staged data contains {duplicate_job_ids} duplicated job IDs"
                )


def upsert_jobs():

    sql_files = [SQL_DIR / file_name for file_name in UPSERT_FILES]

    if not sql_files:
        raise ValueError(f"No sql upsert files configured. Directory:{SQL_DIR}. Files: {UPSERT_FILES}")

    logger.info(f"creating core jobs table and upserting jobs from typed table")

    with get_connection() as conn:
        with conn.cursor() as cur:

            # Execute core table creation and upsert SQL in order
            for sql_file in sql_files:
                logger.info(f"Applying SQL file {sql_file.name}")
                statement = sql_file.read_text(encoding="utf-8")
                cur.execute(statement)

    logger.info("Jobs upserted successfully")
