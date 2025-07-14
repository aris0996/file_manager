# File Manager & Terminal Web Application

A modern Flask-based web application for file and folder management with an integrated Linux terminal interface.

## Features

### File Manager
- 📁 **Browse files and folders** with a modern web interface
- 📂 **Create new folders** with a simple click
- 📤 **Upload files** with drag-and-drop support
- 📥 **Download files** directly from the browser
- ✏️ **Rename files and folders** inline
- 🗑️ **Delete files and folders** with confirmation
- 📦 **Compress folders** into ZIP archives
- 🔍 **Search and navigate** through directory structures
- 📊 **File information** including size, permissions, and modification date

### Terminal Interface
- 💻 **Interactive Linux terminal** accessible via web browser
- ⚡ **Quick command buttons** for common operations
- 📜 **Command history** with easy re-execution
- ⌨️ **Keyboard shortcuts** for power users
- 🔒 **Security features** to prevent dangerous commands
- 📱 **Responsive design** works on all devices

### Security Features
- 🔐 **User authentication** with login system
- 🛡️ **Command filtering** to prevent dangerous operations
- ⏱️ **Command timeout** protection
- 🔒 **Session management** with Flask-Login

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd file-manager-terminal
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your web browser
   - Navigate to `http://localhost:5000`
   - Login with default credentials:
     - Username: `admin`
     - Password: `admin123`

## Usage

### File Manager
1. **Navigation**: Use the breadcrumb navigation or click on folder names
2. **Create Folder**: Click "New Folder" button or press `Ctrl+N`
3. **Upload File**: Click "Upload File" button or press `Ctrl+U`
4. **Download**: Click the download icon next to any file
5. **Rename**: Click the edit icon and enter a new name
6. **Delete**: Click the trash icon and confirm deletion
7. **Compress**: Click the archive icon on folders to create ZIP files

### Terminal
1. **Execute Commands**: Type commands in the terminal input and press Enter
2. **Quick Commands**: Use the predefined buttons for common operations
3. **Command History**: View and re-execute previous commands
4. **Keyboard Shortcuts**:
   - `Ctrl+L`: Clear terminal
   - `Ctrl+K`: Clear input
   - `Arrow Up/Down`: Navigate command history

### Available Commands
The terminal supports most Linux commands including:
- `ls`, `cd`, `pwd` - File navigation
- `mkdir`, `rm`, `cp`, `mv` - File operations
- `cat`, `grep`, `find` - File content operations
- `ps`, `top`, `df`, `du` - System information
- `chmod`, `chown` - File permissions
- `tar`, `zip`, `unzip` - Archive operations
- `wget`, `curl` - Network operations

## Security Notes

⚠️ **Important Security Considerations**:

1. **Default Credentials**: Change the default admin password in production
2. **Network Access**: The application runs on all interfaces (0.0.0.0) by default
3. **Command Restrictions**: Dangerous commands like `rm -rf /`, `sudo`, `su` are blocked
4. **File Permissions**: Ensure proper file permissions on the server
5. **HTTPS**: Use HTTPS in production environments

## Configuration

### Environment Variables
You can configure the application using environment variables:

```bash
export FLASK_SECRET_KEY="your-secret-key"
export FLASK_UPLOAD_FOLDER="/path/to/uploads"
export FLASK_MAX_CONTENT_LENGTH="16777216"  # 16MB in bytes
```

### Customization
- **Upload Folder**: Change `app.config['UPLOAD_FOLDER']` in `app.py`
- **Max File Size**: Modify `app.config['MAX_CONTENT_LENGTH']`
- **Blocked Commands**: Edit the `dangerous_commands` list in the `execute_command` function
- **UI Theme**: Modify CSS variables in `templates/base.html`

## File Structure

```
file-manager-terminal/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template with styling
│   ├── login.html        # Login page
│   ├── file_manager.html # File manager interface
│   └── terminal.html     # Terminal interface
└── uploads/              # Default upload directory
```

## API Endpoints

### File Management
- `GET /file-manager` - File manager interface
- `POST /api/create-folder` - Create new folder
- `POST /api/delete-item` - Delete file/folder
- `POST /api/rename-item` - Rename file/folder
- `POST /api/upload-file` - Upload file
- `GET /api/download-file` - Download file
- `POST /api/compress-folder` - Compress folder

### Terminal
- `GET /terminal` - Terminal interface
- `POST /api/execute-command` - Execute Linux command

### Authentication
- `GET /login` - Login page
- `POST /login` - Authenticate user
- `GET /logout` - Logout user

## Troubleshooting

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
   ```

3. **Command not found**
   - Ensure the command exists on your system
   - Check if the command is in the system PATH

4. **Upload fails**
   - Check file size limits
   - Verify upload directory permissions
   - Ensure sufficient disk space

### Logs
The application logs errors and debug information to the console when running in debug mode.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the code comments
3. Create an issue in the repository

---

**Note**: This application is designed for development and testing purposes. For production use, implement additional security measures and use a proper WSGI server. 