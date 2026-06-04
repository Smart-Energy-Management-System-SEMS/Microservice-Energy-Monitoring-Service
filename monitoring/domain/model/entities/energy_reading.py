# Domain layer: one single reading taken from a meter.
# A reading is just a snapshot of the electricity at one moment in time.
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from bson import ObjectId


@dataclass
class EnergyReading:
    """One measurement sent by a meter at a specific time.

    Many readings together form the history we use to calculate
    consumption and to detect problems.
    """
    user_id: str
    meter_id: str           # which meter sent it
    device_id: str          # which appliance is being measured
    power_watts: float      # power right now, in watts (W)
    voltage: float          # volts (V)
    current: float          # amperes (A)
    frequency: float        # hertz (Hz), around 60 in Peru
    energy_kwh: float       # energy for this reading, in kWh
    timestamp: datetime     # when the measurement was taken
    reading_type: str = "real_time"   # real_time | scheduled | on_demand
    phase: str = "single"             # single | three
    id: Optional[str] = field(default=None)            # None until saved
    created_at: datetime = field(default_factory=datetime.utcnow)

    def is_high_consumption(self, threshold_watts: float = 2000.0) -> bool:
        """Return True if the power is above the limit (2 kW by default)."""
        return self.power_watts > threshold_watts

    def to_kwh_rate(self) -> float:
        """Turn the current power into kWh per hour (watts / 1000)."""
        return self.power_watts / 1000.0
