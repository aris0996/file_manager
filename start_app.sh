#!/bin/bash

echo "================================================"
echo "File Manager & Terminal - Enhanced Version"
echo "================================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

# Create necessary directories
mkdir -p uploads logs backups

echo
echo "================================================"
echo "Starting File Manager & Terminal..."
echo "================================================"
echo
echo "Application will be available at:"
echo "  http://localhost:5000"
echo "  http://127.0.0.1:5000"
echo
echo "Default credentials:"
echo "  Admin: admin / admin123"
echo "  User:  user / user123"
echo
echo "Press Ctrl+C to stop the server"
echo "================================================"
echo

# Start the application
python run_app.py --config development --host 0.0.0.0 --port 5000

echo
echo "Application stopped." 