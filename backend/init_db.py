"""
init_db.py - Tạo tất cả database tables từ SQLAlchemy models
Chạy: python init_db.py
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import Base, engine

# Fix bcrypt version issue - just create tables without importing all models
try:
    from app.models import (
        User, Role, UserRole, Permission, RolePermission,
        Shop, ShopRegistration, ShopEmployee, EmployeeRolePermission, SystemEmployee, SystemEmployeePermission,
        Product, ProductCategory, ProductVariant, ProductReview,
        Order, OrderItem,
        Payment,
        Shipment, Shipper,
        Notification,
        Voucher,
        Dispute,
    )
except ImportError as e:
    print(f"⚠️  Some models may not be available: {e}")

print("🔨 Creating database tables...")

try:
    Base.metadata.create_all(engine)
    print("✅ All tables created successfully!")
    print("\nTables created:")
    for table in sorted(Base.metadata.tables.keys()):
        print(f"  ✓ {table}")
except Exception as e:
    print(f"❌ Error creating tables: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✨ Database initialization complete!")
print("Next: python seed_minimal.py")
