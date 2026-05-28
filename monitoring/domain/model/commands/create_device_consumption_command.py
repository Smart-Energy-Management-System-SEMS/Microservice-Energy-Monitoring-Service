from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreateDeviceConsumptionCommand:
    """Command to record aggregated device consumption for a time period."""
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
