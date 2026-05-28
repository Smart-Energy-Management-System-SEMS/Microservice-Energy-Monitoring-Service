from typing import List, Optional
from datetime import datetime
import motor.motor_asyncio
from monitoring.domain.model.entities.consumption_alert import ConsumptionAlert
from monitoring.domain.model.repositories.consumption_alert_repository import ConsumptionAlertRepository
from monitoring.infrastructure.persistence.mongodb.repositories.base_mongodb_repository import BaseMongoDBRepository
from monitoring.infrastructure.persistence.mongodb.model.document_mappers import ConsumptionAlertDocumentMapper


class ConsumptionAlertMongoDBRepository(BaseMongoDBRepository, ConsumptionAlertRepository):
    """MongoDB implementation of the ConsumptionAlertRepository."""

    COLLECTION = "consumption_alerts"

    def __init__(self, db: motor.motor_asyncio.AsyncIOMotorDatabase):
        super().__init__(db, self.COLLECTION)

    async def save(self, alert: ConsumptionAlert) -> ConsumptionAlert:
        document = ConsumptionAlertDocumentMapper.to_document(alert)
        inserted_id = await self._insert(document)
        alert.id = inserted_id
        return alert

    async def find_by_id(self, alert_id: str) -> Optional[ConsumptionAlert]:
        doc = await self._find_by_id(alert_id)
        return ConsumptionAlertDocumentMapper.to_entity(doc) if doc else None

    async def find_by_user(self, user_id: str, limit: int = 50, skip: int = 0) -> List[ConsumptionAlert]:
        docs = await self._find_many({"user_id": user_id}, limit=limit, skip=skip)
        return [ConsumptionAlertDocumentMapper.to_entity(d) for d in docs]

    async def find_unread_by_user(self, user_id: str) -> List[ConsumptionAlert]:
        docs = await self._find_many({"user_id": user_id, "is_read": False})
        return [ConsumptionAlertDocumentMapper.to_entity(d) for d in docs]

    async def mark_as_read(self, alert_id: str) -> Optional[ConsumptionAlert]:
        doc = await self._update_one(alert_id, {"is_read": True})
        return ConsumptionAlertDocumentMapper.to_entity(doc) if doc else None

    async def resolve(self, alert_id: str) -> Optional[ConsumptionAlert]:
        doc = await self._update_one(alert_id, {
            "is_resolved": True,
            "resolved_at": datetime.utcnow(),
        })
        return ConsumptionAlertDocumentMapper.to_entity(doc) if doc else None
