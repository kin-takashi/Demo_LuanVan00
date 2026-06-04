# 📝 LOGGING SYSTEM - Hệ Thống Ghi Nhật Ký

**Ngày:** 2026-06-03
**Phiên bản:** 1.0
**Mục đích:** Ghi chi tiết tất cả lỗi & kết quả để debug sau

---

## 📁 LOG FILE LOCATION

```
todo/logs/test.log
```

### Cách Truy Cập

```bash
# Xem log
cat todo/logs/test.log

# Xem cuối cùng 20 dòng
tail -20 todo/logs/test.log

# Xem toàn bộ với line numbers
cat -n todo/logs/test.log

# Clear log (xóa sạch)
> todo/logs/test.log

# Append mode (thêm mới vào cuối)
echo "..." >> todo/logs/test.log
```

---

## 📋 LOG FORMAT

### Định Dạng Chuẩn

```
[YYYY-MM-DD HH:MM:SS] [STEP] [STATUS] [MESSAGE] [ERROR_CODE]
```

### Ví Dụ Cụ Thể

```
[2026-06-03 10:30:45] [DOCKER_START] [PASS] Docker containers started successfully
[2026-06-03 10:31:12] [DOCKER_START] [FAIL] Error: Docker daemon not running [ERR_001]
[2026-06-03 10:32:00] [SEED] [PASS] seed.py completed, 16 accounts created
[2026-06-03 10:32:45] [LOGIN_TEST] [FAIL_1] customer1@example.com: Invalid password [ERR_401]
[2026-06-03 10:33:10] [LOGIN_TEST] [FAIL_2] Retry: customer1@example.com [ERR_401]
[2026-06-03 10:33:35] [LOGIN_TEST] [FAIL_3] Retry: customer1@example.com [ERR_401]
[2026-06-03 10:34:00] [LOGIN_TEST] [FAIL_4] Retry: customer1@example.com [ERR_401]
[2026-06-03 10:34:25] [LOGIN_TEST] [FAIL_5] Retry: customer1@example.com [ERR_401]
[2026-06-03 10:34:25] [CIRCUIT_BREAKER] [ACTIVE] Login failed 5 times, using extension
[2026-06-03 10:35:00] [EXTENSION] [CONSULTING] Sent to Claude extension
[2026-06-03 10:35:45] [EXTENSION] [SOLUTION] Run: python seed.py again
[2026-06-03 10:36:00] [ACTION] [RETRY] Running seed.py
[2026-06-03 10:36:30] [SEED] [PASS] Seed successful, retrying login
[2026-06-03 10:36:45] [LOGIN_TEST] [PASS] customer1@example.com login successful
```

---

## 📊 LOG STATUS CODES

### Success Codes

| Code | Ý Nghĩa |
|------|--------|
| `[PASS]` | Bước hoàn tất thành công |
| `[DONE]` | Test xong, có kết quả |
| `[OK]` | Tất cả OK, tiếp tục |

### Failure Codes

| Code | Ý Nghĩa |
|------|--------|
| `[FAIL]` | Bước thất bại |
| `[FAIL_1]` | Lần 1 thất bại |
| `[FAIL_2]` | Lần 2 thất bại |
| ... | ... |
| `[FAIL_5]` | Lần 5 thất bại = CIRCUIT BREAKER |

### Special Codes

| Code | Ý Nghĩa |
|------|--------|
| `[CIRCUIT_BREAKER]` | Kích hoạt bộ an toàn |
| `[EXTENSION]` | Sử dụng Claude extension |
| `[ACTION]` | Hành động được thực hiện |
| `[RETRY]` | Thử lại |

---

## 🔢 ERROR CODES

### Database Errors

```
[ERR_101] Database connection failed
[ERR_102] SQLSTATE[HY000] - SQL connection error
[ERR_103] Authentication failed (wrong password)
[ERR_104] User not found
[ERR_105] Duplicate key error
```

### Server Errors

```
[ERR_201] Backend not running (localhost:8000)
[ERR_202] Port already in use
[ERR_203] Server internal error (500)
[ERR_204] Timeout
```

### API Errors

```
[ERR_301] Invalid credentials (401)
[ERR_302] Not found (404)
[ERR_303] Bad request (400)
[ERR_304] CORS error
[ERR_305] Invalid token
```

### Setup Errors

```
[ERR_401] Environment variable not set
[ERR_402] File not found
[ERR_403] Permission denied
[ERR_404] Module not found
[ERR_405] Docker not installed
```

---

## 🖊️ CÁCH GHI LOG

### Từ Terminal/Bash

```bash
# Ghi log thủ công
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [DOCKER_START] [PASS] Docker started" >> todo/logs/test.log

# Ghi lỗi
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [SEED] [FAIL] Error: Database not ready [ERR_101]" >> todo/logs/test.log

# Ghi với lỗi code
ERROR_CODE="ERR_101"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [SEED] [FAIL] Database connection failed [$ERROR_CODE]" >> todo/logs/test.log
```

### Ghi Lỗi Từ Output

```bash
# Capture error output
docker exec shopvn_backend python seed.py 2>&1 | tee -a todo/logs/test.log

# Nếu có lỗi, ghi vào log
ERROR_MSG=$(docker exec shopvn_backend python seed.py 2>&1)
if [ $? -ne 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [SEED] [FAIL] $ERROR_MSG" >> todo/logs/test.log
fi
```

---

## 📈 LOG ANALYTICS

### Đếm Lỗi Theo Step

```bash
# Đếm lỗi DOCKER
grep "[DOCKER" todo/logs/test.log | grep "FAIL" | wc -l

# Đếm lỗi LOGIN
grep "[LOGIN" todo/logs/test.log | grep "FAIL" | wc -l

# Đếm tất cả FAIL
grep "FAIL" todo/logs/test.log | wc -l

# Đếm tất cả PASS
grep "PASS" todo/logs/test.log | wc -l
```

### Tìm Lỗi Cụ Thể

```bash
# Tìm lỗi connection
grep "connection" todo/logs/test.log

# Tìm lỗi authentication
grep "401\|Invalid\|password" todo/logs/test.log

# Tìm circuit breaker
grep "CIRCUIT_BREAKER" todo/logs/test.log
```

### Xem Timeline Lỗi

```bash
# Xem lỗi theo thời gian
grep "FAIL\|CIRCUIT" todo/logs/test.log | head -10

# Xem 5 lỗi cuối cùng
grep "FAIL" todo/logs/test.log | tail -5
```

---

## 📋 LOG TEMPLATE

### Template PASS

```
[$(date '+%Y-%m-%d %H:%M:%S')] [STEP_NAME] [PASS] Action completed successfully
```

### Template FAIL (Lần 1-4)

```
[$(date '+%Y-%m-%d %H:%M:%S')] [STEP_NAME] [FAIL_N] Error message [ERROR_CODE]
```

### Template CIRCUIT BREAKER

```
[$(date '+%Y-%m-%d %H:%M:%S')] [STEP_NAME] [FAIL_5] Final attempt failed [ERROR_CODE]
[$(date '+%Y-%m-%d %H:%M:%S')] [CIRCUIT_BREAKER] [ACTIVE] Stopping test, using extension
```

### Template EXTENSION

```
[$(date '+%Y-%m-%d %H:%M:%S')] [EXTENSION] [CONSULTING] Sent error to Claude extension
[$(date '+%Y-%m-%d %H:%M:%S')] [EXTENSION] [SOLUTION] Received solution: <solution>
[$(date '+%Y-%m-%d %H:%M:%S')] [ACTION] [RETRY] Implementing solution
```

---

## 🔄 LOG LIFECYCLE

```
Start Test
    ↓
[PASS] → Next Step
    ↓
[PASS] → Next Step
    ↓
[FAIL_1] → Retry
    ↓
[FAIL_2] → Retry
    ↓
[FAIL_3] → Retry
    ↓
[FAIL_4] → Retry
    ↓
[FAIL_5] → CIRCUIT_BREAKER
    ↓
[EXTENSION] → Get Solution
    ↓
[ACTION] → Implement Fix
    ↓
[RETRY] → Try Again
    ↓
[PASS] → Continue or Success
```

---

## ✅ CHECKLIST LOG

- [ ] File `todo/logs/test.log` đã tạo
- [ ] Biết format: `[TIMESTAMP] [STEP] [STATUS] [MESSAGE]`
- [ ] Biết error codes
- [ ] Có thể ghi log thủ công
- [ ] Có thể query log (grep)
- [ ] Hiểu LOG lifecycle

---

## 💡 TIP

```bash
# Auto timestamp khi ghi log
alias log='echo "[$(date "+%Y-%m-%d %H:%M:%S")]'

# Use:
log [STEP] [STATUS] Message" >> todo/logs/test.log

# Hoặc tạo script
# File: log.sh
#!/bin/bash
echo "[$(date '+%Y-%m-%d %H:%M:%S')] $@" >> todo/logs/test.log

# Use:
./log.sh [DOCKER] [PASS] Started successfully
```

---

**Created:** 2026-06-03
**Version:** 1.0
**Last Updated:** 2026-06-03

