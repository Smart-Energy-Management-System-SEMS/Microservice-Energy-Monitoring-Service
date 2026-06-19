from typing import List, Optional
from datetime import datetime
import motor.motor_asyncio
from monitoring.domain.model.entities.energy_reading import EnergyReading
from monitoring.domain.model.repositories.energy_reading_repository import EnergyReadingRepository
from monitoring.infrastructure.persistence.mongodb.repositories.base_mongodb_repository import BaseMongoDBRepository
from monitoring.infrastructure.persistence.mongodb.model.document_mappers import EnergyReadingDocumentMapper


class EnergyReadingMongoDBRepository(BaseMongoDBRepository, EnergyReadingRepository):
    """MongoDB implementation of the EnergyReadingRepository."""

    COLLECTION = "energy_readings"

    def __init__(self, db: motor.motor_asyncio.AsyncIOMotorDatabase):
        super().__init__(db, self.COLLECTION)

    async def save(self, reading: EnergyReading) -> EnergyReading:
        document = EnergyReadingDocumentMapper.to_document(reading)
        inserted_id = await self._insert(document)
        reading.id = inserted_id
        return reading

    async def find_by_id(self, reading_id: str) -> Optional[EnergyReading]:
        doc = await self._find_by_id(reading_id)
        return EnergyReadingDocumentMapper.to_entity(doc) if doc else None

    async def find_by_user(self, user_id: str, limit: int = 50, skip: int = 0) -> List[EnergyReading]:
        docs = await self._find_many({"user_id": user_id}, limit=limit, skip=skip, sort_field="timestamp")
        return [EnergyReadingDocumentMapper.to_entity(d) for d in docs]

    async def find_by_device(self, device_id: str, user_id: str, limit: int = 50, skip: int = 0) -> List[EnergyReading]:
        docs = await self._find_many(
            {"device_id": device_id, "user_id": user_id},
            limit=limit, skip=skip, sort_field="timestamp"
        )
        return [EnergyReadingDocumentMapper.to_entity(d) for d in docs]

    async def find_by_date_range(
        self, user_id: str, start_date: datetime, end_date: datetime,
        device_id: Optional[str] = None, limit: int = 100, skip: int = 0
    ) -> List[EnergyReading]:
        query = {
            "user_id": user_id,
            "timestamp": {"$gte": start_date, "$lte": end_date},
        }
        if device_id:
            query["device_id"] = device_id
        docs = await self._find_many(query, limit=limit, skip=skip, sort_field="timestamp")
        return [EnergyReadingDocumentMapper.to_entity(d) for d in docs]

    async def find_latest_by_meter(self, meter_id: str) -> Optional[EnergyReading]:
        docs = await self._find_many({"meter_id": meter_id}, limit=1, sort_field="timestamp")
        return EnergyReadingDocumentMapper.to_entity(docs[0]) if docs else None

    async def find_latest_by_device(self, device_id: str) -> Optional[EnergyReading]:
        docs = await self._find_many({"device_id": device_id}, limit=1, sort_field="timestamp")
        return EnergyReadingDocumentMapper.to_entity(docs[0]) if docs else None

    async def find_history_by_device(self, device_id: str, limit: int = 50, skip: int = 0) -> List[EnergyReading]:
        docs = await self._find_many({"device_id": device_id}, limit=limit, skip=skip, sort_field="timestamp")
        return [EnergyReadingDocumentMapper.to_entity(d) for d in docs]
