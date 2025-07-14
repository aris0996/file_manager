# File Manager & Terminal Web Application

A modern Flask-based web application for file and folder management with an integrated Linux terminal interface.

## 🚀 **Enhanced Features**

### 📁 **Advanced File Manager**
- **Modern web interface** with Bootstrap 5 and custom styling
- **Browse files and folders** with breadcrumb navigation
- **Search functionality** - Find files and folders instantly
- **Sorting options** - Sort by name, size, modified date, or file type
- **Multiple file selection** - Select and operate on multiple files at once
- **File preview** - Preview text files, images, and binary files
- **Create new folders** with modal dialogs
- **Upload files** with drag-and-drop support and progress tracking
- **Download files** directly from browser
- **Rename files/folders** inline with validation
- **Delete items** with confirmation and bulk operations
- **Compress folders** into ZIP archives
- **File information** (size, permissions, modification date, MIME type)
- **System information** - View CPU, memory, and disk usage
- **Statistics dashboard** - Real-time file and folder statistics

### 💻 **Enhanced Terminal Interface**
- **Interactive Linux terminal** accessible via web browser
- **Command auto-completion** with Tab key support
- **Command suggestions** - Smart suggestions as you type
- **Quick command buttons** for common operations
- **Command history** with easy re-execution and export
- **System monitoring** - Real-time CPU, memory, disk usage
- **File operations shortcuts** - Search, grep, and find by size
- **Keyboard shortcuts** for power users
- **Copy to clipboard** functionality
- **Enhanced security** with improved command filtering
- **Real-time command execution** with output display

### 🔐 **Enhanced Security Features**
- **User authentication** with role-based access
- **Advanced command filtering** - Prevents dangerous operations
- **Command timeout** protection (60 seconds)
- **Session management** with Flask-Login
- **File type validation** - Only allowed file types can be uploaded
- **System directory protection** - Prevents deletion of critical directories
- **Input validation** - Sanitizes all user inputs

### 🎨 **UI/UX Improvements**
- **Responsive design** - Works perfectly on all devices
- **Dark terminal theme** - Professional terminal appearance
- **Progress indicators** - Upload progress and system monitoring
- **Toast notifications** - User-friendly feedback messages
- **Keyboard shortcuts** - Power user productivity features
- **Modern animations** - Smooth transitions and hover effects
- **Accessibility features** - Screen reader friendly

## 📋 **New Features Added**

### File Manager Enhancements:
- ✅ **Search and Filter** - Find files by name with real-time filtering
- ✅ **Advanced Sorting** - Sort by name, size, date, or file type
- ✅ **Multiple Selection** - Select multiple files for bulk operations
- ✅ **File Preview** - Preview text files, images, and binary files
- ✅ **Statistics Dashboard** - Real-time file and folder statistics
- ✅ **System Information** - CPU, memory, and disk usage monitoring
- ✅ **Upload Progress** - Visual progress bar for file uploads
- ✅ **File Type Validation** - Enhanced security with allowed file types
- ✅ **Bulk Operations** - Delete or compress multiple files at once

### Terminal Enhancements:
- ✅ **Command Auto-completion** - Tab key support for command completion
- ✅ **Smart Suggestions** - Context-aware command suggestions
- ✅ **System Monitoring** - Real-time system resource monitoring
- ✅ **File Operations** - Quick search, grep, and find operations
- ✅ **Command History Export** - Export command history to file
- ✅ **Copy to Clipboard** - Easy command copying functionality
- ✅ **Enhanced Security** - Improved command filtering patterns
- ✅ **Current Directory Display** - Shows current working directory

## 🛠️ **Installation & Quick Start**

### **Option 1: Quick Start (Recommended)**

#### **Windows:**
```cmd
# Double click file
quick_start.bat

# Atau jalankan di Command Prompt
start_app.bat
```

#### **Linux/Mac:**
```bash
# Berikan permission execute
chmod +x quick_start.sh start_app.sh

# Jalankan
./quick_start.sh
# Atau
./start_app.sh
```

### **Option 2: Docker Deployment (Production)**

#### **Prerequisites:**
- Docker Desktop terinstall
- Docker Compose v2 tersedia

#### **Setup:**
```bash
# Jalankan deployment script
chmod +x deploy.sh
./deploy.sh
```

### **Option 3: Manual Setup**

#### **Prerequisites:**
- Python 3.7 or higher
- pip (Python package installer)

#### **Setup Instructions:**

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd file-manager-terminal
   ```

2. **Check system compatibility**
   ```bash
   # Windows
   check_system.bat
   
   # Linux/Mac
   chmod +x check_system.sh
   ./check_system.sh
   ```

3. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   # Development mode
   python run_app.py
   
   # Production mode
   python run_app.py --config production --port 8080
   
   # Using management script
   python manage.py run
   ```

6. **Access the application**
   - Open your web browser
   - Navigate to `http://localhost:5000`
   - Login with default credentials:
     - Username: `admin` / Password: `admin123`
     - Username: `user` / Password: `user123`

## 🎯 **Usage Guide**

### File Manager Features:

#### **Navigation & Search**
- **Breadcrumb Navigation**: Click on folder names to navigate
- **Search**: Use the search bar to find files and folders instantly
- **Sorting**: Click column headers or use the sort dropdown
- **Filter**: Use the search bar with real-time filtering

#### **File Operations**
- **Create Folder**: Click "New Folder" button or press `Ctrl+N`
- **Upload File**: Click "Upload File" button or press `Ctrl+U`
- **Download**: Click the download icon next to any file
- **Preview**: Click on file names to preview content
- **Rename**: Click the edit icon and enter a new name
- **Delete**: Click the trash icon and confirm deletion
- **Compress**: Click the archive icon on folders

#### **Multiple Selection**
- **Select All**: Click "Select All" button or press `Ctrl+A`
- **Individual Selection**: Use checkboxes to select specific files
- **Bulk Operations**: Delete or compress multiple selected files
- **Clear Selection**: Click "Clear" to deselect all

#### **System Information**
- **Statistics Dashboard**: View file and folder statistics
- **System Monitor**: Click "System Info" to view resource usage
- **Real-time Updates**: Statistics update automatically

### Terminal Features:

#### **Command Execution**
- **Type Commands**: Enter commands in the terminal input
- **Auto-completion**: Press `Tab` for command completion
- **Suggestions**: See command suggestions as you type
- **History**: Use arrow keys to navigate command history

#### **Quick Commands**
- **System Info**: `pwd`, `ls -la`, `df -h`, `free -h`
- **Process Management**: `ps aux`, `top`, `whoami`
- **File Operations**: `find`, `grep`, `du -sh`
- **Network**: `netstat`, `ping`, `curl`

#### **System Monitoring**
- **Real-time Monitoring**: Click "Monitor" to show system stats
- **CPU Usage**: View current CPU utilization
- **Memory Usage**: Monitor RAM usage
- **Disk Usage**: Check disk space and usage
- **Load Average**: View system load

#### **File Operations**
- **Search Files**: Use the file search input
- **Grep Pattern**: Search for text patterns in files
- **Find by Size**: Find files by size criteria

#### **Keyboard Shortcuts**
- `Ctrl+L`: Clear terminal
- `Ctrl+K`: Clear input
- `Ctrl+R`: Focus on command input
- `Ctrl+F`: Focus on search input
- `Ctrl+A`: Select all files
- `Tab`: Auto-complete commands
- `Arrow Up/Down`: Navigate command history

## 🔧 **Configuration**

### Environment Variables
```bash
export FLASK_SECRET_KEY="your-secret-key"
export FLASK_UPLOAD_FOLDER="/path/to/uploads"
export FLASK_MAX_CONTENT_LENGTH="104857600"  # 100MB in bytes
```

### Customization Options
- **Upload Folder**: Change `app.config['UPLOAD_FOLDER']` in `app.py`
- **Max File Size**: Modify `app.config['MAX_CONTENT_LENGTH']`
- **Allowed File Types**: Edit `app.config['ALLOWED_EXTENSIONS']`
- **Blocked Commands**: Edit the `dangerous_patterns` list
- **UI Theme**: Modify CSS variables in `templates/base.html`
- **Terminal Timeout**: Change command execution timeout

## 📊 **System Requirements**

### Minimum Requirements
- **OS**: Linux, Windows, or macOS
- **Python**: 3.7 or higher
- **RAM**: 512MB available
- **Storage**: 100MB free space

### Recommended Requirements
- **OS**: Linux (Ubuntu 18.04+ or CentOS 7+)
- **Python**: 3.8 or higher
- **RAM**: 2GB or more
- **Storage**: 1GB free space
- **Browser**: Chrome, Firefox, Safari, or Edge (latest versions)

## 🔒 **Security Considerations**

### Production Deployment
1. **Change Default Credentials**: Update admin and user passwords
2. **Use HTTPS**: Implement SSL/TLS encryption
3. **Firewall Configuration**: Restrict access to necessary ports
4. **Regular Updates**: Keep dependencies updated
5. **Backup Strategy**: Implement regular backups
6. **Logging**: Enable application and system logging
7. **User Management**: Implement proper user authentication
8. **File Permissions**: Set appropriate file system permissions

### Security Features
- ✅ **Command Filtering**: Blocks dangerous commands
- ✅ **Input Validation**: Sanitizes all user inputs
- ✅ **File Type Validation**: Prevents malicious file uploads
- ✅ **Session Management**: Secure user sessions
- ✅ **System Protection**: Prevents deletion of critical directories
- ✅ **Timeout Protection**: Prevents long-running commands

## 🐛 **Troubleshooting**

### Common Issues

1. **Port already in use**
   ```bash
   # Change port in app.py
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

2. **Permission denied errors**
   ```bash
   # Ensure proper permissions
   chmod 755 uploads/
   chmod 755 templates/
   ```

3. **Command not found**
   - Ensure the command exists on your system
   - Check if the command is in the system PATH
   - Verify command permissions

4. **Upload fails**
   - Check file size limits (100MB max)
   - Verify upload directory permissions
   - Ensure sufficient disk space
   - Check file type restrictions

5. **System monitoring not working**
   - Install psutil: `pip install psutil`
   - Check system permissions
   - Verify Python version compatibility

6. **File preview issues**
   - Install python-magic: `pip install python-magic`
   - Check file permissions
   - Verify file encoding

### Performance Optimization
- **Large Directories**: Use search and filtering for better performance
- **File Uploads**: Monitor upload progress for large files
- **System Monitoring**: Disable monitoring when not needed
- **Browser Cache**: Clear browser cache if UI issues occur

## 📈 **Performance Metrics**

### File Operations
- **Upload Speed**: Up to 100MB files supported
- **Search Performance**: Real-time filtering
- **Preview Speed**: Instant text file preview
- **Compression**: Efficient ZIP creation

### Terminal Performance
- **Command Execution**: 60-second timeout
- **Auto-completion**: Instant suggestions
- **History Management**: 15 most recent commands
- **System Monitoring**: 2-second update interval

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Run in development mode
python app.py

# Run tests (if available)
python -m pytest tests/
```

## 📄 **License**

This project is open source and available under the MIT License.

## 🆘 **Support**

For issues and questions:
1. Check the troubleshooting section
2. Review the code comments
3. Create an issue in the repository
4. Check the documentation

## 🔄 **Changelog**

### Version 2.0 (Current)
- ✅ Added search and filtering functionality
- ✅ Implemented multiple file selection
- ✅ Added file preview capabilities
- ✅ Enhanced terminal with auto-completion
- ✅ Added system monitoring features
- ✅ Improved security with advanced filtering
- ✅ Enhanced UI with modern design
- ✅ Added statistics dashboard
- ✅ Implemented bulk operations
- ✅ Added command history export

### Version 1.0 (Previous)
- Basic file manager functionality
- Simple terminal interface
- Basic security features

---

**Note**: This application is designed for development and testing purposes. For production use, implement additional security measures and use a proper WSGI server like Gunicorn or uWSGI. 