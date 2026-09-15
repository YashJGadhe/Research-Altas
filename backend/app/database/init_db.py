"""
ResearchAtlas - Database Initialization Module

Handles initial setup:
- Creates indexes for performance
- Initializes the default admin account
- Sets up required collections
- Migrates existing users to include new fields
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
    
    # Research ID indexes (sparse = only applies when field exists)
    await users_collection.create_index("orcid_id", unique=True, sparse=True)
    await users_collection.create_index("scopus_id", unique=True, sparse=True)
    await users_collection.create_index("wos_id", unique=True, sparse=True)

    print("✅ Database indexes created")


async def migrate_existing_users():
    """
    Migrate existing users to include new research ID fields.
    This ensures Phase 1 users have the required fields for Phase 2.
    """
    users_collection = get_collection("users")
    
    # Find all users without the new fields
    users_without_ids = await users_collection.find({
        "$or": [
            {"orcid_id": {"$exists": False}},
            {"scopus_id": {"$exists": False}},
            {"wos_id": {"$exists": False}},
        ]
    }).to_list(length=None)
    
    if users_without_ids:
        from datetime import datetime, timezone
        
        for user in users_without_ids:
            update_data = {"updated_at": datetime.now(timezone.utc)}
            
            # Add missing fields with empty values
            if "orcid_id" not in user:
                update_data["orcid_id"] = ""
            if "scopus_id" not in user:
                update_data["scopus_id"] = ""
            if "wos_id" not in user:
                update_data["wos_id"] = ""
            
            await users_collection.update_one(
                {"_id": user["_id"]},
                {"$set": update_data}
            )
        
        print(f"✅ Migrated {len(users_without_ids)} existing users with research ID fields")
    else:
        print("✅ No users need migration")


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
        
        # Ensure existing admin has the new fields
        needs_update = False
        update_data = {}
        
        if "orcid_id" not in existing_admin or not existing_admin.get("orcid_id"):
            update_data["orcid_id"] = "0000-0000-0000-0000"
            needs_update = True
        if "scopus_id" not in existing_admin or not existing_admin.get("scopus_id"):
            update_data["scopus_id"] = "00000000000"
            needs_update = True
        if "wos_id" not in existing_admin or not existing_admin.get("wos_id"):
            update_data["wos_id"] = "A-0000-0000"
            needs_update = True
        
        if needs_update:
            from datetime import datetime, timezone
            update_data["updated_at"] = datetime.now(timezone.utc)
            await users_collection.update_one(
                {"_id": existing_admin["_id"]},
                {"$set": update_data}
            )
            print(f"✅ Updated default admin with research ID fields")
        else:
            print(f"✅ Default admin already has all required fields")
        
        return

    # Create default admin
    from datetime import datetime, timezone

    admin_user = {
        "full_name": "System Administrator",
        "email": settings.DEFAULT_ADMIN_EMAIL.lower().strip(),
        "password_hash": hash_password(settings.DEFAULT_ADMIN_PASSWORD),
        "role": "admin",
        "department": "CSE",
        "orcid_id": "0000-0000-0000-0000",
        "scopus_id": "00000000000",
        "wos_id": "A-0000-0000",
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
    try:
        await create_indexes()
        await migrate_existing_users()
        await init_default_admin()
        print("✅ Database initialization complete")
    except Exception as e:
        print(f"❌ Database initialization failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
