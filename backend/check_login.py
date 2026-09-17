"""
Diagnostic script to debug login issues
Run this to check if the admin user exists and test login
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.core.security import verify_password


async def check_database():
    """Check what users exist in the database"""
    print("\n" + "="*60)
    print("DATABASE CHECK")
    print("="*60)
    
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    
    # Get all users
    users = await db.users.find({}).to_list(length=None)
    
    print(f"\nTotal users in database: {len(users)}")
    
    for user in users:
        print(f"\n👤 User:")
        print(f"   Email: {user.get('email')}")
        print(f"   Role: {user.get('role')}")
        print(f"   Active: {user.get('is_active')}")
        print(f"   Has password_hash: {'password_hash' in user}")
        if 'password_hash' in user:
            print(f"   Password hash length: {len(user['password_hash'])}")
            print(f"   Password hash starts with: {user['password_hash'][:20]}...")
    
    client.close()
    return users


async def test_password_verification():
    """Test if password verification works"""
    print("\n" + "="*60)
    print("PASSWORD VERIFICATION TEST")
    print("="*60)
    
    from app.core.security import hash_password
    
    # Test password
    test_password = "Admin@123"
    hashed = hash_password(test_password)
    
    print(f"\nTest password: {test_password}")
    print(f"Hashed: {hashed[:30]}...")
    
    # Verify it works
    is_valid = verify_password(test_password, hashed)
    print(f"Verification result: {is_valid}")
    
    if is_valid:
        print("✅ Password hashing and verification works correctly")
    else:
        print("❌ Password verification FAILED")
    
    return is_valid


async def test_login_with_stored_user():
    """Test login with actual stored user"""
    print("\n" + "="*60)
    print("LOGIN TEST WITH STORED USER")
    print("="*60)
    
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    
    # Find admin user
    admin = await db.users.find_one({"email": "admin@raisoni.net"})
    
    if not admin:
        print("\n❌ Admin user not found in database")
        print("💡 You need to register first or create admin manually")
        client.close()
        return False
    
    print(f"\n✅ Found admin user:")
    print(f"   Email: {admin.get('email')}")
    print(f"   Role: {admin.get('role')}")
    print(f"   Active: {admin.get('is_active')}")
    
    # Test password verification
    test_password = "Admin@123"
    stored_hash = admin.get('password_hash')
    
    if not stored_hash:
        print("\n❌ No password hash found for admin user")
        client.close()
        return False
    
    print(f"\n🔐 Testing password verification...")
    print(f"   Stored hash: {stored_hash[:30]}...")
    
    is_valid = verify_password(test_password, stored_hash)
    
    if is_valid:
        print(f"✅ Password '{test_password}' is CORRECT")
    else:
        print(f"❌ Password '{test_password}' is INCORRECT")
        print("\n💡 The password in the database doesn't match 'Admin@123'")
        print("💡 This could mean:")
        print("   1. You registered with a different password")
        print("   2. Password hashing failed during registration")
        print("   3. The password was corrupted")
    
    client.close()
    return is_valid


async def fix_admin_password():
    """Fix the admin password to 'Admin@123'"""
    print("\n" + "="*60)
    print("FIXING ADMIN PASSWORD")
    print("="*60)
    
    from app.core.security import hash_password
    from datetime import datetime
    
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    
    # Find admin user
    admin = await db.users.find_one({"email": "admin@raisoni.net"})
    
    if not admin:
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
    else:
        print("\n🔧 Updating admin password to 'Admin@123'...")
        
        new_hash = hash_password("Admin@123")
        result = await db.users.update_one(
            {"_id": admin["_id"]},
            {"$set": {
                "password_hash": new_hash,
                "updated_at": datetime.utcnow()
            }}
        )
        
        if result.modified_count > 0:
            print("✅ Password updated successfully")
        else:
            print("⚠️  No changes made (password might already be correct)")
    
    client.close()


async def main():
    """Run all diagnostic checks"""
    print("\n" + "🔍 "*20)
    print("ResearchAtlas Login Diagnostic Tool")
    print("🔍 "*20)
    
    # Check database
    users = await check_database()
    
    # Test password verification
    await test_password_verification()
    
    # Test login with stored user
    login_works = await test_login_with_stored_user()
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    if len(users) == 0:
        print("\n❌ No users in database")
        print("💡 Register a new user or run: python fix_login.py")
    elif not login_works:
        print("\n❌ Login will fail with current password")
        print("💡 Run: python fix_login.py to reset admin password")
    else:
        print("\n✅ Everything looks good!")
        print("\n📝 Login Credentials:")
        print("   Email: admin@raisoni.net")
        print("   Password: Admin@123")
    
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
