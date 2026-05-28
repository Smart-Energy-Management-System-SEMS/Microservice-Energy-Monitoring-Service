from typing import List, Optional
from monitoring.domain.model.entities.device_consumption import DeviceConsumption
from monitoring.domain.model.queries.get_by_user_query import GetByUserQuery
from monitoring.domain.model.queries.get_by_device_query import GetByDeviceQuery
from monitoring.domain.model.repositories.device_consumption_repository import DeviceConsumptionRepository


class DeviceConsumptionQueryService:
    """Application service for querying device consumption data (read side)."""

    def __init__(self, consumption_repo: DeviceConsumptionRepository):
        self._consumption_repo = consumption_repo

    async def get_by_user(self, query: GetByUserQuery) -> List[DeviceConsumption]:
        return await self._consumption_repo.find_by_user(query.user_id, query.limit, query.skip)

    async def get_by_device(self, query: GetByDeviceQuery) -> List[DeviceConsumption]:
        return await self._consumption_repo.find_by_device(query.device_id, query.user_id)

    async def get_by_id(self, consumption_id: str) -> Optional[DeviceConsumption]:
        return await self._consumption_repo.find_by_id(consumption_id)

    async def get_top_consumers(self, user_id: str, limit: int = 5) -> List[DeviceConsumption]:
        return await self._consumption_repo.find_top_consumers(user_id, limit)
