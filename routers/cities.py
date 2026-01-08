from fastapi import APIRouter, HTTPException, Depends
from db.database import get_db_connection
import psycopg2
import psycopg2.extras

router = APIRouter(
    prefix="/cities",
    tags=["Cities"]
)

# --- DATABASE DEPENDENCY ---
def get_db():
    conn = get_db_connection()
    try:
        yield conn
    finally:
        conn.close()


@router.get("/")
def get_cities(db=Depends(get_db)):
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cursor.execute("SELECT city_name FROM cities")
        rows = cursor.fetchall()

        return [row["city_name"] for row in rows]

    except psycopg2.Error as err:
        raise HTTPException(
            status_code=500,
            detail="Database Error while fetching cities"
        )

    finally:
        cursor.close()
