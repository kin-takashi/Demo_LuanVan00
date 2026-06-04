"""
seed_minimal.py - Tạo 4 tài khoản test nhanh nhất
Chạy: python seed_minimal.py
Thời gian: ~30 giây
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from app.models.user import User, Role, UserRole

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_engine():
    url = os.getenv("DIRECT_URL") or os.getenv("DATABASE_URL")
    if url and url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
    if url and "pgbouncer=true" in url:
        url = url.replace("?pgbouncer=true", "").replace("&pgbouncer=true", "")
    return create_engine(url, echo=False)

def seed_minimal():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    db = Session()

    print("⚡ Tạo tài khoản test nhanh...\n")

    try:
        # ================================================================
        # 1. CREATE ROLES
        # ================================================================
        print("📝 Tạo Roles...")
        roles = {}
        for role_name in ["ADMIN", "SHOP_OWNER", "SHIPPER", "CUSTOMER"]:
            existing = db.query(Role).filter_by(role_name=role_name).first()
            if not existing:
                role = Role(role_name=role_name, description=role_name)
                db.add(role)
                db.flush()
                roles[role_name] = role
            else:
                roles[role_name] = existing
        db.commit()
        print("  ✅ 4 roles\n")

        # ================================================================
        # 2. CREATE 4 TEST USERS
        # ================================================================
        print("👥 Tạo 4 Tài Khoản Test...")
        users_data = [
            ("customer1@example.com", "Customer@123", "CUSTOMER", "Customer 1"),
            ("owner1@shop.com", "Owner@123", "SHOP_OWNER", "Shop Owner 1"),
            ("shipper1@example.com", "Shipper@123", "SHIPPER", "Shipper 1"),
            ("admin@example.com", "Admin@123", "ADMIN", "Admin User"),
        ]

        for email, password, role_name, full_name in users_data:
            existing = db.query(User).filter_by(email=email).first()
            if not existing:
                user = User(
                    email=email,
                    password_hash=pwd_context.hash(password),
                    full_name=full_name,
                    phone="0123456789",
                    status="active"
                )
                db.add(user)
                db.flush()

                # Assign role
                ur = UserRole(
                    user_id=user.user_id,
                    role_id=roles[role_name].role_id,
                    current_role=True,
                    status="active"
                )
                db.add(ur)
                print(f"  ✅ {email:30} / {password}")
            else:
                print(f"  ℹ️  {email:30} (exists)")

        db.commit()

        # ================================================================
        # SUMMARY
        # ================================================================
        print("\n" + "="*60)
        print("✨ MINIMAL SEED COMPLETE!")
        print("="*60)
        print("\n🔑 Tài khoản test (4 roles):")
        print("  1️⃣  CUSTOMER:     customer1@example.com / Customer@123")
        print("  2️⃣  SHOP_OWNER:   owner1@shop.com / Owner@123")
        print("  3️⃣  SHIPPER:      shipper1@example.com / Shipper@123")
        print("  4️⃣  ADMIN:        admin@example.com / Admin@123")
        print("\n✅ Sẵn sàng test frontend!")
        print("   http://localhost:5173\n")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    seed_minimal()
