import requests
from typing import Optional, Dict, Any
from app.core.config import settings
from app.schemas.monitoring import SlotMetadata
import structlog

logger = structlog.get_logger(__name__)


async def send_telegram_alert(slot: SlotMetadata):
    """Sends a rich alert to the user's Telegram chat."""
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    
    if not token or not chat_id:
        logger.warning("Telegram bot credentials not configured. Skipping alert.")
        return

    message = (
        f"🚨 **VFSMAX SLOT ALERT** 🚨\n\n"
        f"📍 **Location:** {slot.location}\n"
        f"🌍 **Visa Type:** {slot.visa_type}\n"
        f"📅 **Date:** {slot.slot_date.strftime('%Y-%m-%d')}\n"
        f"🕒 **Time:** {slot.slot_time}\n"
        f"📊 **Score:** {slot.score}/100\n\n"
        f"🔗 [Book Now](https://visa.vfsglobal.com/ind/en/login)"
    )

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {"text": "✅ Book Now", "callback_data": f"book_{slot.id}"},
                    {"text": "❌ Ignore", "callback_data": f"ignore_{slot.id}"},
                    {"text": "🔕 Snooze 30m", "callback_data": f"snooze_{slot.id}"}
                ]
            ]
        }
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        logger.info("Telegram alert sent successfully", slot_id=slot.id)
    except Exception as e:
        logger.error("Failed to send Telegram alert", error=str(e))
