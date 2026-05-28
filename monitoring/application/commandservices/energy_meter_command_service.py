import logging
from monitoring.domain.model.commands.register_energy_meter_command import RegisterEnergyMeterCommand
from monitoring.domain.model.entities.energy_meter import EnergyMeter
from monitoring.domain.model.repositories.energy_meter_repository import EnergyMeterRepository

logger = logging.getLogger(__name__)


class EnergyMeterCommandService:
    """Application service for managing energy meter registration and state."""

    def __init__(self, meter_repo: EnergyMeterRepository):
        self._meter_repo = meter_repo

    async def handle_register(self, command: RegisterEnergyMeterCommand) -> EnergyMeter:
        # Check for duplicate serial
        existing = await self._meter_repo.find_by_serial(command.meter_serial)
        if existing:
            raise ValueError(f"Meter with serial '{command.meter_serial}' is already registered.")

        meter = EnergyMeter(
            user_id=command.user_id,
            meter_serial=command.meter_serial,
            model=command.model,
            brand=command.brand,
            location=command.location,
            firmware_version=command.firmware_version,
            max_power_watts=command.max_power_watts,
        )
        saved = await self._meter_repo.save(meter)
        logger.info(f"EnergyMeter registered: id={saved.id}, serial={saved.meter_serial}")
        return saved

    async def handle_deactivate(self, meter_id: str) -> EnergyMeter:
        updated = await self._meter_repo.update_status(meter_id, "inactive")
        if updated is None:
            raise ValueError(f"Meter not found: {meter_id}")
        logger.info(f"EnergyMeter deactivated: id={meter_id}")
        return updated
