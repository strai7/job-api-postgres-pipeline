from psycopg2.extras import Json

from database import get_connection

def laod_raw_pages(pages):
    """Load raw API response pages into Postgres as JSONB"""
    insert_query = """
        INSERT INTO test_env.test1 (page_results)
        VALUES (%s)
    """

    with get_connection() as conn:
        with conn.cursoer() as cur:
            for page_number, page in enumerate(pages, start=1):
                print(f"Loading raw page {page_number}")
                cur.execute(insert_query, (Json(page),))

    print("Raw API pages loaded successfully")