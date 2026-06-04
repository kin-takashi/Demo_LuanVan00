@echo off
REM Force rebuild Docker - remove old images first

cd /d E:\SUB_LUAN_VAN\luan_van

echo.
echo ============================================================
echo        FORCE REBUILD - REMOVE OLD IMAGES
echo ============================================================
echo.

REM Stop containers
echo Stopping containers...
docker-compose -f docker-compose.optimized.yml down

REM Remove old backend image
echo Removing old backend image...
docker rmi luan_van-backend -f 2>nul
docker image prune -f

echo.
echo ============================================================
echo        REBUILDING WITH FRESH IMAGE
echo ============================================================
echo.

REM Rebuild with --no-cache to ensure fresh build
docker-compose -f docker-compose.optimized.yml up -d --build --no-cache

echo.
echo Waiting 40 seconds for containers to start...
timeout /t 40

echo.
echo ============================================================
echo        STATUS CHECK
echo ============================================================
echo.

docker ps

echo.
echo ============================================================
echo Check backend status (should be healthy)
echo ============================================================
echo.
pause
