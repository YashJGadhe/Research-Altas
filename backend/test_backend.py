#!/usr/bin/env python3
"""
ResearchAtlas - Backend Test Script
Tests the authentication system to verify everything is working.
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {str(e)}")
        return False

def test_login():
    """Test login endpoint"""
    print("\n🔍 Testing login endpoint...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json={
                "email": "admin@raisoni.net",
                "password": "Admin@123"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Login successful")
            print(f"   - Access token: {data.get('access_token', '')[:50]}...")
            print(f"   - User: {data.get('user', {}).get('full_name', 'Unknown')}")
            print(f"   - Role: {data.get('user', {}).get('role', 'Unknown')}")
            return data.get('access_token')
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login failed: {str(e)}")
        return None

def test_me(token):
    """Test /me endpoint"""
    if not token:
        print("\n⚠️  Skipping /me test (no token)")
        return False
        
    print("\n🔍 Testing /me endpoint...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ /me endpoint successful")
            print(f"   - ID: {data.get('id', 'Unknown')}")
            print(f"   - Email: {data.get('email', 'Unknown')}")
            print(f"   - ORCID: {data.get('orcid_id', 'Unknown')}")
            print(f"   - Scopus: {data.get('scopus_id', 'Unknown')}")
            print(f"   - WoS: {data.get('wos_id', 'Unknown')}")
            return True
        else:
            print(f"❌ /me failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ /me failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 ResearchAtlas Backend Test Suite")
    print("=" * 60)
    
    # Test 1: Health check
    if not test_health():
        print("\n❌ Backend is not running or not accessible")
        print("💡 Make sure backend is running on http://localhost:8000")
        sys.exit(1)
    
    # Test 2: Login
    token = test_login()
    if not token:
        print("\n❌ Login failed")
        print("💡 Check backend logs for error details")
        sys.exit(1)
    
    # Test 3: /me endpoint
    if not test_me(token):
        print("\n❌ /me endpoint failed")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)
    print("\n🎉 Backend is working correctly!")
    print("\n📝 You can now:")
    print("   1. Login at http://localhost:3000/login")
    print("   2. Use credentials: admin@raisoni.net / Admin@123")
    print("   3. Access admin dashboard")
    print("")

if __name__ == "__main__":
    main()
