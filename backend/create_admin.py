#!/usr/bin/env python3
"""
Quick script to create admin user and test login
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

async def create_admin():
    """Create admin user manually"""
    from motor.motor_asyncio import AsyncIOMotorClient
    from app.core.config import settings
    from app.core.security import hash_password
    from datetime import datetime
    
    print("\n🔧 Creating admin user...")
    
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    db = client[settings.DATABASE_NAME]
    
    # Check if admin exists
    existing = await db.users.find_one({"email": "admin@raisoni.net"})
    
    if existing:
        print("✅ Admin already exists")
        print(f"   Email: {existing.get('email')}")
        print(f"   Role: {existing.get('role')}")
        print(f"   Active: {existing.get('is_active')}")
        
        # Update password to ensure it's correct
        new_hash = hash_password("Admin@123")
        await db.users.update_one(
            {"_id": existing["_id"]},
            {"$set": {"password_hash": new_hash, "updated_at": datetime.utcnow()}}
        )
        print("✅ Password updated to 'Admin@123'")
    else:
        print("❌ Admin not found, creating...")
        
        admin_doc = {
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
        
        result = await db.users.insert_one(admin_doc)
        print(f"✅ Admin created with ID: {result.inserted_id}")
    
    client.close()

async def test_login():
    """Test login with requests"""
    import requests
    
    print("\n🧪 Testing login...")
    
    try:
        response = requests.post(
            "http://localhost:8000/api/auth/login",
            json={
                "email": "admin@raisoni.net",
                "password": "Admin@123"
            },
            timeout=5
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login SUCCESSFUL!")
            print(f"   Token: {data.get('access_token', 'N/A')[:50]}...")
            print(f"   User: {data.get('user', {}).get('email')}")
            print(f"   Role: {data.get('user', {}).get('role')}")
            return True
        else:
            print(f"❌ Login FAILED")
            print(f"   Error: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("Admin User Creation & Login Test")
    print("="*60)
    
    await create_admin()
    success = await test_login()
    
    print("\n" + "="*60)
    if success:
        print("✅ ALL TESTS PASSED")
        print("\n📝 Login Credentials:")
        print("   Email: admin@raisoni.net")
        print("   Password: Admin@123")
        print("\n🌐 Open: http://localhost:3000")
    else:
        print("❌ LOGIN TEST FAILED")
        print("\n💡 Check backend logs for errors")
    print("="*60 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
