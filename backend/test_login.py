"""
Test script to verify admin login works
Run this after starting the backend
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_admin_login():
    """Test admin login with default credentials"""
    print("🧪 Testing Admin Login...")
    print("=" * 50)
    
    # Test credentials from .env
    email = "admin@raisoni.net"
    password = "Admin@123"
    
    print(f"📧 Email: {email}")
    print(f"🔑 Password: {password}")
    print()
    
    try:
        # Test login
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={"email": email, "password": password},
            timeout=10
        )
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login SUCCESSFUL!")
            print()
            print("📋 Response:")
            print(json.dumps(data, indent=2))
            print()
            print("🎉 Admin login is working correctly!")
            return True
        else:
            print(f"❌ Login FAILED!")
            print(f"📋 Error Response:")
            print(json.dumps(response.json(), indent=2))
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend!")
        print("💡 Make sure backend is running: uvicorn app.main:app --reload --port 8000")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_health():
    """Test if backend is running"""
    print("🏥 Testing Backend Health...")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running!")
            print(f"📋 Response: {response.json()}")
            print()
            return True
        else:
            print(f"❌ Backend returned status: {response.status_code}")
            return False
    except:
        print("❌ Backend is not running!")
        print("💡 Start backend with: uvicorn app.main:app --reload --port 8000")
        return False

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("🔬 ResearchAtlas Login Test")
    print("=" * 50 + "\n")
    
    # Test backend health first
    if not test_health():
        print("\n⚠️  Please start the backend first!")
        exit(1)
    
    print()
    
    # Test admin login
    if test_admin_login():
        print("\n✅ All tests passed! You can now login at http://localhost:3000")
    else:
        print("\n❌ Login test failed. Check the error messages above.")
    
    print("\n" + "=" * 50)
