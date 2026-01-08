from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.aqi_fetcher import fetch_and_store_aqi
from services.hourly_aggregator import aggregate_hourly_aqi
from services.daily_feature_aggregator import aggregate_daily_features

import pytz

scheduler = AsyncIOScheduler(timezone=pytz.UTC)

def start_scheduler():
    if not scheduler.get_job("aqi_job_id"):
        scheduler.add_job(
            fetch_and_store_aqi,
            trigger="interval",
            minutes=10,
            id="aqi_job_id",
            coalesce=True,     # merge missed runs
            max_instances=1   # avoid overlap
        )

    if not scheduler.get_job("hourly_agg_job"):
        scheduler.add_job(
            aggregate_hourly_aqi,
            trigger="cron",
            minute=5,
            id="hourly_agg_job",
            coalesce=True,
            max_instances=1
        )

    if not scheduler.get_job("daily_feature_job"):
        scheduler.add_job(
        aggregate_daily_features,
        trigger="cron",
        hour=0,
        minute=10,
        id="daily_feature_job",
        coalesce=True,
        max_instances=1
    )
        
    if not scheduler.running:
        scheduler.start()
