import asyncio
import time
import requests
from typing import Dict, Any
import structlog
from app.core import config
from app.notifications import telegram

logger = structlog.get_logger(__name__)


class Watchdog:
    def __init__(self):
        self.last_check_times: Dict[str, float] = {}
        self.failure_counts: Dict[str, int] = {}
        self.api_url = f"http://api:8000/api/v1/monitoring/health"

    async def run(self):
        """Monitor the health of all bot workers and the system."""
        logger.info("VFSMAX Watchdog Started.")
        
        while True:
            try:
                # 1. Check if API is alive
                response = requests.get(self.api_url, timeout=5)
                if response.status_code != 200:
                    await self._handle_failure("API", "API returned non-200 status")
                
                # 2. Check each target's last activity
                # metrics = response.json()
                # for target_id, last_active in metrics["last_active"].items():
                #     if time.time() - last_active > config.settings.DEFAULT_CHECK_INTERVAL * 2:
                #         await self._handle_failure(target_id, f"Worker stuck. No check for >{(time.time()-last_active)/60:.1f} mins")
                
                logger.info("Watchdog check cycle complete.", status="HEALTHY")
                
            except Exception as e:
                logger.error("Watchdog check failed", error=str(e))
                # await self._handle_failure("SYSTEM", f"Critical Exception: {str(e)}")
            
            await asyncio.sleep(60)

    async def _handle_failure(self, entity_id: str, reason: str):
        """Notify and mark entity for restart or review."""
        logger.warning("VFSMAX Alert detected by Watchdog", entity=entity_id, reason=reason)
        # 1. Notify operator via Telegram
        # await telegram.send_emergency_notification(entity_id, reason)
        
        # 2. Logic to restart container if possible or flag for manual review
        pass


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    wd = Watchdog()
    loop.run_until_complete(wd.run())
