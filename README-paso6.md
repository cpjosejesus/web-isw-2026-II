# Paso 6 — Cache y limites: el peldano mas alto

La peticion mas rapida es la que nunca llega a Flask. Nginx guarda la
respuesta del catalogo unos segundos y rechaza en el borde al que abusa.

## Levantar

    ./nginx/generar-certificado.sh     # si no lo hicieron antes
    docker compose up -d --build --scale web=3

## Que cambio

- `proxy_cache_path` y `limit_req_zone`, fuera de los `server`.
- `location /libros` cachea 30 s y expone `X-Cache-Status`.
- `location /libros/crear` no cachea nunca y limita a 10 r/s por IP.

## Ejercicio

1. Recargar `/libros` dos veces y ver `MISS` y despues `HIT` en las
   DevTools.
2. `for i in $(seq 30); do curl -sk -o /dev/null -w "%{http_code} " \
   https://localhost:8443/libros/crear; done` y contar los `503`.
3. Explicar por que la ficha de un libro se puede cachear y el formulario
   de edicion no.

## Cierre

Aqui termina la escalera. Comparar `nginx/default.conf` de este paso con
el del paso 1: es el mismo archivo, seis capacidades despues.

Slides: `clase5-paso6-cache-y-limites.html`
