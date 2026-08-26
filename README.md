# Biblioteca — Clase 4

Flask + Jinja2 + PostgreSQL. CRUD completo de autores y libros.

## Levantar con Docker Compose

```bash
cp .env.example .env      # y cambiar las claves
docker compose up -d --build
```

La aplicacion queda en http://localhost:8000

### Comandos utiles

```bash
docker compose ps               # estan los dos arriba?
docker compose logs -f web      # seguir los registros
docker compose exec web bash    # entrar al contenedor
docker compose exec web python seed.py   # cargar datos de ejemplo
docker compose down             # bajar (los datos quedan en el volumen)
docker compose down -v          # bajar y BORRAR el volumen
```

## Estructura

```
├── app.py                # entrada del contenedor (puerto 8000)
├── main.py               # la aplicacion: rutas
├── models.py             # Autor 1 — N Libro
├── seed.py               # datos de ejemplo
├── templates/
│   ├── layout.html       # el unico <head> del proyecto
│   ├── libros/           # index, detalle, formulario
│   ├── autores/          # index, detalle
│   └── errores/          # 404, 500
└── static/css/estilos.css
```

## Los dos servicios

`web` escucha en 8000 y es el unico publicado. `db` escucha en 5432 y
solo la alcanza `web`, por la red interna de Compose: publicarla seria
exponer la base de datos a Internet.
