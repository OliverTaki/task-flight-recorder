@echo off
cd /d "%~dp0"

echo ========================================
echo Task Flight Recorder Status
echo ========================================
echo.

python -m tfr.cli status

echo.
echo Exit code: %ERRORLEVEL%
echo.

pause
