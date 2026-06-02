from datetime import datetime

from pydantic import BaseModel


class SimulateEnergyReadingRequest(BaseModel):
    user_id: str
    device_id: str


class EnergyPricingResponse(BaseModel):
    provider: str
    price_per_kwh: float
    currency: str
    timestamp: datetime


class SimulatedEnergyReadingResponse(BaseModel):
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
    estimated_cost: float
    currency: str
    provider: str


class ConsumptionHistoryResponse(BaseModel):
    device_id: str
    records: list[SimulatedEnergyReadingResponse]


class CurrentConsumptionResponse(SimulatedEnergyReadingResponse):
    pass
