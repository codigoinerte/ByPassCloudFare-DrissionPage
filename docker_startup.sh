#!/usr/bin/env bash
set -e

# Ejecuta cualquier comando de configuración adicional aquí
echo "Starting application..."

# Inicia la aplicación
exec gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000