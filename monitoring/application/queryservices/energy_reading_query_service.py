from typing import List, Optional
from monitoring.domain.model.entities.energy_reading import EnergyReading
from monitoring.domain.model.queries.get_by_user_query import GetByUserQuery
from monitoring.domain.model.queries.get_by_device_query import GetByDeviceQuery
from monitoring.domain.model.queries.get_by_date_range_query import GetByDateRangeQuery
from monitoring.domain.model.repositories.energy_reading_repository import EnergyReadingRepository


class EnergyReadingQueryService:
    """Application service for querying energy readings (read side)."""

    def __init__(self, reading_repo: EnergyReadingRepository):
        self._reading_repo = reading_repo

    async def get_by_user(self, query: GetByUserQuery) -> List[EnergyReading]:
        return await self._reading_repo.find_by_user(query.user_id, query.limit, query.skip)

    async def get_by_device(self, query: GetByDeviceQuery) -> List[EnergyReading]:
        return await self._reading_repo.find_by_device(query.device_id, query.user_id, query.limit, query.skip)

    async def get_by_date_range(self, query: GetByDateRangeQuery) -> List[EnergyReading]:
        return await self._reading_repo.find_by_date_range(
            query.user_id, query.start_date, query.end_date,
            query.device_id, query.limit, query.skip,
        )

    async def get_by_id(self, reading_id: str) -> Optional[EnergyReading]:
        return await self._reading_repo.find_by_id(reading_id)

    async def get_latest_by_meter(self, meter_id: str) -> Optional[EnergyReading]:
        return await self._reading_repo.find_latest_by_meter(meter_id)
