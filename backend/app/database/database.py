"""
ResearchAtlas - Database Connection Module

MongoDB connection using Motor (async driver).
Provides database instance and connection lifecycle management.
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings

# Global client and database references
client: AsyncIOMotorClient = None
db: AsyncIOMotorDatabase = None


async def connect_to_mongodb():
    """
    Establish connection to MongoDB.
    Called during application startup.
    """
    global client, db
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    print(f"✅ Connected to MongoDB: {settings.DATABASE_NAME}")


async def close_mongodb_connection():
    """
    Close MongoDB connection.
    Called during application shutdown.
    """
    global client
    if client:
        client.close()
        print("✅ MongoDB connection closed")


def get_database() -> AsyncIOMotorDatabase:
    """
    Get the database instance.
    Used by services to access collections.
    """
    if db is None:
        raise RuntimeError("Database not initialized. Call connect_to_mongodb() first.")
    return db


def get_collection(collection_name: str):
    """
    Get a specific collection from the database.

    Args:
        collection_name: Name of the MongoDB collection

    Returns:
        Motor collection instance
    """
    return get_database()[collection_name]
