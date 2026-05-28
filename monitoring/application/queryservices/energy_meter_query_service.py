from typing import List, Optional
from monitoring.domain.model.entities.energy_meter import EnergyMeter
from monitoring.domain.model.repositories.energy_meter_repository import EnergyMeterRepository


class EnergyMeterQueryService:
    """Application service for querying energy meter data (read side)."""

    def __init__(self, meter_repo: EnergyMeterRepository):
        self._meter_repo = meter_repo

    async def get_by_user(self, user_id: str) -> List[EnergyMeter]:
        return await self._meter_repo.find_by_user(user_id)

    async def get_by_id(self, meter_id: str) -> Optional[EnergyMeter]:
        return await self._meter_repo.find_by_id(meter_id)

    async def get_by_serial(self, meter_serial: str) -> Optional[EnergyMeter]:
        return await self._meter_repo.find_by_serial(meter_serial)
