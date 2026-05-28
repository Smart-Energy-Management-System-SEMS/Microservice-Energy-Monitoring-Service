from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from monitoring.domain.model.entities.energy_reading import EnergyReading


class EnergyReadingRepository(ABC):
    """Abstract repository interface for EnergyReading persistence."""

    @abstractmethod
    async def save(self, reading: EnergyReading) -> EnergyReading:
        pass

    @abstractmethod
    async def find_by_id(self, reading_id: str) -> Optional[EnergyReading]:
        pass

    @abstractmethod
    async def find_by_user(self, user_id: str, limit: int = 50, skip: int = 0) -> List[EnergyReading]:
        pass

    @abstractmethod
    async def find_by_device(self, device_id: str, user_id: str, limit: int = 50, skip: int = 0) -> List[EnergyReading]:
        pass

    @abstractmethod
    async def find_by_date_range(
        self, user_id: str, start_date: datetime, end_date: datetime,
        device_id: Optional[str] = None, limit: int = 100, skip: int = 0
    ) -> List[EnergyReading]:
        pass

    @abstractmethod
    async def find_latest_by_meter(self, meter_id: str) -> Optional[EnergyReading]:
        pass
