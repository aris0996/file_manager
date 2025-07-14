from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash
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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Simple user management (in production, use a proper database)
class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

# Simple user storage (in production, use a database)
users = {
    1: User(1, 'admin', hashlib.sha256('admin123'.encode()).hexdigest())
}

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))

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
        
        for user in users.values():
            if user.username == username and user.password_hash == password_hash:
                login_user(user)
                return redirect(url_for('file_manager'))
        
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/file-manager')
@login_required
def file_manager():
    path = request.args.get('path', '.')
    if not os.path.exists(path):
        path = '.'
    
    try:
        items = []
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            try:
                stat = os.stat(item_path)
                items.append({
                    'name': item,
                    'path': item_path,
                    'is_dir': os.path.isdir(item_path),
                    'size': stat.st_size if os.path.isfile(item_path) else 0,
                    'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                    'permissions': oct(stat.st_mode)[-3:]
                })
            except (OSError, PermissionError):
                continue
        
        items.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
        
        return render_template('file_manager.html', 
                             items=items, 
                             current_path=os.path.abspath(path),
                             parent_path=os.path.dirname(os.path.abspath(path)))
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
        
        # Security: prevent dangerous commands
        dangerous_commands = ['rm -rf /', 'sudo', 'su', 'chmod 777', 'dd if=']
        for dangerous in dangerous_commands:
            if dangerous in command.lower():
                return jsonify({'error': f'Command not allowed: {dangerous}'}), 403
        
        # Execute command
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        
        return jsonify({
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode,
            'command': command
        })
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Command timed out'}), 408
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
        
        full_path = os.path.join(folder_path, folder_name)
        
        if os.path.exists(full_path):
            return jsonify({'error': 'Folder already exists'}), 409
        
        os.makedirs(full_path, exist_ok=True)
        return jsonify({'message': 'Folder created successfully'})
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
        
        new_path = os.path.join(os.path.dirname(old_path), new_name)
        
        if os.path.exists(new_path):
            return jsonify({'error': 'Name already exists'}), 409
        
        os.rename(old_path, new_path)
        return jsonify({'message': 'Item renamed successfully'})
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
        file_path = os.path.join(upload_path, filename)
        
        file.save(file_path)
        return jsonify({'message': 'File uploaded successfully'})
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
        
        return jsonify({'message': 'Folder compressed successfully', 'zip_path': zip_path})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 