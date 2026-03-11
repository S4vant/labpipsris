#!/bin/sh
# entrypoint.sh

echo "Waiting for database..."
# Ждем пока БД будет доступна
while ! nc -z database 3306; do
  sleep 1
done
echo "Database is ready!"

# Запускаем миграции
echo "Running migrations..."
alembic upgrade head

# Запускаем приложение
echo "Starting application..."
exec "$@"