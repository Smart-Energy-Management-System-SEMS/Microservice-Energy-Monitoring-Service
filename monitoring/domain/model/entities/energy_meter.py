# Domain layer: the smart energy meter (the physical device).
# This is the "business" model, so it has no database or framework code.
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum


class MeterStatus(str, Enum):
    """The possible states a meter can be in."""
    ACTIVE = "active"            # working and sending readings
    INACTIVE = "inactive"        # turned off / not sending
    MAINTENANCE = "maintenance"  # offline because it's being serviced
    ERROR = "error"              # something went wrong


@dataclass
class EnergyMeter:
    """A smart energy meter that belongs to a user.

    It represents the real IoT device that measures how much energy
    is being used and produces the readings we store later.
    """
    user_id: str            # who owns the meter
    meter_serial: str       # serial number of the device
    model: str
    brand: str
    location: str           # where it is installed, e.g. "Kitchen"
    status: MeterStatus = MeterStatus.ACTIVE
    firmware_version: str = "1.0.0"
    max_power_watts: float = 10000.0   # max power it can measure
    id: Optional[str] = field(default=None)            # None until saved in the DB
    registered_at: datetime = field(default_factory=datetime.utcnow)
    last_seen_at: Optional[datetime] = field(default=None)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def is_active(self) -> bool:
        """Return True if the meter is currently active."""
        return self.status == MeterStatus.ACTIVE

    def update_last_seen(self) -> None:
        """Save the current time as the last moment the meter reported."""
        self.last_seen_at = datetime.utcnow()

    def deactivate(self) -> None:
        """Turn the meter off and remember when we did it."""
        self.status = MeterStatus.INACTIVE
        self.updated_at = datetime.utcnow()
