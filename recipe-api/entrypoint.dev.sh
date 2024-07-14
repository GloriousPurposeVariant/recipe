#!/bin/bash

echo "Waiting for database to be ready..."

# Wait for PostgreSQL to be ready
while !</dev/tcp/db/5432; do
  sleep 1
done

echo "Database is ready. Applying migrations and collecting static files..."

# Apply database migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start Redis server
redis-server &

# Start Celery worker
celery -A config.celery worker -l info &

# Execute the command passed as arguments or run the development server as default
exec "$@" || exec python manage.py runserver 0.0.0.0:8000
