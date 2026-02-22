#!/bin/bash
# Скрипт применения alembic миграций

echo "Start apply migrations..."
alembic upgrade head
echo "Migrations have been successfully applied."

exec "$@"