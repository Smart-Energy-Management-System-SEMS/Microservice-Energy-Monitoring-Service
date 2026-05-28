from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from monitoring.domain.model.entities.energy_meter import MeterStatus


class RegisterEnergyMeterRequest(BaseModel):
    user_id: str
    meter_serial: str
    model: str
    brand: str
    location: str
    firmware_version: str = "1.0.0"
    max_power_watts: float = 10000.0


class EnergyMeterResponse(BaseModel):
    id: str
    user_id: str
    meter_serial: str
    model: str
    brand: str
    location: str
    status: MeterStatus
    firmware_version: str
    max_power_watts: float
    registered_at: datetime
    last_seen_at: Optional[datetime] = None
    updated_at: datetime


class HealthResource(BaseModel):
    status: str
    service: str
    version: str
    timestamp: datetime
