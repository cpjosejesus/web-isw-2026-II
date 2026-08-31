# Paso 1 — Nginx sirviendo archivos

El caso mas simple: nginx recibe una peticion, busca un archivo en una
carpeta y lo devuelve. Sin Python, sin base de datos.

## Levantar

    docker compose up -d
    open http://localhost:8080

## Que mirar

- `nginx/default.conf` — siete lineas: `listen`, `server_name`, `root`,
  `index` y un `location`.
- La pagina se sirve desde `www/index.html`; el CSS desde `static/`.
- Ningun proceso de Python esta corriendo. `docker compose ps` lo confirma.

## Ejercicio

1. Pedir una URL que no existe y ver el `404` que produce `try_files`.
2. Cambiar `root` por `alias` en `location /` y explicar por que se rompe.
3. Agregar `autoindex on;` y ver el listado de la carpeta.

Slides: `clase5-paso1-estaticos.html`
