@echo off
cd /d "%~dp0"
echo Starting Task Flight Recorder...
echo.
python -m tfr.cli start
echo.
pause
