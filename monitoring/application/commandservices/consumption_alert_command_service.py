import logging
from monitoring.domain.model.commands.create_consumption_alert_command import CreateConsumptionAlertCommand
from monitoring.domain.model.entities.consumption_alert import ConsumptionAlert
from monitoring.domain.model.repositories.consumption_alert_repository import ConsumptionAlertRepository
from monitoring.application.outboundservices.monitoring_event_publisher import MonitoringEventPublisher

logger = logging.getLogger(__name__)


class ConsumptionAlertCommandService:
    """Application service for managing consumption alert write operations."""

    def __init__(
        self,
        alert_repo: ConsumptionAlertRepository,
        event_publisher: MonitoringEventPublisher,
    ):
        self._alert_repo = alert_repo
        self._event_publisher = event_publisher

    async def handle_create(self, command: CreateConsumptionAlertCommand) -> ConsumptionAlert:
        alert = ConsumptionAlert(
            user_id=command.user_id,
            device_id=command.device_id,
            meter_id=command.meter_id,
            alert_type=command.alert_type,
            severity=command.severity,
            threshold_value=command.threshold_value,
            actual_value=command.actual_value,
            message=command.message,
        )
        saved_alert = await self._alert_repo.save(alert)
        logger.info(f"ConsumptionAlert created: id={saved_alert.id}, type={saved_alert.alert_type}")
        self._event_publisher.publish_alert_created(saved_alert)
        return saved_alert

    async def handle_mark_as_read(self, alert_id: str) -> ConsumptionAlert:
        updated = await self._alert_repo.mark_as_read(alert_id)
        if updated is None:
            raise ValueError(f"Alert not found: {alert_id}")
        return updated

    async def handle_resolve(self, alert_id: str) -> ConsumptionAlert:
        updated = await self._alert_repo.resolve(alert_id)
        if updated is None:
            raise ValueError(f"Alert not found: {alert_id}")
        return updated
