@echo off
title File Manager & Terminal

echo Starting File Manager & Terminal...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

REM Run the application
python run_app.py

pause 