# Interfaces layer: the shapes (schemas) of the JSON that goes in and out.
# "Request" is what the client sends; "Response" is what we send back.
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CreateEnergyReadingRequest(BaseModel):
    """JSON body the client sends to create a new reading."""
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
    """JSON we send back to the client to describe a reading."""
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
