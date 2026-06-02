import logging
from monitoring.domain.model.commands.create_energy_reading_command import CreateEnergyReadingCommand
from monitoring.domain.model.entities.energy_reading import EnergyReading
from monitoring.domain.model.repositories.energy_reading_repository import EnergyReadingRepository
from monitoring.domain.model.services.monitoring_rule_service import MonitoringRuleService
from monitoring.application.outboundservices.monitoring_event_publisher import MonitoringEventPublisher

logger = logging.getLogger(__name__)


class EnergyReadingCommandService:
    """Application service for handling energy reading write operations."""

    def __init__(
        self,
        reading_repo: EnergyReadingRepository,
        rule_service: MonitoringRuleService,
        event_publisher: MonitoringEventPublisher,
    ):
        self._reading_repo = reading_repo
        self._rule_service = rule_service
        self._event_publisher = event_publisher

    async def handle_create(self, command: CreateEnergyReadingCommand) -> EnergyReading:
        reading = EnergyReading(
            user_id=command.user_id,
            meter_id=command.meter_id,
            device_id=command.device_id,
            power_watts=command.power_watts,
            voltage=command.voltage,
            current=command.current,
            frequency=command.frequency,
            energy_kwh=command.energy_kwh,
            timestamp=command.timestamp,
            reading_type=command.reading_type,
            phase=command.phase,
        )
        saved_reading = await self._reading_repo.save(reading)
        logger.info(f"EnergyReading saved: id={saved_reading.id}, device={saved_reading.device_id}")

        # Evaluate rules and publish alert if needed
        alert = self._rule_service.evaluate_reading(saved_reading)
        if alert:
            logger.warning(f"Alert triggered for reading {saved_reading.id}: {alert.alert_type}")

        self._event_publisher.publish_reading_processed(saved_reading)
        return saved_reading
