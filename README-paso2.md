# Paso 2 — Proxy inverso: nginx delante de Flask

Nginx deja de ser solo un servidor de archivos: ahora reenvia a la
aplicacion todo lo que no sea `/static/`.

## Levantar

    docker compose up -d --build
    open http://localhost:8080

## Que cambio

- `nginx/default.conf` — aparece `proxy_pass` y las cuatro cabeceras
  `X-Forwarded-*`.
- `docker-compose.yml` — `web` pasa de `ports` a `expose`: la aplicacion
  ya no es alcanzable desde el host.
- `main.py` — `ProxyFix` para que Flask crea esas cabeceras.

## Ejercicio

1. Intentar `curl http://localhost:8000` y comprobar que ya no responde.
2. Comentar las cuatro cabeceras y observar como cambia `request.remote_addr`.
3. Ver en las DevTools que el CSS lo devuelve nginx con `Expires` a 30 dias.

Slides: `clase5-paso2-proxy-inverso.html`
