from abc import ABC, abstractmethod
from typing import List, Optional
from monitoring.domain.model.entities.device_consumption import DeviceConsumption


class DeviceConsumptionRepository(ABC):
    """Abstract repository interface for DeviceConsumption persistence."""

    @abstractmethod
    async def save(self, consumption: DeviceConsumption) -> DeviceConsumption:
        pass

    @abstractmethod
    async def find_by_id(self, consumption_id: str) -> Optional[DeviceConsumption]:
        pass

    @abstractmethod
    async def find_by_user(self, user_id: str, limit: int = 50, skip: int = 0) -> List[DeviceConsumption]:
        pass

    @abstractmethod
    async def find_by_device(self, device_id: str, user_id: str) -> List[DeviceConsumption]:
        pass

    @abstractmethod
    async def find_top_consumers(self, user_id: str, limit: int = 5) -> List[DeviceConsumption]:
        pass
