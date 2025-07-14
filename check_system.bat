@echo off
title System Check - File Manager & Terminal

echo ================================================
echo File Manager & Terminal - System Check
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

REM Run system check
python check_system.py

echo.
echo System check completed.
pause 