#!/bin/bash

# File Manager & Terminal - Production Deployment Script
# This script sets up the application for production deployment

set -e

echo "================================================"
echo "File Manager & Terminal - Production Deployment"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root"
   exit 1
fi

# Check prerequisites
print_status "Checking prerequisites..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose (v2) is available
if ! docker compose version &> /dev/null; then
    print_error "Docker Compose (v2) is not available. Please install it or fix Docker setup."
    exit 1
fi

print_success "Prerequisites check passed"

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p uploads logs ssl
print_success "Directories created"

# Generate SSL certificates (self-signed for development)
if [ ! -f ssl/cert.pem ] || [ ! -f ssl/key.pem ]; then
    print_status "Generating SSL certificates..."
    openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
    print_success "SSL certificates generated"
else
    print_status "SSL certificates already exist"
fi

# Set proper permissions
print_status "Setting proper permissions..."
chmod 600 ssl/key.pem
chmod 644 ssl/cert.pem
chmod 755 uploads logs
print_success "Permissions set"

# Generate production secret key
if [ ! -f .env ]; then
    print_status "Creating environment file..."
    cat > .env << EOF
# Production Environment Variables
FLASK_CONFIG=production
SECRET_KEY=$(openssl rand -hex 32)
UPLOAD_FOLDER=/app/uploads
MAX_CONTENT_LENGTH=104857600
COMMAND_TIMEOUT=60
MONITORING_ENABLED=true
LOG_LEVEL=INFO
LOG_FILE=/app/logs/app.log
EOF
    print_success "Environment file created"
else
    print_warning "Environment file already exists"
fi

# Build and start the application
print_status "Building and starting the application..."
docker compose up -d --build

# Wait for application to start
print_status "Waiting for application to start..."
sleep 10

# Check if application is running
if curl -f http://localhost:5000/ > /dev/null 2>&1; then
    print_success "Application is running successfully!"
else
    print_error "Application failed to start. Check logs with: docker compose logs"
    exit 1
fi

# Display deployment information
echo ""
echo "================================================"
echo "Deployment Complete!"
echo "================================================"
echo ""
echo "Application URLs:"
echo "  HTTP:  http://localhost"
echo "  HTTPS: https://localhost"
echo ""
echo "Default credentials:"
echo "  Admin: admin / admin123"
echo "  User:  user / user123"
echo ""
echo "Useful commands:"
echo "  View logs:     docker compose logs -f"
echo "  Stop app:      docker compose down"
echo "  Restart app:   docker compose restart"
echo "  Update app:    ./deploy.sh"
echo ""
echo "Security notes:"
echo "  - Change default passwords immediately"
echo "  - Use proper SSL certificates for production"
echo "  - Configure firewall rules"
echo "  - Set up regular backups"
echo ""

print_success "Deployment completed successfully!" 