"""
Test script to verify password hashing works correctly
"""
from passlib.context import CryptContext

# Test with pbkdf2_sha256 (used by seed_minimal.py)
pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")

# This is what seed_minimal.py created
test_password = "Customer@123"
hashed_from_seed = pwd_context.hash(test_password)

print("=" * 60)
print("✅ PASSWORD HASHING TEST")
print("=" * 60)
print(f"\n📝 Test Password: {test_password}")
print(f"\n🔐 Hashed (pbkdf2_sha256): {hashed_from_seed}")

# Try to verify
verified = pwd_context.verify(test_password, hashed_from_seed)
print(f"\n✔️  Verification Result: {verified}")

if verified:
    print("\n✅ SUCCESS! Password hashing and verification is working!")
else:
    print("\n❌ FAILED! Password verification is not working!")

# Also test if we can verify an already hashed password
# This simulates what happens when login tries to verify
print("\n" + "=" * 60)
print("TESTING LOGIN VERIFICATION")
print("=" * 60)

# Create a hash as seed_minimal.py would
seeded_hash = pwd_context.hash(test_password)
print(f"\nSimulated hash from database: {seeded_hash}")

# Test verification (as login would do)
login_password = "Customer@123"
can_login = pwd_context.verify(login_password, seeded_hash)

print(f"Login with correct password: {'✅ PASS' if can_login else '❌ FAIL'}")

wrong_password = "WrongPassword"
cannot_login = pwd_context.verify(wrong_password, seeded_hash)
print(f"Login with wrong password: {'✅ FAIL (as expected)' if not cannot_login else '❌ PASS (unexpected!)'}")

print("\n" + "=" * 60)
if verified and can_login and not cannot_login:
    print("🎉 ALL TESTS PASSED! Login should work!")
else:
    print("❌ TESTS FAILED! There's still an issue")
print("=" * 60)
