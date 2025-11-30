"""MongoDB connection and client management."""

from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import os


class MongoClient:
    """Async MongoDB client wrapper."""

    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db = None

    async def connect(self, uri: str = None, db_name: str = "chain_of_truth"):
        """Connect to MongoDB."""
        if uri is None:
            uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")

        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]

        # Create indexes
        await self._create_indexes()

    async def _create_indexes(self):
        """Create database indexes for performance."""
        # Index on session_id for fast lookups
        await self.db.sessions.create_index("session_id", unique=True)

        # Index on last_activity for cleanup queries
        await self.db.sessions.create_index("last_activity")

    async def disconnect(self):
        """Close MongoDB connection."""
        if self.client:
            self.client.close()

    def get_sessions_collection(self):
        """Get sessions collection."""
        return self.db.sessions


# Global instance
mongo_client = MongoClient()
