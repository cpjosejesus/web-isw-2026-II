# Paso 5 — Balanceo de carga: varias replicas

Un contenedor sigue siendo un solo punto de falla. Ahora nginx reparte
entre varias replicas de la aplicacion.

## Levantar

    ./nginx/generar-certificado.sh     # si no lo hicieron antes
    docker compose up -d --build --scale web=3
    docker compose ps                  # tres contenedores web

## Que cambio

- `nginx/default.conf` — aparece el bloque `upstream biblioteca` y
  `proxy_pass` pasa de un host a un grupo. Una sola palabra.
- `least_conn` para repartir, `max_fails` / `fail_timeout` para sacar de
  rotacion a la replica que falla.

## Ejercicio

1. `docker compose stop $(docker compose ps -q web | head -1)` y comprobar
   que el sitio sigue respondiendo.
2. Cambiar `least_conn` por `ip_hash` y explicar cuando haria falta.
3. Escalar a 5 con nginx corriendo y ver que no toma las nuevas hasta
   `docker compose restart nginx`.

Slides: `clase5-paso5-balanceo.html`
