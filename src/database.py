import psycopg2

from config import DB_CONFIG

def get_connection():
    """Create a connection to the Postgres database."""

    return psycopg2.connect(**DB_CONFIG)