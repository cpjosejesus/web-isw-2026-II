"""Punto de entrada WSGI.

Gunicorn importa este modulo y usa el objeto `app`. Ya no llamamos a
app.run(): quien abre el socket y atiende HTTP es gunicorn, no Flask.
"""
from main import app
from models import db

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # Solo para desarrollo local sin contenedor.
    app.run(host='0.0.0.0', port=8000)
