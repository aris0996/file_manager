from flask import Flask, request, send_from_directory, jsonify, render_template, redirect, url_for
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='../static', template_folder='../templates')
CORS(app)

BASE_DIR = os.path.abspath('.')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/list', methods=['GET'])
def list_files():
    path = request.args.get('path', '')
    abs_path = os.path.join(BASE_DIR, path)
    if not os.path.exists(abs_path):
        return jsonify({'error': 'Path not found'}), 404
    files = []
    folders = []
    for entry in os.listdir(abs_path):
        full_path = os.path.join(abs_path, entry)
        if os.path.isdir(full_path):
            folders.append(entry)
        else:
            files.append(entry)
    return jsonify({'folders': folders, 'files': files})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    path = request.form.get('path', '')
    file = request.files['file']
    abs_path = os.path.join(BASE_DIR, path)
    if not os.path.exists(abs_path):
        os.makedirs(abs_path)
    filename = secure_filename(file.filename)
    file.save(os.path.join(abs_path, filename))
    return jsonify({'success': True})

@app.route('/api/download', methods=['GET'])
def download_file():
    path = request.args.get('path', '')
    filename = request.args.get('filename')
    abs_path = os.path.join(BASE_DIR, path)
    return send_from_directory(abs_path, filename, as_attachment=True)

@app.route('/api/delete', methods=['POST'])
def delete_file():
    data = request.json
    path = data.get('path', '')
    name = data.get('name')
    abs_path = os.path.join(BASE_DIR, path, name)
    if os.path.isdir(abs_path):
        import shutil
        shutil.rmtree(abs_path)
    else:
        os.remove(abs_path)
    return jsonify({'success': True})

@app.route('/api/rename', methods=['POST'])
def rename_file():
    data = request.json
    path = data.get('path', '')
    old_name = data.get('old_name')
    new_name = data.get('new_name')
    abs_old = os.path.join(BASE_DIR, path, old_name)
    abs_new = os.path.join(BASE_DIR, path, new_name)
    os.rename(abs_old, abs_new)
    return jsonify({'success': True})

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('../static', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True) 