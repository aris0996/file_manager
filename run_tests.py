#!/usr/bin/env python3
"""
Test runner for File Manager & Terminal application
"""

import sys
import os
import subprocess
import unittest
from test_app import run_tests

def main():
    """Main test runner"""
    print("=" * 50)
    print("File Manager & Terminal - Test Suite")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("Error: app.py not found. Please run from the project root directory.")
        sys.exit(1)
    
    # Check if dependencies are installed
    try:
        import flask
        import flask_login
        import psutil
        import magic
    except ImportError as e:
        print(f"Error: Missing dependency - {e}")
        print("Please install dependencies: pip install -r requirements.txt")
        sys.exit(1)
    
    print("Running tests...")
    print("-" * 50)
    
    # Run the test suite
    exit_code = run_tests()
    
    print("-" * 50)
    if exit_code == 0:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
    
    return exit_code

if __name__ == '__main__':
    sys.exit(main()) 