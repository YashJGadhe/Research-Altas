#!/usr/bin/env python3
"""
Debug script to diagnose login issues
"""
import sys
import requests
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

def check_backend_running():
    """Check if backend is running"""
    print("\n" + "="*60)
    print("STEP 1: Checking if backend is running...")
    print("="*60)
    try:
        response = requests.get("http://localhost:8000/health", timeout=3)
        if response.status_code == 200:
            print("✅ Backend is running")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Backend returned status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is NOT running")
        print("\n💡 Please start the backend with:")
        print("   cd backend")
        print("   uvicorn app.main:app --reload --port 8000")
        return False
    except Exception as e:
        print(f"❌ Error checking backend: {e}")
        return False

def check_admin_exists():
    """Check if admin user exists in database"""
    print("\n" + "="*60)
    print("STEP 2: Checking if admin user exists...")
    print("="*60)
    
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        from app.core.config import settings
        import asyncio
        
        async def check_db():
            client = AsyncIOMotorClient(settings.MONGODB_URL)
            db = client[settings.DATABASE_NAME]
            
            # Check if admin exists
            admin = await db.users.find_one({"email": "admin@raisoni.net"})
            
            if admin:
                print("✅ Admin user exists in database")
                print(f"   Email: {admin.get('email')}")
                print(f"   Role: {admin.get('role')}")
                print(f"   Active: {admin.get('is_active')}")
                print(f"   Has password_hash: {'password_hash' in admin}")
                return True
            else:
                print("❌ Admin user NOT found in database")
                print("\n💡 Creating admin user...")
                
                from app.core.security import hash_password
                from datetime import datetime
                
                admin_doc = {
                    "email": "admin@raisoni.net",
                    "password_hash": hash_password("Admin@123"),
                    "full_name": "Admin User",
                    "role": "admin",
                    "is_active": True,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
                
                result = await db.users.insert_one(admin_doc)
                print(f"✅ Admin user created with ID: {result.inserted_id}")
                return True
        
        return asyncio.run(check_db())
        
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        print("\n💡 Make sure MongoDB is running:")
        print("   Check with: mongosh")
        return False

def test_login_endpoint():
    """Test the login endpoint directly"""
    print("\n" + "="*60)
    print("STEP 3: Testing login endpoint...")
    print("="*60)
    
    try:
        response = requests.post(
            "http://localhost:8000/api/auth/login",
            json={
                "email": "admin@raisoni.net",
                "password": "Admin@123"
            },
            timeout=5
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ Login SUCCESSFUL!")
            print(f"   Access Token: {data.get('access_token', 'N/A')[:50]}...")
            print(f"   User: {data.get('user', {}).get('email', 'N/A')}")
            print(f"   Role: {data.get('user', {}).get('role', 'N/A')}")
            return True
        else:
            print(f"\n❌ Login FAILED")
            print(f"   Error: {response.json().get('detail', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing login: {e}")
        return False

def check_api_docs():
    """Check if API docs are accessible"""
    print("\n" + "="*60)
    print("STEP 4: Checking API documentation...")
    print("="*60)
    
    try:
        response = requests.get("http://localhost:8000/docs", timeout=3)
        if response.status_code == 200:
            print("✅ API docs accessible at: http://localhost:8000/docs")
            return True
        else:
            print(f"❌ API docs returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error checking API docs: {e}")
        return False

def main():
    """Run all diagnostic checks"""
    print("\n" + "🔍 "*20)
    print("ResearchAtlas Login Diagnostic Tool")
    print("🔍 "*20)
    
    results = {
        "Backend Running": check_backend_running(),
        "Admin Exists": False,
        "Login Works": False,
        "API Docs": False
    }
    
    if results["Backend Running"]:
        results["Admin Exists"] = check_admin_exists()
        results["Login Works"] = test_login_endpoint()
        results["API Docs"] = check_api_docs()
    
    # Summary
    print("\n" + "="*60)
    print("DIAGNOSTIC SUMMARY")
    print("="*60)
    
    for check, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {check}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 All checks passed! Login should work now.")
        print("\n📝 Login Credentials:")
        print("   Email: admin@raisoni.net")
        print("   Password: Admin@123")
        print("\n🌐 Open: http://localhost:3000")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        
        if not results["Backend Running"]:
            print("\n💡 Fix: Start the backend server")
        if not results["Admin Exists"]:
            print("\n💡 Fix: Check MongoDB connection and create admin user")
        if not results["Login Works"]:
            print("\n💡 Fix: Check backend logs for authentication errors")
    
    print("\n" + "="*60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
