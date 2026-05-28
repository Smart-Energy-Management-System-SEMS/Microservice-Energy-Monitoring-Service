from abc import ABC, abstractmethod
from typing import List, Optional
from monitoring.domain.model.entities.energy_meter import EnergyMeter


class EnergyMeterRepository(ABC):
    """Abstract repository interface for EnergyMeter persistence."""

    @abstractmethod
    async def save(self, meter: EnergyMeter) -> EnergyMeter:
        pass

    @abstractmethod
    async def find_by_id(self, meter_id: str) -> Optional[EnergyMeter]:
        pass

    @abstractmethod
    async def find_by_serial(self, meter_serial: str) -> Optional[EnergyMeter]:
        pass

    @abstractmethod
    async def find_by_user(self, user_id: str) -> List[EnergyMeter]:
        pass

    @abstractmethod
    async def update_status(self, meter_id: str, status: str) -> Optional[EnergyMeter]:
        pass

    @abstractmethod
    async def update_last_seen(self, meter_id: str) -> Optional[EnergyMeter]:
        pass
