#!/bin/bash

echo "================================================"
echo "File Manager & Terminal - System Check"
echo "================================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

# Run system check
python3 check_system.py

echo
echo "System check completed." 