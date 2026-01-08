from fastapi import APIRouter
from datetime import datetime
from db.database import get_db_connection
import psycopg2

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)

@router.get("/")
def health_check():
    health_status = {
        "status": "ok",
        "backend": "online",
        "database": "offline",  # default
        "message": "AQI backend is operational",
        "timestamp": datetime.utcnow().isoformat()
    }

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1;")  # lightweight DB check
        cur.fetchone()

        health_status["database"] = "online"

        cur.close()
        conn.close()

    except psycopg2.Error as e:
        health_status["status"] = "error"
        health_status["database"] = "unreachable"

    return health_status
