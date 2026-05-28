from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional
import json


@dataclass
class EnergyReadingIngestedEvent:
    """Event published when a new energy reading is received from the IoT device."""
    event_type: str = "EnergyReadingIngested"
    reading_id: str = ""
    user_id: str = ""
    meter_id: str = ""
    device_id: str = ""
    power_watts: float = 0.0
    energy_kwh: float = 0.0
    timestamp: str = ""
    occurred_at: str = ""

    def to_json(self) -> str:
        return json.dumps(asdict(self))


@dataclass
class ConsumptionAlertCreatedEvent:
    """Event published when a new consumption alert is generated."""
    event_type: str = "ConsumptionAlertCreated"
    alert_id: str = ""
    user_id: str = ""
    device_id: str = ""
    meter_id: str = ""
    alert_type: str = ""
    severity: str = ""
    message: str = ""
    actual_value: float = 0.0
    threshold_value: float = 0.0
    occurred_at: str = ""

    def to_json(self) -> str:
        return json.dumps(asdict(self))


@dataclass
class AnomalyDetectedExternalEvent:
    """
    Event consumed from the Analytics Service when an anomaly is detected.
    This is an inbound event from another bounded context.
    """
    event_type: str = ""
    anomaly_id: str = ""
    user_id: str = ""
    device_id: str = ""
    description: str = ""
    score: float = 0.0
    detected_at: str = ""

    @classmethod
    def from_json(cls, data: dict) -> "AnomalyDetectedExternalEvent":
        return cls(
            event_type=data.get("event_type", ""),
            anomaly_id=data.get("anomaly_id", ""),
            user_id=data.get("user_id", ""),
            device_id=data.get("device_id", ""),
            description=data.get("description", ""),
            score=data.get("score", 0.0),
            detected_at=data.get("detected_at", ""),
        )
