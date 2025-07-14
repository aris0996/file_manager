#!/usr/bin/env python3
"""
Build executable for File Manager & Terminal application
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def main():
    """Build executable"""
    print("=" * 50)
    print("File Manager & Terminal - Build Executable")
    print("=" * 50)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Create build directory
    build_dir = Path("build")
    dist_dir = Path("dist")
    
    if build_dir.exists():
        shutil.rmtree(build_dir)
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    
    print("Building executable...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=FileManagerTerminal",
        "--add-data=templates;templates",
        "--add-data=uploads;uploads",
        "--hidden-import=flask",
        "--hidden-import=flask_login",
        "--hidden-import=psutil",
        "--hidden-import=magic",
        "--hidden-import=werkzeug",
        "--hidden-import=jinja2",
        "run_app.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✅ Build completed successfully!")
        print(f"Executable location: {dist_dir / 'FileManagerTerminal.exe'}")
        
        # Create a simple launcher script
        launcher_content = '''@echo off
echo Starting File Manager & Terminal...
FileManagerTerminal.exe
pause
'''
        
        with open(dist_dir / "start.bat", "w") as f:
            f.write(launcher_content)
        
        print("✅ Launcher script created: start.bat")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main()) 