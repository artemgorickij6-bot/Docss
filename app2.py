from flask import Flask, request, send_file
import json
from datetime import datetime

app = Flask(__name__)
data_store = []

@app.route('/')
def index():
    return send_file("index.html")

@app.route('/log', methods=['POST'])
def log():
    data_store.append(request.get_json())
    return '', 204

@app.route('/loading')
def loading():
    return "<html><body style='font-family:sans-serif;text-align:center;padding-top:50px;'>Загрузка…</body></html>"

@app.route('/admin')
def admin():
    out = "<html><body style='font-family:sans-serif;padding:20px;'><h2>Все заходы:</h2><pre>"
    for d in reversed(data_store):
        out += json.dumps(d, indent=2) + "\n\n"
    out += "</pre></body></html>"
    return out

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
