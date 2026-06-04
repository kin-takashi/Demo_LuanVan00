# 🛑 CIRCUIT BREAKER - Bức Tường Chắn

**Ngày:** 2026-06-03
**Phiên bản:** 1.0
**Mục đích:** Ngăn chặn hệ thống chạy không kiểm soát

---

## 🚨 CIRCUIT BREAKER LÀ GÌ?

**Circuit Breaker** là một bộ máy an toàn tự động:
- Giám sát quá trình test
- Nếu gặp vấn đề → ngừng ngay
- Tránh hệ thống chạy quá dáng

---

## 🔴 CIRCUIT BREAKER TRIGGER (Kích Hoạt)

### Trigger 1: Lỗi Lặp Lại 5 Lần

```
Lần 1: ❌ Lỗi → ghi log, retry
Lần 2: ❌ Lỗi → ghi log, retry
Lần 3: ❌ Lỗi → ghi log, retry
Lần 4: ❌ Lỗi → ghi log, retry
Lần 5: ❌ Lỗi → CIRCUIT BREAKER ACTIVE 🛑

Action:
  1. Dừng test ngay
  2. Ghi log: [CIRCUIT_BREAKER] [ACTIVE]
  3. Dùng Claude extension để fix
  4. Chỉ retry sau khi fix
```

### Trigger 2: Process Zombie (Chạy Mãi Không Kết Thúc)

```
Lệnh chạy lâu quá bình thường (vd: npm run dev timeout 5 phút)

Action:
  1. Bấm Ctrl + C để dừng
  2. Nếu không dừng được → kill process
  3. Ghi log: [ZOMBIE_PROCESS] [KILLED]
  4. Restart từ bước trước
```

### Trigger 3: Resource Quá Cao

```
CPU: >80% đứng yên (không tăng/giảm)
Memory: >1GB bị stuck
Disk: Full (no space left)

Action:
  1. Dừng tất cả processes
  2. Kiểm tra Resource Manager
  3. Xóa cache, clear temp files
  4. Restart Docker: docker-compose down && up -d
```

### Trigger 4: Database Crashed

```
Khi seed.py hoặc login test lỗi:
  "Connection to server refused"
  "SQLSTATE[HY000]"
  "Broken pipe"

Action:
  1. Kiểm tra Docker: docker ps
  2. Nếu db container down → docker-compose up -d
  3. Chờ DB healthy (xem logs: docker logs shopvn_db)
  4. Retry
```

### Trigger 5: Port Bị Stuck

```
Port 8000 (backend) bị chiếm
Port 3000/5173 (frontend) bị chiếm
Port 3306 (MySQL) bị chiếm

Action:
  1. Tìm process: netstat -ano | findstr :8000
  2. Kill process: taskkill /PID <PID> /F
  3. Hoặc: docker-compose down (sẽ free tất cả ports)
```

---

## 🛑 CIRCUIT BREAKER STATES

### STATE 1: CLOSED ✅ (Bình thường)
```
Hệ thống chạy tốt, lỗi < 2 lần liên tiếp
→ Tiếp tục test bình thường
```

### STATE 2: OPEN 🔴 (Ngừng)
```
Lỗi ≥ 5 lần hoặc resource quá cao
→ DỪNG TEST NGAY
→ Dùng extension để fix
→ Chỉ restart khi chắc chắn fix được
```

### STATE 3: HALF-OPEN 🟡 (Chuẩn Bị Retry)
```
Vừa fix được (theo hướng từ extension)
→ Test 1 lần thử
  ✅ Nếu thành công → quay lại CLOSED
  ❌ Nếu fail → quay lại OPEN (dùng extension lại)
```

---

## 📊 STATE DIAGRAM

```
        CLOSED (✅)
           ↓
    [Lỗi xảy ra]
           ↓
        OPEN (🔴)
           ↓
    [Fix theo extension]
           ↓
      HALF-OPEN (🟡)
           ↓
    [Retry 1 lần]
         ↙   ↘
       ✅     ❌
       ↙       ↘
    CLOSED   OPEN
```

---

## 🛡️ CÁCH IMPLEMENT

### Ghi Nhớ Error Count

```
Trong quá trình test, tự đếm số lỗi:

Step 1: Docker
  Error count = 0 → PASS
  
Step 2: Seed
  Lần 1: ❌ count = 1
  Lần 2: ❌ count = 2
  Lần 3: ❌ count = 3
  Lần 4: ❌ count = 4
  Lần 5: ❌ count = 5 → CIRCUIT BREAKER!

Nếu khác step, count reset:
Step 3: Login test (count = 0, mới bắt đầu)
```

### Ghi Log Circuit Breaker

```bash
# Khi lỗi lần 1, 2, 3, 4
echo "[$(date)] [STEP_NAME] [FAIL_#] Error message" >> todo/logs/test.log

# Khi lỗi lần 5
echo "[$(date)] [STEP_NAME] [CIRCUIT_BREAKER_ACTIVE] Lỗi 5 lần liên tiếp" >> todo/logs/test.log
echo "[$(date)] [ACTION] Dừng test, sử dụng Claude extension" >> todo/logs/test.log

# Khi fix xong
echo "[$(date)] [STEP_NAME] [CIRCUIT_BREAKER_RESET] Lỗi đã fix, retry" >> todo/logs/test.log
```

---

## 🔧 CÁCH RESET CIRCUIT BREAKER

### Nếu Fix Được

```bash
# 1. Ghi lỗi final vào log
echo "[$(date)] [FIX] Giải pháp: ..." >> todo/logs/test.log

# 2. Thực hiện fix (ví dụ: sửa .env)
nano backend/.env

# 3. Restart Docker nếu cần
docker-compose down
docker-compose up -d

# 4. Reset error count = 0

# 5. Retry step đó 1 lần
docker exec shopvn_backend python seed.py

# 6. Ghi kết quả
echo "[$(date)] [RETRY_AFTER_FIX] [PASS] Thành công!" >> todo/logs/test.log

# 7. Tiếp tục test
```

### Nếu Không Fix Được (Dùng Extension)

```bash
# 1. Ghi lỗi final
echo "[$(date)] [CANNOT_FIX] Không thể fix, cần hỏi extension" >> todo/logs/test.log

# 2. Copy lỗi + log output

# 3. Mở Claude extension trong VSCode
# File → Extensions → Claude

# 4. Paste lỗi vào chat

# 5. Chờ Claude trả lời

# 6. Thực hiện giải pháp Claude đưa ra

# 7. Retry test

# 8. Ghi kết quả
echo "[$(date)] [EXTENSION_SOLUTION] [APPLIED] Thực hiện giải pháp từ extension" >> todo/logs/test.log
```

---

## 📋 CHECKLIST CIRCUIT BREAKER

- [ ] Hiểu 5 triggers
- [ ] Biết cách count errors
- [ ] Có thể ghi log đúng format
- [ ] Biết reset circuit breaker
- [ ] Cài Claude extension trong VSCode
- [ ] Biết cách paste error vào extension
- [ ] Hiểu HALF-OPEN state

---

## ⚠️ CẢNH BÁO

### ❌ KHÔNG ĐƯỢC

```bash
# KHÔNG bỏ qua Circuit Breaker
# KHÔNG chạy thêm lệnh khi CB đã active
# KHÔNG spam retry (lỗi 5 lần rồi vẫn retry)
# KHÔNG kill Docker mạnh mà không backup
```

### ✅ NÊN LÀM

```bash
# ✅ Tôn trọng Circuit Breaker
# ✅ Đợi fix trước khi retry
# ✅ Sử dụng extension khi cần
# ✅ Ghi log chi tiết mọi lỗi
```

---

## 🔍 TROUBLESHOOTING

| Vấn Đề | Xảy Ra Khi | Giải Pháp |
|--------|-----------|----------|
| "Connection refused" x5 | Docker không chạy | `docker-compose up -d` |
| "SQLSTATE" x5 | DB crashed | Xem docker logs, restart |
| "npm not found" x5 | Node/npm chưa cài | Cài Node.js |
| "Module not found" x5 | npm install chưa đủ | `npm install` lại |
| Port already in use x5 | Process cũ chưa close | Kill process cũ |

---

**Created:** 2026-06-03
**Version:** 1.0
**Last Updated:** 2026-06-03

