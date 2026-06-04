@echo off
REM Check Docker and container status

echo.
echo ============================================================
echo        CHECKING DOCKER STATUS
echo ============================================================
echo.

echo 1. Docker version:
docker --version

echo.
echo 2. Docker running containers:
docker ps -a

echo.
echo 3. Backend container logs (last 100 lines):
echo.
docker logs -n 100 sub_shopvn_backend 2>&1

echo.
echo ============================================================
echo If containers are missing or logs show errors, we need to rebuild
echo ============================================================
echo.
pause
