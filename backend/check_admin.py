"""
Script to check and fix admin user in database
Run this to verify admin exists and password is correct
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def check_admin():
    """Check if admin exists and fix if needed"""
    print("🔍 Checking admin user in database...")
    print("=" * 50)
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    users_collection = db["users"]
    
    # Check if admin exists
    admin_email = settings.DEFAULT_ADMIN_EMAIL.lower().strip()
    admin_password = settings.DEFAULT_ADMIN_PASSWORD
    
    print(f"📧 Looking for admin: {admin_email}")
    
    existing_admin = await users_collection.find_one({"email": admin_email})
    
    if existing_admin:
        print("✅ Admin user found!")
        print(f"   ID: {existing_admin['_id']}")
        print(f"   Name: {existing_admin.get('full_name')}")
        print(f"   Role: {existing_admin.get('role')}")
        print(f"   Active: {existing_admin.get('is_active')}")
        
        # Verify password
        stored_hash = existing_admin.get('password_hash')
        if stored_hash:
            is_valid = pwd_context.verify(admin_password, stored_hash)
            if is_valid:
                print("✅ Password is CORRECT!")
            else:
                print("❌ Password is WRONG! Fixing...")
                # Update password
                new_hash = pwd_context.hash(admin_password)
                await users_collection.update_one(
                    {"_id": existing_admin["_id"]},
                    {"$set": {"password_hash": new_hash}}
                )
                print("✅ Password updated!")
        else:
            print("❌ No password hash found! Fixing...")
            new_hash = pwd_context.hash(admin_password)
            await users_collection.update_one(
                {"_id": existing_admin["_id"]},
                {"$set": {"password_hash": new_hash}}
            )
            print("✅ Password hash added!")
    else:
        print("❌ Admin user NOT found! Creating...")
        
        # Create admin user
        from datetime import datetime, timezone
        
        admin_user = {
            "full_name": "System Administrator",
            "email": admin_email,
            "password_hash": pwd_context.hash(admin_password),
            "role": "admin",
            "department": "CSE",
            "orcid_id": "0000-0000-0000-0000",
            "scopus_id": "00000000000",
            "wos_id": "A-0000-0000",
            "is_active": True,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }
        
        result = await users_collection.insert_one(admin_user)
        print(f"✅ Admin created with ID: {result.inserted_id}")
    
    print()
    print("=" * 50)
    print("✅ Admin user check complete!")
    print()
    print("📋 Login Credentials:")
    print(f"   Email: {admin_email}")
    print(f"   Password: {admin_password}")
    print()
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_admin())
