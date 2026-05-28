from typing import Optional, List, Dict, Any
from bson import ObjectId
import motor.motor_asyncio


class BaseMongoDBRepository:
    """
    Base repository providing common CRUD operations for MongoDB collections.
    All concrete repositories should extend this class.
    """

    def __init__(self, db: motor.motor_asyncio.AsyncIOMotorDatabase, collection_name: str):
        self._collection: motor.motor_asyncio.AsyncIOMotorCollection = db[collection_name]

    async def _insert(self, document: Dict[str, Any]) -> str:
        result = await self._collection.insert_one(document)
        return str(result.inserted_id)

    async def _find_by_id(self, entity_id: str) -> Optional[Dict[str, Any]]:
        try:
            return await self._collection.find_one({"_id": ObjectId(entity_id)})
        except Exception:
            return None

    async def _find_many(
        self,
        query: Dict[str, Any],
        limit: int = 50,
        skip: int = 0,
        sort_field: str = "created_at",
        sort_order: int = -1,
    ) -> List[Dict[str, Any]]:
        cursor = (
            self._collection.find(query)
            .sort(sort_field, sort_order)
            .skip(skip)
            .limit(limit)
        )
        return await cursor.to_list(length=limit)

    async def _update_one(self, entity_id: str, update_fields: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            result = await self._collection.find_one_and_update(
                {"_id": ObjectId(entity_id)},
                {"$set": update_fields},
                return_document=True,
            )
            return result
        except Exception:
            return None

    async def _count(self, query: Dict[str, Any]) -> int:
        return await self._collection.count_documents(query)
