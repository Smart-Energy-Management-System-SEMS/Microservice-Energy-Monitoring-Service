from abc import ABC, abstractmethod
from typing import List, Optional
from monitoring.domain.model.entities.consumption_alert import ConsumptionAlert


class ConsumptionAlertRepository(ABC):
    """Abstract repository interface for ConsumptionAlert persistence."""

    @abstractmethod
    async def save(self, alert: ConsumptionAlert) -> ConsumptionAlert:
        pass

    @abstractmethod
    async def find_by_id(self, alert_id: str) -> Optional[ConsumptionAlert]:
        pass

    @abstractmethod
    async def find_by_user(self, user_id: str, limit: int = 50, skip: int = 0) -> List[ConsumptionAlert]:
        pass

    @abstractmethod
    async def find_unread_by_user(self, user_id: str) -> List[ConsumptionAlert]:
        pass

    @abstractmethod
    async def mark_as_read(self, alert_id: str) -> Optional[ConsumptionAlert]:
        pass

    @abstractmethod
    async def resolve(self, alert_id: str) -> Optional[ConsumptionAlert]:
        pass
