#!/bin/sh
# Certificado autofirmado para la clase. El navegador va a advertir, y
# hace bien: nadie avala este certificado. En un dominio real esto lo
# reemplaza certbot contra Let's Encrypt.
set -e
mkdir -p "$(dirname "$0")/certs"
openssl req -x509 -newkey rsa:2048 -nodes -days 365 \
  -keyout "$(dirname "$0")/certs/privkey.pem" \
  -out    "$(dirname "$0")/certs/fullchain.pem" \
  -subj "/CN=localhost"
echo "Certificado generado en nginx/certs/"
