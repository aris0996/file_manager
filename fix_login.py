#!/usr/bin/env python3
"""
Auto-fix login issues for File Manager & Terminal
"""

import os
import sys
import subprocess
import time
import hashlib
import requests
import json

def print_step(step, message):
    """Print step with formatting"""
    print(f"\n{'='*60}")
    print(f"STEP {step}: {message}")
    print(f"{'='*60}")

def run_command(command, description):
    """Run command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ {description} - Success")
            return True
        else:
            print(f"❌ {description} - Failed")
            print(f"Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} - Timeout")
        return False
    except Exception as e:
        print(f"❌ {description} - Error: {e}")
        return False

def check_app_running():
    """Check if application is running"""
    try:
        response = requests.get("http://localhost:5000/login", timeout=5)
        return response.status_code == 200
    except:
        return False

def test_login(username, password):
    """Test login functionality"""
    try:
        session = requests.Session()
        login_data = {'username': username, 'password': password}
        response = session.post("http://localhost:5000/login", data=login_data, allow_redirects=False)
        return response.status_code == 302
    except:
        return False

def main():
    print("=" * 60)
    print("File Manager & Terminal - Auto Login Fix")
    print("=" * 60)
    
    # Step 1: Check system
    print_step(1, "Checking System")
    
    # Check Python
    if not run_command("python3 --version", "Checking Python version"):
        print("❌ Python 3 is required")
        return False
    
    # Check dependencies
    if not run_command("pip3 list | grep -E '(flask|werkzeug)'", "Checking Flask dependencies"):
        print("⚠️  Flask dependencies may not be installed")
    
    # Step 2: Stop existing processes
    print_step(2, "Stopping Existing Processes")
    
    # Kill Python processes
    run_command("pkill -f 'python.*app.py'", "Stopping Python app processes")
    run_command("pkill -f flask", "Stopping Flask processes")
    
    # Wait for processes to stop
    time.sleep(3)
    
    # Step 3: Clean session files
    print_step(3, "Cleaning Session Files")
    
    session_files = ['flask_session', '.flask_session', 'session', '.session']
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
    
    # Step 4: Verify user credentials
    print_step(4, "Verifying User Credentials")
    
    # Expected hashes
    expected_hashes = {
        'admin': '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9',
        'user': 'e606e38b0d8c19b24cf0ee3808183162ea7cd63ff7912dbb22b5e803286b4446',
        'test': 'ecd71870d1963316a97e3ac3408c9835ad8cf0f3c1bc703527c30265534f75ae'
    }
    
    test_credentials = [
        ('admin', 'admin123'),
        ('user', 'user123'),
        ('test', 'test123')
    ]
    
    for username, password in test_credentials:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if username in expected_hashes and password_hash == expected_hashes[username]:
            print(f"✅ {username} / {password} - Hash matches")
        else:
            print(f"❌ {username} / {password} - Hash mismatch")
    
    # Step 5: Start application
    print_step(5, "Starting Application")
    
    if not os.path.exists('app.py'):
        print("❌ app.py not found in current directory")
        return False
    
    # Start application in background
    try:
        process = subprocess.Popen([
            sys.executable, 'app.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print(f"✅ Application started with PID: {process.pid}")
        
        # Wait for app to start
        print("Waiting for application to start...")
        for i in range(10):
            time.sleep(1)
            if check_app_running():
                print("✅ Application is running and accessible")
                break
        else:
            print("❌ Application failed to start or is not accessible")
            return False
            
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        return False
    
    # Step 6: Test login
    print_step(6, "Testing Login")
    
    successful_logins = 0
    for username, password in test_credentials:
        if test_login(username, password):
            print(f"✅ Login successful: {username} / {password}")
            successful_logins += 1
        else:
            print(f"❌ Login failed: {username} / {password}")
    
    # Step 7: Summary
    print_step(7, "Summary")
    
    if successful_logins >= 2:  # At least admin and user should work
        print("✅ Login system is working correctly!")
        print("\nAccess the application at:")
        print("  http://localhost:5000")
        print("\nWorking credentials:")
        for username, password in test_credentials:
            if test_login(username, password):
                print(f"  {username} / {password}")
        
        print("\n🎉 Login issues have been resolved!")
        return True
    else:
        print("❌ Login system still has issues")
        print("\nTroubleshooting steps:")
        print("1. Check application logs")
        print("2. Verify app.py configuration")
        print("3. Check browser cache")
        print("4. Try different browser")
        return False

if __name__ == '__main__':
    try:
        success = main()
        if success:
            print("\n" + "="*60)
            print("✅ Auto-fix completed successfully!")
            print("="*60)
        else:
            print("\n" + "="*60)
            print("❌ Auto-fix failed. Check manual troubleshooting.")
            print("="*60)
    except KeyboardInterrupt:
        print("\n\n⚠️  Auto-fix interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Auto-fix error: {e}")
    
    print("\nFor manual troubleshooting, see TROUBLESHOOTING.md") 