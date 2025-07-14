@echo off
title File Manager & Terminal - Restart Application

echo ================================================
echo File Manager & Terminal - Application Restart
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

REM Kill existing Python processes running app.py
echo Stopping existing Flask processes...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im python3.exe >nul 2>&1

REM Clean session files
echo Cleaning session files...
if exist flask_session rmdir /s /q flask_session
if exist .flask_session rmdir /s /q .flask_session
if exist session del /q session
if exist .session del /q .session

REM Wait a moment
echo Waiting for cleanup...
timeout /t 2 /nobreak >nul

REM Start the application
echo Starting application...
start "File Manager & Terminal" python app.py

REM Wait for app to start
timeout /t 3 /nobreak >nul

echo.
echo ================================================
echo Application restarted successfully!
echo ================================================
echo.
echo Access the application at:
echo   http://localhost:5000
echo.
echo Default credentials:
echo   Admin: admin / admin123
echo   User:  user / user123
echo   Test:  test / test123
echo.
echo To test login, run:
echo   python test_login.py
echo.

pause 