@echo off
REM Rebuild Docker with the fixed requirements.txt

cd /d E:\SUB_LUAN_VAN\luan_van

echo.
echo ============================================================
echo        REBUILDING DOCKER BACKEND
echo ============================================================
echo.

REM Stop the old container
docker-compose -f docker-compose.optimized.yml down

REM Rebuild and start
docker-compose -f docker-compose.optimized.yml up -d --build

echo.
echo Waiting 30 seconds for container to start...
timeout /t 30

echo.
echo ============================================================
echo        CHECKING BACKEND STATUS
echo ============================================================
echo.

docker ps --filter "name=sub_shopvn_backend"

echo.
echo ============================================================
echo Done! Check if backend is (healthy) now
echo ============================================================
echo.
pause
