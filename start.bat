@echo off
echo ================================================
echo File Manager & Terminal Web Application
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

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

REM Create uploads folder
if not exist "uploads" (
    echo Creating uploads folder...
    mkdir uploads
)

REM Start the application
echo.
echo Starting application...
echo Access the application at: http://localhost:5000
echo Default credentials: admin / admin123
echo Press Ctrl+C to stop the server
echo.
python run.py

pause 