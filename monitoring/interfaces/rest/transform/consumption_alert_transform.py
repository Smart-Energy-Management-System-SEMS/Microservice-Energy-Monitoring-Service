from monitoring.domain.model.entities.consumption_alert import ConsumptionAlert
from monitoring.interfaces.rest.resources.consumption_alert_resource import ConsumptionAlertResponse


class ConsumptionAlertTransform:
    @staticmethod
    def to_response(alert: ConsumptionAlert) -> ConsumptionAlertResponse:
        return ConsumptionAlertResponse(
            id=alert.id,
            user_id=alert.user_id,
            device_id=alert.device_id,
            meter_id=alert.meter_id,
            alert_type=alert.alert_type,
            severity=alert.severity,
            threshold_value=alert.threshold_value,
            actual_value=alert.actual_value,
            message=alert.message,
            is_read=alert.is_read,
            is_resolved=alert.is_resolved,
            created_at=alert.created_at,
            resolved_at=alert.resolved_at,
        )
