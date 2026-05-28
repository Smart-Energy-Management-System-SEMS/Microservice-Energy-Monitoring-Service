from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class DeviceConsumption:
    """
    Entity: Aggregated energy consumption per device for a given period.
    Summarizes usage and estimated cost for billing/analytics purposes.
    """
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
    id: Optional[str] = field(default=None)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def cost_per_kwh(self, tariff: float = 0.68) -> float:
        """Calculate cost using the given tariff (PEN/kWh). Default is Peruvian average."""
        return self.total_kwh * tariff

    def is_high_consumer(self, threshold_kwh: float = 100.0) -> bool:
        return self.total_kwh > threshold_kwh
