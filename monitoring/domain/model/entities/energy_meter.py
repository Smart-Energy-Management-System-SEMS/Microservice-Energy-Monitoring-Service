from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum


class MeterStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    ERROR = "error"


@dataclass
class EnergyMeter:
    """
    Entity: Smart energy meter registered and linked to a user account.
    Represents the physical IoT device that captures energy readings.
    """
    user_id: str
    meter_serial: str
    model: str
    brand: str
    location: str
    status: MeterStatus = MeterStatus.ACTIVE
    firmware_version: str = "1.0.0"
    max_power_watts: float = 10000.0
    id: Optional[str] = field(default=None)
    registered_at: datetime = field(default_factory=datetime.utcnow)
    last_seen_at: Optional[datetime] = field(default=None)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def is_active(self) -> bool:
        return self.status == MeterStatus.ACTIVE

    def update_last_seen(self) -> None:
        self.last_seen_at = datetime.utcnow()

    def deactivate(self) -> None:
        self.status = MeterStatus.INACTIVE
        self.updated_at = datetime.utcnow()
