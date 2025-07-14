from flask import Flask, render_template, redirect, url_for, request, flash, send_from_directory
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
import os
from werkzeug.utils import secure_filename
from flask import send_file, abort
import shutil
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Dummy user for demonstration
class User(UserMixin):
    def __init__(self, id, is_sudo=False):
        self.id = id
        self.is_sudo = is_sudo

users = {
    'admin': {'password': 'admin', 'is_sudo': True},
    'user': {'password': 'user', 'is_sudo': False}
}

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id, users[user_id]['is_sudo'])
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user = User(username, users[username]['is_sudo'])
            login_user(user)
            return redirect(url_for('file_manager'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

ROOT_DIR = os.path.abspath('./user_files')
if not os.path.exists(ROOT_DIR):
    os.makedirs(ROOT_DIR)

def safe_join(base, *paths):
    # Prevent directory traversal
    final_path = os.path.abspath(os.path.join(base, *paths))
    if not final_path.startswith(base):
        abort(403)
    return final_path

def get_breadcrumbs(rel_path):
    crumbs = [{'name': 'root', 'path': ''}]
    if rel_path:
        parts = rel_path.strip('/').split('/')
        for i, part in enumerate(parts):
            crumbs.append({'name': part, 'path': '/'.join(parts[:i+1])})
    return crumbs

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@login_required
def file_manager(path):
    abs_path = safe_join(ROOT_DIR, path)
    if not os.path.exists(abs_path):
        flash('Path does not exist')
        return redirect(url_for('file_manager'))
    items = []
    for name in os.listdir(abs_path):
        item_path = os.path.join(abs_path, name)
        items.append({
            'name': name,
            'is_dir': os.path.isdir(item_path),
            'rel_path': os.path.relpath(item_path, ROOT_DIR).replace('\\', '/')
        })
    breadcrumbs = get_breadcrumbs(path)
    return render_template('file_manager.html', items=items, breadcrumbs=breadcrumbs, current_path=path, is_sudo=getattr(current_user, 'is_sudo', False))

@app.route('/upload/<path:path>', methods=['POST'])
@login_required
def upload(path):
    abs_path = safe_join(ROOT_DIR, path)
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('file_manager', path=path))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('file_manager', path=path))
    filename = secure_filename(file.filename)
    file.save(os.path.join(abs_path, filename))
    flash('File uploaded')
    return redirect(url_for('file_manager', path=path))

@app.route('/download/<path:path>')
@login_required
def download(path):
    abs_path = safe_join(ROOT_DIR, path)
    if not os.path.isfile(abs_path):
        abort(404)
    return send_file(abs_path, as_attachment=True)

def sudo_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not getattr(current_user, 'is_sudo', False):
            flash('Sudo privilege required for this action.')
            return redirect(url_for('file_manager'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/create', methods=['POST'])
@login_required
@sudo_required
def create():
    path = request.form.get('path', '')
    name = secure_filename(request.form.get('name', ''))
    type_ = request.form.get('type', 'folder')
    abs_path = safe_join(ROOT_DIR, path, name)
    if type_ == 'folder':
        os.makedirs(abs_path, exist_ok=True)
    else:
        open(abs_path, 'w').close()
    flash(f'{type_.capitalize()} created')
    return redirect(url_for('file_manager', path=path))

@app.route('/rename', methods=['POST'])
@login_required
@sudo_required
def rename():
    path = request.form.get('path', '')
    new_name = secure_filename(request.form.get('new_name', ''))
    abs_path = safe_join(ROOT_DIR, path)
    parent = os.path.dirname(abs_path)
    new_path = os.path.join(parent, new_name)
    os.rename(abs_path, new_path)
    flash('Renamed successfully')
    return redirect(url_for('file_manager', path=os.path.relpath(parent, ROOT_DIR)))

@app.route('/delete', methods=['POST'])
@login_required
@sudo_required
def delete():
    path = request.form.get('path', '')
    abs_path = safe_join(ROOT_DIR, path)
    if os.path.isdir(abs_path):
        shutil.rmtree(abs_path)
    else:
        os.remove(abs_path)
    flash('Deleted successfully')
    parent = os.path.dirname(abs_path)
    return redirect(url_for('file_manager', path=os.path.relpath(parent, ROOT_DIR)))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 