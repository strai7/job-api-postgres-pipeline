import psycopg2
import logging

from config import DB_CONFIG, DB_SCHEMA, DB_TABLE, LOGGING_ROOT

logger = logging.getLogger(f"{LOGGING_ROOT}.database")

def get_connection():
    """Create a connection to the Postgres database."""

    # Set up logging
    logger.info("Establishing connection to the Postgres database")

    return psycopg2.connect(**DB_CONFIG)

def create_table():
    """Create the table for storing raw API response pages if it doesn't exist."""#

    # Set up logging
    logger.info(f"Creating table {DB_SCHEMA}.{DB_TABLE} for storing raw API response pages")

    # Create the table query with a JSONB column for storing raw API response pages
    create_table_query = f"""
        DROP TABLE IF EXISTS {DB_SCHEMA}.{DB_TABLE};
        CREATE TABLE {DB_SCHEMA}.{DB_TABLE} (
            page_results JSONB NOT NULL
        )
    """

    # Execute the create table query
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(create_table_query)
            conn.commit()

    logger.info(f"Table {DB_SCHEMA}.{DB_TABLE} created successfully")
