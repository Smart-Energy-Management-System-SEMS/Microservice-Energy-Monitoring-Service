from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CreateDeviceConsumptionRequest(BaseModel):
    user_id: str
    device_id: str
    device_name: str
    meter_id: str
    total_kwh: float
    cost_estimate_soles: float
    period_start: datetime
    period_end: datetime
    peak_power_watts: float
    average_power_watts: float
    reading_count: int


class DeviceConsumptionResponse(BaseModel):
    id: str
    user_id: str
    device_id: str
    device_name: str
    meter_id: str
    total_kwh: float
    cost_estimate_soles: float
    period_start: datetime
    period_end: datetime
    peak_power_watts: float
    average_power_watts: float
    reading_count: int
    created_at: datetime
    updated_at: datetime
