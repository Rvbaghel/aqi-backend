import logging
from db.database import get_db_connection
import psycopg2

logging.basicConfig(level=logging.INFO)

def aggregate_daily_features():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO aqi_daily_features (
                city_id,
                feature_date,
                mean_aqi,
                std_aqi,
                min_aqi,
                max_aqi,
                mean_pm2_5,
                mean_pm10,
                mean_no2,
                mean_co
            )
            SELECT
                city_id,
                DATE(hour_ts) AS feature_date,
                AVG(avg_aqi),
                STDDEV(avg_aqi),
                MIN(avg_aqi),
                MAX(avg_aqi),
                AVG(avg_pm2_5),
                AVG(avg_pm10),
                AVG(avg_no2),
                AVG(avg_co)
            FROM aqi_hourly_history
            WHERE hour_ts >= CURRENT_DATE - INTERVAL '1 day'
              AND hour_ts <  CURRENT_DATE
            GROUP BY city_id, feature_date
            ON CONFLICT (city_id, feature_date) DO UPDATE
            SET
                mean_aqi   = EXCLUDED.mean_aqi,
                std_aqi    = EXCLUDED.std_aqi,
                min_aqi    = EXCLUDED.min_aqi,
                max_aqi    = EXCLUDED.max_aqi,
                mean_pm2_5 = EXCLUDED.mean_pm2_5,
                mean_pm10  = EXCLUDED.mean_pm10,
                mean_no2   = EXCLUDED.mean_no2,
                mean_co    = EXCLUDED.mean_co;
        """)

        conn.commit()
        logging.info("Daily ML features aggregated successfully.")

    except psycopg2.Error as e:
        logging.error(f"Daily feature aggregation failed: {e}")
        if conn:
            conn.rollback()

    finally:
        if conn:
            conn.close()
