# Paso 4 — HTTPS y cabeceras: el borde publico

Nginx termina el TLS. La aplicacion sigue hablando HTTP en la red
interna y no sabe que existe un certificado.

## Levantar

    ./nginx/generar-certificado.sh     # una sola vez
    docker compose up -d --build
    open https://localhost:8443        # el navegador va a advertir

## Que cambio

- `nginx/default.conf` — dos bloques `server`: el del 80 solo redirige.
- Cabeceras de seguridad, `client_max_body_size` y `gzip`, una vez para
  todo el sitio.
- `docker-compose.yml` — se publica el 443 y se monta `nginx/certs`.
- Los certificados **no** se versionan: estan en `nginx/.gitignore`.

## Ejercicio

1. `curl -I http://localhost:8080` y ver el `301`.
2. Comprobar que `url_for(..., _external=True)` ahora genera `https://`.
3. Quitar `X-Forwarded-Proto` y ver como se rompe lo anterior.

Slides: `clase5-paso4-tls.html`
