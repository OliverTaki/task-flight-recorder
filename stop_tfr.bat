@echo off
cd /d "%~dp0"
echo Stopping Task Flight Recorder...
echo.
python -m tfr.cli stop
echo.
pause
