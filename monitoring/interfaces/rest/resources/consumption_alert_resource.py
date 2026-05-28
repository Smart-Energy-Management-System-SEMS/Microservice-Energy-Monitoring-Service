from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from monitoring.domain.model.entities.consumption_alert import AlertType, AlertSeverity


class CreateConsumptionAlertRequest(BaseModel):
    user_id: str
    device_id: str
    meter_id: str
    alert_type: AlertType
    severity: AlertSeverity
    threshold_value: float
    actual_value: float
    message: str


class ConsumptionAlertResponse(BaseModel):
    id: str
    user_id: str
    device_id: str
    meter_id: str
    alert_type: AlertType
    severity: AlertSeverity
    threshold_value: float
    actual_value: float
    message: str
    is_read: bool
    is_resolved: bool
    created_at: datetime
    resolved_at: Optional[datetime] = None
