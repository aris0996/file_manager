#!/usr/bin/env python3
"""
System Check for File Manager & Terminal application
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 7:
        print("✅ Python version is compatible")
        return True
    else:
        print("❌ Python 3.7+ is required")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\nChecking dependencies...")
    
    dependencies = [
        ('flask', 'Flask'),
        ('flask_login', 'Flask-Login'),
        ('psutil', 'psutil'),
        ('magic', 'python-magic'),
        ('werkzeug', 'Werkzeug'),
        ('jinja2', 'Jinja2')
    ]
    
    all_installed = True
    for package, name in dependencies:
        try:
            __import__(package)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} - Not installed")
            all_installed = False
    
    return all_installed

def check_docker():
    """Check Docker installation"""
    print("\nChecking Docker...")
    
    try:
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Docker: {result.stdout.strip()}")
            
            # Check Docker Compose v2
            try:
                result = subprocess.run(['docker', 'compose', 'version'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"✅ Docker Compose v2: {result.stdout.strip()}")
                    return True
                else:
                    print("❌ Docker Compose v2 not available")
                    return False
            except:
                print("❌ Docker Compose v2 not available")
                return False
        else:
            print("❌ Docker not installed")
            return False
    except:
        print("❌ Docker not installed")
        return False

def check_system_info():
    """Check system information"""
    print("\nSystem Information:")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Processor: {platform.processor()}")
    
    # Check available memory
    try:
        import psutil
        memory = psutil.virtual_memory()
        print(f"Memory: {memory.total / (1024**3):.1f} GB total, {memory.available / (1024**3):.1f} GB available")
    except:
        print("Memory: Unable to determine")

def check_project_files():
    """Check if project files exist"""
    print("\nChecking project files...")
    
    required_files = [
        'app.py',
        'config.py',
        'requirements.txt',
        'README.md',
        'run_app.py'
    ]
    
    required_dirs = [
        'templates',
        'uploads',
        'logs',
        'backups'
    ]
    
    all_exist = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - Missing")
            all_exist = False
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✅ {directory}/")
        else:
            print(f"⚠️  {directory}/ - Will be created automatically")
    
    return all_exist

def check_ports():
    """Check if required ports are available"""
    print("\nChecking ports...")
    
    import socket
    
    ports_to_check = [5000, 80, 443]
    
    for port in ports_to_check:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            result = sock.connect_ex(('localhost', port))
            if result == 0:
                print(f"⚠️  Port {port} is in use")
            else:
                print(f"✅ Port {port} is available")
        except:
            print(f"❌ Unable to check port {port}")
        finally:
            sock.close()

def check_permissions():
    """Check file permissions"""
    print("\nChecking permissions...")
    
    # Check if we can write to current directory
    try:
        test_file = Path("test_permission.tmp")
        test_file.write_text("test")
        test_file.unlink()
        print("✅ Write permission to current directory")
    except Exception as e:
        print(f"❌ No write permission to current directory: {e}")

def main():
    """Main function"""
    print("=" * 60)
    print("File Manager & Terminal - System Check")
    print("=" * 60)
    
    all_good = True
    
    # Check Python version
    if not check_python_version():
        all_good = False
    
    # Check dependencies
    if not check_dependencies():
        all_good = False
    
    # Check Docker
    docker_available = check_docker()
    
    # Check system info
    check_system_info()
    
    # Check project files
    if not check_project_files():
        all_good = False
    
    # Check ports
    check_ports()
    
    # Check permissions
    check_permissions()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if all_good:
        print("✅ System check passed! You can run the application.")
        print("\nRecommended next steps:")
        print("1. For development: python run_app.py")
        print("2. For production: ./deploy.sh")
        print("3. For testing: python manage.py test")
    else:
        print("❌ System check failed! Please fix the issues above.")
        print("\nCommon solutions:")
        print("1. Install missing dependencies: pip install -r requirements.txt")
        print("2. Install Docker Desktop for containerized deployment")
        print("3. Check file permissions and Python version")
    
    if docker_available:
        print("\n🐳 Docker is available - you can use containerized deployment")
    else:
        print("\n🐍 Docker not available - use Python native deployment")
    
    print("=" * 60)

if __name__ == '__main__':
    main() 