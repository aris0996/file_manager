#!/usr/bin/env python3
"""
File Manager & Terminal Web Application
Startup script for easy launching
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import flask
        import flask_login
        print("✓ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def create_upload_folder():
    """Create upload folder if it doesn't exist"""
    upload_folder = "uploads"
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
        print(f"✓ Created upload folder: {upload_folder}")
    else:
        print(f"✓ Upload folder exists: {upload_folder}")

def main():
    """Main startup function"""
    print("=" * 50)
    print("File Manager & Terminal Web Application")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Create upload folder
    create_upload_folder()
    
    print("\nStarting application...")
    print("Access the application at: http://localhost:5000")
    print("Default credentials: admin / admin123")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Import and run the Flask app
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except Exception as e:
        print(f"\nError starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 