from typing import List, Optional
from datetime import datetime
import motor.motor_asyncio
from monitoring.domain.model.entities.energy_meter import EnergyMeter
from monitoring.domain.model.repositories.energy_meter_repository import EnergyMeterRepository
from monitoring.infrastructure.persistence.mongodb.repositories.base_mongodb_repository import BaseMongoDBRepository
from monitoring.infrastructure.persistence.mongodb.model.document_mappers import EnergyMeterDocumentMapper


class EnergyMeterMongoDBRepository(BaseMongoDBRepository, EnergyMeterRepository):
    """MongoDB implementation of the EnergyMeterRepository."""

    COLLECTION = "energy_meters"

    def __init__(self, db: motor.motor_asyncio.AsyncIOMotorDatabase):
        super().__init__(db, self.COLLECTION)

    async def save(self, meter: EnergyMeter) -> EnergyMeter:
        document = EnergyMeterDocumentMapper.to_document(meter)
        inserted_id = await self._insert(document)
        meter.id = inserted_id
        return meter

    async def find_by_id(self, meter_id: str) -> Optional[EnergyMeter]:
        doc = await self._find_by_id(meter_id)
        return EnergyMeterDocumentMapper.to_entity(doc) if doc else None

    async def find_by_serial(self, meter_serial: str) -> Optional[EnergyMeter]:
        doc = await self._collection.find_one({"meter_serial": meter_serial})
        return EnergyMeterDocumentMapper.to_entity(doc) if doc else None

    async def find_by_user(self, user_id: str) -> List[EnergyMeter]:
        docs = await self._find_many({"user_id": user_id})
        return [EnergyMeterDocumentMapper.to_entity(d) for d in docs]

    async def update_status(self, meter_id: str, status: str) -> Optional[EnergyMeter]:
        doc = await self._update_one(meter_id, {"status": status, "updated_at": datetime.utcnow()})
        return EnergyMeterDocumentMapper.to_entity(doc) if doc else None

    async def update_last_seen(self, meter_id: str) -> Optional[EnergyMeter]:
        doc = await self._update_one(meter_id, {"last_seen_at": datetime.utcnow()})
        return EnergyMeterDocumentMapper.to_entity(doc) if doc else None
