@echo off
echo Checking Task Flight Recorder status...
tasklist | findstr python
if %errorlevel%==0 (
    echo Python process found.
) else (
    echo Not running.
)

if exist tfr.db (
    echo.
    echo DB status:
    for %%I in (tfr.db) do echo Last modified: %%~tI
) else (
    echo No DB file found.
)
