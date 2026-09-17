"""
Fix login issues by resetting admin password
This script will:
1. Check if admin exists
2. Create admin if it doesn't exist
3. Reset password to 'Admin@123'
4. Verify the fix works
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.core.security import hash_password, verify_password
from datetime import datetime


async def fix_login():
    """Fix login by ensuring admin exists with correct password"""
    print("\n" + "="*60)
    print("FIXING LOGIN ISSUES")
    print("="*60)
    
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    
    # Check if admin exists
    admin = await db.users.find_one({"email": "admin@raisoni.net"})
    
    if admin:
        print("\n✅ Admin user found")
        print(f"   Email: {admin.get('email')}")
        print(f"   Role: {admin.get('role')}")
        print(f"   Active: {admin.get('is_active')}")
        
        # Reset password
        print("\n🔧 Resetting password to 'Admin@123'...")
        new_hash = hash_password("Admin@123")
        
        result = await db.users.update_one(
            {"_id": admin["_id"]},
            {"$set": {
                "password_hash": new_hash,
                "is_active": True,
                "updated_at": datetime.utcnow()
            }}
        )
        
        if result.modified_count > 0:
            print("✅ Password reset successfully")
        else:
            print("⚠️  Password update had no effect")
    else:
        print("\n❌ Admin user not found. Creating new admin...")
        
        new_admin = {
            "email": "admin@raisoni.net",
            "password_hash": hash_password("Admin@123"),
            "full_name": "System Administrator",
            "role": "admin",
            "department": "CSE",
            "orcid_id": "0000-0000-0000-0000",
            "scopus_id": "00000000000",
            "wos_id": "A-0000-0000",
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = await db.users.insert_one(new_admin)
        print(f"✅ Created new admin with ID: {result.inserted_id}")
    
    # Verify the fix
    print("\n🔐 Verifying login works...")
    admin = await db.users.find_one({"email": "admin@raisoni.net"})
    
    if admin:
        test_password = "Admin@123"
        stored_hash = admin.get('password_hash')
        
        is_valid = verify_password(test_password, stored_hash)
        
        if is_valid:
            print("✅ Login verification PASSED")
            print("\n" + "="*60)
            print("✅ FIX COMPLETE - LOGIN SHOULD WORK NOW")
            print("="*60)
            print("\n📝 Login Credentials:")
            print("   Email: admin@raisoni.net")
            print("   Password: Admin@123")
            print("\n🌐 Open: http://localhost:3000")
            print("="*60 + "\n")
        else:
            print("❌ Login verification FAILED")
            print("💡 There might be an issue with password hashing")
    else:
        print("❌ Admin user still not found after creation")
    
    client.close()


async def check_all_users():
    """Check all users in database"""
    print("\n" + "="*60)
    print("ALL USERS IN DATABASE")
    print("="*60)
    
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    
    users = await db.users.find({}).to_list(length=None)
    
    if not users:
        print("\n❌ No users found in database")
    else:
        print(f"\nTotal users: {len(users)}\n")
        
        for i, user in enumerate(users, 1):
            print(f"{i}. {user.get('email')}")
            print(f"   Role: {user.get('role')}")
            print(f"   Active: {user.get('is_active')}")
            print(f"   Has password: {'password_hash' in user}")
            print()
    
    client.close()


async def main():
    """Main function"""
    print("\n" + "🔧 "*20)
    print("ResearchAtlas Login Fix Tool")
    print("🔧 "*20)
    
    # Check all users first
    await check_all_users()
    
    # Fix the login
    await fix_login()


if __name__ == "__main__":
    asyncio.run(main())
