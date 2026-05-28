from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum


class AlertType(str, Enum):
    HIGH_CONSUMPTION = "high_consumption"
    ANOMALY_DETECTED = "anomaly_detected"
    DEVICE_ALWAYS_ON = "device_always_on"
    THRESHOLD_EXCEEDED = "threshold_exceeded"
    UNUSUAL_PATTERN = "unusual_pattern"


class AlertSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ConsumptionAlert:
    """
    Entity: Alert generated when energy consumption exceeds defined thresholds
    or when an anomalous pattern is detected by the analytics service.
    """
    user_id: str
    device_id: str
    meter_id: str
    alert_type: AlertType
    severity: AlertSeverity
    threshold_value: float
    actual_value: float
    message: str
    is_read: bool = False
    is_resolved: bool = False
    id: Optional[str] = field(default=None)
    created_at: datetime = field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = field(default=None)

    def mark_as_read(self) -> None:
        self.is_read = True

    def resolve(self) -> None:
        self.is_resolved = True
        self.resolved_at = datetime.utcnow()

    def excess_percentage(self) -> float:
        """Returns the percentage by which actual_value exceeds threshold_value."""
        if self.threshold_value == 0:
            return 0.0
        return ((self.actual_value - self.threshold_value) / self.threshold_value) * 100
