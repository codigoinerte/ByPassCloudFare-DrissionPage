#!/usr/bin/env bash
set -e

# Ejecuta cualquier comando de configuración adicional aquí
echo "Starting application..."

exec /dockerstartup/vnc_startup.sh  > /dev/null 2>&1 &

# Inicia la aplicación Flask con Gunicorn y aumenta el tiempo de espera
exec gunicorn -w 4 -b 0.0.0.0:8000 main:app