# 🧪 TEST PROCEDURE - Quy Trình Test Toàn Bộ

**Ngày:** 2026-06-03
**Phiên bản:** 1.0
**Mục đích:** Hướng dẫn test hệ thống từng bước, chạy lệnh đúng trình tự

---

## 📋 Tổng Quan

Test được chia thành **7 bước chính**, mỗi bước chạy **tuần tự** (không song song):

```
Step 1  → Step 2  → Step 3  → Step 4  → Step 5  → Step 6  → Step 7
Docker   Seed     Login    API Docs  Frontend  UI Test   Verify
```

**QUAN TRỌNG:** Chạy từng bước một, chờ hoàn tất rồi mới sang bước tiếp theo!

---

## ⚙️ YÊU CẦU TRƯỚC KHI BẮT ĐẦU

### Kiểm tra
- [ ] Docker Desktop đã cài (Windows/Mac)
- [ ] Git Bash hoặc Terminal/PowerShell
- [ ] Python 3.10+
- [ ] Node.js 18+
- [ ] VSCode (có Claude extension)

### Chuẩn Bị
- [ ] Đã clone project
- [ ] Đã tạo `backend/.env`
- [ ] Đã backup nếu cần

---

## 🔄 QUY TRÌNH TEST CHÍNH

### STEP 1️⃣: Khởi Động Docker (3-5 phút)

**Lệnh:**
```bash
cd /e/SUB_LUAN_VAN/luan_van
docker-compose down
docker-compose up -d
```

**Chờ đợi:**
- Xem các containers khởi động
- Chờ ~30 giây tất cả containers "healthy"

**Kiểm tra:**
```bash
docker ps
# Output: 3 containers chạy (db, redis, backend)
```

**Kết quả mong đợi:**
- ✅ shopvn_db: running
- ✅ shopvn_redis: running
- ✅ shopvn_backend: running

**Nếu lỗi:**
→ Ghi vào `logs/test.log` (format: `[TIMESTAMP] [DOCKER_START] [FAIL] Error message`)
→ Xem `03_CIRCUIT_BREAKER.md` để quyết định tiếp tục hay không

**Chuyển sang Step 2 khi:** Cả 3 containers chạy bình thường

---

### STEP 2️⃣: Tạo Test Data (2-3 phút)

**2A - Tạo Dữ Liệu Ban Đầu:**
```bash
docker exec shopvn_backend python seed.py
```

**Chờ log output:**
```
✅ Roles...
✅ Permissions...
✅ Users...
✅ Shops...
✅ Products...
...
✨ Seed dữ liệu hoàn tất!
```

**2B - Tạo Dữ Liệu Mở Rộng (Tài Khoản Thêm):**
```bash
docker exec shopvn_backend python seed_extended.py
```

**Chờ log output:**
```
✅ Customers bổ sung...
✅ Shop Owners bổ sung...
✅ Shippers bổ sung...
✅ Moderator...
✅ Test Account MỚI Created!
```

**Kết quả mong đợi:**
- ✅ 6 original accounts
- ✅ 10+ new accounts  
- ✅ Total: 16 accounts
- ✅ Shops, products, orders created

**Nếu lỗi:**
→ Ghi `[SEED] [FAIL]` vào log
→ Likely: DATABASE_URL trong .env sai
→ Fix: Sửa backend/.env, restart Docker, retry

**Chuyển sang Step 3 khi:** Cả 2 seed scripts chạy xong, không lỗi

---

### STEP 3️⃣: Test Login (5 phút)

**Chạy script test login:**
```bash
docker exec shopvn_backend python test_login.py
```

**Output mong đợi:**
```
======================================================================
  🔐 LOGIN TEST - All Test Accounts
======================================================================

📌 ADMIN (2 accounts)
  ✅ admin      | admin@example.com           | Token: ...
  ✅ moderator  | moderator@example.com       | Token: ...

📌 CUSTOMER (7 accounts)
  ✅ customer1  | customer1@example.com       | Token: ...
  ✅ customer3  | customer3@example.com       | Token: ...
  ...

📌 SHOP_OWNER (4 accounts)
  ✅ owner1     | owner1@shop.com             | Token: ...
  ...

📌 SHIPPER (3 accounts)
  ✅ shipper1   | shipper1@example.com        | Token: ...
  ...

======================================================================
  📊 SUMMARY
======================================================================
  Total: 16 accounts
  ✅ Passed: 16
  ❌ Failed: 0
  Success Rate: 100.0%

  🎉 ALL ACCOUNTS WORKING!
```

**Các kết quả cần kiểm tra:**
- [ ] ADMIN: 2/2 passed
- [ ] CUSTOMER: 7/7 passed
- [ ] SHOP_OWNER: 4/4 passed
- [ ] SHIPPER: 3/3 passed
- [ ] Success Rate: 100%

**Nếu có lỗi (Failed > 0):**
→ Ghi `[LOGIN_TEST] [FAIL]` + chi tiết lỗi
→ Có thể: seed.py chưa chạy xong, hoặc database chưa sẵn sàng
→ Retry: Chạy seed.py lại

**Chuyển sang Step 4 khi:** Tất cả 16 accounts login thành công

---

### STEP 4️⃣: Kiểm tra API Documentation (2 phút)

**Chạy script test API:**
```bash
docker exec shopvn_backend python test_api.py
```

**Output mong đợi:**
```
✅ Backend Health: PASS
✅ Swagger UI (Docs): PASS
✅ OpenAPI Schema: PASS
✅ Login (customer): PASS
✅ Get User Profile: PASS
✅ Get Products List: PASS
✅ Get Shops List: PASS
✅ Get User Orders: PASS
✅ Invalid Login (wrong password): PASS
✅ Get Non-existent Product: PASS
```

**Kiểm tra bằng Browser:**
```
http://localhost:8000/docs
```
→ Nên thấy Swagger UI với tất cả API endpoints

**Nếu lỗi:**
→ Ghi `[API_TEST] [FAIL]`
→ Check: Backend có chạy trên port 8000?
→ Check: Docker logs: `docker logs shopvn_backend`

**Chuyển sang Step 5 khi:** Test API đạt 100%

---

### STEP 5️⃣: Khởi Động Frontend (2-3 phút)

**Mở Terminal/Bash MỚI (không đóng terminal Docker):**

```bash
cd /e/SUB_LUAN_VAN/luan_van/frontend
npm install
npm run dev
```

**Chờ output:**
```
  VITE v5.0.0  ready in 234 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

**Kiểm tra:**
```
http://localhost:5173
```
→ Nên thấy home page load bình thường

**Nếu lỗi:**
→ Ghi `[FRONTEND_START] [FAIL]`
→ Check: Node.js version `node -v`
→ Check: npm packages: `npm install` lại
→ Check: VITE_API_URL trong frontend/.env.local

**Chuyển sang Step 6 khi:** Frontend load thành công trên :5173

---

### STEP 6️⃣: Test Manual UI (10-15 phút)

**Không đóng frontend, mở http://localhost:5173 trong browser:**

#### Test 6A: Login as CUSTOMER
```
Email: customer1@example.com
Password: Customer@123
```
✅ Kết quả: Đăng nhập thành công, thấy trang chủ
✅ Thấy: User menu, Shopping cart, Products

#### Test 6B: Login as SHOP_OWNER
```
Email: owner1@shop.com
Password: Owner@123
```
✅ Kết quả: Vào seller dashboard
✅ Thấy: Orders, Products management, Analytics

#### Test 6C: Login as SHIPPER
```
Email: shipper1@example.com
Password: Shipper@123
```
✅ Kết quả: Vào shipper dashboard
✅ Thấy: Deliveries, Status updates

#### Test 6D: Login as ADMIN
```
Email: admin@example.com
Password: Admin@123
```
✅ Kết quả: Vào admin panel
✅ Thấy: User management, Shop management

**Ghi vào log nếu có lỗi UI:**
```
[2026-06-03 11:30:00] [UI_LOGIN] [FAIL] Login button không click được
[2026-06-03 11:31:00] [UI_CUSTOMER] [FAIL] Products không load
```

**Chuyển sang Step 7 khi:** Cả 4 roles login thành công, UI hiển thị

---

### STEP 7️⃣: Kiểm Tra Tổng Thể (5 phút)

**Checklist Cuối Cùng:**

- [ ] Docker containers đang chạy
- [ ] Backend API hoạt động (docs trên :8000/docs)
- [ ] Frontend load thành công (:5173)
- [ ] 16 test accounts login thành công
- [ ] Cả 4 roles access được hệ thống
- [ ] Không có error lớn trong console

**Nếu tất cả ✅ = SUCCESS!**

```
🎉 TESTING COMPLETE - HỆ THỐNG SẴN SÀNG
```

---

## ⚠️ LỖI PHỔ BIẾN & FIX

| Lỗi | Nguyên Nhân | Fix |
|-----|-----------|-----|
| Connection refused 5432 | PostgreSQL không chạy | `docker-compose up -d` |
| DATABASE_URL is None | .env không set | `cp backend/.env.example backend/.env` |
| Port 8000 already in use | Backend đang chạy | `docker-compose down` rồi `up -d` |
| Login failed (401) | Tài khoản không tồn tại | Chạy `python seed.py` |
| Frontend not connecting | API URL sai | Check `.env.local`: `VITE_API_URL=http://localhost:8000` |
| npm install fail | Node version cũ | `node -v` ≥ 18.0.0 |

---

## 📝 Ghi Nhớ

1. **CHẠY TUẦN TỰ** - Không dùng `&` để chạy song song (xem 02_RULES.md)
2. **GHI LOG** - Mỗi lỗi ghi vào `logs/test.log`
3. **5 LỖI RULE** - Nếu lỗi 5 lần → dùng Claude extension (05_EXTENSION_INTEGRATION.md)
4. **CIRCUIT BREAKER** - Nếu hệ thống chạy không kiểm soát → dừng ngay (03_CIRCUIT_BREAKER.md)

---

**Created:** 2026-06-03
**Version:** 1.0

