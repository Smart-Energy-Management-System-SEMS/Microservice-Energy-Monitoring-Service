import logging
from monitoring.domain.model.commands.create_device_consumption_command import CreateDeviceConsumptionCommand
from monitoring.domain.model.entities.device_consumption import DeviceConsumption
from monitoring.domain.model.repositories.device_consumption_repository import DeviceConsumptionRepository
from monitoring.domain.model.repositories.consumption_alert_repository import ConsumptionAlertRepository
from monitoring.domain.model.services.monitoring_rule_service import MonitoringRuleService
from monitoring.application.outboundservices.monitoring_event_publisher import MonitoringEventPublisher

logger = logging.getLogger(__name__)


class DeviceConsumptionCommandService:
    """Application service for handling device consumption write operations."""

    def __init__(
        self,
        consumption_repo: DeviceConsumptionRepository,
        alert_repo: ConsumptionAlertRepository,
        rule_service: MonitoringRuleService,
        event_publisher: MonitoringEventPublisher,
    ):
        self._consumption_repo = consumption_repo
        self._alert_repo = alert_repo
        self._rule_service = rule_service
        self._event_publisher = event_publisher

    async def handle_create(self, command: CreateDeviceConsumptionCommand) -> DeviceConsumption:
        consumption = DeviceConsumption(
            user_id=command.user_id,
            device_id=command.device_id,
            device_name=command.device_name,
            meter_id=command.meter_id,
            total_kwh=command.total_kwh,
            cost_estimate_soles=command.cost_estimate_soles,
            period_start=command.period_start,
            period_end=command.period_end,
            peak_power_watts=command.peak_power_watts,
            average_power_watts=command.average_power_watts,
            reading_count=command.reading_count,
        )
        saved = await self._consumption_repo.save(consumption)
        logger.info(f"DeviceConsumption saved: id={saved.id}, device={saved.device_id}")

        # Evaluate consumption rules
        alert = self._rule_service.evaluate_device_consumption(saved)
        if alert:
            saved_alert = await self._alert_repo.save(alert)
            self._event_publisher.publish_alert_created(saved_alert)
            logger.info(f"Alert created for device consumption: alert_id={saved_alert.id}")

        return saved
