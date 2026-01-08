import psycopg2
from app.core.config import DB_CONFIG

def get_db_connection():
    return psycopg2.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        port=DB_CONFIG["port"],
        sslmode="require"
    )
