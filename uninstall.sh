#!/bin/bash

echo "================================================"
echo "File Manager & Terminal - Complete Uninstall"
echo "================================================"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to confirm action
confirm_action() {
    local message="$1"
    echo -e "${YELLOW}$message${NC}"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        return 0
    else
        return 1
    fi
}

# Step 1: Stop and remove Docker containers
print_status "Step 1: Stopping and removing Docker containers..."

if command -v docker &> /dev/null; then
    # Stop all containers
    print_status "Stopping all containers..."
    docker stop $(docker ps -aq) 2>/dev/null || true
    
    # Remove all containers
    print_status "Removing all containers..."
    docker rm $(docker ps -aq) 2>/dev/null || true
    
    # Remove all images
    print_status "Removing all images..."
    docker rmi $(docker images -q) 2>/dev/null || true
    
    # Remove all volumes
    print_status "Removing all volumes..."
    docker volume rm $(docker volume ls -q) 2>/dev/null || true
    
    # Remove all networks
    print_status "Removing all networks..."
    docker network rm $(docker network ls -q) 2>/dev/null || true
    
    # Prune everything
    print_status "Pruning Docker system..."
    docker system prune -af --volumes
    
    print_success "Docker containers, images, and volumes removed"
else
    print_warning "Docker not found, skipping Docker cleanup"
fi

# Step 2: Stop Python processes
print_status "Step 2: Stopping Python processes..."

# Kill Python processes running our app
pkill -f "python.*app.py" 2>/dev/null || true
pkill -f "flask" 2>/dev/null || true
pkill -f "run_app.py" 2>/dev/null || true

print_success "Python processes stopped"

# Step 3: Remove application files
print_status "Step 3: Removing application files..."

# List of files and directories to remove
files_to_remove=(
    "app.py"
    "config.py"
    "run_app.py"
    "wsgi.py"
    "requirements.txt"
    "Dockerfile"
    "docker-compose.yml"
    "nginx.conf"
    "deploy.sh"
    "quick_start.sh"
    "quick_start.bat"
    "start_app.sh"
    "start_app.bat"
    "check_system.py"
    "check_system.sh"
    "check_system.bat"
    "run.sh"
    "run.bat"
    "test.sh"
    "test.bat"
    "monitor.sh"
    "monitor.bat"
    "restart_app.py"
    "restart_app.sh"
    "restart_app.bat"
    "fix_login.py"
    "test_login.py"
    "reset_users.py"
    "system_monitor.py"
    "backup_restore.py"
    "manage.py"
    "build_exe.py"
    "run_tests.py"
    "test_app.py"
    "README.md"
    "QUICK_START.md"
    "TROUBLESHOOTING.md"
    "LICENSE"
    ".env"
    ".gitignore"
)

dirs_to_remove=(
    "templates"
    "static"
    "uploads"
    "logs"
    "backups"
    "ssl"
    "venv"
    "build"
    "dist"
    "__pycache__"
    "*.pyc"
    "flask_session"
    ".flask_session"
    "session"
    ".session"
)

# Remove files
for file in "${files_to_remove[@]}"; do
    if [ -f "$file" ]; then
        rm -f "$file"
        print_success "Removed file: $file"
    fi
done

# Remove directories
for dir in "${dirs_to_remove[@]}"; do
    if [ -d "$dir" ]; then
        rm -rf "$dir"
        print_success "Removed directory: $dir"
    fi
done

# Remove Python cache files
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

print_success "Application files removed"

# Step 4: Uninstall Python dependencies
print_status "Step 4: Uninstalling Python dependencies..."

if [ -d "venv" ]; then
    print_status "Removing virtual environment..."
    rm -rf venv
    print_success "Virtual environment removed"
fi

# Uninstall packages if they were installed globally
if command -v pip3 &> /dev/null; then
    print_status "Uninstalling Flask and related packages..."
    pip3 uninstall -y flask flask-login werkzeug jinja2 psutil python-magic 2>/dev/null || true
    print_success "Python packages uninstalled"
fi

# Step 5: Remove Docker (optional)
if confirm_action "Do you want to completely uninstall Docker from your system?"; then
    print_status "Step 5: Uninstalling Docker..."
    
    # Detect OS and uninstall Docker
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        print_status "Uninstalling Docker on Linux..."
        
        # Stop Docker service
        sudo systemctl stop docker
        sudo systemctl stop docker.socket
        
        # Remove Docker packages
        if command -v apt-get &> /dev/null; then
            # Ubuntu/Debian
            sudo apt-get purge -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
            sudo apt-get autoremove -y
        elif command -v yum &> /dev/null; then
            # CentOS/RHEL
            sudo yum remove -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
        elif command -v dnf &> /dev/null; then
            # Fedora
            sudo dnf remove -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
        fi
        
        # Remove Docker data
        sudo rm -rf /var/lib/docker
        sudo rm -rf /etc/docker
        sudo rm -rf ~/.docker
        
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        print_status "Uninstalling Docker Desktop on macOS..."
        
        # Stop Docker Desktop
        osascript -e 'quit app "Docker Desktop"' 2>/dev/null || true
        
        # Remove Docker Desktop
        sudo rm -rf /Applications/Docker.app
        sudo rm -rf ~/Library/Group\ Containers/group.com.docker
        sudo rm -rf ~/Library/Containers/com.docker.docker
        sudo rm -rf ~/.docker
        
    else
        print_warning "Automatic Docker uninstall not supported for this OS"
        print_status "Please uninstall Docker manually from your system"
    fi
    
    print_success "Docker uninstalled"
else
    print_status "Skipping Docker uninstall"
fi

# Step 6: Clean system
print_status "Step 6: Cleaning system..."

# Remove any remaining files
rm -f app.log 2>/dev/null || true
rm -f *.log 2>/dev/null || true
rm -f .env* 2>/dev/null || true

# Clean temporary files
rm -rf /tmp/file-manager-* 2>/dev/null || true

print_success "System cleaned"

# Final summary
echo
echo "================================================"
echo "UNINSTALL COMPLETE"
echo "================================================"
echo
print_success "File Manager & Terminal has been completely removed!"
echo
echo "What was removed:"
echo "✅ Docker containers, images, and volumes"
echo "✅ Python processes"
echo "✅ Application files and directories"
echo "✅ Python dependencies"
echo "✅ Virtual environment"
echo "✅ System cache and temporary files"
echo
if confirm_action "Do you want to uninstall Docker completely?"; then
    echo "✅ Docker (if confirmed above)"
fi
echo
echo "If you want to reinstall later:"
echo "1. Clone the repository again"
echo "2. Run: ./deploy.sh (for Docker)"
echo "3. Or run: ./quick_start.sh (for Python)"
echo
print_success "Uninstall completed successfully!" 