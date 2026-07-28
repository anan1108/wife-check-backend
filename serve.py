from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

BARK_URL = os.environ.get('BARK_URL', 'https://api.day.app/Ewk8BYE4bPxUPRdHUnjTrn')
PASSWORD = os.environ.get('AUTH_PASSWORD', 'loveyou')

@app.route('/')
def home():
    return jsonify({'status': 'alive', 'message': 'Wife Check Backend is running!'})

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'time': datetime.now().isoformat()})

@app.route('/send', methods=['POST'])
def send_bark():
    data = request.json
    auth = request.headers.get('Authorization')
    
    if auth != PASSWORD:
        return jsonify({'error': 'unauthorized'}), 401
    
    title = data.get('title', 'Wife Check')
    body = data.get('body', '')
    
    res = requests.post(f'{BARK_URL}/{title}/{body}', timeout=10)
    return jsonify({'sent': True, 'bark_response': res.json() if res.ok else res.text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
