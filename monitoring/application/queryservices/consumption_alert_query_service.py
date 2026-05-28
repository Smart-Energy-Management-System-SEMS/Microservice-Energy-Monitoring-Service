from typing import List, Optional
from monitoring.domain.model.entities.consumption_alert import ConsumptionAlert
from monitoring.domain.model.queries.get_by_user_query import GetByUserQuery
from monitoring.domain.model.repositories.consumption_alert_repository import ConsumptionAlertRepository


class ConsumptionAlertQueryService:
    """Application service for querying consumption alerts (read side)."""

    def __init__(self, alert_repo: ConsumptionAlertRepository):
        self._alert_repo = alert_repo

    async def get_by_user(self, query: GetByUserQuery) -> List[ConsumptionAlert]:
        return await self._alert_repo.find_by_user(query.user_id, query.limit, query.skip)

    async def get_unread_by_user(self, user_id: str) -> List[ConsumptionAlert]:
        return await self._alert_repo.find_unread_by_user(user_id)

    async def get_by_id(self, alert_id: str) -> Optional[ConsumptionAlert]:
        return await self._alert_repo.find_by_id(alert_id)
