# Application layer: creates FAKE readings to test the system without real meters.
import uuid

from monitoring.application.commandservices.energy_reading_command_service import EnergyReadingCommandService
from monitoring.application.outboundservices.monitoring_event_publisher import MonitoringEventPublisher
from monitoring.domain.model.commands.create_energy_reading_command import CreateEnergyReadingCommand
from monitoring.domain.model.entities.energy_reading import EnergyReading
from monitoring.domain.model.services.energy_pricing_provider import EnergyPricingProvider
from monitoring.domain.model.services.eos_iot_provider import EosIotProvider
from monitoring.domain.model.valueobjects.energy_price import EnergyPrice


class EnergySimulationCommandService:
    """Builds a simulated reading, saves it and sends out an event."""

    def __init__(
        self,
        eos_provider: EosIotProvider,
        pricing_provider: EnergyPricingProvider,
        reading_command_service: EnergyReadingCommandService,
        event_publisher: MonitoringEventPublisher,
    ):
        # All the helpers we need are passed in from outside.
        self._eos_provider = eos_provider
        self._pricing_provider = pricing_provider
        self._reading_command_service = reading_command_service
        self._event_publisher = event_publisher

    async def generate_reading(
        self,
        user_id: str,
        device_id: str,
        device_type: str = "unknown",
    ) -> tuple[EnergyReading, EnergyPrice, float]:
        """Make a fake reading, save it, and return it with the price and cost."""
        # 1) Ask the fake IoT provider for telemetry and the current price.
        telemetry = await self._eos_provider.generate_reading(device_id, device_type=device_type)
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

        # 2) Estimate the cost (energy * price) and announce the new reading.
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
        """Make a fake meter id from the device id."""
        return f"sim-meter-{device_id}"
