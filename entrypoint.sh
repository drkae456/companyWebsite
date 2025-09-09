#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting Django application setup..."

# Install django-cron
pip install django-cron

# Wait for database to be ready
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database is ready!"

# Create migrations for any new model changes
echo "Creating migrations..."
python manage.py makemigrations

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Check if database has been populated (using a flag file)
POPULATE_FLAG="/app/.db_populated"

if [ ! -f "$POPULATE_FLAG" ]; then
    echo "Database not yet populated. Running populate_database command..."
    python manage.py populate_database
    
    # Create flag file to indicate database has been populated
    touch "$POPULATE_FLAG"
    echo "Database population completed and flagged."
else
    echo "Database already populated (flag file exists). Skipping population."
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the application
echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000
