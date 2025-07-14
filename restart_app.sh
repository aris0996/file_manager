#!/bin/bash

echo "================================================"
echo "File Manager & Terminal - Application Restart"
echo "================================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

# Kill existing Python processes running app.py
echo "Stopping existing Flask processes..."
pkill -f "python.*app.py" 2>/dev/null || true
pkill -f "flask" 2>/dev/null || true

# Clean session files
echo "Cleaning session files..."
rm -rf flask_session .flask_session session .session 2>/dev/null || true

# Wait a moment
echo "Waiting for cleanup..."
sleep 2

# Start the application
echo "Starting application..."
nohup python3 app.py > app.log 2>&1 &
APP_PID=$!

# Wait for app to start
sleep 3

# Check if app is running
if kill -0 $APP_PID 2>/dev/null; then
    echo
    echo "================================================"
    echo "✅ Application restarted successfully!"
    echo "================================================"
    echo
    echo "Access the application at:"
    echo "  http://localhost:5000"
    echo
    echo "Default credentials:"
    echo "  Admin: admin / admin123"
    echo "  User:  user / user123"
    echo "  Test:  test / test123"
    echo
    echo "To test login, run:"
    echo "  python3 test_login.py"
    echo
    echo "To view logs:"
    echo "  tail -f app.log"
    echo
    echo "To stop the application:"
    echo "  kill $APP_PID"
else
    echo
    echo "================================================"
    echo "❌ Failed to restart application"
    echo "================================================"
    echo
    echo "Check the logs:"
    echo "  cat app.log"
    echo
    echo "Troubleshooting:"
    echo "1. Check if Python and dependencies are installed"
    echo "2. Run: pip3 install -r requirements.txt"
    echo "3. Check for errors in app.py"
    echo "4. Try running manually: python3 app.py"
fi 