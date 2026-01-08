from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from routers.aqi import router as aqi_router
from routers.health import router as health_router
from routers.cities import router as cities_router
from core.scheduler import start_scheduler, scheduler

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    start_scheduler()
    logging.info("Scheduler started...")
    try:
        yield
    finally:
        # Shutdown (safe)
        if scheduler.running:
            scheduler.shutdown()
            logging.info("Scheduler shut down.")

app = FastAPI(
    title="AQI Monitoring Backend",
    lifespan=lifespan
)

# Routers
app.include_router(cities_router)
app.include_router(health_router)
app.include_router(aqi_router)

@app.get("/")
def root():
    return {"status": "AQI Backend Running"}
