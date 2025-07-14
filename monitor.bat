@echo off
title File Manager & Terminal - System Monitor

echo Starting System Monitor...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

REM Run system monitor
python system_monitor.py

pause 