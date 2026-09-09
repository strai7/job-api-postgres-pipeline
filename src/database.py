import psycopg2
from psycopg2 import sql
import logging
from contextlib import contextmanager
from pathlib import Path

from config import DB_CONFIG, DB_SCHEMA, DB_TABLE, LOGGING_ROOT

logger = logging.getLogger(f"{LOGGING_ROOT}.database")
SQL_DIR = Path(__file__).resolve().parent / "sql"

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

    logger.info(f"Table {DB_SCHEMA}.{DB_TABLE} reset successfully")

def apply_transformations():
    """Create trhe staging schemas and views from this versioned SQL files."""

    # Get a list of all SQL files in the sql directory and sort them by name
    sql_files = sorted(SQL_DIR.glob("*.sql"))
    logger.info(f"Applying {len(sql_files)} SQL transformation files")

    with get_connection() as conn:
        with conn.cursor() as cur:

            # Apply each transformation SQL file in order, formatting the raw table name into the SQL statement
            for sql_file in sql_files:
                logger.info(f"Applying SQL file {sql_file.name}")
                statement = sql.SQL(sql_file.read_text(encoding="utf-8")).format(
                    raw_table=sql.SQL("{}.{}").format(
                        sql.Identifier(DB_SCHEMA),
                        sql.Identifier(DB_TABLE),
                    )
                )
                cur.execute(statement)

    logger.info("SQL transformations applied successfully")
