#!/usr/bin/env python3
"""
Management script for File Manager & Terminal application
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_command(cmd, description):
    """Run a command with description"""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"{'='*50}")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 50)
    
    try:
        result = subprocess.run(cmd, check=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"❌ Command not found: {cmd[0]}")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    print("Checking dependencies...")
    
    required_packages = [
        'flask', 'flask_login', 'psutil', 'python-magic'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed")
    return True

def install_dependencies():
    """Install dependencies"""
    return run_command([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      "Installing dependencies")

def run_tests():
    """Run test suite"""
    return run_command([sys.executable, 'run_tests.py'], "Running test suite")

def run_app(env='development', host='0.0.0.0', port=5000, debug=False):
    """Run the application"""
    cmd = [sys.executable, 'run_app.py', '--config', env, '--host', host, '--port', str(port)]
    if debug:
        cmd.append('--debug')
    
    return run_command(cmd, f"Starting application ({env} mode)")

def run_system_monitor(interval=5):
    """Run system monitor"""
    cmd = [sys.executable, 'system_monitor.py', '--interval', str(interval)]
    return run_command(cmd, "Starting system monitor")

def create_backup():
    """Create backup"""
    return run_command([sys.executable, 'backup_restore.py', 'backup'], "Creating backup")

def list_backups():
    """List backups"""
    return run_command([sys.executable, 'backup_restore.py', 'list'], "Listing backups")

def build_executable():
    """Build executable"""
    return run_command([sys.executable, 'build_exe.py'], "Building executable")

def deploy_docker():
    """Deploy with Docker"""
    if not os.path.exists('deploy.sh'):
        print("❌ deploy.sh not found")
        return False
    
    # Make deploy script executable
    os.chmod('deploy.sh', 0o755)
    
    return run_command(['./deploy.sh'], "Deploying with Docker")

def clean_project():
    """Clean project files"""
    print("\nCleaning project...")
    
    # Files and directories to clean
    clean_items = [
        '__pycache__',
        '*.pyc',
        '*.pyo',
        '*.pyd',
        '.pytest_cache',
        'htmlcov',
        '.coverage',
        'build',
        'dist',
        '*.egg-info',
        'temp_restore',
        'logs/*.log'
    ]
    
    for item in clean_items:
        if '*' in item:
            # Handle wildcards
            import glob
            for file in glob.glob(item):
                try:
                    if os.path.isfile(file):
                        os.remove(file)
                    elif os.path.isdir(file):
                        import shutil
                        shutil.rmtree(file)
                except Exception as e:
                    print(f"Warning: Could not remove {file}: {e}")
        else:
            # Handle specific items
            if os.path.exists(item):
                try:
                    if os.path.isfile(item):
                        os.remove(item)
                    elif os.path.isdir(item):
                        import shutil
                        shutil.rmtree(item)
                except Exception as e:
                    print(f"Warning: Could not remove {item}: {e}")
    
    print("✅ Project cleaned")

def show_status():
    """Show project status"""
    print("\n" + "="*50)
    print("PROJECT STATUS")
    print("="*50)
    
    # Check if main files exist
    main_files = ['app.py', 'config.py', 'requirements.txt', 'README.md']
    for file in main_files:
        status = "✅" if os.path.exists(file) else "❌"
        print(f"{status} {file}")
    
    # Check if directories exist
    directories = ['templates', 'uploads', 'logs', 'backups']
    for directory in directories:
        status = "✅" if os.path.exists(directory) else "❌"
        print(f"{status} {directory}/")
    
    # Check dependencies
    print("\nDependencies:")
    check_dependencies()
    
    # Show file sizes
    print("\nFile sizes:")
    total_size = 0
    for root, dirs, files in os.walk('.'):
        if 'venv' in root or '__pycache__' in root or '.git' in root:
            continue
        for file in files:
            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path)
                total_size += size
                if size > 1024*1024:  # Show files larger than 1MB
                    print(f"  {file_path}: {size/(1024*1024):.1f}MB")
            except:
                pass
    
    print(f"Total project size: {total_size/(1024*1024):.1f}MB")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='File Manager & Terminal Management')
    parser.add_argument('command', choices=[
        'install', 'test', 'run', 'monitor', 'backup', 'backups', 
        'build', 'deploy', 'clean', 'status', 'help'
    ], help='Command to run')
    parser.add_argument('--env', choices=['development', 'production', 'testing'], 
                       default='development', help='Environment for run command')
    parser.add_argument('--host', default='0.0.0.0', help='Host for run command')
    parser.add_argument('--port', type=int, default=5000, help='Port for run command')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--interval', type=int, default=5, help='Monitor interval')
    
    args = parser.parse_args()
    
    if args.command == 'install':
        install_dependencies()
    
    elif args.command == 'test':
        if check_dependencies():
            run_tests()
    
    elif args.command == 'run':
        if check_dependencies():
            run_app(args.env, args.host, args.port, args.debug)
    
    elif args.command == 'monitor':
        if check_dependencies():
            run_system_monitor(args.interval)
    
    elif args.command == 'backup':
        if check_dependencies():
            create_backup()
    
    elif args.command == 'backups':
        if check_dependencies():
            list_backups()
    
    elif args.command == 'build':
        if check_dependencies():
            build_executable()
    
    elif args.command == 'deploy':
        deploy_docker()
    
    elif args.command == 'clean':
        clean_project()
    
    elif args.command == 'status':
        show_status()
    
    elif args.command == 'help':
        print("""
File Manager & Terminal - Management Commands

Commands:
  install    Install dependencies
  test       Run test suite
  run        Start the application
  monitor    Start system monitoring
  backup     Create backup
  backups    List available backups
  build      Build executable
  deploy     Deploy with Docker
  clean      Clean project files
  status     Show project status
  help       Show this help

Examples:
  python manage.py install
  python manage.py run --env production --port 8080
  python manage.py monitor --interval 10
  python manage.py backup
  python manage.py deploy

For more information, see README.md
        """)

if __name__ == '__main__':
    main() 