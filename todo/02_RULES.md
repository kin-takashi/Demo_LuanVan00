# 📋 RULES - Quy Tắc & Ràng Buộc

**Ngày:** 2026-06-03
**Phiên bản:** 1.0
**Mục đích:** Định nghĩa các quy tắc khi chạy test và tương tác với hệ thống

---

## 🚫 RULE 1: BAN CÁC LỆNHsong song với `&`

### ❌ KHÔNG ĐƯỢC LÀM

```bash
# SAI - Chạy 2 lệnh cùng lúc
docker-compose up -d & npm run dev

# SAI - Chạy 3 lệnh liên tiếp
python seed.py & python seed_extended.py & npm run dev

# SAI - Nối bằng && (chạy nếu trước đó success)
docker-compose up -d && python seed.py && npm run dev
```

### ❌ TẠI SAO?

1. **VSCode không hiểu** - VSCode terminal không parse `&` operator đúng
2. **Khó debug** - Khi có lỗi, không biết lỗi từ lệnh nào
3. **Race condition** - Docker chưa ready, code đã chạy → lỗi
4. **Log lộn xộn** - Output từ 2 process trộn lẫn, khó đọc

### ✅ CÁCH ĐÚNG

**Cách 1: Chạy lệnh một cái một cái**

```bash
# Terminal 1: Docker
cd /e/SUB_LUAN_VAN/luan_van
docker-compose down
docker-compose up -d
# Chờ 30 giây, thấy "Healthy" thì bấm Enter

# Terminal 2: Seed data
docker exec shopvn_backend python seed.py
# Chờ xong, thấy "✨ Seed dữ liệu hoàn tất!" thì bấm Enter

# Terminal 3: Frontend
cd frontend
npm run dev
# Chờ xong, thấy "ready in XXX ms" thì OK
```

**Cách 2: Mở Terminal khác nhau cho mỗi process**

```
Terminal 1 ┌─────────────────────┐
           │  docker-compose     │
           │  (chạy backend)     │
           └─────────────────────┘
                    ↓ (chờ ready)
           
Terminal 2 ┌─────────────────────┐
           │  python seed.py     │
           │  (tạo data)         │
           └─────────────────────┘
                    ↓ (chờ xong)

Terminal 3 ┌─────────────────────┐
           │  npm run dev        │
           │  (chạy frontend)    │
           └─────────────────────┘
```

---

## 🔄 RULE 2: CHẠY TUẦN TỰ, KHÔNG SONG SONG

### ❌ KHÔNG ĐƯỢC LÀM

Không mở Terminal 1 → hết chưa → vẫn mở Terminal 2

```bash
Terminal 1: docker-compose up -d (chưa chạy xong)
Terminal 2: python seed.py (vội chạy)
Terminal 3: npm run dev (chạy thêm)
→ CHAOS! Database chưa ready, code đã chạy
```

### ✅ CÁCH ĐÚNG

**Đợi cho mỗi bước hoàn tất mới sang bước tiếp theo:**

```
STEP 1: Docker
└─ docker-compose up -d
└─ Kiểm tra: docker ps (thấy 3 containers)
└─ HOÀN TẤT ✅

    ↓ (có được xác nhận từ người dùng hoặc log)

STEP 2: Seed
└─ docker exec shopvn_backend python seed.py
└─ Kiểm tra: (xem log cuối: "✨ Seed dữ liệu hoàn tất!")
└─ HOÀN TẤT ✅

    ↓

STEP 3: Frontend
└─ cd frontend && npm run dev
└─ Kiểm tra: http://localhost:5173 load được
└─ HOÀN TẤT ✅
```

---

## ⏱️ RULE 3: CÓ TIMEOUT CỰNG TỲ

### Quy tắc Timeout

| Bước | Lệnh | Timeout | Nếu quá thời gian |
|------|------|---------|------------------|
| 1 | `docker-compose up -d` | 1 phút | → Kiểm tra Docker, restart |
| 2 | `python seed.py` | 2 phút | → Kiểm tra database, xem logs |
| 3 | `npm run dev` | 1 phút | → Kiểm tra npm, clear node_modules |
| 4 | Login test | 30 giây | → Kiểm tra backend, restart |

### Cách Check

```bash
# Docker timeout?
docker ps
# Nếu container chưa running → restart

# Seed timeout?
docker logs shopvn_backend
# Xem error messages, kiểm tra database URL

# Frontend timeout?
npm list
# Check dependencies have error?

# API timeout?
curl http://localhost:8000/docs
# Nếu fail → backend died
```

---

## 🛑 RULE 4: CIRCUIT BREAKER (Xem 03_CIRCUIT_BREAKER.md)

### Khi Nào Dừng?

**Dừng ngay nếu:**
- [ ] Lỗi lặp lại 5 lần và chưa fix được
- [ ] Process "zombie" - chạy mãi không kết thúc
- [ ] CPU/Memory dùng quá cao (>80%)
- [ ] Database crashed, không connect được
- [ ] Server port bị stuck, không thể free up

### Cách Dừng An Toàn

```bash
# Dừng frontend
Ctrl + C (trong terminal chạy npm run dev)

# Dừng docker
docker-compose down

# Kill zombie process
ps aux | grep python  # tìm PID
kill -9 <PID>

# Clear ports
# Windows: netstat -ano | findstr :8000
# Mac/Linux: lsof -i :8000
```

---

## 📋 RULE 5: GHI LOG CHI TIẾT

### Format Log

```
[TIMESTAMP] [STEP] [STATUS] [MESSAGE]

Ví dụ:
[2026-06-03 10:30:45] [DOCKER_START] [PASS] Docker containers started
[2026-06-03 10:31:12] [SEED] [FAIL] Error: SQLSTATE[HY000]
[2026-06-03 10:32:00] [LOGIN] [PASS] customer1@example.com login OK
```

### Ghi Log Mỗi Khi:
- [ ] Bắt đầu bước mới → `[PASS]`
- [ ] Có lỗi → `[FAIL]` + chi tiết error
- [ ] Hoàn tất bước → `[DONE]`

### File Log

```bash
# Xem log
cat todo/logs/test.log

# Thêm vào log
echo "[TIMESTAMP] [STEP] [STATUS] MESSAGE" >> todo/logs/test.log

# Clear log
> todo/logs/test.log
```

---

## 🚨 RULE 6: ERROR HANDLING

### Khi Có Lỗi

**Step 1: GHI LOG**
```bash
echo "[$(date +%Y-%m-%d\ %H:%M:%S)] [STEP_NAME] [FAIL] Error message" >> todo/logs/test.log
```

**Step 2: KIỂM TRA**
```bash
# Xem logs chi tiết
docker logs shopvn_backend

# Hoặc
docker-compose logs -f backend
```

**Step 3: RETRY**
```bash
# Nếu lần đầu fail → retry lần 2
# Nếu lần 2 fail → retry lần 3
# ...
# Nếu lần 5 fail → DÙNG EXTENSION CLAUDE
```

**Step 4: GHI LỖI CUỐI CÙNG**
```bash
echo "[$(date +%Y-%m-%d\ %H:%M:%S)] [STEP_NAME] [ERROR_5] Final error after 5 attempts: <error>" >> todo/logs/test.log
```

---

## 🔗 RULE 7: EXTENSION INTEGRATION (Xem 05_EXTENSION_INTEGRATION.md)

### Khi Nào Dùng Extension?

**CHỈ dùng khi:**
- Lỗi xảy ra 5 lần liên tiếp
- Không biết fix thế nào
- Cần ai đó giúp (Claude hoặc Blackbox)

### Cách Dùng

1. Mở VSCode
2. Mở Claude extension (hoặc Blackbox)
3. Paste lỗi + log vào
4. Chờ câu trả lời
5. Thực hiện giải pháp đó
6. Retry test

---

## 📊 RULE PRIORITY (Mức ưu tiên)

```
Priority 1 (MUST):
  ✅ Chạy tuần tự, không song song
  ✅ Không dùng & operator
  ✅ Ghi log chi tiết
  ✅ Circuit breaker nếu cần

Priority 2 (SHOULD):
  ✅ Có timeout limit
  ✅ Check output sau mỗi step
  ✅ Dùng extension khi cần

Priority 3 (NICE):
  ✅ Tạo script automation
  ✅ Parallel testing (sau)
```

---

## ✅ CHECKLIST TRƯỚC KHI CHẠY

- [ ] Đọc kỹ 01_TEST_PROCEDURE.md
- [ ] Hiểu rules trong file này
- [ ] Chuẩn bị logs folder: `mkdir -p todo/logs`
- [ ] Xóa log cũ: `> todo/logs/test.log`
- [ ] Mở 3 terminals sẵn sàng
- [ ] Hiểu Circuit Breaker (03_CIRCUIT_BREAKER.md)
- [ ] Biết cách dùng Claude extension

---

**Created:** 2026-06-03
**Version:** 1.0
**Last Updated:** 2026-06-03

