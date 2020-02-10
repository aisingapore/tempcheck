#!/bin/bash
echo "Migrating database"
python manage.py migrate

echo "Starting Gunicorn."
exec gunicorn vishnu.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3