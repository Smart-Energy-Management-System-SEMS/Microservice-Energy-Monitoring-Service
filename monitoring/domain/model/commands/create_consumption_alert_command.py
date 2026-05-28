from dataclasses import dataclass
from monitoring.domain.model.entities.consumption_alert import AlertType, AlertSeverity


@dataclass
class CreateConsumptionAlertCommand:
    """Command to create a new consumption alert for a user/device."""
    user_id: str
    device_id: str
    meter_id: str
    alert_type: AlertType
    severity: AlertSeverity
    threshold_value: float
    actual_value: float
    message: str
