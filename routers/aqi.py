from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.db.database import get_db_connection
import psycopg2.extras

router = APIRouter(prefix="/aqi", tags=["AQI"])


# --- DATABASE DEPENDENCY ---
def get_db():
    conn = get_db_connection()
    try:
        yield conn
    finally:
        conn.close()


# --- AQI CLASSIFICATION ---
def classify_aqi_owm(aqi: int) -> str:
    mapping = {
        1: "Good",
        2: "Fair",
        3: "Moderate",
        4: "Poor",
        5: "Very Poor"
    }
    return mapping.get(aqi, "Unknown")


# --- ENDPOINTS ---

@router.get("/current")
def get_current_aqi(city: str, db=Depends(get_db)):
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        # 1. Get city_id
        cursor.execute(
            "SELECT city_id FROM cities WHERE city_name = %s",
            (city,)
        )
        city_row = cursor.fetchone()
        if not city_row:
            raise HTTPException(status_code=404, detail="City not found")

        city_id = city_row["city_id"]

        # 2. Get latest AQI record
        cursor.execute("""
            SELECT * FROM aqi_realtime
            WHERE city_id = %s
            ORDER BY recorded_at DESC
            LIMIT 1
        """, (city_id,))
        aqi_row = cursor.fetchone()

        if not aqi_row:
            raise HTTPException(status_code=404, detail="No data found for this city")

        return {
            "city": city,
            "aqi": aqi_row["aqi"],
            "category": classify_aqi_owm(aqi_row["aqi"]),
            "pollutants": {
                "pm2_5": aqi_row["pm2_5"],
                "pm10": aqi_row["pm10"],
                "co": aqi_row["co"],
                "no2": aqi_row["no2"],
                "so2": aqi_row["so2"],
                "o3": aqi_row["o3"],
                "nh3": aqi_row["nh3"]
            },
            "recorded_at": aqi_row["recorded_at"]
        }
    finally:
        cursor.close()


@router.get("/last-24-hours")
def get_last_24_hours_aqi(city: str, db=Depends(get_db)):
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cursor.execute(
            "SELECT city_id FROM cities WHERE city_name = %s",
            (city,)
        )
        city_row = cursor.fetchone()
        if not city_row:
            return []

        cursor.execute("""
            SELECT aqi, recorded_at
            FROM aqi_realtime
            WHERE city_id = %s
              AND recorded_at >= NOW() - INTERVAL '24 HOURS'
            ORDER BY recorded_at ASC
        """, (city_row["city_id"],))

        return cursor.fetchall()
    finally:
        cursor.close()

