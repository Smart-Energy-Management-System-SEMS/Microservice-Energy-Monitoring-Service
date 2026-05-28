from typing import List, Optional
import motor.motor_asyncio
from monitoring.domain.model.entities.device_consumption import DeviceConsumption
from monitoring.domain.model.repositories.device_consumption_repository import DeviceConsumptionRepository
from monitoring.infrastructure.persistence.mongodb.repositories.base_mongodb_repository import BaseMongoDBRepository
from monitoring.infrastructure.persistence.mongodb.model.document_mappers import DeviceConsumptionDocumentMapper


class DeviceConsumptionMongoDBRepository(BaseMongoDBRepository, DeviceConsumptionRepository):
    """MongoDB implementation of the DeviceConsumptionRepository."""

    COLLECTION = "device_consumptions"

    def __init__(self, db: motor.motor_asyncio.AsyncIOMotorDatabase):
        super().__init__(db, self.COLLECTION)

    async def save(self, consumption: DeviceConsumption) -> DeviceConsumption:
        document = DeviceConsumptionDocumentMapper.to_document(consumption)
        inserted_id = await self._insert(document)
        consumption.id = inserted_id
        return consumption

    async def find_by_id(self, consumption_id: str) -> Optional[DeviceConsumption]:
        doc = await self._find_by_id(consumption_id)
        return DeviceConsumptionDocumentMapper.to_entity(doc) if doc else None

    async def find_by_user(self, user_id: str, limit: int = 50, skip: int = 0) -> List[DeviceConsumption]:
        docs = await self._find_many({"user_id": user_id}, limit=limit, skip=skip)
        return [DeviceConsumptionDocumentMapper.to_entity(d) for d in docs]

    async def find_by_device(self, device_id: str, user_id: str) -> List[DeviceConsumption]:
        docs = await self._find_many({"device_id": device_id, "user_id": user_id})
        return [DeviceConsumptionDocumentMapper.to_entity(d) for d in docs]

    async def find_top_consumers(self, user_id: str, limit: int = 5) -> List[DeviceConsumption]:
        cursor = (
            self._collection.find({"user_id": user_id})
            .sort("total_kwh", -1)
            .limit(limit)
        )
        docs = await cursor.to_list(length=limit)
        return [DeviceConsumptionDocumentMapper.to_entity(d) for d in docs]
