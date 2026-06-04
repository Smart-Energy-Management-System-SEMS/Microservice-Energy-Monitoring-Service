# Domain layer: a summary of how much energy one device used in a period.
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class DeviceConsumption:
    """Total energy and cost of a device for a given period of time.

    Instead of looking at thousands of single readings, we save the
    important numbers already added up (total kWh, cost, peak power...).
    """
    user_id: str
    device_id: str
    device_name: str          # friendly name, e.g. "Refrigerator"
    meter_id: str
    total_kwh: float          # total energy used in the period
    cost_estimate_soles: float  # estimated cost in soles (PEN)
    period_start: datetime
    period_end: datetime
    peak_power_watts: float     # highest power seen
    average_power_watts: float  # average power
    reading_count: int          # how many readings were summed
    id: Optional[str] = field(default=None)            # None until saved
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def cost_per_kwh(self, tariff: float = 0.68) -> float:
        """Estimate the cost using a price per kWh (0.68 is the Peru average)."""
        return self.total_kwh * tariff

    def is_high_consumer(self, threshold_kwh: float = 100.0) -> bool:
        """Return True if the device used more than the limit (100 kWh)."""
        return self.total_kwh > threshold_kwh
