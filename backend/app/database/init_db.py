"""
ResearchAtlas - Database Initialization Module

Handles initial setup:
- Creates indexes for performance
- Initializes the default admin account
- Sets up required collections
"""

from app.database.database import get_database, get_collection
from app.core.security import hash_password
from app.core.config import settings


async def create_indexes():
    """Create required indexes for all collections."""
    db = get_database()

    # Users collection indexes
    users_collection = db["users"]
    await users_collection.create_index("email", unique=True)
    await users_collection.create_index("role")
    await users_collection.create_index("department")
    await users_collection.create_index("is_active")

    print("✅ Database indexes created")


async def init_default_admin():
    """
    Create the default admin account if it doesn't exist.
    Credentials come from environment variables.
    """
    if not settings.DEFAULT_ADMIN_EMAIL or not settings.DEFAULT_ADMIN_PASSWORD:
        print("⚠️  Default admin credentials not configured. Skipping admin initialization.")
        return

    users_collection = get_collection("users")

    # Check if admin already exists
    existing_admin = await users_collection.find_one({
        "email": settings.DEFAULT_ADMIN_EMAIL.lower().strip()
    })

    if existing_admin:
        print(f"ℹ️  Default admin already exists: {settings.DEFAULT_ADMIN_EMAIL}")
        return

    # Create default admin
    from datetime import datetime, timezone

    admin_user = {
        "full_name": "System Administrator",
        "email": settings.DEFAULT_ADMIN_EMAIL.lower().strip(),
        "password_hash": hash_password(settings.DEFAULT_ADMIN_PASSWORD),
        "role": "admin",
        "department": "CSE",
        "is_active": True,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }

    await users_collection.insert_one(admin_user)
    print(f"✅ Default admin created: {settings.DEFAULT_ADMIN_EMAIL}")


async def initialize_database():
    """
    Full database initialization.
    Called during application startup after MongoDB connection.
    """
    await create_indexes()
    await init_default_admin()
    print("✅ Database initialization complete")
