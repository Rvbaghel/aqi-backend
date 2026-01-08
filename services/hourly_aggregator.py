import logging
from app.db.database import get_db_connection
import psycopg2

logging.basicConfig(level=logging.INFO)

def aggregate_hourly_aqi():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO aqi_hourly_history (
                city_id,
                hour_ts,
                avg_aqi,
                avg_pm2_5,
                avg_pm10,
                avg_co,
                avg_no2,
                avg_so2,
                avg_o3,
                avg_nh3
            )
            SELECT
                city_id,
                date_trunc('hour', recorded_at) AS hour_ts,
                AVG(aqi),
                AVG(pm2_5),
                AVG(pm10),
                AVG(co),
                AVG(no2),
                AVG(so2),
                AVG(o3),
                AVG(nh3)
            FROM aqi_realtime
            WHERE recorded_at >= date_trunc('hour', NOW()) - INTERVAL '1 hour'
              AND recorded_at <  date_trunc('hour', NOW())
            GROUP BY city_id, hour_ts
            ON CONFLICT (city_id, hour_ts) DO UPDATE
            SET
                avg_aqi   = EXCLUDED.avg_aqi,
                avg_pm2_5 = EXCLUDED.avg_pm2_5,
                avg_pm10  = EXCLUDED.avg_pm10,
                avg_co    = EXCLUDED.avg_co,
                avg_no2   = EXCLUDED.avg_no2,
                avg_so2   = EXCLUDED.avg_so2,
                avg_o3    = EXCLUDED.avg_o3,
                avg_nh3   = EXCLUDED.avg_nh3;
        """)

        conn.commit()
        logging.info("Hourly AQI aggregation completed successfully.")

    except psycopg2.Error as e:
        logging.error(f"Hourly aggregation failed: {e}")
        if conn:
            conn.rollback()

    finally:
        if conn:
            conn.close()
