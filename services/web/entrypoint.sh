#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Initialize migrations
echo "Initializing migrations..."
python manage.py db init

# Create migrations
echo "Creating migrations..."
python manage.py db migrate

# Apply migrations
echo "Applying migrations..."
python manage.py db upgrade

# Seed the database
echo "Seeding initial data..."
python manage.py seed_db

echo "Initialization completed!"

exec "$@" 