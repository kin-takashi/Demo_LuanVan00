@echo off
cd E:\SUB_LUAN_VAN\luan_van

echo === Step 1: Stop Docker containers ===
docker-compose -f docker-compose.optimized.yml down

echo.
echo === Step 2: Remove old database volume ===
for /f "tokens=*" %%i in ('docker volume ls -q --filter name=luan_van') do docker volume rm %%i

echo.
echo === Step 3: Start Docker containers ===
docker-compose -f docker-compose.optimized.yml up -d

echo.
echo === Waiting for database to be ready (30 seconds) ===
timeout /t 30

echo.
echo === Step 4: Initialize database ===
cd backend
python init_db.py

echo.
echo === Step 5: Seed minimal accounts ===
python seed_minimal.py

echo.
echo === DONE! ===
pause
