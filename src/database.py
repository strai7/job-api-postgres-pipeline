import psycopg2
from psycopg2 import sql
import logging
from contextlib import contextmanager

from .config import APP_ID, APP_KEY, DB_CONFIG, DB_SCHEMA, DB_TABLE, LOGGING_ROOT, SQL_DIR

logger = logging.getLogger(f"{LOGGING_ROOT}.database")


def apply_transformations(transform_files, db_schema, db_table, ingestion_timestamp):
    """Creates the staging schemas and views from this versioned SQL files."""

    # Get a list of all SQL files in the sql directory and sort them by name
    transform_files = [SQL_DIR / file_name for file_name in transform_files]
    logger.info(f"Applying {len(transform_files)} SQL transformation files")

    if not transform_files:
        raise ValueError(f"No sql transformation files configured. Directory:{SQL_DIR}. Files: {transform_files}")

    with get_connection() as conn:
        with conn.cursor() as cur:

            # Apply each transformation SQL file in order, formatting the raw table name into the SQL statement
            for sql_file in transform_files:
                logger.info(f"Applying SQL file {sql_file.name}")
                statement = sql.SQL(sql_file.read_text(encoding="utf-8")).format(
                    raw_table=sql.SQL("{}.{}").format(
                        sql.Identifier(db_schema),
                        sql.Identifier(db_table),),
                    ingestion_timestamp=sql.Literal(ingestion_timestamp)
                    )
                cur.execute(statement)

    logger.info("SQL transformations applied successfully")


def create_postgres_env(sql_files_paths):

    sql_files = [SQL_DIR / file_name for file_name in sql_files_paths]

    if not sql_files_paths:
        raise ValueError(f"No sql upsert files configured. Directory:{SQL_DIR}. File paths: {sql_files_paths}")

    logger.info(f"Creating postgres environment with {len(sql_files)} SQL files")

    with get_connection() as conn:
        with conn.cursor() as cur:

            # Execute core table creation and upsert SQL in order
            for sql_file in sql_files:
                logger.info(f"Applying SQL file {sql_file.name}")
                statement = sql_file.read_text(encoding="utf-8")
                cur.execute(statement)

    logger.info("Postgres environment created successfully")


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


def validate_config():
    """ Fail fast if any required configuration is missing. """

    env_vars = {
        "ADZUNA_APP_ID": APP_ID,
        "ADZUNA_APP_KEY": APP_KEY,
        "DB_HOST": DB_CONFIG["host"],
        "DB_PORT": DB_CONFIG["port"],
        "DB_NAME": DB_CONFIG["dbname"],
        "DB_USER": DB_CONFIG["user"],
        "DB_PASSWORD": DB_CONFIG["password"]
    }

    missing_vars = [var for var, value in env_vars.items() if not value]

    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")


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


def validate_sql_files(sql_files):
    """Validate that all required SQL files exist in the sql directory."""

    logger.info(f"Validating existence of required SQL files in directory: {SQL_DIR}")

    for filename in sql_files:
        sql_file = SQL_DIR / filename
        if not sql_file.is_file():
            raise FileNotFoundError(f"Required SQL file not found: {sql_file}")
