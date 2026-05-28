import motor.motor_asyncio
from monitoring.infrastructure.configuration.settings import settings


class MongoDBClient:
    """Singleton MongoDB client using Motor (async driver)."""

    _client: motor.motor_asyncio.AsyncIOMotorClient = None
    _db: motor.motor_asyncio.AsyncIOMotorDatabase = None

    @classmethod
    def get_client(cls) -> motor.motor_asyncio.AsyncIOMotorClient:
        if cls._client is None:
            cls._client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongodb_url)
        return cls._client

    @classmethod
    def get_database(cls) -> motor.motor_asyncio.AsyncIOMotorDatabase:
        if cls._db is None:
            cls._db = cls.get_client()[settings.mongodb_database]
        return cls._db

    @classmethod
    async def close(cls):
        if cls._client is not None:
            cls._client.close()
            cls._client = None
            cls._db = None
