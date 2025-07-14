#!/usr/bin/env python3
"""
Restart File Manager & Terminal application with clean state
"""

import os
import sys
import subprocess
import time
import signal
import psutil

def find_flask_processes():
    """Find running Flask processes"""
    flask_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['cmdline']:
                cmdline = ' '.join(proc.info['cmdline'])
                if 'flask' in cmdline.lower() or 'python' in cmdline.lower() and 'app.py' in cmdline:
                    flask_processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return flask_processes

def kill_processes(processes):
    """Kill processes gracefully"""
    for proc in processes:
        try:
            print(f"Stopping process {proc.pid}...")
            proc.terminate()
            proc.wait(timeout=5)
            print(f"✅ Process {proc.pid} stopped")
        except psutil.TimeoutExpired:
            print(f"⚠️  Process {proc.pid} not responding, force killing...")
            proc.kill()
        except psutil.NoSuchProcess:
            print(f"⚠️  Process {proc.pid} already stopped")
        except Exception as e:
            print(f"❌ Error stopping process {proc.pid}: {e}")

def clean_session_files():
    """Clean session files"""
    session_files = [
        'flask_session',
        '.flask_session',
        'session',
        '.session'
    ]
    
    for session_file in session_files:
        if os.path.exists(session_file):
            try:
                if os.path.isdir(session_file):
                    import shutil
                    shutil.rmtree(session_file)
                else:
                    os.remove(session_file)
                print(f"✅ Cleaned {session_file}")
            except Exception as e:
                print(f"⚠️  Could not clean {session_file}: {e}")

def start_application():
    """Start the application"""
    print("\nStarting application...")
    
    # Check if app.py exists
    if not os.path.exists('app.py'):
        print("❌ app.py not found in current directory")
        return False
    
    try:
        # Start the application
        process = subprocess.Popen([
            sys.executable, 'app.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print(f"✅ Application started with PID: {process.pid}")
        
        # Wait a bit for the app to start
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Application is running")
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Application failed to start")
            print(f"STDOUT: {stdout.decode()}")
            print(f"STDERR: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        return False

def main():
    print("=" * 60)
    print("File Manager & Terminal - Application Restart")
    print("=" * 60)
    
    # Step 1: Find and stop existing processes
    print("\n1. Finding existing Flask processes...")
    flask_processes = find_flask_processes()
    
    if flask_processes:
        print(f"Found {len(flask_processes)} Flask processes:")
        for proc in flask_processes:
            print(f"  - PID {proc.pid}: {' '.join(proc.info['cmdline'])}")
        
        print("\n2. Stopping existing processes...")
        kill_processes(flask_processes)
    else:
        print("✅ No existing Flask processes found")
    
    # Step 3: Clean session files
    print("\n3. Cleaning session files...")
    clean_session_files()
    
    # Step 4: Wait a moment
    print("\n4. Waiting for cleanup...")
    time.sleep(2)
    
    # Step 5: Start application
    print("\n5. Starting application...")
    if start_application():
        print("\n" + "=" * 60)
        print("✅ Application restarted successfully!")
        print("=" * 60)
        print("\nAccess the application at:")
        print("  http://localhost:5000")
        print("\nDefault credentials:")
        print("  Admin: admin / admin123")
        print("  User:  user / user123")
        print("  Test:  test / test123")
        print("\nTo test login, run:")
        print("  python3 test_login.py")
    else:
        print("\n" + "=" * 60)
        print("❌ Failed to restart application")
        print("=" * 60)
        print("\nTroubleshooting:")
        print("1. Check if Python and dependencies are installed")
        print("2. Run: pip install -r requirements.txt")
        print("3. Check for errors in app.py")
        print("4. Try running manually: python3 app.py")

if __name__ == '__main__':
    main() 