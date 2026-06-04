"""
test_api.py — Simple API tests
Chạy: python test_api.py
"""
import requests
import json
from typing import Dict, Any

# ============================================================
# CONFIG
# ============================================================
BASE_URL = "http://localhost:8000"
API_PREFIX = "/api"

# Test credentials (sau khi chạy seed.py)
TEST_ACCOUNTS = {
    "admin": {"email": "admin@example.com", "password": "Admin@123"},
    "customer": {"email": "customer1@example.com", "password": "Customer@123"},
    "owner": {"email": "owner1@shop.com", "password": "Owner@123"},
    "shipper": {"email": "shipper1@example.com", "password": "Shipper@123"},
}

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def print_section(title: str):
    """Print section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_test(name: str, status: str, data: Any = None):
    """Print test result"""
    symbol = "✅" if status == "PASS" else "❌"
    print(f"{symbol} {name}: {status}")
    if data and status == "FAIL":
        print(f"   Response: {data}")

def test_endpoint(
    method: str,
    endpoint: str,
    name: str,
    headers: Dict = None,
    data: Dict = None,
    expected_status: int = 200,
) -> Dict:
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"

    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=5)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=5)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=5)
        else:
            print_test(name, "FAIL", "Unknown method")
            return {}

        status = "PASS" if response.status_code == expected_status else "FAIL"
        print_test(name, status)

        if response.status_code != expected_status:
            print(f"   Expected: {expected_status}, Got: {response.status_code}")
            print(f"   Response: {response.text[:200]}")

        try:
            return response.json()
        except:
            return response.text

    except requests.exceptions.ConnectionError:
        print_test(name, "FAIL", "Connection refused - Backend not running?")
        return {}
    except Exception as e:
        print_test(name, "FAIL", str(e))
        return {}

# ============================================================
# TEST SUITES
# ============================================================

def test_health():
    """Test if backend is running"""
    print_section("1️⃣ HEALTH CHECK")

    result = test_endpoint(
        "GET",
        "/",
        "Backend Health",
        expected_status=404  # 404 is OK for root endpoint
    )

def test_api_docs():
    """Test API documentation"""
    print_section("2️⃣ API DOCUMENTATION")

    test_endpoint(
        "GET",
        "/docs",
        "Swagger UI (Docs)",
        expected_status=200
    )

    test_endpoint(
        "GET",
        "/openapi.json",
        "OpenAPI Schema",
        expected_status=200
    )

def test_auth():
    """Test authentication endpoints"""
    print_section("3️⃣ AUTHENTICATION")

    customer = TEST_ACCOUNTS["customer"]

    # Test login
    login_response = test_endpoint(
        "POST",
        f"{API_PREFIX}/auth/login",
        "Login (customer)",
        data=customer,
        expected_status=200
    )

    if login_response and "access_token" in login_response:
        print(f"   🔐 Token: {login_response['access_token'][:20]}...")
        return login_response.get("access_token")

    return None

def test_users(token: str = None):
    """Test user endpoints"""
    print_section("4️⃣ USER ENDPOINTS")

    if not token:
        print("   ⚠️  Skipped (no auth token)")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # Get profile
    test_endpoint(
        "GET",
        f"{API_PREFIX}/users/profile",
        "Get User Profile",
        headers=headers,
        expected_status=200
    )

def test_products(token: str = None):
    """Test product endpoints"""
    print_section("5️⃣ PRODUCT ENDPOINTS")

    # Get products (no auth needed)
    products = test_endpoint(
        "GET",
        f"{API_PREFIX}/products",
        "Get Products List",
        expected_status=200
    )

    if isinstance(products, dict) and "data" in products:
        print(f"   📦 Found {len(products['data'])} products")
        return products.get("data", [])

    return []

def test_shops(token: str = None):
    """Test shop endpoints"""
    print_section("6️⃣ SHOP ENDPOINTS")

    # Get shops
    shops = test_endpoint(
        "GET",
        f"{API_PREFIX}/shops",
        "Get Shops List",
        expected_status=200
    )

    if isinstance(shops, dict) and "data" in shops:
        print(f"   🏪 Found {len(shops['data'])} shops")

def test_orders(token: str = None):
    """Test order endpoints"""
    print_section("7️⃣ ORDER ENDPOINTS")

    if not token:
        print("   ⚠️  Skipped (no auth token)")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # Get user orders
    test_endpoint(
        "GET",
        f"{API_PREFIX}/orders",
        "Get User Orders",
        headers=headers,
        expected_status=200
    )

def test_error_handling():
    """Test error scenarios"""
    print_section("8️⃣ ERROR HANDLING")

    # Invalid login
    test_endpoint(
        "POST",
        f"{API_PREFIX}/auth/login",
        "Invalid Login (wrong password)",
        data={"email": "customer1@example.com", "password": "wrongpassword"},
        expected_status=401
    )

    # Not found
    test_endpoint(
        "GET",
        f"{API_PREFIX}/products/99999",
        "Get Non-existent Product",
        expected_status=404
    )

# ============================================================
# MAIN
# ============================================================

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  🧪 E-COMMERCE API TEST SUITE")
    print("="*60)
    print(f"  Base URL: {BASE_URL}")
    print(f"  Test Credentials: {len(TEST_ACCOUNTS)} accounts")

    # Test health
    test_health()

    # Test docs
    test_api_docs()

    # Test auth (get token)
    token = test_auth()

    # Test endpoints
    test_users(token)
    test_products(token)
    test_shops(token)
    test_orders(token)

    # Test errors
    test_error_handling()

    # Summary
    print_section("✅ TEST COMPLETE")
    print("\n💡 Tips:")
    print(f"   • API Docs: {BASE_URL}/docs")
    print(f"   • Try login: {TEST_ACCOUNTS['customer']['email']}")
    print(f"   • All test accounts: admin, customer, owner, shipper")
    print(f"   • Password for all: Admin@123, Customer@123, etc.")
    print()

if __name__ == "__main__":
    main()
