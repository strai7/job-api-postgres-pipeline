from psycopg2.extras import Json
from config import DB_SCHEMA, DB_TABLE, LOGGING_ROOT
from database import get_connection
import logging

logger = logging.getLogger(f"{LOGGING_ROOT}.load")

def load_raw_pages(pages):
    """Load raw API response pages into Postgres as JSONB"""

    logger.info(f"Loading process started: Loading raw API response pages into Postgres table {DB_SCHEMA}.{DB_TABLE}")

    insert_query = f"""
        INSERT INTO {DB_SCHEMA}.{DB_TABLE} (page_results)
        VALUES (%s)
    """

    logger.info(f"Establishing connection to the Postgres database and loading raw API response pages into table {DB_SCHEMA}.{DB_TABLE}")
    with get_connection() as conn:
        with conn.cursor() as cur:
            for page_number, page in enumerate(pages, start=1):
                logger.info(f"Loading raw page {page_number}")
                cur.execute(insert_query, (Json(page),))

    logger.info(f"Loading process completed: Loaded {len(pages)} raw API response pages into Postgres table {DB_SCHEMA}.{DB_TABLE}")
