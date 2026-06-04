@echo off
REM Double-click this file to reset Docker and reseed database
REM This will rebuild Docker containers and create 4 test accounts

cd /d E:\SUB_LUAN_VAN\luan_van

echo.
echo ============================================================
echo         REBUILD DOCKER & RESEED DATABASE
echo ============================================================
echo.
echo STEP 1: Stopping Docker containers...
echo ============================================================
docker-compose -f docker-compose.optimized.yml down

echo.
echo ============================================================
echo STEP 2: Removing old database volume...
echo ============================================================
echo Searching for luan_van volumes...
for /f "tokens=*" %%i in ('docker volume ls -q') do (
  echo %%i | findstr /i luan_van >nul && (
    echo Removing: %%i
    docker volume rm %%i 2>nul
  )
)

echo.
echo ============================================================
echo STEP 3: Starting Docker containers (building images)...
echo ============================================================
docker-compose -f docker-compose.optimized.yml up -d --build

echo.
echo Waiting 45 seconds for containers to fully initialize...
timeout /t 45

echo.
echo ============================================================
echo STEP 4: Creating database tables...
echo ============================================================
cd /d E:\SUB_LUAN_VAN\luan_van\backend
python init_db.py

echo.
echo ============================================================
echo STEP 5: Seeding 4 test accounts (Quick seed)...
echo ============================================================
python seed_minimal.py

echo.
echo ============================================================
echo     DONE! Ready to test! =================
echo ============================================================
echo.
echo TEST ACCOUNTS (4 roles):
echo   1. CUSTOMER:   customer1@example.com / Customer@123
echo   2. SHOP_OWNER: owner1@shop.com / Owner@123
echo   3. SHIPPER:    shipper1@example.com / Shipper@123
echo   4. ADMIN:      admin@example.com / Admin@123
echo.
echo Access Frontend:
echo   http://localhost:3000    (if npm not running)
echo   http://localhost:3001    (if npm using alternate port)
echo   http://localhost:5173    (if npm run dev)
echo.
echo Backend API Docs:
echo   http://localhost:8000/docs
echo.
pause
