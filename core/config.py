from dotenv import load_dotenv
import os

load_dotenv()   # <-- THIS LINE IS IMPORTANT
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": os.getenv("DB_PORT", "5432")
}
