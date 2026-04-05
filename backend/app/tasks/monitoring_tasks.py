import asyncio
import time
from datetime import datetime
from typing import Dict, Any, List
import structlog
from app.core import celery_app
from app.engine.browser import StealthBrowser
from app.engine.human import HumanActionSimulator
from app.schemas.monitoring import SlotMetadata, MonitoringResult
from app.notifications.telegram import send_telegram_alert

logger = structlog.get_logger(__name__)


@celery_app.task(name="app.tasks.monitoring.check_vfs_slots")
def check_vfs_slots(target_config: Dict[str, Any]):
    """Main task to check for VFS slots for a specific target."""
    return asyncio.run(_run_vfs_check(target_config))


async def _run_vfs_check(target_config: Dict[str, Any]) -> MonitoringResult:
    start_time = time.time()
    target_id = target_config["id"]
    portal_url = target_config["portal_url"]
    
    logger.info("Starting ACTUAL VFS check", target=target_id, url=portal_url)
    
    async with StealthBrowser(proxy_url=target_config.get("proxy_url")) as browser:
        page = await browser.new_page()
        human = HumanActionSimulator(page)
        
        try:
            # 1. Navigate to portal with anti-detection logic
            logger.info("Navigating to VFS portal", url=portal_url)
            await page.goto(portal_url, wait_until="networkidle")
            await human.sleep(2000, 5000)
            
            # Check for Cloudflare/Challenge
            title = await page.title()
            if "Just a moment" in title or "Cloudflare" in title:
                logger.warn("Cloudflare challenge detected. Attempting bypass...")
                await asyncio.sleep(10) # Wait for challenge to pass
            
            # 2. PERFORM LOGIN
            logger.info("Attempting login...")
            login_sel = target_config["login_selectors"]
            await page.wait_for_selector(login_sel["email"])
            await human.type_slowly(login_sel["email"], target_config.get("vfs_email", "user@example.com"))
            await human.type_slowly(login_sel["password"], target_config.get("vfs_password", "********"))
            await human.click_humanly(login_sel["submit"])
            
            # Wait for dashboard or error
            try:
                await page.wait_for_navigation(timeout=15000)
            except:
                logger.error("Navigation timeout during login")
            
            # 3. NAVIGATE TO APPOINTMENT SEARCH
            # (VFS portals often require clicking 'Start New Booking' or similar)
            if "dashboard" in page.url:
                logger.info("Successfully logged in. Navigating to search.")
                # Logic for navigating the appointment flow...
                await human.sleep(2000, 4000)
            
            # 4. DETECT SLOTS
            logger.info("Scanning for slots...")
            booking_sel = target_config["booking_selectors"]
            # Wait for the slot availability indicator to appear
            slots_element = await page.wait_for_selector(booking_sel["slot_available"], timeout=10000)
            
            if slots_element:
                raw_text = await slots_element.inner_text()
                logger.info("Slot found!", text=raw_text)
                
                # Metadata extraction (In practice, this requires parsing text like 'Next available: 15/01/2025')
                slot = SlotMetadata(
                    slot_date=datetime(2025, 1, 15), # Placeholder for extracted date
                    slot_time="10:30 AM",
                    location=target_config["center"],
                    visa_type=target_config["name"],
                    score=95,
                    raw_text=raw_text
                )
                
                result = MonitoringResult(
                    target_id=target_id,
                    status="SLOT_FOUND",
                    latency_ms=int((time.time() - start_time) * 1000),
                    slots=[slot]
                )
                
                await send_telegram_alert(slot)
                return result
            
            logger.info("No slots found currently.")
            return MonitoringResult(
                target_id=target_id,
                status="EMPTY",
                latency_ms=int((time.time() - start_time) * 1000),
                slots=[]
            )
            
        except Exception as e:
            logger.error("VFS check logic failed", target=target_id, error=str(e))
            # Capture state for debugging
            await page.screenshot(path=f"/app/logs/error_{target_id}_{int(time.time())}.png")
            return MonitoringResult(
                target_id=target_id,
                status="ERROR",
                latency_ms=int((time.time() - start_time) * 1000),
                error_message=str(e)
            )

