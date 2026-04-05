from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class SlotMetadata(BaseModel):
    id: str = Field(default_factory=lambda: "slot_" + str(datetime.now().timestamp()))
    found_at: datetime = Field(default_factory=datetime.now)
    slot_date: datetime
    slot_time: str
    location: str
    visa_type: str
    capacity: int = 1
    score: int = 0
    raw_text: Optional[str] = None


class MonitoringResult(BaseModel):
    target_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    status: str  # SLOT_FOUND, EMPTY, ERROR, CAPTCHA, BANNED
    latency_ms: int
    slots: List[SlotMetadata] = []
    screenshot_path: Optional[str] = None
    error_message: Optional[str] = None
