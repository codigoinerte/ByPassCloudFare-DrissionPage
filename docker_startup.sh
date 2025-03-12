#!/usr/bin/env bash
set -e

# Ejecuta cualquier comando de configuración adicional aquí
echo "Starting application..."

# Inicia la aplicación Flask con Gunicorn y aumenta el tiempo de espera
exec gunicorn --timeout 120 -w 4 -b 0.0.0.0:8000 main:app