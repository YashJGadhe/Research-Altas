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


async def seed_citation_demo_data():
    """
    Seed demo citation data for 17 CSE faculty members.
    Only runs if citation_records collection is empty.
    """
    from app.models.citation import CitationRecord
    
    collection = get_collection(CitationRecord.COLLECTION_NAME)
    
    # Check if data already exists
    existing_count = await collection.count_documents({})
    if existing_count > 0:
        print(f"ℹ️  Citation records already exist ({existing_count} records). Skipping demo data seed.")
        return
    
    print("📊 Seeding demo citation data for 17 CSE faculty members...")
    
    # Demo data for 17 faculty members
    demo_faculty = [
        {
            "faculty_id": "faculty_001",
            "faculty_name": "Dr. Mangala Madankar",
            "web_of_science": {"papers": 14, "citations": 39, "h_index": 4, "profile_url": ""},
            "scopus": {"papers": 46, "citations": 285, "h_index": 10, "profile_url": ""},
            "google_scholar": {"papers": 80, "citations": 541, "h_index": 13, "i10_index": 15, "profile_url": ""},
            "publons_url": "", "scopus_url": "", "google_scholar_url": "", "researchgate_url": "",
            "orcid": {"id": "", "url": ""},
            "openalex": {"id": "", "url": ""},
            "source_status": {"web_of_science": "not_configured", "scopus": "not_configured", "google_scholar": "not_configured", "orcid": "not_configured", "openalex": "not_configured"}
        },
        {
            "faculty_id": "faculty_002",
            "faculty_name": "Dr. Apeksha Sakhare",
            "web_of_science": {"papers": 11, "citations": 51, "h_index": 2, "profile_url": ""},
            "scopus": {"papers": 41, "citations": 236, "h_index": 10, "profile_url": ""},
            "google_scholar": {"papers": 74, "citations": 626, "h_index": 12, "i10_index": 19, "profile_url": ""},
            "publons_url": "", "scopus_url": "", "google_scholar_url": "", "researchgate_url": "",
            "orcid": {"id": "", "url": ""},
            "openalex": {"id": "", "url": ""},
            "source_status": {"web_of_science": "not_configured", "scopus": "not_configured", "google_scholar": "not_configured", "orcid": "not_configured", "openalex": "not_configured"}
        },
        {
            "faculty_id": "faculty_003",
            "faculty_name": "Dr. Girish Talmale",
            "web_of_science": {"papers": 17, "citations": 103, "h_index": 4, "profile_url": ""},
            "scopus": {"papers": 25, "citations": 220, "h_index": 7, "profile_url": ""},
            "google_scholar": {"papers": 48, "citations": 428, "h_index": 8, "i10_index": 6, "profile_url": ""},
            "publons_url": "", "scopus_url": "", "google_scholar_url": "", "researchgate_url": "",
            "orcid": {"id": "", "url": ""},
            "openalex": {"id": "", "url": ""},
            "source_status": {"web_of_science": "not_configured", "scopus": "not_configured", "google_scholar": "not_configured", "orcid": "not_configured", "openalex": "not_configured"}
        },
        {
            "faculty_id": "faculty_004",
            "faculty_name": "Prof. Prashant K. Khobragade",
            "web_of_science": {"papers": 3, "citations": 6, "h_index": 2, "profile_url": ""},
            "scopus": {"papers": 42, "citations": 656, "h_index": 13, "profile_url": ""},
            "google_scholar": {"papers": 61, "citations": 834, "h_index": 16, "i10_index": 24, "profile_url": ""},
            "publons_url": "", "scopus_url": "", "google_scholar_url": "", "researchgate_url": "",
            "orcid": {"id": "", "url": ""},
            "openalex": {"id": "", "url": ""},
            "source_status": {"web_of_science": "not_configured", "scopus": "not_configured", "google_scholar": "not_configured", "orcid": "not_configured", "openalex": "not_configured"}
        },
        {
            "faculty_id": "faculty_005",
            "faculty_name": "Dr. Atiya Khan",
            "web_of_science": {"papers": 3, "citations": 300, "h_index": 2, "profile_url": ""},
            "scopus": {"papers": 24, "citations": 650, "h_index": 9, "profile_url": ""},
            "google_scholar": {"papers": 29, "citations": 656, "h_index": 9, "i10_index": 8, "profile_url": ""},
            "publons_url": "", "scopus_url": "", "google_scholar_url": "", "researchgate_url": "",
            "orcid": {"id": "", "url": ""},
            "openalex": {"id": "", "url": ""},
            "source_status": {"web_of_science": "not_configured", "scopus": "not_configured", "google_scholar": "not_configured", "orcid": "not_configured", "openalex": "not_configured"}
        },
        {
            "faculty_id": "faculty_006",
            "faculty_name": "Prof. Neha Purohit",
            "web_of_science": {"papers": 3, "citations": 4, "h_index": 1, "profile_url": ""},
            "scopus": {"papers": 23, "citations": 194, "h_index": 8, "profile_url": ""},
            "google_scholar": {"papers": 30, "citations": 270, "h_index": 7, "i10_index": 7, "profile_url": ""},
            "publons_url": "", "scopus_url": "", "google_scholar_url": "", "researchgate_url": "",
            "orcid": {"id": "", "url": ""},
            "openalex": {"id": "", "url": ""},
            "source_status": {"web_of_science": "not_configured", "scopus": "not_configured", "google_scholar": "not_configured", "orcid": "not_configured", "openalex": "not_configured"}
        },
        {
            "faculty_id": "faculty_007",
            "faculty_name": "Dr. Prasad Lokulwar",
            "web_of_science": {"papers": 1, "citations": 5, "h_index": 1, "profile_url": ""},
            "scopus": {"papers": 41, "citations": 240, "h_index": 10, "profile_url": ""},
            "google_scholar": {"papers": 50, "citations": 374, "h_index": 12, "i10_index": 14, "profile_url": ""},
            "publons_url": "", "scopus_url": "", "google_scholar_url": "", "researchgate_url": "",
            "orcid": {"id": "", "url": ""},
            "openalex": {"id": "", "url": ""},
            "source_status": {"web_of_science": "not_configured", "scopus": "not_configured", "google_scholar": "not_configured", "orcid": "not_configured", "openalex": "not_configured"}
        },
        {
            "faculty_id": "faculty_008",
            "faculty_name": "Dr. Shruti Thakur",
            "web_of_science": {"papers": 2, "citations": 5, "h_index": 2, "profile_url": ""},
            "scopus": {"papers": 22, "citations": 95, "h_index": 6, "profile_url": ""},
            "google_scholar": {"papers": 47, "citations": 135, "h_index": 7, "i10_index": 5, "profile_url": ""},
            "publons_url": "", "scopus_url": "", "google_scholar_url": "", "researchgate_url": "",
            "orcid": {"id": "", "url": ""},
            "openalex": {"id": "", "url": ""},
            "source_status": {"web_of_science": "not_configured", "scopus": "not_configured", "google_scholar": "not_configured", "orcid": "not_configured", "openalex": "not_configured"}
        },
        {
            "faculty_id": "faculty_009",
            "faculty_name": "Dr. Sarika Khandelwal",
            "web_of_science": {"papers": 15, "citations": 41, "h_index": 3, "profile_url": ""},
            "scopus": {"papers": 58, "citations": 247, "h_index": 9, "profile_url": ""},
            "google_scholar": {"papers": 85, "citations": 375, "h_index": 11, "i10_index": 15, "profile_url": ""},
            "publons_url": "", "scopus_url": "", "google_scholar_url": "", "researchgate_url": "",
            "orcid": {"id": "", "url": ""},
            "openalex": {"id": "", "url": ""},
            "source_status": {"web_of_science": "not_configured", "scopus": "not_configured", "google_scholar": "not_configured", "orcid": "not_configured", "openalex": "not_configured"}
        },
        {
            "faculty_id": "faculty_010",
            "faculty_name": "Prof. Ashish Soni",
            "web_of_science": {"papers": 0, "citations": 0, "h_index": 0, "profile_url": ""},
            "scopus": {"papers": 7, "citations": 12, "h_index": 2, "profile_url": ""},
            "google_scholar": {"papers": 14, "citations": 20, "h_index": 3, "i10_index": 0, "profile_url": ""},
            "publons_url": "", "scopus_url": "", "google_scholar_url": "", "researchgate_url": "",
            "orcid": {"id": "", "url": ""},
            "openalex": {"id": "", "url": ""},
            "source_status": {"web_of_science": "not_configured", "scopus": "not_configured", "google_scholar": "not_configured", "orcid": "not_configured", "openalex": "not_configured"}
        },
        {
            "faculty_id": "faculty_011",
            "faculty_name": "Prof. Anuradha Joshi",
            "web_of_science": {"papers": 0, "citations": 0, "h_index": 0, "profile_url": ""},
            "scopus": {"papers": 6, "citations": 17, "h_index": 2, "profile_url": ""},
            "google_scholar": {"papers": 4, "citations": 22, "h_index": 2, "i10_index": 1, "profile_url": ""},
            "publons_url": "", "scopus_url": "", "google_scholar_url": "", "researchgate_url": "",
            "orcid": {"id": "", "url": ""},
            "openalex": {"id": "", "url": ""},
            "source_status": {"web_of_science": "not_configured", "scopus": "not_configured", "google_scholar": "not_configured", "orcid": "not_configured", "openalex": "not_configured"}
        },
        {
            "faculty_id": "faculty_012",
            "faculty_name": "Prof. Imran Ahmad",
            "web_of_science": {"papers": 0, "citations": 0, "h_index": 0, "profile_url": ""},
            "scopus": {"papers": 6, "citations": 0, "h_index": 0, "profile_url": ""},
            "google_scholar": {"papers": 4, "citations": 0, "h_index": 0, "i10_index": 0, "profile_url": ""},
            "publons_url": "", "scopus_url": "", "google_scholar_url": "", "researchgate_url": "",
            "orcid": {"id": "", "url": ""},
            "openalex": {"id": "", "url": ""},
            "source_status": {"web_of_science": "not_configured", "scopus": "not_configured", "google_scholar": "not_configured", "orcid": "not_configured", "openalex": "not_configured"}
        },
        {
            "faculty_id": "faculty_013",
            "faculty_name": "Prof. Mrunali Dhone",
            "web_of_science": {"papers": 0, "citations": 0, "h_index": 0, "profile_url": ""},
            "scopus": {"papers": 13, "citations": 253, "h_index": 4, "profile_url": ""},
            "google_scholar": {"papers": 16, "citations": 286, "h_index": 6, "i10_index": 4, "profile_url": ""},
            "publons_url": "", "scopus_url": "", "google_scholar_url": "", "researchgate_url": "",
            "orcid": {"id": "", "url": ""},
            "openalex": {"id": "", "url": ""},
            "source_status": {"web_of_science": "not_configured", "scopus": "not_configured", "google_scholar": "not_configured", "orcid": "not_configured", "openalex": "not_configured"}
        },
        {
            "faculty_id": "faculty_014",
            "faculty_name": "Dr. Aditya Turankar",
            "web_of_science": {"papers": 0, "citations": 0, "h_index": 0, "profile_url": ""},
            "scopus": {"papers": 8, "citations": 12, "h_index": 2, "profile_url": ""},
            "google_scholar": {"papers": 20, "citations": 632, "h_index": 7, "i10_index": 7, "profile_url": ""},
            "publons_url": "", "scopus_url": "", "google_scholar_url": "", "researchgate_url": "",
            "orcid": {"id": "", "url": ""},
            "openalex": {"id": "", "url": ""},
            "source_status": {"web_of_science": "not_configured", "scopus": "not_configured", "google_scholar": "not_configured", "orcid": "not_configured", "openalex": "not_configured"}
        },
        {
            "faculty_id": "faculty_015",
            "faculty_name": "Prof. Sonali Bhardwaj",
            "web_of_science": {"papers": 0, "citations": 0, "h_index": 0, "profile_url": ""},
            "scopus": {"papers": 0, "citations": 0, "h_index": 0, "profile_url": ""},
            "google_scholar": {"papers": 0, "citations": 0, "h_index": 0, "i10_index": 0, "profile_url": ""},
            "publons_url": "", "scopus_url": "", "google_scholar_url": "", "researchgate_url": "",
            "orcid": {"id": "", "url": ""},
            "openalex": {"id": "", "url": ""},
            "source_status": {"web_of_science": "not_configured", "scopus": "not_configured", "google_scholar": "not_configured", "orcid": "not_configured", "openalex": "not_configured"}
        },
        {
            "faculty_id": "faculty_016",
            "faculty_name": "Prof. Wani Bisen",
            "web_of_science": {"papers": 2, "citations": 11, "h_index": 1, "profile_url": ""},
            "scopus": {"papers": 5, "citations": 39, "h_index": 3, "profile_url": ""},
            "google_scholar": {"papers": 10, "citations": 66, "h_index": 5, "i10_index": 2, "profile_url": ""},
            "publons_url": "", "scopus_url": "", "google_scholar_url": "", "researchgate_url": "",
            "orcid": {"id": "", "url": ""},
            "openalex": {"id": "", "url": ""},
            "source_status": {"web_of_science": "not_configured", "scopus": "not_configured", "google_scholar": "not_configured", "orcid": "not_configured", "openalex": "not_configured"}
        },
        {
            "faculty_id": "faculty_017",
            "faculty_name": "Dr. Sonia Bajaj",
            "web_of_science": {"papers": 0, "citations": 0, "h_index": 0, "profile_url": ""},
            "scopus": {"papers": 0, "citations": 0, "h_index": 0, "profile_url": ""},
            "google_scholar": {"papers": 10, "citations": 15, "h_index": 2, "i10_index": 0, "profile_url": ""},
            "publons_url": "", "scopus_url": "", "google_scholar_url": "", "researchgate_url": "",
            "orcid": {"id": "", "url": ""},
            "openalex": {"id": "", "url": ""},
            "source_status": {"web_of_science": "not_configured", "scopus": "not_configured", "google_scholar": "not_configured", "orcid": "not_configured", "openalex": "not_configured"}
        }
    ]
    
    # Insert demo data
    for faculty_data in demo_faculty:
        record = CitationRecord.create_record(**faculty_data)
        await collection.insert_one(record)
    
    print(f"✅ Successfully seeded {len(demo_faculty)} faculty citation records")


async def initialize_database():
    """
    Full database initialization.
    Called during application startup after MongoDB connection.
    """
    try:
        await create_indexes()
        await migrate_existing_users()
        await init_default_admin()
        await seed_citation_demo_data()
        print("✅ Database initialization complete")
    except Exception as e:
        print(f"❌ Database initialization failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
