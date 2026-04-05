#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Ensuring superuser exists..."
python manage.py ensure_superuser

echo "Starting gunicorn..."
exec gunicorn lexiflow_backend.wsgi:application --bind 0.0.0.0:8000 --workers 3 --threads 2