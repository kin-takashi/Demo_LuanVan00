# 🔌 EXTENSION INTEGRATION - Tích Hợp Claude & Blackbox

**Ngày:** 2026-06-03
**Phiên bản:** 1.0
**Mục đích:** Sử dụng extensions để fix lỗi khi quá 5 lần

---

## 🚀 CÀI ĐẶT EXTENSIONS

### Extension 1: Claude (Khuyên Dùng)

**1. Mở VSCode**
```
File → Extensions (Ctrl+Shift+X)
```

**2. Tìm "Claude"**
```
Search: "Claude"
Author: Anthropic
```

**3. Click Install**

**4. Login vào Claude**
- Sẽ yêu cầu đăng nhập
- Chọn account Claude của bạn
- Grant permissions

### Extension 2: Blackbox

**1. Mở VSCode**
```
File → Extensions (Ctrl+Shift+X)
```

**2. Tìm "Blackbox"**
```
Search: "Blackbox AI"
```

**3. Click Install**

**4. Setup**
- Blackbox có thể không cần login (free version)
- Hoặc login account nếu cần features

---

## 🎯 KHI NÀO DÙNG EXTENSION?

### CHỈ dùng khi:

```
Lỗi xảy ra 5 lần liên tiếp
    ↓
Circuit Breaker kích hoạt
    ↓
Dừng test
    ↓
Mở extension
    ↓
Paste lỗi + log
    ↓
Chờ solution
    ↓
Implement fix
    ↓
Retry
```

### KHÔNG dùng khi:

- [ ] Lỗi lần đầu → debug sẵn
- [ ] Lỗi lần 2-3 → search Google trước
- [ ] Biết fix rồi → làm luôn

---

## 📝 CÁCH DÙNG CLAUDE EXTENSION

### Step 1: Mở Claude Extension

```
VSCode → View → Command Palette (Ctrl+Shift+P)
Search: "Claude: Start New Chat"
Enter
```

### Step 2: Chuẩn Bị Message

**Viết message gồm 3 phần:**

#### Phần 1: Context
```
I'm testing an e-commerce system with:
- Docker containers (backend, MySQL, Redis)
- FastAPI backend on port 8000
- React frontend on port 5173
- PostgreSQL database
```

#### Phần 2: Error Description
```
Error: Database connection failed after 5 attempts
Step: Running python seed.py
Error Code: ERR_101

Error Message:
sqlalchemy.exc.ArgumentError: Expected string or URL object, got None

Full Log:
[2026-06-03 10:31:12] [SEED] [FAIL] Error: SQLSTATE[HY000]
[2026-06-03 10:31:37] [SEED] [FAIL_2] Retry: SQLSTATE[HY000]
...
```

#### Phần 3: Context Từ Log
```
Last 20 lines of todo/logs/test.log:
[paste log output here]

Output từ docker logs:
[paste docker logs here]

Output từ environment:
Docker version: ...
Python version: ...
```

### Step 3: Gửi Message

```
Claude Extension sẽ:
  1. Phân tích lỗi
  2. Đề xuất giải pháp
  3. Cho code hoặc commands nếu cần
```

### Step 4: Thực Hiện Giải Pháp

**Claude sẽ trả lời như:**
```
The error is because DATABASE_URL environment variable is not set.

Solution:
1. Check your backend/.env file
2. Make sure it has:
   DATABASE_URL=mysql+pymysql://shopvn_user:shopvn_pass@db:3306/ecommerce_db

3. Run: docker-compose down && docker-compose up -d
4. Then retry: docker exec shopvn_backend python seed.py
```

**Bạn làm:**
```bash
# 1. Sửa .env
nano backend/.env
# Thêm: DATABASE_URL=...

# 2. Restart Docker
docker-compose down
docker-compose up -d

# 3. Ghi log
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ACTION] [FIX] DATABASE_URL added to .env" >> todo/logs/test.log

# 4. Retry
docker exec shopvn_backend python seed.py

# 5. Ghi kết quả
if [ $? -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [EXTENSION_FIX] [SUCCESS] seed.py passed after fix" >> todo/logs/test.log
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [EXTENSION_FIX] [FAILED] Still not working" >> todo/logs/test.log
fi
```

---

## 📝 CÁCH DÙNG BLACKBOX

### Step 1: Mở Blackbox

```
VSCode → Blackbox icon (trái sidebar)
hoặc: Ctrl+Shift+A
```

### Step 2: Hỏi Blackbox

```
"I get this error when running seed.py:
[paste error message]

How to fix?"
```

### Step 3: Nhận Giải Pháp

**Blackbox sẽ code suggestion**

```
Có thể không chi tiết như Claude
Nhưng còn OK cho lỗi đơn giản
```

---

## 🔍 DETAILED EXAMPLE

### Scenario: Login Test Thất Bại 5 Lần

**Log đầu tiên:**
```
[2026-06-03 10:32:45] [LOGIN_TEST] [FAIL_1] customer1@example.com: Invalid password
[2026-06-03 10:33:10] [LOGIN_TEST] [FAIL_2] customer1@example.com: Invalid password
[2026-06-03 10:33:35] [LOGIN_TEST] [FAIL_3] customer1@example.com: Invalid password
[2026-06-03 10:34:00] [LOGIN_TEST] [FAIL_4] customer1@example.com: Invalid password
[2026-06-03 10:34:25] [LOGIN_TEST] [FAIL_5] customer1@example.com: Invalid password
[2026-06-03 10:34:25] [CIRCUIT_BREAKER] [ACTIVE] Login failed 5 times
```

**Mở Claude Extension, viết:**

```
🔴 CRITICAL ERROR: Login Test Failed 5 Times

System Context:
- Backend: FastAPI on localhost:8000
- Frontend: React on localhost:5173
- DB: MySQL with seed data
- 16 test accounts created via seed.py

Error Details:
Attempting to login as: customer1@example.com
Password used: Customer@123
Expected: JWT token returned
Actual: "Invalid password" error

Step where it happens:
Running python test_login.py

Attempts:
1. Fresh Docker start (did docker-compose up -d)
2. Ran python seed.py successfully (shows 16 accounts created)
3. Ran test_login.py
4. All 16 accounts fail with "Invalid password"
5. Retried 4 more times with same error

Log output (full):
[paste full log section]

Questions:
1. Why would all accounts fail login after successful seed?
2. Is there a password hashing issue?
3. Should I reset password hashes?

What should I do next?
```

**Claude sẽ trả lời:**

```
The issue is likely:
1. seed.py uses bcrypt to hash passwords
2. But your API might be expecting plain text or different hash

Check:
1. Open backend/app/routes/auth.py (or similar)
2. Look for password verification logic
3. Ensure it uses same bcrypt library

Or simpler:
Try with plain text password first to isolate issue:
1. Delete all users from DB
2. Modify seed.py to NOT hash password
3. Re-run seed
4. Try login

Or even simpler:
Run this test:
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "customer1@example.com", "password": "Customer@123"}'

Share output with me.
```

**Bạn:**
```bash
# Jalankan curl command
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "customer1@example.com", "password": "Customer@123"}'

# Copy output, paste ke Claude extension
# Dapatkan clue lebih lanjut
# Implement fix
# Retry test
# Ghi log: [EXTENSION] [SOLUTION_APPLIED] ...
```

---

## 💾 SAVE EXTENSION CONVERSATIONS

### Simpan Solusi untuk Nanti

```bash
# Copy chat dari extension
# Paste ke file

mkdir todo/extension-solutions/
cat > todo/extension-solutions/login-failed-solution.txt <<EOF
Problem: Login test failed 5 times
Solution from Claude: [paste solution]
Status: [FIXED/PENDING]
Date: 2026-06-03
EOF
```

---

## ⚙️ EXTENSION TIPS

### Tip 1: Format Error Dengan Jelas

```
❌ BURUK:
"why login not work?"

✅ BAIK:
System: FastAPI + React + MySQL (Docker)
Error: Login returns 401 "Invalid password" 
Expected: JWT token
Tried: 5 times with correct credentials
Question: Why all 16 accounts fail after seed.py succeeds?
```

### Tip 2: Lampirkan Full Context

```
❌ BURUK:
Hanya paste error message

✅ BAIK:
Docker status
Python/Node versions
Error message
Full stack trace
Relevant code snippet
What you've already tried
```

### Tip 3: Jangan Spam Extension

```
❌ BURUK:
Bertanya setiap 30 detik (lỗi 5 lần = paling 5 lần bertanya)

✅ BAIK:
Tunggu circuit breaker kick in
Kumpulkan semua info
Bertanya 1 kali dengan detail lengkap
```

---

## 🔄 WORKFLOW LENGKAP

```
Test running
    ↓
Error terjadi
    ↓
Retry 1-4 kali
    ↓
Fail 5 kali
    ↓
Circuit Breaker Active
    ↓
Buka Extension (Claude/Blackbox)
    ↓
Paste full error + log + context
    ↓
Chờ solution
    ↓
Implement solution
    ↓
Ghi log: [EXTENSION] [SOLUTION_APPLIED]
    ↓
Retry test 1 kali
    ↓
Nếu PASS → lanjut test
Nếu FAIL → tanya extension lagi
```

---

## ✅ CHECKLIST

- [ ] Claude extension cài thành công
- [ ] Blackbox extension cài thành công
- [ ] Biết khi nào dùng extension (lỗi 5 lần)
- [ ] Biết cách paste error + context
- [ ] Folder `todo/extension-solutions/` tạo
- [ ] Có sample solution file

---

**Created:** 2026-06-03
**Version:** 1.0
**Last Updated:** 2026-06-03

