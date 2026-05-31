# Automated Daily Pipeline Scheduler
# Runs briefing generation at 6AM UTC daily

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timezone
import httpx

logger = logging.getLogger(__name__)

class BriefingScheduler:
    """Handles automated daily briefing generation"""

    def __init__(self, api_base_url: str = "http://localhost:8000"):
        self.scheduler = AsyncIOScheduler()
        self.api_base_url = api_base_url

    async def trigger_pipeline(self):
        """Trigger the weekly pipeline endpoint"""
        try:
            logger.info("Scheduler triggering daily pipeline run...")
            async with httpx.AsyncClient(timeout=600.0) as client:
                response = await client.post(f"{self.api_base_url}/pipeline/run-weekly")
                if response.status_code == 200:
                    logger.info(f"Pipeline triggered successfully at {datetime.now(timezone.utc)}")
                else:
                    logger.error(f"Pipeline trigger failed: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"Failed to trigger pipeline: {e}")

    def start(self):
        """Start the scheduler with daily 6AM UTC trigger"""
        # Schedule daily at 6:00 AM UTC
        self.scheduler.add_job(
            self.trigger_pipeline,
            trigger=CronTrigger(hour=6, minute=0, timezone='UTC'),
            id='daily_briefing_pipeline',
            name='Daily Briefing Generation',
            replace_existing=True
        )

        self.scheduler.start()
        logger.info("Briefing scheduler started - daily runs at 06:00 UTC")

        # Log next run time
        next_run = self.scheduler.get_job('daily_briefing_pipeline').next_run_time
        logger.info(f"Next scheduled run: {next_run}")

    def shutdown(self):
        """Gracefully shutdown the scheduler"""
        self.scheduler.shutdown()
        logger.info("Briefing scheduler stopped")
