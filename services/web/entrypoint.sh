#!/bin/sh

if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

echo "Initializing migrations..."
python manage.py db init || true  # не падаем, если уже инициализировано

echo "Creating migrations..."
python manage.py db migrate || true

echo "Applying migrations..."
python manage.py db upgrade

# Условная загрузка mock-данных — только если в базе нет пользователей
echo "Checking if we need to load mock data..."
python -c "
from project import create_app, db
from project.models import User

app = create_app()
with app.app_context():
    if db.session.query(User).count() == 0:
        from project.load_mock_data import load_mock_data
        load_mock_data()
        print('Mock data loaded.')
    else:
        print('Skipping mock data load — users already exist.')
"

echo "Initialization completed!"
exec "$@"
