#!/bin/bash

echo "Starting File Manager & Terminal..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

# Run the application
python3 run_app.py 