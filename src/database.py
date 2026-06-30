import psycopg2

from config import DB_CONFIG, DB_SCHEMA, DB_TABLE

def get_connection():
    """Create a connection to the Postgres database."""
    return psycopg2.connect(**DB_CONFIG)

def create_table():
    """Create the table for storing raw API response pages if it doesn't exist."""
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {DB_SCHEMA}.{DB_TABLE} (
            page_results JSONB NOT NULL
        )
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(create_table_query)
            conn.commit()

    print(f"Table {DB_SCHEMA}.{DB_TABLE} is ready.")
