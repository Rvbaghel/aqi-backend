import requests
import logging
from core.config import OPENWEATHER_API_KEY
from db.database import get_db_connection
import psycopg2

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

AQI_URL = "http://api.openweathermap.org/data/2.5/air_pollution"


def fetch_and_store_aqi():
    conn = None
    try:
        conn = get_db_connection()

        # 1️⃣ Fetch all cities
        read_cursor = conn.cursor()
        read_cursor.execute(
            "SELECT city_id, city_name, latitude, longitude FROM cities"
        )
        cities = read_cursor.fetchall()
        read_cursor.close()

        write_cursor = conn.cursor()

        for city_id, city_name, lat, lon in cities:
            try:
                params = {
                    "lat": lat,
                    "lon": lon,
                    "appid": OPENWEATHER_API_KEY
                }

                response = requests.get(AQI_URL, params=params, timeout=10)
                response.raise_for_status()

                data = response.json()
                item = data["list"][0]

                aqi = item["main"]["aqi"]
                comp = item["components"]

                insert_query = """
                    INSERT INTO aqi_realtime
                    (city_id, aqi, pm2_5, pm10, co, no2, so2, o3, nh3, recorded_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                """

                write_cursor.execute(
                    insert_query,
                    (
                        city_id,
                        aqi,
                        comp.get("pm2_5"),
                        comp.get("pm10"),
                        comp.get("co"),
                        comp.get("no2"),
                        comp.get("so2"),
                        comp.get("o3"),
                        comp.get("nh3"),
                    )
                )

                logging.info(f"AQI stored successfully for {city_name}")

            except requests.exceptions.RequestException as e:
                logging.error(f"API error for {city_name}: {e}")
                continue

            except psycopg2.Error as e:
                logging.error(f"DB insert failed for {city_name}: {e}")
                conn.rollback()
                continue

        conn.commit()
        write_cursor.close()
        logging.info("AQI data committed successfully.")

    except Exception as e:
        logging.critical(f"Fatal error in AQI fetcher: {e}")

    finally:
        if conn:
            conn.close()
            logging.info("Database connection closed.")


if __name__ == "__main__":
    fetch_and_store_aqi()
