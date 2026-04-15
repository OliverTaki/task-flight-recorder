@echo off
setlocal
cd /d "%~dp0"
start "Task Flight Recorder" /min cmd /c python main_v3.py
echo Task Flight Recorder started.
echo Use status_tfr.bat to check status.
echo Use stop_tfr.bat to stop it.
endlocal
