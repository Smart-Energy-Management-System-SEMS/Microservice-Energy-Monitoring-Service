from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from bson import ObjectId


@dataclass
class EnergyReading:
    """
    Entity: Raw telemetry reading from a smart energy meter.
    Represents a single measurement captured at a specific point in time.
    """
    user_id: str
    meter_id: str
    device_id: str
    power_watts: float
    voltage: float
    current: float
    frequency: float
    energy_kwh: float
    timestamp: datetime
    reading_type: str = "real_time"       # real_time | scheduled | on_demand
    phase: str = "single"                 # single | three
    id: Optional[str] = field(default=None)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def is_high_consumption(self, threshold_watts: float = 2000.0) -> bool:
        return self.power_watts > threshold_watts

    def to_kwh_rate(self) -> float:
        """Returns the instantaneous power in kWh per hour."""
        return self.power_watts / 1000.0
