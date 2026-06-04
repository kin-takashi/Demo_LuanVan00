# Hướng dẫn chạy Frontend Local & Test 4 Role

---

## 1. Chuẩn bị Backend (cần chạy trước)

### 1.1 Cấu hình .env local

```bash
cd backend
copy .env.local .env      # Windows
# hoặc: cp .env.local .env    (Mac/Linux)
```

### 1.2 Tạo MySQL database + user

Mở MySQL (cmd hoặc MySQL Workbench) và chạy:

```sql
CREATE DATABASE IF NOT EXISTS ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'shopvn_user'@'localhost' IDENTIFIED BY 'shopvn_pass';
GRANT ALL PRIVILEGES ON ecommerce_db.* TO 'shopvn_user'@'localhost';
FLUSH PRIVILEGES;
```

### 1.3 Cài thư viện Python

```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 1.4 Chạy migrations (tạo tables)

```bash
# Trong thư mục backend, venv đã activate:
python -c "from app.database import engine, Base; import app.models; Base.metadata.create_all(engine)"
```

Hoặc nếu dùng Alembic:

```bash
alembic upgrade head
```

### 1.5 Chạy Seed (tạo dữ liệu mẫu 4 role)

```bash
python seed.py
```

Seed sẽ tạo các tài khoản:

| Email | Password | Role |
|-------|----------|------|
| admin@example.com | Admin@123 | Admin |
| owner1@shop.com | Owner@123 | Shop Owner |
| owner2@shop.com | Owner@123 | Shop Owner |
| shipper1@example.com | Shipper@123 | Shipper |
| customer1@example.com | Customer@123 | Customer |

### 1.6 Chạy Backend

```bash
# Trong thư mục backend, venv đã activate:
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Kiểm tra backend hoạt động:
# Mở http://localhost:8000/health
# Swagger UI: http://localhost:8000/docs
```

---

## 2. Chạy Frontend Local

```bash
cd frontend
npm install
npm run dev
```

Frontend sẽ chạy tại: **http://localhost:3000**

> Vite config đã proxy `/api/*` → `http://localhost:8000` nên không cần thêm biến môi trường.

---

## 3. Test từng Role (Login riêng từng tài khoản)

### Role 1 — 👤 Customer (Người mua)
- Login: `customer1@example.com` / `Customer@123`
- Xem trang: `/products`, `/cart`, `/orders`
- Layout: UserLayout với navbar thường

### Role 2 — 🏪 Shop Owner (Chủ shop)
- Login: `owner1@shop.com` / `Owner@123`
- Xem trang: `/shop`, `/shop/products`, `/shop/orders`, `/shop/analytics`
- Layout: ShopLayout với sidebar quản lý

### Role 3 — 🚚 Shipper
- Login: `shipper1@example.com` / `Shipper@123`
- Xem trang: `/shipper`, `/shipper/deliveries`
- Layout: ShipperLayout

### Role 4 — ⚙️ Admin
- Login: `admin@example.com` / `Admin@123`
- Xem trang: `/admin`, `/admin/users`, `/admin/approvals`, `/admin/logs`
- Layout: AdminLayout với full sidebar

---

## 4. Lưu ý về Security Bypass (DEBUG mode)

Backend đã được sửa để **bỏ qua tất cả kiểm tra bảo mật** khi `DEBUG=True`:

- `get_current_user`: chấp nhận token hết hạn, fallback về user đầu tiên trong DB
- `require_admin`, `require_shop_owner`, `require_shipper`: luôn pass
- `require_permission`: luôn pass

> ⚠️ **Chỉ dùng khi phát triển frontend.** Khi deploy production, set `DEBUG=False` trong .env.

---

## 5. Troubleshooting

**Lỗi CORS**: Kiểm tra `ALLOWED_ORIGINS` trong `.env` có chứa `http://localhost:3000`.

**Lỗi kết nối DB**: Kiểm tra MySQL đang chạy, user/pass/db đúng trong `.env`.

**Lỗi `ModuleNotFoundError`**: Chắc chắn đã `activate` venv trước khi chạy uvicorn/seed.

**Frontend báo 401**: Backend đang ở DEBUG=True — kiểm tra `.env` và restart uvicorn.

**Seed lỗi "Duplicate entry"**: Seed đã có guard `if not existing`, chạy lại sẽ an toàn. Nếu muốn reset sạch:
```sql
-- Trong MySQL:
DROP DATABASE ecommerce_db;
CREATE DATABASE ecommerce_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- Sau đó chạy lại create_all + seed
```
