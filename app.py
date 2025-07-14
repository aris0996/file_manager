from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
import shutil
import subprocess
import json
import hashlib
from datetime import datetime
from werkzeug.utils import secure_filename
import zipfile
import tempfile
import mimetypes
import magic
import threading
import time
from pathlib import Path
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx', 'zip', 'rar', 'py', 'js', 'html', 'css', 'json', 'xml', 'csv', 'md'}

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# File operation queue for background processing
file_operations = {}

class User(UserMixin):
    def __init__(self, id, username, password_hash, role='user'):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role

# Enhanced user management
users = {
    1: User(1, 'admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin'),
    2: User(2, 'user', 'e606e38b0d8c19b24cf0ee3808183162ea7cd63ff7912dbb22b5e803286b4446', 'user'),
    3: User(3, 'test', 'ecd71870d1963316a97e3ac3408c9835ad8cf0f3c1bc703527c30265534f75ae', 'user')
}

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_file_info(file_path):
    """Get detailed file information"""
    try:
        stat = os.stat(file_path)
        mime_type, _ = mimetypes.guess_type(file_path)
        
        # Try to get file type using python-magic
        try:
            file_type = magic.from_file(file_path, mime=True)
        except:
            file_type = mime_type or 'application/octet-stream'
        
        return {
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime),
            'created': datetime.fromtimestamp(stat.st_ctime),
            'permissions': oct(stat.st_mode)[-3:],
            'mime_type': file_type,
            'is_readable': os.access(file_path, os.R_OK),
            'is_writable': os.access(file_path, os.W_OK),
            'is_executable': os.access(file_path, os.X_OK)
        }
    except Exception as e:
        return None

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f} {size_names[i]}"

@app.route('/')
@login_required
def index():
    return redirect(url_for('file_manager'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        print(f"Login attempt: {username} with hash: {password_hash}")
        
        # Find user by username
        user_found = None
        for user in users.values():
            if user.username == username:
                user_found = user
                break
        
        if user_found and user_found.password_hash == password_hash:
            print(f"Login successful for user: {username}")
            login_user(user_found)
            session['user_role'] = user_found.role
            session['username'] = user_found.username
            return redirect(url_for('file_manager'))
        else:
            print(f"Login failed for user: {username}")
            if user_found:
                print(f"Password hash mismatch. Expected: {user_found.password_hash}, Got: {password_hash}")
            else:
                print(f"User not found: {username}")
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))

@app.route('/debug/users')
def debug_users():
    """Debug endpoint to check users (remove in production)"""
    user_list = []
    for user_id, user in users.items():
        user_list.append({
            'id': user_id,
            'username': user.username,
            'role': user.role,
            'password_hash': user.password_hash
        })
    return jsonify({'users': user_list})

@app.route('/debug/session')
def debug_session():
    """Debug endpoint to check session (remove in production)"""
    return jsonify({
        'session': dict(session),
        'current_user': current_user.username if current_user.is_authenticated else None,
        'user_role': session.get('user_role'),
        'username': session.get('username')
    })

@app.route('/file-manager')
@login_required
def file_manager():
    path = request.args.get('path', '.')
    search = request.args.get('search', '')
    sort_by = request.args.get('sort', 'name')
    sort_order = request.args.get('order', 'asc')
    
    if not os.path.exists(path):
        path = '.'
    
    try:
        items = []
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            
            # Apply search filter
            if search and search.lower() not in item.lower():
                continue
                
            try:
                file_info = get_file_info(item_path)
                if file_info:
                    items.append({
                        'name': item,
                        'path': item_path,
                        'is_dir': os.path.isdir(item_path),
                        'size': file_info['size'],
                        'size_formatted': format_file_size(file_info['size']) if not os.path.isdir(item_path) else '-',
                        'modified': file_info['modified'].strftime('%Y-%m-%d %H:%M:%S'),
                        'permissions': file_info['permissions'],
                        'mime_type': file_info['mime_type'],
                        'is_readable': file_info['is_readable'],
                        'is_writable': file_info['is_writable'],
                        'is_executable': file_info['is_executable']
                    })
            except (OSError, PermissionError):
                continue
        
        # Sorting
        reverse = sort_order == 'desc'
        if sort_by == 'name':
            items.sort(key=lambda x: (not x['is_dir'], x['name'].lower()), reverse=reverse)
        elif sort_by == 'size':
            items.sort(key=lambda x: x['size'], reverse=reverse)
        elif sort_by == 'modified':
            items.sort(key=lambda x: x['modified'], reverse=reverse)
        elif sort_by == 'type':
            items.sort(key=lambda x: (not x['is_dir'], x['mime_type'], x['name'].lower()), reverse=reverse)
        
        # Calculate directory statistics
        total_files = len([item for item in items if not item['is_dir']])
        total_dirs = len([item for item in items if item['is_dir']])
        total_size = sum([item['size'] for item in items if not item['is_dir']])
        
        return render_template('file_manager.html', 
                             items=items, 
                             current_path=os.path.abspath(path),
                             parent_path=os.path.dirname(os.path.abspath(path)),
                             search=search,
                             sort_by=sort_by,
                             sort_order=sort_order,
                             stats={
                                 'total_files': total_files,
                                 'total_dirs': total_dirs,
                                 'total_size': format_file_size(total_size)
                             })
    except Exception as e:
        flash(f'Error accessing directory: {str(e)}')
        return redirect(url_for('file_manager', path='.'))

@app.route('/terminal')
@login_required
def terminal():
    return render_template('terminal.html')

@app.route('/api/execute-command', methods=['POST'])
@login_required
def execute_command():
    try:
        data = request.get_json()
        command = data.get('command', '')
        
        if not command.strip():
            return jsonify({'error': 'No command provided'}), 400
        
        # Enhanced security: prevent dangerous commands
        dangerous_patterns = [
            r'rm\s+-rf\s+/', r'sudo\s+', r'su\s+', r'chmod\s+777', r'dd\s+if=',
            r':\(\)\{\s*:\|:\s*&\s*\};:', r'wget\s+.*\|\s*bash', r'curl\s+.*\|\s*bash',
            r'nc\s+', r'ncat\s+', r'telnet\s+', r'ssh\s+.*\|\s*bash'
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return jsonify({'error': f'Command not allowed: {pattern}'}), 403
        
        # Execute command with enhanced environment
        env = os.environ.copy()
        env['PATH'] = '/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin'
        
        result = subprocess.run(command, shell=True, capture_output=True, text=True, 
                              timeout=60, env=env, cwd=os.getcwd())
        
        return jsonify({
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode,
            'command': command,
            'cwd': os.getcwd()
        })
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Command timed out (60 seconds)'}), 408
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/create-folder', methods=['POST'])
@login_required
def create_folder():
    try:
        data = request.get_json()
        folder_path = data.get('path', '')
        folder_name = data.get('name', '')
        
        if not folder_name:
            return jsonify({'error': 'Folder name is required'}), 400
        
        # Validate folder name
        if not re.match(r'^[a-zA-Z0-9._-]+$', folder_name):
            return jsonify({'error': 'Invalid folder name. Use only letters, numbers, dots, underscores, and hyphens.'}), 400
        
        full_path = os.path.join(folder_path, folder_name)
        
        if os.path.exists(full_path):
            return jsonify({'error': 'Folder already exists'}), 409
        
        os.makedirs(full_path, exist_ok=True)
        return jsonify({'message': 'Folder created successfully', 'path': full_path})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/delete-item', methods=['POST'])
@login_required
def delete_item():
    try:
        data = request.get_json()
        item_path = data.get('path', '')
        
        if not os.path.exists(item_path):
            return jsonify({'error': 'Item not found'}), 404
        
        # Prevent deletion of system directories
        protected_paths = ['/', '/home', '/etc', '/var', '/usr', '/bin', '/sbin']
        for protected in protected_paths:
            if item_path.startswith(protected):
                return jsonify({'error': 'Cannot delete system directories'}), 403
        
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)
        
        return jsonify({'message': 'Item deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/rename-item', methods=['POST'])
@login_required
def rename_item():
    try:
        data = request.get_json()
        old_path = data.get('old_path', '')
        new_name = data.get('new_name', '')
        
        if not os.path.exists(old_path):
            return jsonify({'error': 'Item not found'}), 404
        
        # Validate new name
        if not re.match(r'^[a-zA-Z0-9._-]+$', new_name):
            return jsonify({'error': 'Invalid name. Use only letters, numbers, dots, underscores, and hyphens.'}), 400
        
        new_path = os.path.join(os.path.dirname(old_path), new_name)
        
        if os.path.exists(new_path):
            return jsonify({'error': 'Name already exists'}), 409
        
        os.rename(old_path, new_path)
        return jsonify({'message': 'Item renamed successfully', 'new_path': new_path})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload-file', methods=['POST'])
@login_required
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        upload_path = request.form.get('path', app.config['UPLOAD_FOLDER'])
        filename = secure_filename(file.filename)
        
        # Check file extension
        if not allowed_file(filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        file_path = os.path.join(upload_path, filename)
        
        # Handle duplicate filenames
        counter = 1
        original_filename = filename
        while os.path.exists(file_path):
            name, ext = os.path.splitext(original_filename)
            filename = f"{name}_{counter}{ext}"
            file_path = os.path.join(upload_path, filename)
            counter += 1
        
        file.save(file_path)
        
        # Get file info
        file_info = get_file_info(file_path)
        
        return jsonify({
            'message': 'File uploaded successfully',
            'filename': filename,
            'size': format_file_size(file_info['size']) if file_info else 'Unknown'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download-file')
@login_required
def download_file():
    try:
        file_path = request.args.get('path', '')
        
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/compress-folder', methods=['POST'])
@login_required
def compress_folder():
    try:
        data = request.get_json()
        folder_path = data.get('path', '')
        
        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            return jsonify({'error': 'Folder not found'}), 404
        
        zip_path = f"{folder_path}.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_path)
                    zipf.write(file_path, arcname)
        
        file_info = get_file_info(zip_path)
        return jsonify({
            'message': 'Folder compressed successfully', 
            'zip_path': zip_path,
            'size': format_file_size(file_info['size']) if file_info else 'Unknown'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/file-preview')
@login_required
def file_preview():
    try:
        file_path = request.args.get('path', '')
        
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        file_info = get_file_info(file_path)
        if not file_info:
            return jsonify({'error': 'Cannot read file info'}), 500
        
        # Preview text files
        if file_info['mime_type'].startswith('text/') or file_path.endswith(('.py', '.js', '.html', '.css', '.json', '.xml', '.md', '.txt')):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read(5000)  # Read first 5000 characters
                    return jsonify({
                        'type': 'text',
                        'content': content,
                        'truncated': len(content) >= 5000
                    })
            except UnicodeDecodeError:
                return jsonify({'error': 'Cannot preview binary file'}), 400
        
        # Preview images
        elif file_info['mime_type'].startswith('image/'):
            return jsonify({
                'type': 'image',
                'mime_type': file_info['mime_type']
            })
        
        else:
            return jsonify({
                'type': 'binary',
                'mime_type': file_info['mime_type'],
                'size': format_file_size(file_info['size'])
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/multiple-operations', methods=['POST'])
@login_required
def multiple_operations():
    try:
        data = request.get_json()
        operation = data.get('operation', '')
        items = data.get('items', [])
        
        if not items:
            return jsonify({'error': 'No items selected'}), 400
        
        results = []
        
        if operation == 'delete':
            for item_path in items:
                try:
                    if os.path.exists(item_path):
                        if os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                        else:
                            os.remove(item_path)
                        results.append({'path': item_path, 'status': 'success'})
                    else:
                        results.append({'path': item_path, 'status': 'not_found'})
                except Exception as e:
                    results.append({'path': item_path, 'status': 'error', 'message': str(e)})
        
        elif operation == 'compress':
            # Create a temporary directory for the zip
            temp_dir = tempfile.mkdtemp()
            zip_path = os.path.join(temp_dir, 'selected_files.zip')
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for item_path in items:
                    if os.path.exists(item_path):
                        if os.path.isdir(item_path):
                            for root, dirs, files in os.walk(item_path):
                                for file in files:
                                    file_path = os.path.join(root, file)
                                    arcname = os.path.relpath(file_path, os.path.dirname(item_path))
                                    zipf.write(file_path, arcname)
                        else:
                            zipf.write(item_path, os.path.basename(item_path))
            
            results.append({'path': zip_path, 'status': 'success', 'type': 'zip'})
        
        return jsonify({'results': results})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/system-info')
@login_required
def system_info():
    try:
        # Get system information
        import platform
        import psutil
        
        info = {
            'platform': platform.system(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'processor': platform.processor(),
            'hostname': platform.node(),
            'cpu_count': psutil.cpu_count(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory': {
                'total': format_file_size(psutil.virtual_memory().total),
                'available': format_file_size(psutil.virtual_memory().available),
                'percent': psutil.virtual_memory().percent
            },
            'disk': {
                'total': format_file_size(psutil.disk_usage('/').total),
                'used': format_file_size(psutil.disk_usage('/').used),
                'free': format_file_size(psutil.disk_usage('/').free),
                'percent': psutil.disk_usage('/').percent
            }
        }
        
        return jsonify(info)
    except ImportError:
        return jsonify({'error': 'psutil not available'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 