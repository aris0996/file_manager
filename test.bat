@echo off
title File Manager & Terminal - Tests

echo Running tests...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

REM Run tests
python run_tests.py

pause 