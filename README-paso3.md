# Paso 3 — Gunicorn: quien ejecuta Python de verdad

Se acabo el aviso de "development server". Gunicorn levanta cuatro
procesos que atienden en paralelo y reinicia al que falle.

## Levantar

    docker compose up -d --build
    docker compose logs web        # cuatro workers arrancando

## Que cambio

- `Dockerfile` — el `CMD` pasa de `python app.py` a `gunicorn ... app:app`.
- `app.py` — ya no llama a `app.run()`; solo expone el objeto `app`.
- Nada de `main.py`, `models.py` ni las plantillas se toca. Ese es el
  punto del contrato WSGI.

## Ejercicio

1. `docker compose exec web ps aux` y contar los procesos.
2. Agregar una ruta que guarde un contador en una variable global,
   recargar varias veces y explicar por que el numero salta.
3. Bajar a `--workers 1` y comparar el comportamiento.

Slides: `clase5-paso3-gunicorn.html`
