"""
Test login API directly to see exact error
"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 70)
print("TEST LOGIN API")
print("=" * 70)

# Test account
test_email = "customer1@example.com"
test_password = "Customer@123"

print(f"\n📧 Email:    {test_email}")
print(f"🔑 Password: {test_password}")

# Test 1: Check if backend is running
print("\n" + "=" * 70)
print("STEP 1: Check if backend is running")
print("=" * 70)

try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    print(f"✅ Backend is responding!")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"❌ Backend not responding!")
    print(f"   Error: {e}")
    exit(1)

# Test 2: Try login
print("\n" + "=" * 70)
print("STEP 2: Test login")
print("=" * 70)

login_url = f"{BASE_URL}/api/v1/auth/login"
login_data = {
    "email": test_email,
    "password": test_password
}

print(f"\n📤 Sending POST to: {login_url}")
print(f"📝 Data: {json.dumps(login_data, indent=2)}")

try:
    response = requests.post(login_url, json=login_data, timeout=10)
    print(f"\n📥 Response Status: {response.status_code}")
    print(f"📥 Response Body:")
    print(json.dumps(response.json(), indent=2))

    if response.status_code == 200:
        print(f"\n✅ LOGIN SUCCESS!")
        print(f"🎉 Access Token received!")
    else:
        print(f"\n❌ LOGIN FAILED!")
        print(f"   Status Code: {response.status_code}")
        print(f"   Error: {response.json().get('detail', 'Unknown error')}")

except Exception as e:
    print(f"❌ Request failed!")
    print(f"   Error: {e}")

# Test 3: Check if account exists
print("\n" + "=" * 70)
print("STEP 3: Check database (advanced)")
print("=" * 70)

try:
    import sys
    sys.path.insert(0, "E:\\SUB_LUAN_VAN\\luan_van\\backend")
    from app.database import SessionLocal
    from app.models.user import User

    db = SessionLocal()
    user = db.query(User).filter(User.email == test_email).first()
    db.close()

    if user:
        print(f"\n✅ User found in database!")
        print(f"   User ID: {user.user_id}")
        print(f"   Email: {user.email}")
        print(f"   Full Name: {user.full_name}")
        print(f"   Status: {user.status}")
        print(f"   Password Hash: {user.password_hash[:50]}...")
    else:
        print(f"\n❌ User NOT found in database!")
        print(f"   Email: {test_email}")

except Exception as e:
    print(f"⚠️  Could not check database: {e}")

print("\n" + "=" * 70)
