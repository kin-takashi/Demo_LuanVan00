# 📋 TODO - Testing & Documentation Center

Tất cả tài liệu, quy trình, rules, và hướng dẫn cho dự án đều được gom ở đây.

## 📁 Cấu Trúc

```
todo/
├── README.md                      # File này
├── 01_TEST_PROCEDURE.md          # Quy trình test từng bước
├── 02_RULES.md                   # Rules & constraints
├── 03_CIRCUIT_BREAKER.md         # Safety mechanism
├── 04_LOGGING_SYSTEM.md          # Error logging & tracking
├── 05_EXTENSION_INTEGRATION.md   # Claude + Blackbox integration
├── 06_EXPECTED_RESULTS.md        # Kết quả mong đợi
└── logs/
    └── test.log                  # File log lỗi
```

## 🎯 Hướng Dẫn Nhanh

### Bắt Đầu Testing
```bash
1. Đọc: 01_TEST_PROCEDURE.md
2. Đọc: 02_RULES.md
3. Thực hiện các bước trong test procedure
4. Ghi log lỗi vào: logs/test.log
5. Nếu lỗi 5 lần → 05_EXTENSION_INTEGRATION.md
```

### Quy Trình Testing Toàn Bộ
```
┌─────────────────────────────────────────┐
│  1. Start Docker                        │
├─────────────────────────────────────────┤
│  2. Create Test Data (seed)             │
├─────────────────────────────────────────┤
│  3. Test Login (4 roles)                │
├─────────────────────────────────────────┤
│  4. Check API (Swagger docs)            │
├─────────────────────────────────────────┤
│  5. Start Frontend                      │
├─────────────────────────────────────────┤
│  6. Manual Testing (UI)                 │
├─────────────────────────────────────────┤
│  7. Verify All Features                 │
└─────────────────────────────────────────┘
```

## 📚 Documents

| File | Nội Dung |
|------|----------|
| **01_TEST_PROCEDURE.md** | Step-by-step testing, commands, parallel terminals |
| **02_RULES.md** | Rules, constraints, no `&` operator, sequential execution |
| **03_CIRCUIT_BREAKER.md** | Safety mechanism, error limits, auto-stop |
| **04_LOGGING_SYSTEM.md** | Error logging, tracking, debugging |
| **05_EXTENSION_INTEGRATION.md** | VSCode extensions, Claude, Blackbox |
| **06_EXPECTED_RESULTS.md** | What should happen at each step |

## 🚀 Quick Commands

```bash
# Xem tất cả files
ls -la todo/

# Xem test procedure
cat todo/01_TEST_PROCEDURE.md

# Xem test log
cat todo/logs/test.log

# Clear log (start fresh)
> todo/logs/test.log
```

## 📝 Log Format

```
[TIMESTAMP] [STEP] [STATUS] [MESSAGE]
[2026-06-03 10:30:45] [DOCKER_START] [PASS] Docker containers started successfully
[2026-06-03 10:31:12] [SEED] [FAIL] Database connection error: SQLSTATE[HY000]
[2026-06-03 10:32:00] [LOGIN_ADMIN] [PASS] admin@example.com logged in successfully
```

---

**Last Updated:** 2026-06-03

