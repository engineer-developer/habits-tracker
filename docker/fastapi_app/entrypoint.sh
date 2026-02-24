#!/bin/bash
# Скрипт применения alembic миграций

echo "Start apply migrations..."
cd ./fastapi_app
alembic upgrade head
echo "Migrations have been successfully applied."

exec "$@"