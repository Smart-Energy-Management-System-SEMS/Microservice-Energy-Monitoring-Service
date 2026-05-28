from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CreateEnergyReadingRequest(BaseModel):
    user_id: str
    meter_id: str
    device_id: str
    power_watts: float
    voltage: float
    current: float
    frequency: float
    energy_kwh: float
    timestamp: datetime
    reading_type: str = "real_time"
    phase: str = "single"


class EnergyReadingResponse(BaseModel):
    id: str
    user_id: str
    meter_id: str
    device_id: str
    power_watts: float
    voltage: float
    current: float
    frequency: float
    energy_kwh: float
    timestamp: datetime
    reading_type: str
    phase: str
    created_at: datetime
