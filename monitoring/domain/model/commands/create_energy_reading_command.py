from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreateEnergyReadingCommand:
    """Command to record a new raw energy reading from a smart meter."""
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
