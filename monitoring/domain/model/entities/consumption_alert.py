# Domain layer: an alert we create when something looks wrong with the energy use.
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum


class AlertType(str, Enum):
    """The reason why the alert was created."""
    HIGH_CONSUMPTION = "high_consumption"     # using too much power
    ANOMALY_DETECTED = "anomaly_detected"     # analytics found something odd
    DEVICE_ALWAYS_ON = "device_always_on"     # a device never turns off
    THRESHOLD_EXCEEDED = "threshold_exceeded" # passed a kWh limit
    UNUSUAL_PATTERN = "unusual_pattern"       # behaves differently than usual


class AlertSeverity(str, Enum):
    """How urgent the alert is (low is least, critical is most)."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ConsumptionAlert:
    """A warning shown to the user when consumption breaks a rule.

    It saves what we expected (threshold_value) and what really happened
    (actual_value), plus a message explaining it.
    """
    user_id: str
    device_id: str
    meter_id: str
    alert_type: AlertType
    severity: AlertSeverity
    threshold_value: float   # the limit we were checking
    actual_value: float      # the real value that broke the limit
    message: str             # text shown to the user
    is_read: bool = False
    is_resolved: bool = False
    id: Optional[str] = field(default=None)            # None until saved
    created_at: datetime = field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = field(default=None)

    def mark_as_read(self) -> None:
        """Mark the alert as seen by the user."""
        self.is_read = True

    def resolve(self) -> None:
        """Close the alert and save when it was solved."""
        self.is_resolved = True
        self.resolved_at = datetime.utcnow()

    def excess_percentage(self) -> float:
        """How much (in %) the real value went over the limit."""
        if self.threshold_value == 0:
            return 0.0  # avoid dividing by zero
        return ((self.actual_value - self.threshold_value) / self.threshold_value) * 100
