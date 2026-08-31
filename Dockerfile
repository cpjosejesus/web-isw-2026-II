FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Antes: CMD ["python", "app.py"]  -> servidor de desarrollo, un proceso.
# Ahora: gunicorn ejecuta la misma app de Flask en varios procesos y
# reemplaza al worker que se cuelga. No cambia una linea de main.py.
CMD ["gunicorn", \
     "--workers", "4", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "30", \
     "--access-logfile", "-", \
     "app:app"]
