#!/usr/bin/env bash
set -e

# Ejecuta cualquier comando de configuración adicional aquí
echo "Starting application..."

# Inicia la aplicación Flask con Gunicorn
exec gunicorn -w 4 -b 0.0.0.0:8000 main:app