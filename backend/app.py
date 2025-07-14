from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

# Placeholder: tambahkan endpoint file/folder management di sini

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 