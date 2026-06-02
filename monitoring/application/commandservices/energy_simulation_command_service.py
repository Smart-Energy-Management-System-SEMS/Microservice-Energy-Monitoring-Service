import uuid

from monitoring.application.commandservices.energy_reading_command_service import EnergyReadingCommandService
from monitoring.application.outboundservices.monitoring_event_publisher import MonitoringEventPublisher
from monitoring.domain.model.commands.create_energy_reading_command import CreateEnergyReadingCommand
from monitoring.domain.model.entities.energy_reading import EnergyReading
from monitoring.domain.model.services.energy_pricing_provider import EnergyPricingProvider
from monitoring.domain.model.services.eos_iot_provider import EosIotProvider
from monitoring.domain.model.valueobjects.energy_price import EnergyPrice


class EnergySimulationCommandService:
    """Orchestrates simulated telemetry creation and publication."""

    def __init__(
        self,
        eos_provider: EosIotProvider,
        pricing_provider: EnergyPricingProvider,
        reading_command_service: EnergyReadingCommandService,
        event_publisher: MonitoringEventPublisher,
    ):
        self._eos_provider = eos_provider
        self._pricing_provider = pricing_provider
        self._reading_command_service = reading_command_service
        self._event_publisher = event_publisher

    async def generate_reading(self, user_id: str, device_id: str) -> tuple[EnergyReading, EnergyPrice, float]:
        telemetry = await self._eos_provider.generate_reading(device_id)
        price = await self._pricing_provider.get_current_price()

        reading = await self._reading_command_service.handle_create(
            CreateEnergyReadingCommand(
                user_id=user_id,
                meter_id=self._build_meter_id(device_id),
                device_id=device_id,
                power_watts=telemetry.power_watts,
                voltage=telemetry.voltage,
                current=telemetry.current,
                frequency=telemetry.frequency,
                energy_kwh=telemetry.energy_kwh,
                timestamp=telemetry.timestamp,
                reading_type=telemetry.reading_type,
                phase=telemetry.phase,
            )
        )

        estimated_cost = round(reading.energy_kwh * price.price_per_kwh, 2)
        self._event_publisher.publish_energy_reading_created(
            event_id=str(uuid.uuid4()),
            reading=reading,
            estimated_cost=estimated_cost,
            currency=price.currency,
        )
        return reading, price, estimated_cost

    @staticmethod
    def _build_meter_id(device_id: str) -> str:
        return f"sim-meter-{device_id}"
