@echo off
REM Check what's wrong with the backend container

echo.
echo ============================================================
echo        CHECKING BACKEND LOGS
echo ============================================================
echo.

REM Get the backend container ID and show its logs
docker logs -n 100 sub_shopvn_backend

echo.
echo ============================================================
echo If you see errors above, please share them with me!
echo ============================================================
echo.
pause
