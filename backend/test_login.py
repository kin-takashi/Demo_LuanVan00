"""
test_login.py — Test login với tất cả test accounts
Chạy: python test_login.py
"""
import requests
import json
from typing import Dict, Tuple

BASE_URL = "http://localhost:8000"
API_PREFIX = "/api"

# Tất cả test accounts (từ seed.py + seed_extended.py)
TEST_ACCOUNTS = {
    # ADMIN
    "admin": {
        "email": "admin@example.com",
        "password": "Admin@123",
        "role": "ADMIN",
    },

    # CUSTOMERS (Original)
    "customer1": {
        "email": "customer1@example.com",
        "password": "Customer@123",
        "role": "CUSTOMER",
    },
    "customer2": {
        "email": "customer2@example.com",
        "password": "Customer@123",
        "role": "CUSTOMER",
    },

    # CUSTOMERS (Extended - mới)
    "customer3": {
        "email": "customer3@example.com",
        "password": "Customer@123",
        "role": "CUSTOMER",
    },
    "customer4": {
        "email": "customer4@example.com",
        "password": "Customer@123",
        "role": "CUSTOMER",
    },
    "customer5": {
        "email": "customer5@example.com",
        "password": "Customer@123",
        "role": "CUSTOMER",
    },
    "customer6": {
        "email": "customer6@example.com",
        "password": "Customer@123",
        "role": "CUSTOMER",
    },
    "customer7": {
        "email": "customer7@example.com",
        "password": "Customer@123",
        "role": "CUSTOMER",
    },

    # SHOP OWNERS (Original)
    "owner1": {
        "email": "owner1@shop.com",
        "password": "Owner@123",
        "role": "SHOP_OWNER",
    },
    "owner2": {
        "email": "owner2@shop.com",
        "password": "Owner@123",
        "role": "SHOP_OWNER",
    },

    # SHOP OWNERS (Extended - mới)
    "owner3": {
        "email": "owner3@shop.com",
        "password": "Owner@123",
        "role": "SHOP_OWNER",
    },
    "owner4": {
        "email": "owner4@shop.com",
        "password": "Owner@123",
        "role": "SHOP_OWNER",
    },

    # SHIPPERS (Original)
    "shipper1": {
        "email": "shipper1@example.com",
        "password": "Shipper@123",
        "role": "SHIPPER",
    },

    # SHIPPERS (Extended - mới)
    "shipper2": {
        "email": "shipper2@example.com",
        "password": "Shipper@123",
        "role": "SHIPPER",
    },
    "shipper3": {
        "email": "shipper3@example.com",
        "password": "Shipper@123",
        "role": "SHIPPER",
    },

    # MODERATOR (Extended - mới)
    "moderator": {
        "email": "moderator@example.com",
        "password": "Moderator@123",
        "role": "ADMIN",
    },
}

def test_login(name: str, email: str, password: str) -> Tuple[bool, str]:
    """Test single login"""
    try:
        url = f"{BASE_URL}{API_PREFIX}/auth/login"
        response = requests.post(
            url,
            json={"email": email, "password": password},
            timeout=5
        )

        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token", "")[:30] + "..."
            user_id = data.get("user", {}).get("user_id", "?")
            return True, f"Token: {token} (user_id: {user_id})"
        else:
            return False, f"Status: {response.status_code} - {response.text[:100]}"

    except requests.exceptions.ConnectionError:
        return False, "❌ Backend not running (localhost:8000)"
    except Exception as e:
        return False, str(e)

def main():
    print("\n" + "="*70)
    print("  🔐 LOGIN TEST - All Test Accounts")
    print("="*70)
    print(f"  Base URL: {BASE_URL}\n")

    # Group by role
    roles = {}
    for name, account in TEST_ACCOUNTS.items():
        role = account["role"]
        if role not in roles:
            roles[role] = []
        roles[role].append((name, account))

    total = len(TEST_ACCOUNTS)
    passed = 0
    failed = 0

    # Test each role
    for role in sorted(roles.keys()):
        print(f"\n📌 {role} ({len(roles[role])} accounts)")
        print("-" * 70)

        for name, account in roles[role]:
            email = account["email"]
            password = account["password"]

            success, message = test_login(name, email, password)

            if success:
                print(f"  ✅ {name:15} | {email:30} | {message}")
                passed += 1
            else:
                print(f"  ❌ {name:15} | {email:30}")
                print(f"     Error: {message}")
                failed += 1

    # Summary
    print("\n" + "="*70)
    print("  📊 SUMMARY")
    print("="*70)
    print(f"  Total: {total} accounts")
    print(f"  ✅ Passed: {passed}")
    print(f"  ❌ Failed: {failed}")
    print(f"  Success Rate: {(passed/total)*100:.1f}%")

    if failed == 0:
        print("\n  🎉 ALL ACCOUNTS WORKING!\n")
    else:
        print(f"\n  ⚠️  {failed} account(s) failed - check seed.py output\n")

    print("="*70)

if __name__ == "__main__":
    main()
