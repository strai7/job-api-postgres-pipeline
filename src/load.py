from psycopg2.extras import Json
from config import DB_SCHEMA, DB_TABLE
from database import get_connection


def load_raw_pages(pages):
    """Load raw API response pages into Postgres as JSONB"""
    insert_query = f"""
        INSERT INTO {DB_SCHEMA}.{DB_TABLE} (page_results)
        VALUES (%s)
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            for page_number, page in enumerate(pages, start=1):
                print(f"Loading raw page {page_number}")
                cur.execute(insert_query, (Json(page),))

    print("Raw API pages loaded successfully")
