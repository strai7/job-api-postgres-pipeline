import psycopg2
import logging
from contextlib import contextmanager

from config import DB_CONFIG, DB_SCHEMA, DB_TABLE, LOGGING_ROOT

logger = logging.getLogger(f"{LOGGING_ROOT}.database")

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

    # Reset the table query with a JSONB column for storing raw API response pages
    ## Currently dropping table during development, but in production this should be changed to a CREATE TABLE IF NOT EXISTS statement
    reset_table_query = f"""
        DROP TABLE IF EXISTS {DB_SCHEMA}.{DB_TABLE};
        CREATE TABLE {DB_SCHEMA}.{DB_TABLE} (
            page_results JSONB NOT NULL
        )
    """

    # Execute the create table query
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(reset_table_query)

    logger.info(f"Table {DB_SCHEMA}.{DB_TABLE} reset successfully")
