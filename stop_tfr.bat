@echo off
echo Stopping Task Flight Recorder...
for /f "tokens=2" %%a in ('tasklist ^| findstr python') do (
    taskkill /PID %%a /F >nul 2>&1
)
echo Done.
