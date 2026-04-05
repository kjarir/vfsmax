from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional, Any


class MonitoringTargetBase(BaseModel):
    country: str
    visa_type: str
    status: str
    config_json: Optional[Any] = None


class MonitoringTargetRead(MonitoringTargetBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class SlotFoundBase(BaseModel):
    target_id: int
    slot_date: datetime
    slot_time: str
    center: str
    score: int
    action: str


class SlotFoundRead(SlotFoundBase):
    id: int
    found_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


from pydantic import field_validator

class CheckLogRead(BaseModel):
    id: int
    target_id: int
    status: str
    latency_ms: int
    message: Optional[str] = None
    timestamp: datetime
    
    @field_validator('timestamp', mode='before')
    @classmethod
    def ensure_utc(cls, v: Any) -> Any:
        if isinstance(v, datetime) and v.tzinfo is None:
            return v.strftime("%Y-%m-%dT%H:%M:%SZ")
        return v

    model_config = ConfigDict(from_attributes=True)

class ChartData(BaseModel):
    time: str
    checks: int
    slots: int
