"""
seed_extended.py — Tạo dữ liệu mẫu mở rộng (bổ sung seed.py)
Thêm các tài khoản test bổ sung cho frontend testing.

Chạy: python seed_extended.py
"""
import os
import sys
from datetime import datetime
from decimal import Decimal

from dotenv import load_dotenv

# Load .env trước khi import app
load_dotenv()

# Đảm bảo DIRECT_URL được ưu tiên cho seed (bypass pgbouncer)
direct_url = os.getenv("DIRECT_URL")
if direct_url:
    os.environ["DATABASE_URL_OVERRIDE"] = direct_url

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

from app.models.user import User, Role, UserRole, Permission, RolePermission
from app.models.shop import Shop, ShopRegistration
from app.models.product import Product, ProductCategory, ProductVariant, ProductReview
from app.models.order import Order, OrderItem
from app.models.payment import Payment
from app.models.shipment import Shipment, Shipper
from app.models.notification import Notification
from app.models.voucher import Voucher

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_engine():
    url = os.getenv("DIRECT_URL") or os.getenv("DATABASE_URL")
    # Đảm bảo dùng psycopg2 driver
    if url and url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
    if url and "pgbouncer=true" in url:
        # Xóa pgbouncer param cho direct connection
        url = url.replace("?pgbouncer=true", "").replace("&pgbouncer=true", "")
    return create_engine(url, echo=False)


def seed_extended():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    db = Session()

    print("🌱 Bắt đầu tạo tài khoản test bổ sung...\n")

    try:
        # ================================================================
        # 1. LẤY ROLES TỪ DATABASE
        # ================================================================
        print("🔍 Lấy Roles từ database...")
        roles = {}
        for role_name in ["ADMIN", "SHOP_OWNER", "SHIPPER", "CUSTOMER", "EMPLOYEE"]:
            role = db.query(Role).filter_by(role_name=role_name).first()
            if role:
                roles[role_name] = role
        print(f"  ✅ Đã lấy {len(roles)} roles\n")

        # ================================================================
        # 2. TẠO CUSTOMERS BỔ SUNG
        # ================================================================
        print("👥 Tạo Customers bổ sung...")
        customers_data = [
            {
                "email": "customer3@example.com",
                "password": "Customer@123",
                "full_name": "Customer 3 (Premium)",
                "phone": "0967890123",
                "address": "404 VIP Lane, Q7, TP.HCM",
            },
            {
                "email": "customer4@example.com",
                "password": "Customer@123",
                "full_name": "Customer 4 (New User)",
                "phone": "0978901234",
                "address": "505 New Street, Q4, TP.HCM",
            },
            {
                "email": "customer5@example.com",
                "password": "Customer@123",
                "full_name": "Customer 5 (Active Shopper)",
                "phone": "0989012345",
                "address": "606 Active Avenue, Q5, TP.HCM",
            },
            {
                "email": "customer6@example.com",
                "password": "Customer@123",
                "full_name": "Customer 6 (Bulk Buyer)",
                "phone": "0990123456",
                "address": "707 Bulk Street, Q8, TP.HCM",
            },
            {
                "email": "customer7@example.com",
                "password": "Customer@123",
                "full_name": "Customer 7 (Test Account)",
                "phone": "0901234567",
                "address": "808 Test Lane, Q9, TP.HCM",
            },
        ]
        users = {}
        for u in customers_data:
            existing = db.query(User).filter_by(email=u["email"]).first()
            if not existing:
                obj = User(
                    email=u["email"],
                    password_hash=pwd_context.hash(u["password"]),
                    full_name=u["full_name"],
                    phone=u["phone"],
                    address=u["address"],
                    status="active",
                )
                db.add(obj)
                db.flush()
                users[u["email"]] = obj
                print(f"  ✅ {u['email']}")
            else:
                users[u["email"]] = existing
                print(f"  ℹ️  {u['email']} (already exists)")
        db.commit()
        print(f"  📋 Đã tạo {len([u for u in customers_data if u['email'] not in users or db.query(User).filter_by(email=u['email']).first()])} customers mới\n")

        # ================================================================
        # 3. TẠO SHOP OWNERS BỔ SUNG
        # ================================================================
        print("🏪 Tạo Shop Owners bổ sung...")
        owners_data = [
            {
                "email": "owner3@shop.com",
                "password": "Owner@123",
                "full_name": "Shop Owner 3",
                "phone": "0923456789",
                "address": "901 Beauty Street, Q2, TP.HCM",
            },
            {
                "email": "owner4@shop.com",
                "password": "Owner@123",
                "full_name": "Shop Owner 4",
                "phone": "0934567890",
                "address": "1002 Food Lane, Q6, TP.HCM",
            },
        ]
        owners = {}
        for u in owners_data:
            existing = db.query(User).filter_by(email=u["email"]).first()
            if not existing:
                obj = User(
                    email=u["email"],
                    password_hash=pwd_context.hash(u["password"]),
                    full_name=u["full_name"],
                    phone=u["phone"],
                    address=u["address"],
                    status="active",
                )
                db.add(obj)
                db.flush()
                owners[u["email"]] = obj
                users[u["email"]] = obj
                print(f"  ✅ {u['email']}")
            else:
                owners[u["email"]] = existing
                users[u["email"]] = existing
                print(f"  ℹ️  {u['email']} (already exists)")
        db.commit()
        print(f"  📋 Owners bổ sung\n")

        # ================================================================
        # 4. TẠO SHIPPERS BỔ SUNG
        # ================================================================
        print("🚚 Tạo Shippers bổ sung...")
        shippers_data = [
            {
                "email": "shipper2@example.com",
                "password": "Shipper@123",
                "full_name": "Shipper 2",
                "phone": "0912345670",
                "address": "110 Shipper Ave, Q8, TP.HCM",
            },
            {
                "email": "shipper3@example.com",
                "password": "Shipper@123",
                "full_name": "Shipper 3",
                "phone": "0901234568",
                "address": "120 Truck Street, Q9, TP.HCM",
            },
        ]
        shippers = {}
        for u in shippers_data:
            existing = db.query(User).filter_by(email=u["email"]).first()
            if not existing:
                obj = User(
                    email=u["email"],
                    password_hash=pwd_context.hash(u["password"]),
                    full_name=u["full_name"],
                    phone=u["phone"],
                    address=u["address"],
                    status="active",
                )
                db.add(obj)
                db.flush()
                shippers[u["email"]] = obj
                users[u["email"]] = obj
                print(f"  ✅ {u['email']}")
            else:
                shippers[u["email"]] = existing
                users[u["email"]] = existing
                print(f"  ℹ️  {u['email']} (already exists)")
        db.commit()
        print(f"  📋 Shippers bổ sung\n")

        # ================================================================
        # 5. TẠO MODERATOR
        # ================================================================
        print("🛡️  Tạo Moderator...")
        moderator_data = {
            "email": "moderator@example.com",
            "password": "Moderator@123",
            "full_name": "Content Moderator",
            "phone": "0901112233",
            "address": "200 Mod Street, Q1, TP.HCM",
        }
        existing = db.query(User).filter_by(email=moderator_data["email"]).first()
        if not existing:
            moderator = User(
                email=moderator_data["email"],
                password_hash=pwd_context.hash(moderator_data["password"]),
                full_name=moderator_data["full_name"],
                phone=moderator_data["phone"],
                address=moderator_data["address"],
                status="active",
            )
            db.add(moderator)
            db.flush()
            users[moderator_data["email"]] = moderator
            print(f"  ✅ {moderator_data['email']}\n")
        else:
            users[moderator_data["email"]] = existing
            print(f"  ℹ️  {moderator_data['email']} (already exists)\n")
        db.commit()

        # ================================================================
        # 6. GÁN USER ROLES
        # ================================================================
        print("🎭 Gán User Roles...")
        role_assignments = [
            # Customers
            (users.get("customer3@example.com"), "CUSTOMER"),
            (users.get("customer4@example.com"), "CUSTOMER"),
            (users.get("customer5@example.com"), "CUSTOMER"),
            (users.get("customer6@example.com"), "CUSTOMER"),
            (users.get("customer7@example.com"), "CUSTOMER"),
            # Owners
            (users.get("owner3@shop.com"), "SHOP_OWNER"),
            (users.get("owner4@shop.com"), "SHOP_OWNER"),
            # Shippers
            (users.get("shipper2@example.com"), "SHIPPER"),
            (users.get("shipper3@example.com"), "SHIPPER"),
            # Moderator
            (users.get("moderator@example.com"), "ADMIN"),
        ]

        count = 0
        for user_obj, role_name in role_assignments:
            if user_obj and role_name in roles:
                role_obj = roles[role_name]
                exists = db.query(UserRole).filter_by(
                    user_id=user_obj.user_id, role_id=role_obj.role_id
                ).first()
                if not exists:
                    db.add(
                        UserRole(
                            user_id=user_obj.user_id,
                            role_id=role_obj.role_id,
                            current_role=True,
                            status="active",
                        )
                    )
                    count += 1
                    print(f"  ✅ {user_obj.email} → {role_name}")
        db.commit()
        print(f"  📋 Gán {count} roles\n")

        # ================================================================
        # 7. TẠO SHOPS CHO OWNERS MỚI
        # ================================================================
        print("🏪 Tạo Shops cho owners mới...")
        shops_data = [
            {
                "shop_id": owners["owner3@shop.com"].user_id if "owner3@shop.com" in owners else None,
                "shop_name": "Beauty & Care Hub",
                "description": "Mỹ phẩm, tỉ dầu dưỡng da chất lượng cao",
                "address": "901 Beauty Street, Q2, TP.HCM",
                "phone": "0923456789",
                "rating": Decimal("4.3"),
                "total_followers": 600,
                "total_orders": 80,
                "verification_status": "approved",
            },
            {
                "shop_id": owners["owner4@shop.com"].user_id if "owner4@shop.com" in owners else None,
                "shop_name": "Food & Beverage Store",
                "description": "Thực phẩm sạch, nước uống, đồ ăn nhẹ",
                "address": "1002 Food Lane, Q6, TP.HCM",
                "phone": "0934567890",
                "rating": Decimal("4.6"),
                "total_followers": 1200,
                "total_orders": 300,
                "verification_status": "approved",
            },
        ]
        for s in shops_data:
            if s["shop_id"]:
                existing = db.query(Shop).filter_by(shop_id=s["shop_id"]).first()
                if not existing:
                    obj = Shop(**s)
                    db.add(obj)
                    print(f"  ✅ {s['shop_name']}")
        db.commit()
        print(f"  📋 Tạo shops\n")

        # ================================================================
        # 8. TẠO SHIPPER PROFILES
        # ================================================================
        print("🚚 Tạo Shipper Profiles...")
        shipper_profiles = [
            {
                "shipper_id": shippers["shipper2@example.com"].user_id if "shipper2@example.com" in shippers else None,
                "vehicle_type": "Xe máy",
                "rating": Decimal("4.5"),
                "total_deliveries": 120,
                "status": "available",
            },
            {
                "shipper_id": shippers["shipper3@example.com"].user_id if "shipper3@example.com" in shippers else None,
                "vehicle_type": "Xe tải",
                "rating": Decimal("4.8"),
                "total_deliveries": 200,
                "status": "available",
            },
        ]
        for s in shipper_profiles:
            if s["shipper_id"]:
                existing = db.query(Shipper).filter_by(shipper_id=s["shipper_id"]).first()
                if not existing:
                    db.add(Shipper(**s))
                    print(f"  ✅ Shipper {s['shipper_id']} - {s['vehicle_type']}")
        db.commit()
        print(f"  📋 Tạo shipper profiles\n")

        # ================================================================
        # SUMMARY
        # ================================================================
        print("\n✨ ========================================")
        print("✨ Tạo tài khoản bổ sung hoàn tất!")
        print("✨ ========================================\n")

        print("🔑 TÀI KHOẢN TEST MỚI:")
        print("\n👥 CUSTOMERS:")
        for u in customers_data:
            print(f"   {u['email']} / {u['password']}")

        print("\n🏪 SHOP OWNERS:")
        for u in owners_data:
            print(f"   {u['email']} / {u['password']}")

        print("\n🚚 SHIPPERS:")
        for u in shippers_data:
            print(f"   {u['email']} / {u['password']}")

        print("\n🛡️  MODERATOR:")
        print(f"   {moderator_data['email']} / {moderator_data['password']}")

        print("\n✅ Sẵn sàng để test frontend!\n")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Lỗi khi seed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    seed_extended()
