@echo off
title File Manager & Terminal - Quick Start

echo ================================================
echo File Manager & Terminal - Quick Start
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

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create necessary directories
if not exist "uploads" mkdir uploads
if not exist "logs" mkdir logs
if not exist "backups" mkdir backups

echo.
echo ================================================
echo Starting File Manager & Terminal...
echo ================================================
echo.
echo Application will be available at:
echo   http://localhost:5000
echo   http://127.0.0.1:5000
echo.
echo Default credentials:
echo   Admin: admin / admin123
echo   User:  user / user123
echo.
echo Press Ctrl+C to stop the server
echo ================================================
echo.

REM Start the application
python run_app.py --config development --host 0.0.0.0 --port 5000

echo.
echo Application stopped.
pause 