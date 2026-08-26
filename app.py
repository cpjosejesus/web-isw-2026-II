"""Punto de entrada del contenedor.

Crea las tablas si no existen y levanta el servidor en el 8000, que es
el puerto que el Dockerfile expone y Compose publica.
"""
from main import app
from models import db

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
