import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, session, abort, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import mimetypes
import io
import zipfile

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ganti_ini_dengan_secret_key_anda'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@login_required
def dashboard(path):
    root = app.config['UPLOAD_FOLDER']
    abs_path = os.path.abspath(os.path.join(root, path))
    if not abs_path.startswith(root):
        abort(403)
    if not os.path.exists(abs_path):
        flash('Folder tidak ditemukan!')
        return redirect(url_for('dashboard'))
    files = os.listdir(abs_path)
    files = sorted(files, key=lambda x: (not os.path.isdir(os.path.join(abs_path, x)), x.lower()))
    return render_template('dashboard.html', files=files, current_path=path)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Login gagal!')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username sudah terdaftar!')
            return redirect(url_for('register'))
        hashed_pw = generate_password_hash(password)
        user = User(username=username, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Registrasi berhasil! Silakan login.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/upload', methods=['GET', 'POST'])
@app.route('/upload/<path:path>', methods=['GET', 'POST'])
@login_required
def upload(path=''):
    root = app.config['UPLOAD_FOLDER']
    abs_path = os.path.abspath(os.path.join(root, path))
    if not abs_path.startswith(root):
        abort(403)
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        filename = secure_filename(file.filename)
        file.save(os.path.join(abs_path, filename))
        flash('File berhasil diupload!')
        return redirect(url_for('dashboard', path=path))
    return render_template('file_upload.html', current_path=path)

@app.route('/download/<path:path>')
@login_required
def download(path):
    root = app.config['UPLOAD_FOLDER']
    abs_path = os.path.abspath(os.path.join(root, path))
    if not abs_path.startswith(root) or not os.path.isfile(abs_path):
        abort(403)
    return send_file(abs_path, as_attachment=True)

@app.route('/download_zip/<path:path>')
@login_required
def download_zip(path):
    root = app.config['UPLOAD_FOLDER']
    abs_path = os.path.abspath(os.path.join(root, path))
    if not abs_path.startswith(root) or not os.path.isdir(abs_path):
        abort(403)
    mem_zip = io.BytesIO()
    with zipfile.ZipFile(mem_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for foldername, subfolders, filenames in os.walk(abs_path):
            rel_folder = os.path.relpath(foldername, abs_path)
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arcname = os.path.join(rel_folder, filename) if rel_folder != '.' else filename
                zf.write(file_path, arcname)
    mem_zip.seek(0)
    zip_filename = os.path.basename(abs_path) + '.zip'
    return send_file(mem_zip, download_name=zip_filename, as_attachment=True)

@app.route('/preview/<path:path>')
@login_required
def preview(path):
    root = app.config['UPLOAD_FOLDER']
    abs_path = os.path.abspath(os.path.join(root, path))
    if not abs_path.startswith(root) or not os.path.isfile(abs_path):
        abort(403)
    mime, _ = mimetypes.guess_type(abs_path)
    file_info = {
        'name': os.path.basename(abs_path),
        'size': os.path.getsize(abs_path),
        'mtime': os.path.getmtime(abs_path),
        'type': mime or 'Unknown',
    }
    if mime and mime.startswith('image/'):
        return render_template('preview_image.html', file_info=file_info, file_url=url_for('download', path=path), current_path=path)
    elif mime and (mime.startswith('text/') or os.path.splitext(abs_path)[1] in ['.py', '.md', '.txt', '.json', '.csv']):
        with open(abs_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read(10000)
        return render_template('preview_text.html', file_info=file_info, content=content, current_path=path)
    else:
        return render_template('preview_other.html', file_info=file_info, current_path=path)

@app.route('/create_folder', methods=['GET', 'POST'])
@app.route('/create_folder/<path:path>', methods=['GET', 'POST'])
@login_required
def create_folder(path=''):
    root = app.config['UPLOAD_FOLDER']
    abs_path = os.path.abspath(os.path.join(root, path))
    if not abs_path.startswith(root):
        abort(403)
    if request.method == 'POST':
        folder_name = secure_filename(request.form['folder_name'])
        new_folder_path = os.path.join(abs_path, folder_name)
        try:
            os.makedirs(new_folder_path)
            flash('Folder berhasil dibuat!')
        except Exception as e:
            flash(f'Gagal membuat folder: {e}')
        return redirect(url_for('dashboard', path=path))
    return render_template('create_folder.html', current_path=path)

@app.route('/edit/<path:path>', methods=['GET', 'POST'])
@login_required
def edit_file(path):
    root = app.config['UPLOAD_FOLDER']
    abs_path = os.path.abspath(os.path.join(root, path))
    if not abs_path.startswith(root) or not os.path.isfile(abs_path):
        abort(403)
    if request.method == 'POST':
        content = request.form['content']
        try:
            with open(abs_path, 'w', encoding='utf-8') as f:
                f.write(content)
            flash('File berhasil disimpan!')
        except Exception as e:
            flash(f'Gagal menyimpan file: {e}')
        return redirect(url_for('dashboard', path=os.path.dirname(path)))
    with open(abs_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return render_template('file_edit.html', filename=os.path.basename(path), content=content, current_path=path)

@app.route('/rename/<path:path>', methods=['GET', 'POST'])
@login_required
def rename(path):
    root = app.config['UPLOAD_FOLDER']
    abs_path = os.path.abspath(os.path.join(root, path))
    if not abs_path.startswith(root) or not os.path.exists(abs_path):
        abort(403)
    if request.method == 'POST':
        new_name = secure_filename(request.form['new_name'])
        new_path = os.path.join(os.path.dirname(abs_path), new_name)
        if not new_path.startswith(root):
            abort(403)
        try:
            os.rename(abs_path, new_path)
            flash('Berhasil rename!')
        except Exception as e:
            flash(f'Gagal rename: {e}')
        return redirect(url_for('dashboard', path=os.path.dirname(path)))
    return render_template('rename.html', filename=os.path.basename(path), current_path=path)

@app.route('/delete/<path:path>', methods=['GET', 'POST'])
@login_required
def delete(path):
    root = app.config['UPLOAD_FOLDER']
    abs_path = os.path.abspath(os.path.join(root, path))
    if not abs_path.startswith(root) or not os.path.exists(abs_path):
        abort(403)
    parent_path = os.path.dirname(path)
    try:
        if os.path.isfile(abs_path):
            os.remove(abs_path)
        else:
            import shutil
            shutil.rmtree(abs_path)
        flash('Berhasil dihapus!')
    except Exception as e:
        flash(f'Gagal menghapus: {e}')
    return redirect(url_for('dashboard', path=parent_path))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True) 