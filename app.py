from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from werkzeug.security import check_password_hash, generate_password_hash
import pathlib
import shutil
from werkzeug.utils import secure_filename
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.secret_key = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Dummy user (replace with DB in production)
class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

users = {
    'admin': User('1', 'admin', generate_password_hash('admin123'))
}

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.id == user_id:
            return user
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    return render_template('index.html', user=current_user)

# Set root directory (ganti sesuai kebutuhan)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'files'))
os.makedirs(ROOT_DIR, exist_ok=True)

def secure_path(path):
    # Pastikan path tetap di ROOT_DIR
    full_path = os.path.abspath(os.path.join(ROOT_DIR, path))
    if not full_path.startswith(ROOT_DIR):
        raise ValueError('Invalid path')
    return full_path

@app.route('/explore', defaults={'req_path': ''})
@app.route('/explore/<path:req_path>')
@login_required
def explore(req_path):
    try:
        abs_path = secure_path(req_path)
    except Exception:
        flash('Akses path tidak valid', 'danger')
        return redirect(url_for('dashboard'))
    if not os.path.exists(abs_path):
        flash('Folder tidak ditemukan', 'danger')
        return redirect(url_for('dashboard'))
    files = []
    folders = []
    for entry in os.scandir(abs_path):
        if entry.is_file():
            files.append(entry.name)
        elif entry.is_dir():
            folders.append(entry.name)
    parent = os.path.relpath(os.path.dirname(abs_path), ROOT_DIR) if abs_path != ROOT_DIR else None
    return render_template('explore.html', files=files, folders=folders, current=req_path, parent=parent)

@app.route('/folder/create', methods=['POST'])
@login_required
def create_folder():
    parent = request.form.get('parent', '')
    name = request.form.get('name', '')
    if not name:
        flash('Nama folder wajib diisi', 'danger')
        return redirect(url_for('explore', req_path=parent))
    try:
        abs_path = secure_path(os.path.join(parent, name))
        os.makedirs(abs_path)
        flash('Folder berhasil dibuat', 'success')
    except Exception as e:
        flash(f'Gagal membuat folder: {e}', 'danger')
    return redirect(url_for('explore', req_path=parent))

@app.route('/folder/rename', methods=['POST'])
@login_required
def rename_folder():
    parent = request.form.get('parent', '')
    old_name = request.form.get('old_name', '')
    new_name = request.form.get('new_name', '')
    if not old_name or not new_name:
        flash('Nama lama dan baru wajib diisi', 'danger')
        return redirect(url_for('explore', req_path=parent))
    try:
        old_path = secure_path(os.path.join(parent, old_name))
        new_path = secure_path(os.path.join(parent, new_name))
        os.rename(old_path, new_path)
        flash('Folder berhasil di-rename', 'success')
    except Exception as e:
        flash(f'Gagal rename folder: {e}', 'danger')
    return redirect(url_for('explore', req_path=parent))

@app.route('/folder/delete', methods=['POST'])
@login_required
def delete_folder():
    parent = request.form.get('parent', '')
    name = request.form.get('name', '')
    try:
        abs_path = secure_path(os.path.join(parent, name))
        shutil.rmtree(abs_path)
        flash('Folder berhasil dihapus', 'success')
    except Exception as e:
        flash(f'Gagal hapus folder: {e}', 'danger')
    return redirect(url_for('explore', req_path=parent))

@app.route('/file/create', methods=['POST'])
@login_required
def create_file():
    parent = request.form.get('parent', '')
    name = request.form.get('name', '')
    if not name:
        flash('Nama file wajib diisi', 'danger')
        return redirect(url_for('explore', req_path=parent))
    try:
        abs_path = secure_path(os.path.join(parent, name))
        with open(abs_path, 'x'):
            pass
        flash('File berhasil dibuat', 'success')
    except Exception as e:
        flash(f'Gagal membuat file: {e}', 'danger')
    return redirect(url_for('explore', req_path=parent))

@app.route('/file/edit/<path:req_path>', methods=['GET', 'POST'])
@login_required
def edit_file(req_path):
    try:
        abs_path = secure_path(req_path)
    except Exception:
        flash('Akses path tidak valid', 'danger')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        content = request.form.get('content', '')
        try:
            with open(abs_path, 'w') as f:
                f.write(content)
            flash('File berhasil diupdate', 'success')
        except Exception as e:
            flash(f'Gagal update file: {e}', 'danger')
        return redirect(url_for('explore', req_path=os.path.dirname(req_path)))
    else:
        try:
            with open(abs_path, 'r') as f:
                content = f.read()
        except Exception:
            content = ''
        return render_template('edit_file.html', file=req_path, content=content)

@app.route('/file/delete', methods=['POST'])
@login_required
def delete_file():
    parent = request.form.get('parent', '')
    name = request.form.get('name', '')
    try:
        abs_path = secure_path(os.path.join(parent, name))
        os.remove(abs_path)
        flash('File berhasil dihapus', 'success')
    except Exception as e:
        flash(f'Gagal hapus file: {e}', 'danger')
    return redirect(url_for('explore', req_path=parent))

ALLOWED_EXTENSIONS = set(['txt', 'md', 'py', 'json', 'csv', 'log', 'conf', 'ini', 'html', 'css', 'js', 'xml', 'yml', 'yaml'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/file/upload', methods=['POST'])
@login_required
def upload_file():
    parent = request.form.get('parent', '')
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('explore', req_path=parent))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('explore', req_path=parent))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        try:
            abs_path = secure_path(os.path.join(parent, filename))
            file.save(abs_path)
            flash('File berhasil diupload', 'success')
        except Exception as e:
            flash(f'Gagal upload file: {e}', 'danger')
    else:
        flash('Ekstensi file tidak diizinkan', 'danger')
    return redirect(url_for('explore', req_path=parent))

@app.route('/file/download/<path:req_path>')
@login_required
def download_file(req_path):
    try:
        abs_path = secure_path(req_path)
        if not os.path.isfile(abs_path):
            flash('File tidak ditemukan', 'danger')
            return redirect(url_for('explore', req_path=os.path.dirname(req_path)))
        rel_dir = os.path.relpath(os.path.dirname(abs_path), ROOT_DIR)
        return send_from_directory(os.path.dirname(abs_path), os.path.basename(abs_path), as_attachment=True)
    except Exception:
        flash('Akses path tidak valid', 'danger')
        return redirect(url_for('dashboard'))

app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['REMEMBER_COOKIE_HTTPONLY'] = True
app.config['REMEMBER_COOKIE_SECURE'] = True
app.config['WTF_CSRF_TIME_LIMIT'] = 3600

csrf = CSRFProtect(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 