from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

# MongoDB client instance
client = None
database = None


async def init_db():
    """Initialize MongoDB connection"""
    global client, database
    try:
        client = AsyncIOMotorClient(settings.mongodb_uri)
        database = client[settings.database_name]
        
        # Test connection
        await client.admin.command('ping')
        print(f"✓ Connected to MongoDB: {settings.database_name}")
        
        # Create indexes for better query performance
        await database.users.create_index("username", unique=True)
        await database.users.create_index("email", unique=True)
        await database.booths.create_index("booth_id", unique=True)
        await database.booths.create_index("constituency")
        await database.booths.create_index("status")
        await database.alerts.create_index("booth_id")
        await database.alerts.create_index("is_read")
        await database.alerts.create_index("timestamp")
        await database.audit_logs.create_index("username")
        await database.audit_logs.create_index("timestamp")
        
        print("✓ Database indexes created")
    except Exception as e:
        print(f"✗ Failed to connect to MongoDB: {e}")
        raise


async def close_db():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        print("✓ MongoDB connection closed")


def get_database():
    """Get database instance (for dependency injection)"""
    if database is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return database


def get_collection(collection_name: str):
    """Get a specific collection"""
    db = get_database()
    return db[collection_name]
