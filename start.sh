#!/bin/bash

echo "================================================"
echo "File Manager & Terminal Web Application"
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

# Create uploads folder
if [ ! -d "uploads" ]; then
    echo "Creating uploads folder..."
    mkdir uploads
fi

# Start the application
echo
echo "Starting application..."
echo "Access the application at: http://localhost:5000"
echo "Default credentials: admin / admin123"
echo "Press Ctrl+C to stop the server"
echo
python run.py 